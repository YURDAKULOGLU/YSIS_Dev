import asyncio
import os
import re
import subprocess
from pathlib import Path

import httpx

from src.agentic.core.plugins.model_router import default_router
from src.agentic.core.protocols import CodeResult, ExecutorProtocol, Plan


def _get_code_root() -> Path:
    from src.agentic.core.config import PROJECT_ROOT

    override = os.getenv("YBIS_CODE_ROOT")
    if override:
        return Path(override).resolve()
    return Path(PROJECT_ROOT).resolve()


class PatchExecutor(ExecutorProtocol):
    """
    Deterministic executor that requests a unified diff and applies via git.
    """

    def __init__(self, router=None, base_url: str | None = None):
        self.router = router or default_router
        self.model_config = self.router.get_model("CODING")
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def name(self) -> str:
        return "PatchExecutor(diff-only)"

    async def execute(
        self,
        plan: Plan,
        sandbox_path: str,
        error_history: list[str] | None = None,
        retry_count: int = 0
    ) -> CodeResult:
        if not plan or not plan.files_to_modify:
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={},
                success=False,
                error="Plan missing files_to_modify; refusing to execute."
            )

        if self.model_config.provider != "ollama":
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={},
                success=False,
                error="PatchExecutor currently supports only Ollama provider."
            )

        git_root = _get_code_root()
        log_dir = Path(sandbox_path) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        normalized_files = []
        for f in plan.files_to_modify:
            f_path = Path(f)
            full_path = f_path if f_path.is_absolute() else (git_root / f_path)
            try:
                rel_to_root = full_path.relative_to(git_root)
                normalized_files.append(str(rel_to_root).replace("\\", "/"))
            except ValueError:
                normalized_files.append(str(full_path))

        task_id = str(plan.metadata.get("task_id") or "UNKNOWN")
        prompt = self._build_prompt(plan, normalized_files, git_root, error_history or [], task_id)
        (log_dir / "patch_prompt.txt").write_text(prompt, encoding="utf-8")

        patch_text = await self._call_ollama(prompt)
        (log_dir / "patch_response.txt").write_text(patch_text or "", encoding="utf-8")

        diff_body = self._extract_diff(patch_text or "")
        if not diff_body.strip():
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={"response": patch_text or ""},
                success=False,
                error="Model did not return a unified diff."
            )

        if self._contains_placeholder_ids(diff_body, task_id):
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={"response": patch_text or "", "diff_body": diff_body[:5500]},
                success=False,
                error="Patch contains placeholder task IDs. Refusing to apply."
            )

        # Fail-fast: Validate diff format before attempting to apply
        is_valid, validation_error = self._validate_diff_format(diff_body)
        if not is_valid:
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={"response": patch_text or "", "diff_body": diff_body[:500]},
                success=False,
                error=f"Invalid diff format: {validation_error}"
            )

        (log_dir / "patch.diff").write_text(diff_body, encoding="utf-8")

        touched = self._extract_files_from_diff(diff_body)
        allowed = {Path(p).as_posix() for p in normalized_files}
        unexpected = [p for p in touched if p not in allowed]
        if unexpected:
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={"unexpected": "\n".join(unexpected)},
                success=False,
                error=f"Patch touches unexpected files: {', '.join(unexpected)}"
            )

        check_result = subprocess.run(
            ["git", "apply", "--check", "--whitespace=nowarn", "-"],
            cwd=str(git_root),
            input=diff_body,
            text=True,
            capture_output=True,
        )
        if check_result.returncode != 0:
            return CodeResult(
                files_modified={},
                commands_run=["git apply --check"],
                outputs={"stderr": check_result.stderr},
                success=False,
                error="Patch failed git apply --check"
            )

        apply_result = subprocess.run(
            ["git", "apply", "--whitespace=nowarn", "-"],
            cwd=str(git_root),
            input=diff_body,
            text=True,
            capture_output=True,
        )
        if apply_result.returncode != 0:
            return CodeResult(
                files_modified={},
                commands_run=["git apply"],
                outputs={"stderr": apply_result.stderr},
                success=False,
                error="Patch failed to apply"
            )

        status_lines = await self._collect_git_status(git_root)
        files_modified = self._parse_git_status(status_lines)
        filtered = {
            str((git_root / path).resolve()): status
            for path, status in files_modified.items()
            if Path(path).as_posix() in allowed
        }

        if not filtered:
            return CodeResult(
                files_modified={},
                commands_run=["git apply"],
                outputs={},
                success=False,
                error="Patch applied but no tracked changes detected"
            )

        return CodeResult(
            files_modified=filtered,
            commands_run=["git apply --check", "git apply"],
            outputs={"status": "patch-applied"},
            success=True,
            error=None
        )

    async def _collect_git_status(self, git_root: Path) -> list[str]:
        proc = await asyncio.create_subprocess_shell(
            "git status --porcelain=v1 -uall",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(git_root)
        )
        stdout, _ = await proc.communicate()
        return stdout.decode("utf-8").splitlines()

    def _parse_git_status(self, status_lines: list[str]) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for line in status_lines:
            if not line:
                continue
            status_code = line[:2].strip()
            path = line[3:].strip().replace('"', '')
            if " -> " in path:
                path = path.split(" -> ")[-1].strip()
            parsed[path] = status_code or "??"
        return parsed

    def _build_prompt(
        self,
        plan: Plan,
        files: list[str],
        git_root: Path,
        error_history: list[str],
        task_id: str,
    ) -> str:
        content_blocks = []
        for rel_path in files:
            path = git_root / rel_path
            if not path.exists():
                content_blocks.append(f"FILE: {rel_path}\n<new file>\n")
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                content = ""
            content_blocks.append(f"FILE: {rel_path}\n{content}\n")

        prompt = (
            "You are a coding assistant. Output ONLY a unified diff.\n"
            "Rules:\n"
            "- Respond with a single unified diff (git apply compatible).\n"
            "- Do NOT include explanations.\n"
            "- Only modify files in the allowed list.\n"
            "- If you need a new file, include it in diff.\n\n"
            "- Do NOT use placeholder task IDs. If an ID is required, use the TASK ID above.\n"
            "- Use the exact FILE CONTENTS below as the base context.\n"
            "- If context does not match, output an empty diff.\n\n"
            f"TASK ID:\n{task_id}\n\n"
            f"OBJECTIVE:\n{plan.objective}\n\n"
            f"STEPS:\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan.steps)) + "\n\n"
            "ALLOWED FILES:\n" + "\n".join(f"- {p}" for p in files) + "\n\n"
            "FILE CONTENTS:\n" + "\n".join(content_blocks)
        )

        if error_history:
            prompt += "\nRECOVERY NOTES:\n" + "\n".join(f"- {err}" for err in error_history) + "\n"

        return prompt

    def _contains_placeholder_ids(self, diff_text: str, task_id: str) -> bool:
        placeholders = {
            "TASK-1234",
            "TASK-0000",
            "TASK-XXXX",
            "TASK-TEST",
            "TASK-ID",
            "TASK-PLACEHOLDER",
        }
        if any(p in diff_text for p in placeholders):
            return True
        tokens = set(re.findall(r"TASK-[A-Za-z0-9_-]+", diff_text))
        if not tokens:
            return False
        if task_id and task_id != "UNKNOWN":
            tokens.discard(task_id)
        return any(token in placeholders for token in tokens)

    async def _call_ollama(self, prompt: str) -> str:
        base = self.base_url.rstrip("/").replace("/v1", "")
        url = f"{base}/api/generate"
        payload = {
            "model": self.model_config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 2048,
                "num_ctx": self.model_config.context_window,
            },
        }
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")

    def _extract_diff(self, response: str) -> str:
        """
        Extract unified diff from model response.
        Handles multiple diff blocks and various markdown formats.
        """
        diff_parts = []

        # Try to extract from markdown code blocks (```diff or ```)
        if "```" in response:
            # Match ```diff, ```patch, or plain ``` blocks
            blocks = re.findall(r"```(?:diff|patch)?\s*\n(.*?)```", response, re.S)
            for block in blocks:
                block = block.strip()
                # Validate it looks like a diff
                if self._looks_like_diff(block):
                    diff_parts.append(block)

        # If no valid blocks found, try the raw response
        if not diff_parts:
            raw = response.strip()
            if self._looks_like_diff(raw):
                diff_parts.append(raw)

        if not diff_parts:
            return ""

        # Concatenate all diff blocks with newlines
        return "\n".join(diff_parts) + "\n"

    def _looks_like_diff(self, text: str) -> bool:
        """
        Quick heuristic to check if text looks like a unified diff.
        Must have at least one --- and +++ line pair.
        """
        has_minus = "--- " in text or "---\t" in text
        has_plus = "+++ " in text or "+++\t" in text
        has_hunk = "@@ " in text
        return has_minus and has_plus and has_hunk

    def _validate_diff_format(self, diff_text: str) -> tuple[bool, str]:
        """
        Validate that diff_text is a proper unified diff format.
        Returns (is_valid, error_message).
        """
        if not diff_text.strip():
            return False, "Empty diff"

        lines = diff_text.splitlines()

        # Must have at least header lines and one hunk
        if len(lines) < 4:
            return False, "Diff too short (need at least header + hunk)"

        # Check for proper diff structure
        has_file_header = False
        has_hunk_header = False
        in_hunk = False

        for line in lines:
            if line.startswith("--- "):
                has_file_header = True
            elif line.startswith("+++ "):
                if not has_file_header:
                    return False, "Found +++ before --- (malformed diff)"
            elif line.startswith("@@ "):
                if not has_file_header:
                    return False, "Found hunk before file header"
                has_hunk_header = True
                in_hunk = True
            elif in_hunk:
                # Inside a hunk, lines must start with +, -, space, or \
                if line and not line[0] in ('+', '-', ' ', '\\'):
                    # Could be a new file header
                    if line.startswith("diff ") or line.startswith("--- "):
                        in_hunk = False
                        has_file_header = line.startswith("--- ")
                    else:
                        return False, f"Invalid line in hunk: {line[:50]}"

        if not has_hunk_header:
            return False, "No hunk headers (@@ ... @@) found"

        return True, ""

    def _extract_files_from_diff(self, diff_text: str) -> list[str]:
        """
        Extract all file paths mentioned in the diff.
        Checks both --- (source) and +++ (destination) lines.
        """
        files = set()
        for line in diff_text.splitlines():
            path = None

            if line.startswith("+++ "):
                path = line.split("+++ ", 1)[1].strip()
                # Remove b/ prefix (git diff format)
                if path.startswith("b/"):
                    path = path[2:]
            elif line.startswith("--- "):
                path = line.split("--- ", 1)[1].strip()
                # Remove a/ prefix (git diff format)
                if path.startswith("a/"):
                    path = path[2:]

            if path and path != "/dev/null":
                # Remove any trailing timestamps (some diff formats include them)
                path = path.split("\t")[0].strip()
                files.add(path)

        return list(files)
