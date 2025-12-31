import asyncio
import os
from collections import deque
from pathlib import Path

from src.agentic.core.config import (
    AIDER_BIN,
    AIDER_CHAT_LANGUAGE,
    AIDER_ENCODING,
    AIDER_VENV_PATH,
    ALLOWLIST_MODE,
    ENABLE_VALIDATION,
    SANDBOX_MODE,
    USE_ACI,
)
from src.agentic.core.plugins.model_router import default_router
from src.agentic.core.protocols import CodeResult, ExecutorProtocol, Plan


class AiderExecutorEnhanced(ExecutorProtocol):
    """
    Enhanced Executor that enforces YBIS Constitution and Test-First workflow.
    Injects architectural principles and coding standards into every prompt.

    Features:
    - Constitutional prompt injection
    - Test-first workflow enforcement
    - Optional ACI (Agent-Computer Interface) integration for constrained execution
    """

    def __init__(self, router=None, use_aci: bool = None):
        self.router = router or default_router
        self.constitution_path = "docs/governance/YBIS_CONSTITUTION.md"

        # ACI integration (feature-flagged)
        self.use_aci = use_aci if use_aci is not None else USE_ACI
        self._aci = None  # Lazy-loaded

        if self.use_aci:
            print(f"[AiderEnhanced] ACI mode enabled (allowlist={ALLOWLIST_MODE}, sandbox={SANDBOX_MODE})")

    def name(self) -> str:
        return "Aider-Enhanced-Executor"

    def _ensure_log_dir(self, sandbox_path: str) -> Path:
        log_dir = Path(sandbox_path) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    def _write_log(self, log_dir: Path, name: str, content: str) -> None:
        try:
            (log_dir / name).write_text(content or "", encoding="utf-8")
        except Exception:
            # Logging must never block execution
            pass

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

    def _extract_aider_failure(self, stdout_text: str, stderr_text: str) -> str | None:
        combined = "\n".join([stdout_text or "", stderr_text or ""]).lower()

        # Critical failures that should block
        critical_signatures = [
            "the search section must exactly match",  # SEARCH/REPLACE mismatch
            "please explain the changes",
            "please explain changes",
            "lutfen yapmam",  # Turkish "please don't"
            "only 3 reflections allowed",
            "valueerror: badgatewayerror",
            "please consider reporting this bug to help improve aider",
        ]

        # Non-critical issues (log but don't fail)
        # ">>>>>>> replace" - normal in whole-file-edit mode
        # "summarizer unexpectedly failed" - code still applied
        # "summarization failed" - cosmetic issue
        # "cannot schedule new futures after shutdown" - cleanup issue

        for sig in critical_signatures:
            if sig in combined:
                return f"Aider failure detected: {sig}"
        return None

    def _collect_context_files(self, target_files: list[str], git_root: Path) -> list[str]:
        """
        Collect context files for --read injection.

        This ensures Aider sees the actual file content before editing.
        Also includes related files (imports, tests, etc.)
        """
        context_files = []

        for target in target_files:
            target_path = git_root / target

            # 1. If file exists, add it as context (Aider will see current content)
            if target_path.exists():
                context_files.append(target)

            # 2. Find related test file
            if target.endswith('.py'):
                test_candidates = [
                    target.replace('src/', 'tests/').replace('.py', '_test.py'),
                    target.replace('src/', 'tests/test_'),
                    f"tests/test_{Path(target).stem}.py"
                ]
                for test_path in test_candidates:
                    if (git_root / test_path).exists():
                        context_files.append(test_path)
                        break

            # 3. Find related imports (simple heuristic)
            if target_path.exists() and target.endswith('.py'):
                try:
                    content = target_path.read_text(encoding='utf-8')
                    # Look for local imports
                    import re
                    local_imports = re.findall(r'from (src\.[^\s]+) import', content)
                    for imp in local_imports[:3]:  # Limit to 3
                        imp_path = imp.replace('.', '/') + '.py'
                        if (git_root / imp_path).exists():
                            context_files.append(imp_path)
                except Exception:
                    pass

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for f in context_files:
            if f not in seen:
                seen.add(f)
                unique.append(f)

        return unique[:10]  # Limit context to 10 files

    def _resolve_aider_command(self) -> list[str]:
        if AIDER_BIN:
            candidate = Path(AIDER_BIN)
            if candidate.exists():
                return [str(candidate)]

        venv_root = Path(AIDER_VENV_PATH)
        windows_bin = venv_root / "Scripts" / "aider.exe"
        windows_shim = venv_root / "Scripts" / "aider"
        posix_bin = venv_root / "bin" / "aider"

        if windows_bin.exists():
            return [str(windows_bin)]
        if windows_shim.exists():
            return [str(windows_shim)]
        if posix_bin.exists():
            return [str(posix_bin)]

        return ["aider"]

    def _write_message_file(self, sandbox_path: str, content: str) -> Path:
        log_dir = self._ensure_log_dir(sandbox_path)
        message_path = log_dir / "aider_message.txt"
        message_path.write_text(content, encoding="utf-8")
        return message_path

    async def _stream_to_file(
        self, stream: asyncio.StreamReader, log_path: Path, buffer: deque,
        live_prefix: str = "", live_output: bool = True
    ) -> None:
        """Stream subprocess output to file with optional live console output."""
        import datetime
        with log_path.open("w", encoding="utf-8") as handle:
            while True:
                chunk = await stream.readline()
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="replace")
                # Write to file with timestamp
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                handle.write(f"[{ts}] {text}")
                handle.flush()
                buffer.append(text)
                # Live console output (sanitized for Windows terminal)
                if live_output and text.strip():
                    safe_text = text.encode('ascii', 'replace').decode('ascii')
                    print(f"{live_prefix}[{ts}] {safe_text.rstrip()}")

    async def execute(
        self, plan: Plan, sandbox_path: str,
        error_history: list[str] = None, retry_count: int = 0
    ) -> CodeResult:
        """
        Execute the plan with enhanced prompt engineering and strict enforcement.

        If USE_ACI is enabled, uses constrained Agent-Computer Interface.
        Otherwise, uses direct Aider execution (original behavior).
        """
        # Route to ACI execution if enabled
        if self.use_aci:
            return await self._execute_with_aci(plan, sandbox_path, error_history, retry_count)

        # Original direct execution (fallback)
        return await self._execute_direct(plan, sandbox_path, error_history, retry_count)

    async def _execute_direct(
        self, plan: Plan, sandbox_path: str,
        error_history: list[str] = None, retry_count: int = 0
    ) -> CodeResult:
        """
        Direct Aider execution (original behavior).
        No ACI constraints - full shell access to Aider.
        """
        model_config = self.router.get_model("CODING")
        print(f"[AiderEnhanced] Using model: {model_config.model_name} ({model_config.provider}) [DIRECT MODE]")

        # 1. Load Contextual Knowledge
        constitution = ""
        if os.path.exists(self.constitution_path):
            try:
                with open(self.constitution_path, encoding="utf-8") as f:
                    constitution = f.read()
            except Exception:
                pass

        # 2. Construct the Hyper-Prompt
        prompt = "### YBIS ENHANCED EXECUTION PROTOCOL ###\n"
        prompt += "You are an elite autonomous developer in the YBIS Software Factory.\n\n"

        if constitution:
            prompt += "## CONSTITUTIONAL MANDATES (FOLLOW STRICTLY):\n"
            prompt += constitution + "\n\n"

        prompt += "## CODE STANDARDS:\n"
        prompt += "- Style: PEP8, snake_case for functions and variables.\n"
        prompt += "- Documentation: Google-style docstrings for all classes and functions.\n"
        prompt += "- Typing: MANDATORY type hints for all parameters and return types.\n"
        prompt += "- Quality: Ensure the code passes 'ruff check' with zero errors.\n\n"
        prompt += "## EXECUTION RULES:\n"
        prompt += "- Do not ask clarifying questions. Make reasonable assumptions and proceed.\n"
        prompt += "- Provide only actionable edits. No meta commentary.\n\n"
        prompt += "## WINDOWS PATHS:\n"
        prompt += "- Use raw strings for Windows paths (prefix with r\"\") to avoid escape errors.\n\n"
        prompt += "## OUTPUT LANGUAGE:\n"
        prompt += "- Respond only in English. Avoid non-ASCII characters.\n\n"

        prompt += "## TEST-FIRST WORKFLOW:\n"
        prompt += "1. Identify the core logic being added or modified.\n"
        prompt += "2. CREATE or UPDATE a unit test in 'tests/unit/' that covers this logic.\n"
        prompt += "3. IMPLEMENT the code to make the test pass.\n"
        prompt += "4. Verification will fail if no tests are added/updated for new features.\n\n"

        if error_history and len(error_history) > 0:
            prompt += "## RECOVERY PROTOCOL (FIX PREVIOUS ERRORS):\n"
            for i, err in enumerate(error_history):
                prompt += f"ERR_{i}: {err}\n"
            prompt += "Analyze why the previous attempt failed and implement a robust fix.\n\n"

        prompt += f"## MISSION OBJECTIVE:\n{plan.objective}\n\n"
        prompt += "## EXECUTION STEPS:\n"
        for i, step in enumerate(plan.steps):
            prompt += f"{i+1}. {step}\n"

        # 3. Handle File Paths
        from src.agentic.core.config import PROJECT_ROOT
        git_root = Path(PROJECT_ROOT).resolve()

        files = plan.files_to_modify if plan.files_to_modify else []
        if not files:
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={},
                success=False,
                error="Plan missing files_to_modify; refusing to execute."
            )
        normalized_files = []
        for f in files:
            f_path = Path(f)
            if f_path.is_absolute():
                full_path = f_path
            else:
                full_path = git_root / f_path

            try:
                rel_to_root = full_path.relative_to(git_root)
                normalized_files.append(str(rel_to_root))
            except ValueError:
                normalized_files.append(str(full_path))

        prompt += "\n## FILE GUARDRAILS:\n"
        prompt += "- Only modify or create files in the explicit list below.\n"
        prompt += "- Do NOT create new files unless listed.\n"
        prompt += "Allowed files:\n"
        for f in normalized_files:
            prompt += f"- {f}\n"

        # 4. Construct Command
        cmd = self._resolve_aider_command()
        cmd.extend(normalized_files)

        # 4.1 Add --read flags for context injection (CRITICAL FIX)
        # This ensures Aider sees actual file content before trying SEARCH/REPLACE
        context_files = self._collect_context_files(normalized_files, git_root)
        for ctx_file in context_files:
            if ctx_file not in normalized_files:  # Don't double-add edit targets
                cmd.extend(["--read", ctx_file])
        if context_files:
            print(f"[AiderEnhanced] Context injection: {len(context_files)} files via --read")

        prompt += f"\nNote: All paths provided are relative to the Git Root: {git_root}\n"
        message_path = self._write_message_file(sandbox_path, prompt)
        cmd.extend(["--message-file", str(message_path)])

        model_full_name = model_config.model_name
        if model_config.provider == "ollama":
            model_full_name = f"ollama/{model_config.model_name}"
        cmd.extend(["--model", model_full_name])

        edit_format = "whole" if retry_count > 0 else "diff"
        cmd.extend([
            "--model-settings-file", "config/aider_model_settings.yml",
            "--no-show-model-warnings",
            "--no-pretty",
            "--no-auto-lint",
            "--no-suggest-shell-commands",
            "--edit-format", edit_format,
            "--no-multiline",
            "--aiderignore", "config/.sandbox_aiderignore",
            "--encoding", AIDER_ENCODING,
            "--chat-language", AIDER_CHAT_LANGUAGE,
            "--no-restore-chat-history",
            "--input-history-file", str(self._ensure_log_dir(sandbox_path) / "aider_input_history.txt"),
            "--chat-history-file", str(self._ensure_log_dir(sandbox_path) / "aider_chat_history.md"),
            "--llm-history-file", str(self._ensure_log_dir(sandbox_path) / "aider_llm_history.jsonl"),
            "--yes",
            "--yes-always",
            "--no-auto-commits"
        ])

        # 5. Execute Aider
        try:
            log_dir = self._ensure_log_dir(sandbox_path)
            stdout_path = log_dir / "aider_stdout.log"
            stderr_path = log_dir / "aider_stderr.log"
            stdout_tail = deque(maxlen=200)
            stderr_tail = deque(maxlen=200)
            pre_status = self._parse_git_status(await self._collect_git_status(git_root))
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            env["AIDER_ENCODING"] = AIDER_ENCODING
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(git_root),
                env=env
            )
            print("[Aider] === LIVE OUTPUT START ===")
            stdout_task = asyncio.create_task(
                self._stream_to_file(process.stdout, stdout_path, stdout_tail, "[AIDER] ", live_output=True)
            )
            stderr_task = asyncio.create_task(
                self._stream_to_file(process.stderr, stderr_path, stderr_tail, "[AIDER:ERR] ", live_output=True)
            )

            import time
            start_time = time.time()
            timed_out = False
            try:
                await asyncio.wait_for(process.wait(), timeout=300)
            except asyncio.TimeoutError:
                timed_out = True
                process.kill()
                await process.wait()
                success = False
            else:
                success = (process.returncode == 0)

            elapsed = time.time() - start_time
            print(f"[Aider] === LIVE OUTPUT END === (elapsed: {elapsed:.1f}s, exit: {process.returncode}, timeout: {timed_out})")

            await stdout_task
            await stderr_task

            stdout_text = "".join(stdout_tail)
            stderr_text = "".join(stderr_tail)
            detected_failure = self._extract_aider_failure(stdout_text, stderr_text)

            # Detect Changes - IMPROVED: Parse Aider's "Applied edit to" output
            # This is more reliable than git status delta when files are already modified
            import re
            applied_edits = re.findall(r"Applied edit to ([^\n]+)", stdout_text)
            print(f"[AiderEnhanced] Detected applied edits: {applied_edits}")

            actual_files = {}
            unexpected = []
            allowed_set = {Path(p).as_posix() for p in normalized_files}

            # Method 1: Use Aider's "Applied edit to" output
            for edit_path in applied_edits:
                edit_path = edit_path.strip()
                posix_path = Path(edit_path).as_posix()
                if posix_path in allowed_set or edit_path in normalized_files:
                    abs_path = (git_root / edit_path).resolve()
                    actual_files[str(abs_path)] = "Modified"
                else:
                    unexpected.append(edit_path)

            # Method 2: Fallback to git status delta if no applied edits found
            if not actual_files and not applied_edits:
                try:
                    status_lines = await self._collect_git_status(git_root)
                    post_status = self._parse_git_status(status_lines)
                    delta = {
                        path: status
                        for path, status in post_status.items()
                        if pre_status.get(path) != status
                    }
                    for path, status_code in delta.items():
                        posix_path = Path(path).as_posix()
                        if posix_path in allowed_set:
                            abs_path = (git_root / path).resolve()
                            actual_files[str(abs_path)] = status_code
                        else:
                            unexpected.append(path)
                except Exception:
                    actual_files = {f: "Modified" for f in normalized_files}

            if unexpected:
                return CodeResult(
                    files_modified=actual_files,
                    commands_run=[' '.join(cmd)],
                    outputs={"status": "Unexpected files modified", "stdout": stdout_text, "stderr": stderr_text},
                    success=False,
                    error=f"Unexpected file changes: {', '.join(unexpected)}"
                )

            error_message = None
            if not success:
                error_message = "Aider execution timed out" if timed_out else "Aider execution failed (see logs)"
            if detected_failure:
                error_message = detected_failure if not error_message else f"{error_message}; {detected_failure}"
                success = False

            return CodeResult(
                files_modified=actual_files,
                commands_run=[' '.join(cmd)],
                outputs={"status": "Executed", "stdout": stdout_text, "stderr": stderr_text},
                success=success,
                error=None if success else error_message
            )

        except Exception as e:
            return CodeResult(
                files_modified={},
                commands_run=[' '.join(cmd)],
                outputs={},
                success=False,
                error=str(e)
            )

    async def _execute_with_aci(
        self, plan: Plan, sandbox_path: str,
        error_history: list[str] = None, retry_count: int = 0
    ) -> CodeResult:
        """
        Execute using Agent-Computer Interface (ACI).

        Provides:
        - Constrained command execution (allowlist)
        - Pre-validation (guardrails)
        - Sandboxed execution (resource limits)
        - Structured file operations

        This is safer than direct execution but may be less flexible.
        """
        print("[AiderEnhanced] Executing with ACI (constrained mode)")

        # Lazy-load ACI
        if self._aci is None:
            from src.agentic.core.config import PROJECT_ROOT
            from src.agentic.core.execution import AgentComputerInterface

            self._aci = AgentComputerInterface(
                base_dir=str(PROJECT_ROOT),
                enable_validation=ENABLE_VALIDATION,
                enable_allowlist=True,
                enable_sandbox=True
            )

        # For now, ACI-based execution still calls Aider but through sandbox
        # In the future, this could be replaced with direct file operations via ACI
        # TODO: Implement pure ACI-based code modifications (without Aider)

        # Current approach: Run Aider through ACI sandbox
        model_config = self.router.get_model("CODING")
        print(f"[AiderEnhanced] Using model: {model_config.model_name} ({model_config.provider}) [ACI MODE]")

        # Build Aider command (same as direct mode)
        from src.agentic.core.config import PROJECT_ROOT
        git_root = Path(PROJECT_ROOT).resolve()

        constitution = ""
        if os.path.exists(self.constitution_path):
            try:
                with open(self.constitution_path, encoding="utf-8") as f:
                    constitution = f.read()
            except Exception:
                pass

        # Construct prompt (same as direct mode)
        prompt = "### YBIS ENHANCED EXECUTION PROTOCOL ###\n"
        prompt += "You are an elite autonomous developer in the YBIS Software Factory.\n\n"

        if constitution:
            prompt += "## CONSTITUTIONAL MANDATES (FOLLOW STRICTLY):\n"
            prompt += constitution + "\n\n"

        prompt += "## CODE STANDARDS:\n"
        prompt += "- Style: PEP8, snake_case for functions and variables.\n"
        prompt += "- Documentation: Google-style docstrings for all classes and functions.\n"
        prompt += "- Typing: MANDATORY type hints for all parameters and return types.\n"
        prompt += "- Quality: Ensure the code passes 'ruff check' with zero errors.\n\n"
        prompt += "## EXECUTION RULES:\n"
        prompt += "- Do not ask clarifying questions. Make reasonable assumptions and proceed.\n"
        prompt += "- Provide only actionable edits. No meta commentary.\n\n"
        prompt += "## WINDOWS PATHS:\n"
        prompt += "- Use raw strings for Windows paths (prefix with r\"\") to avoid escape errors.\n\n"
        prompt += "## OUTPUT LANGUAGE:\n"
        prompt += "- Respond only in English. Avoid non-ASCII characters.\n\n"
        if retry_count > 0:
            prompt += "## RETRY MODE:\n"
            prompt += "- Apply full-file edits (no SEARCH/REPLACE blocks).\n\n"

        prompt += "## TEST-FIRST WORKFLOW:\n"
        prompt += "1. Identify the core logic being added or modified.\n"
        prompt += "2. CREATE or UPDATE a unit test in 'tests/unit/' that covers this logic.\n"
        prompt += "3. IMPLEMENT the code to make the test pass.\n"
        prompt += "4. Verification will fail if no tests are added/updated for new features.\n\n"

        if error_history and len(error_history) > 0:
            prompt += "## RECOVERY PROTOCOL (FIX PREVIOUS ERRORS):\n"
            for i, err in enumerate(error_history):
                prompt += f"ERR_{i}: {err}\n"
            prompt += "Analyze why the previous attempt failed and implement a robust fix.\n\n"

        prompt += f"## MISSION OBJECTIVE:\n{plan.objective}\n\n"
        prompt += "## EXECUTION STEPS:\n"
        for i, step in enumerate(plan.steps):
            prompt += f"{i+1}. {step}\n"

        # Handle file paths
        files = plan.files_to_modify if plan.files_to_modify else []
        if not files:
            return CodeResult(
                files_modified={},
                commands_run=[],
                outputs={},
                success=False,
                error="Plan missing files_to_modify; refusing to execute."
            )
        normalized_files = []
        for f in files:
            f_path = Path(f)
            if f_path.is_absolute():
                full_path = f_path
            else:
                full_path = git_root / f_path

            try:
                rel_to_root = full_path.relative_to(git_root)
                normalized_files.append(str(rel_to_root))
            except ValueError:
                normalized_files.append(str(full_path))

        prompt += "\n## FILE GUARDRAILS:\n"
        prompt += "- Only modify or create files in the explicit list below.\n"
        prompt += "- Do NOT create new files unless listed.\n"
        prompt += "Allowed files:\n"
        for f in normalized_files:
            prompt += f"- {f}\n"

        # Build command
        cmd_parts = self._resolve_aider_command()
        cmd_parts.extend(normalized_files)

        prompt += f"\nNote: All paths provided are relative to the Git Root: {git_root}\n"
        message_path = self._write_message_file(sandbox_path, prompt)
        cmd_parts.extend(["--message-file", str(message_path)])

        model_full_name = model_config.model_name
        if model_config.provider == "ollama":
            model_full_name = f"ollama/{model_config.model_name}"
        cmd_parts.extend(["--model", model_full_name])

        cmd_parts.extend([
            "--model-settings-file", "config/aider_model_settings.yml",
            "--no-show-model-warnings",
            "--no-pretty",
            "--no-auto-lint",
            "--no-suggest-shell-commands",
            "--edit-format", "diff",
            "--no-multiline",
            "--aiderignore", "config/.sandbox_aiderignore",
            "--encoding", AIDER_ENCODING,
            "--chat-language", AIDER_CHAT_LANGUAGE,
            "--no-restore-chat-history",
            "--input-history-file", str(self._ensure_log_dir(sandbox_path) / "aider_input_history.txt"),
            "--chat-history-file", str(self._ensure_log_dir(sandbox_path) / "aider_chat_history.md"),
            "--llm-history-file", str(self._ensure_log_dir(sandbox_path) / "aider_llm_history.jsonl"),
            "--yes",
            "--yes-always",
            "--no-auto-commits"
        ])

        # Execute through ACI (sandboxed)
        quoted_parts = []
        for part in cmd_parts:
            if " " in part or "\t" in part:
                quoted_parts.append(f"\"{part}\"")
            else:
                quoted_parts.append(part)
        command = ' '.join(quoted_parts)

        try:
            log_dir = self._ensure_log_dir(sandbox_path)
            pre_status = self._parse_git_status(await self._collect_git_status(git_root))
            result = await self._aci.run_command(command, timeout=300, cwd=str(git_root))
            self._write_log(log_dir, "aider_stdout.log", result.stdout)
            self._write_log(log_dir, "aider_stderr.log", result.stderr)
            detected_failure = self._extract_aider_failure(result.stdout, result.stderr)

            if not result.success:
                return CodeResult(
                    files_modified={},
                    commands_run=[command],
                    outputs={"stdout": result.stdout, "stderr": result.stderr},
                    success=False,
                    error=detected_failure or result.message
                )

            # Detect changes (strict allowlist)
            actual_files = {}
            try:
                status_lines = await self._collect_git_status(git_root)
                post_status = self._parse_git_status(status_lines)
                delta = {
                    path: status
                    for path, status in post_status.items()
                    if pre_status.get(path) != status
                }
                unexpected = []
                allowed_set = {Path(p).as_posix() for p in normalized_files}
                for path, status_code in delta.items():
                    posix_path = Path(path).as_posix()
                    if posix_path in allowed_set:
                        abs_path = (git_root / path).resolve()
                        actual_files[str(abs_path)] = status_code
                    else:
                        unexpected.append(path)
            except Exception:
                actual_files = {f: "Modified" for f in normalized_files}
                unexpected = []

            if unexpected:
                return CodeResult(
                    files_modified=actual_files,
                    commands_run=[command],
                    outputs={"stdout": result.stdout, "stderr": result.stderr, "status": "Unexpected files modified"},
                    success=False,
                    error=f"Unexpected file changes: {', '.join(unexpected)}"
                )

            return CodeResult(
                files_modified=actual_files,
                commands_run=[command],
                outputs={"stdout": result.stdout, "stderr": result.stderr, "status": "ACI-Executed"},
                success=False if detected_failure else True,
                error=detected_failure
            )

        except Exception as e:
            return CodeResult(
                files_modified={},
                commands_run=[command],
                outputs={},
                success=False,
                error=f"ACI execution error: {str(e)}"
            )
