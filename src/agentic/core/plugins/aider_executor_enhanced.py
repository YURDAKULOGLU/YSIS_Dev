import os
import subprocess
import asyncio
from collections import deque
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.agentic.core.protocols import ExecutorProtocol, Plan, CodeResult
from src.agentic.core.plugins.model_router import default_router
from src.agentic.core.config import USE_ACI, ALLOWLIST_MODE, SANDBOX_MODE, ENABLE_VALIDATION

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

    async def _collect_git_status(self, git_root: Path) -> List[str]:
        proc = await asyncio.create_subprocess_shell(
            "git status --porcelain",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(git_root)
        )
        stdout, _ = await proc.communicate()
        return stdout.decode("utf-8").splitlines()

    async def _stream_to_file(self, stream: asyncio.StreamReader, log_path: Path, buffer: deque) -> None:
        with log_path.open("w", encoding="utf-8") as handle:
            while True:
                chunk = await stream.readline()
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="replace")
                handle.write(text)
                handle.flush()
                buffer.append(text)

    async def execute(self, plan: Plan, sandbox_path: str, error_history: List[str] = None, retry_count: int = 0) -> CodeResult:
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

    async def _execute_direct(self, plan: Plan, sandbox_path: str, error_history: List[str] = None, retry_count: int = 0) -> CodeResult:
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
                with open(self.constitution_path, "r", encoding="utf-8") as f:
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
        cmd = ["aider"]
        cmd.extend(normalized_files)
        
        prompt += f"\nNote: All paths provided are relative to the Git Root: {git_root}\n"
        cmd.extend(["--message", prompt])

        model_full_name = model_config.model_name
        if model_config.provider == "ollama":
            model_full_name = f"ollama/{model_config.model_name}"
        cmd.extend(["--model", model_full_name])
        
        cmd.extend([
            "--model-settings-file", "config/aider_model_settings.yml",
            "--no-show-model-warnings",
            "--no-pretty",
            "--no-auto-lint",
            "--no-suggest-shell-commands",
            "--aiderignore", "config/.sandbox_aiderignore",
            "--yes",
            "--no-auto-commits"
        ])

        # 5. Execute Aider
        try:
            log_dir = self._ensure_log_dir(sandbox_path)
            stdout_path = log_dir / "aider_stdout.log"
            stderr_path = log_dir / "aider_stderr.log"
            stdout_tail = deque(maxlen=200)
            stderr_tail = deque(maxlen=200)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(git_root),
                env=os.environ
            )
            stdout_task = asyncio.create_task(self._stream_to_file(process.stdout, stdout_path, stdout_tail))
            stderr_task = asyncio.create_task(self._stream_to_file(process.stderr, stderr_path, stderr_tail))

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

            await stdout_task
            await stderr_task

            stdout_text = "".join(stdout_tail)
            stderr_text = "".join(stderr_tail)

            # Detect Changes (strict allowlist)
            actual_files = {}
            try:
                status_lines = await self._collect_git_status(git_root)
                unexpected = []
                allowed_set = {Path(p).as_posix() for p in normalized_files}
                for line in status_lines:
                    status_code = line[:2].strip()
                    path = line[3:].strip().replace('"', '')
                    if " -> " in path:
                        path = path.split(" -> ")[-1].strip()

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
                    commands_run=[' '.join(cmd)],
                    outputs={"status": "Unexpected files modified", "stdout": stdout_text, "stderr": stderr_text},
                    success=False,
                    error=f"Unexpected file changes: {', '.join(unexpected)}"
                )

            error_message = None
            if not success:
                error_message = "Aider execution timed out" if timed_out else "Aider execution failed (see logs)"

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

    async def _execute_with_aci(self, plan: Plan, sandbox_path: str, error_history: List[str] = None, retry_count: int = 0) -> CodeResult:
        """
        Execute using Agent-Computer Interface (ACI).

        Provides:
        - Constrained command execution (allowlist)
        - Pre-validation (guardrails)
        - Sandboxed execution (resource limits)
        - Structured file operations

        This is safer than direct execution but may be less flexible.
        """
        print(f"[AiderEnhanced] Executing with ACI (constrained mode)")

        # Lazy-load ACI
        if self._aci is None:
            from src.agentic.core.execution import AgentComputerInterface
            from src.agentic.core.config import PROJECT_ROOT

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
                with open(self.constitution_path, "r", encoding="utf-8") as f:
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
        cmd_parts = ["aider"]
        cmd_parts.extend(normalized_files)

        prompt += f"\nNote: All paths provided are relative to the Git Root: {git_root}\n"
        cmd_parts.extend(["--message", prompt])

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
            "--aiderignore", "config/.sandbox_aiderignore",
            "--yes",
            "--no-auto-commits"
        ])

        # Execute through ACI (sandboxed)
        command = ' '.join(cmd_parts)

        try:
            log_dir = self._ensure_log_dir(sandbox_path)
            result = await self._aci.run_command(command, timeout=300, cwd=str(git_root))
            self._write_log(log_dir, "aider_stdout.log", result.stdout)
            self._write_log(log_dir, "aider_stderr.log", result.stderr)

            if not result.success:
                return CodeResult(
                    files_modified={},
                    commands_run=[command],
                    outputs={"stdout": result.stdout, "stderr": result.stderr},
                    success=False,
                    error=result.message
                )

            # Detect changes (strict allowlist)
            actual_files = {}
            try:
                status_lines = await self._collect_git_status(git_root)
                unexpected = []
                allowed_set = {Path(p).as_posix() for p in normalized_files}
                for line in status_lines:
                    status_code = line[:2].strip()
                    path = line[3:].strip().replace('"', '')
                    if " -> " in path:
                        path = path.split(" -> ")[-1].strip()

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
                success=True,
                error=None
            )

        except Exception as e:
            return CodeResult(
                files_modified={},
                commands_run=[command],
                outputs={},
                success=False,
                error=f"ACI execution error: {str(e)}"
            )
