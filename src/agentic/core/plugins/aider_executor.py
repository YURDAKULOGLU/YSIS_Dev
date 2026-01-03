import os
import subprocess
import asyncio
from pathlib import Path
from typing import List, Set
from src.agentic.core.protocols import ExecutorProtocol, Plan, CodeResult

from src.agentic.core.plugins.model_router import default_router
from src.agentic.core.config import AIDER_VENV_PATH, AIDER_BIN, AIDER_ENCODING, AIDER_CHAT_LANGUAGE, PROJECT_ROOT
from src.agentic.core.utils.logging_utils import log_event

# Execution settings
AIDER_TIMEOUT_SECONDS = 300  # 5 minutes max
AIDER_MAX_RETRIES = 3


def _get_code_root() -> Path:
    override = os.getenv("YBIS_CODE_ROOT")
    if override:
        return Path(override).resolve()
    return Path(PROJECT_ROOT).resolve()

class AiderExecutor(ExecutorProtocol):
    """
    Executor that delegates coding tasks to 'aider', a powerful AI pair programmer.
    This acts as a bridge between our Orchestrator and the Aider CLI.
    """

    def __init__(self, router=None):
        self.router = router or default_router

    def _write_message_file(self, sandbox_path: str, content: str) -> Path:
        log_dir = Path(sandbox_path) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        message_path = log_dir / "aider_message.txt"
        message_path.write_text(content, encoding="utf-8")
        return message_path

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

    def _get_baseline_files(self) -> Set[str]:
        """Capture current dirty files before execution (for clean diff later)."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=10,
                cwd=_get_code_root()
            )
            files = set()
            for line in result.stdout.strip().splitlines():
                if line:
                    # Extract file path (skip status codes)
                    file_path = line[3:].strip().replace('"', '')
                    if " -> " in file_path:
                        file_path = file_path.split(" -> ")[-1]
                    files.add(file_path)
            return files
        except Exception as e:
            log_event(f"Warning: Could not get baseline: {e}", component="aider_executor", level="warning")
            return set()

    def _get_new_changes(self, baseline: Set[str]) -> Set[str]:
        """Get only NEW changes since baseline (ignore pre-existing dirty files)."""
        current = self._get_baseline_files()
        return current - baseline

    def _verify_changes(self) -> tuple[bool, str]:
        """Run verify_code.py on modified files."""
        try:
            result = subprocess.run(
                ["python", "scripts/verify_code.py", "--quiet"],
                capture_output=True, text=True, timeout=60,
                cwd=_get_code_root()
            )
            if result.returncode == 0:
                return True, "Verification passed"
            return False, result.stdout + result.stderr
        except FileNotFoundError:
            log_event("Warning: verify_code.py not found, skipping verification", component="aider_executor", level="warning")
            return True, "Skipped (verify_code.py not found)"
        except Exception as e:
            return False, str(e)

    def _rollback_changes(self, files: Set[str] = None):
        """Rollback changes on failure."""
        try:
            if files:
                for f in files:
                    subprocess.run(["git", "checkout", "--", f], cwd=_get_code_root(), timeout=10)
                log_event(f"Rolled back {len(files)} files", component="aider_executor")
            else:
                subprocess.run(["git", "checkout", "--", "."], cwd=_get_code_root(), timeout=10)
            log_event("Rolled back all changes", component="aider_executor")
        except Exception as e:
            log_event(f"Warning: Rollback failed: {e}", component="aider_executor", level="warning")

    def name(self) -> str:
        return "Aider-CLI-Executor"

    async def execute(
        self, plan: Plan, sandbox_path: str,
        error_history: List[str] = None, retry_count: int = 0
    ) -> CodeResult:
        """
        Execute the plan by constructing a prompt for Aider and running it.
        Includes: baseline capture, timeout, verification, and rollback.
        """
        # Get model config from router
        model_config = self.router.get_model("CODING")
        log_event(f"Using model: {model_config.model_name} via {model_config.provider}", component="aider_executor")
        log_event(f"Preparing to execute plan with {len(plan.steps)} steps.", component="aider_executor")

        # CAPTURE BASELINE - to detect only NEW changes (fixes dirty tree false positives)
        baseline_files = self._get_baseline_files()
        if baseline_files:
            log_event(f"Baseline: {len(baseline_files)} pre-existing dirty files (will be ignored)", component="aider_executor")

        # 1. Construct the prompt for Aider
        prompt = ""

        # INJECT ERROR HISTORY (The Feedback Loop)
        if error_history and len(error_history) > 0:
            prompt += "CRITICAL: PREVIOUS ATTEMPT FAILED\n"
            prompt += "You must fix the following errors from the previous run:\n"
            for err in error_history:
                prompt += f"- {err}\n"
            prompt += "DO NOT REPEAT THESE MISTAKES.\n\n"

        prompt += f"OBJECTIVE: {plan.objective}\n\nPLAN STEPS:\n"
        for i, step in enumerate(plan.steps):
            prompt += f"{i+1}. {step}\n"

        prompt += "\nIMPORTANT:\n"
        prompt += "- Implement these changes exactly.\n"
        prompt += "- Use REAL file paths. DO NOT use placeholders.\n"
        prompt += "- Run tests if valid.\n"


        # 2. Identify target files and normalize paths relative to Git Root
        git_root = _get_code_root()

        log_event(f"Using CODE_ROOT as Git Root: {git_root}", component="aider_executor")

        current_path = Path(sandbox_path).resolve()
        rel_path_from_root = current_path.relative_to(git_root)

        files = plan.files_to_modify if plan.files_to_modify else []
        normalized_files = []
        for f in files:
            # We want to edit files in the REAL project, not the sandbox.
            # Planner usually returns paths relative to project root (e.g. "src/main.py").

            # Treat all paths as relative to git_root unless absolute
            f_path = Path(f)
            if f_path.is_absolute():
                full_path = f_path
            else:
                full_path = git_root / f_path

            try:
                # Calculate path relative to Git Root (Aider expects relative paths usually)
                rel_to_root = full_path.relative_to(git_root)
                normalized_files.append(str(rel_to_root))
            except ValueError:
                # If path is not inside git root, use absolute path
                normalized_files.append(str(full_path))

        log_event(f"Normalized Files: {normalized_files}", component="aider_executor")

        # 3. Construct the command
        cmd = self._resolve_aider_command()
        cmd.extend(normalized_files)

        # Update prompt to be explicit about paths
        prompt += f"\nNOTE: You are running in the Git Root: {git_root}\n"
        prompt += f"My Current Working Directory (Sandbox) is: {current_path}\n"
        prompt += f"Please edit files relative to the Git Root, e.g. {rel_path_from_root}/filename.py\n"

        message_path = self._write_message_file(sandbox_path, prompt)
        cmd.extend(["--message-file", str(message_path)])

        # FORCE MODEL FROM ROUTER
        model_full_name = model_config.model_name
        if model_config.provider == "ollama":
            model_full_name = f"ollama/{model_config.model_name}"

        cmd.extend(["--model", model_full_name])

        # Inject Model Settings to silence warnings & Enforce Model
        cmd.extend(["--model-settings-file", "config/aider_model_settings.yml"])
        cmd.extend(["--no-show-model-warnings"])
        cmd.extend(["--edit-format", "diff"])
        cmd.extend(["--no-multiline"])
        cmd.extend(["--encoding", AIDER_ENCODING])
        cmd.extend(["--chat-language", AIDER_CHAT_LANGUAGE])
        cmd.extend(["--no-restore-chat-history"])
        log_dir = Path(sandbox_path) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--input-history-file", str(log_dir / "aider_input_history.txt")])
        cmd.extend(["--chat-history-file", str(log_dir / "aider_chat_history.md")])
        cmd.extend(["--llm-history-file", str(log_dir / "aider_llm_history.jsonl")])

        # NON-INTERACTIVE & BACKGROUND FLAGS
        cmd.extend(["--no-pretty"])            # Disable rich/colorful output (Fixes Windows encoding crash)
        cmd.extend(["--no-auto-lint"])          # We handle linting via Sentinel
        cmd.extend(["--no-suggest-shell-commands"]) # Don't wait for user to confirm shell commands

        # FORCE SANDBOX CONTAINMENT
        # Only allow Aider to see what we explicitly permit
        cmd.extend(["--aiderignore", "config/.sandbox_aiderignore"])

        cmd.extend(["--yes", "--yes-always"])
        cmd.extend(["--no-auto-commits"]) # Let Orchestrator handle commits after verification

        log_event(f"Running command: {' '.join(cmd)}", component="aider_executor")

        # 4. Run Aider
        try:
            # Setup UTF-8 encoding environment
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            env["PYTHONIOENCODING"] = "utf-8"

            # We run synchronously for now as subprocess, but wrap in asyncio in real app
            # In a real async app we'd use asyncio.create_subprocess_exec
            process = await asyncio.create_subprocess_exec(
                *cmd,
                # Inherit stdout/stderr so user sees progress in real-time
                stdout=None,
                stderr=None,
                cwd=str(git_root),
                env=env  # Use UTF-8 environment
            )

            # TIMEOUT - prevent hanging forever
            try:
                await asyncio.wait_for(process.wait(), timeout=AIDER_TIMEOUT_SECONDS)
            except asyncio.TimeoutError:
                process.kill()
                log_event(f"TIMEOUT after {AIDER_TIMEOUT_SECONDS}s - killed process", component="aider_executor", level="warning")
                return CodeResult(
                    files_modified={},
                    commands_run=[' '.join(cmd)],
                    outputs={"error": f"Timeout after {AIDER_TIMEOUT_SECONDS} seconds"},
                    success=False,
                    error=f"Process killed after {AIDER_TIMEOUT_SECONDS}s timeout"
                )

            success = process.returncode == 0
            output_str = "Output streamed to console."

            # Detect NEW changes only (ignore baseline dirty files)
            new_changes = self._get_new_changes(baseline_files)
            log_event(f"Detected {len(new_changes)} new file changes", component="aider_executor")

            if success and new_changes:
                # VERIFICATION - check code quality before accepting
                log_event("Running verification...", component="aider_executor")
                verify_ok, verify_msg = self._verify_changes()

                if verify_ok:
                    log_event(f"Verification passed: {verify_msg}", component="aider_executor")
                else:
                    log_event(f"Verification FAILED: {verify_msg}", component="aider_executor", level="warning")
                    # ROLLBACK - revert only new changes
                    self._rollback_changes(new_changes)
                    success = False
                    output_str = f"Verification failed: {verify_msg}"

            if success:
                log_event("Success!", component="aider_executor")
            else:
                log_event("Failed!", component="aider_executor", level="warning")

            # Detect actually modified files using git
            actual_files = {}
            try:
                # We assume git_root is a git repo
                proc = await asyncio.create_subprocess_shell(
                    "git status --porcelain=v1 -uall",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(git_root)
                )
                stdout, _ = await proc.communicate()
                entries = stdout.decode('utf-8').splitlines()

                for entry in entries:
                    # Format: " M path/to/file", "?? path/to/file", "R  old -> new"
                    status_code = entry[:2].strip()
                    file_path_part = entry[3:].strip()

                    # Handle renamed files: "old -> new"
                    if " -> " in file_path_part:
                        file_path = file_path_part.split(" -> ")[-1].strip()
                    else:
                        file_path = file_path_part

                    if file_path:
                         # Aider might have double quotes if there are spaces
                         file_path = file_path.replace('"', '')
                         abs_path = (git_root / file_path).resolve()
                         actual_files[str(abs_path)] = f"Detected change: {status_code}"
            except Exception as git_err:
                 log_event(f"Failed to detect changes: {git_err}", component="aider_executor", level="warning")
                 # Fallback to plan files
                 actual_files = {f: "Modified by Aider (Fallback)" for f in files}

            return CodeResult(
                files_modified=actual_files,
                commands_run=[' '.join(cmd)],
                outputs={"aider": output_str},
                success=success,
                error=None if success else output_str
            )

        except Exception as e:
            return CodeResult(
                files_modified={},
                commands_run=[' '.join(cmd)],
                outputs={},
                success=False,
                error=str(e)
            )
