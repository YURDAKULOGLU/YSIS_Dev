"""
Aider Adapter - Wraps Aider to implement ExecutorProtocol.

Converts Aider command-line interface into a standard YBIS executor.

Fixed Aider adapter with proper CLI integration.
"""

import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path

from ..constants import PROJECT_ROOT
from ..contracts import ExecutorProtocol, ExecutorReport, Plan, RunContext
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)


class AiderExecutor:
    """
    Aider Executor - Wraps Aider CLI as ExecutorProtocol.

    Executes Aider commands and converts output to ExecutorReport.
    """

    def __init__(self, aider_path: str = "aider", cwd: Path | None = None, model: str = "ollama/codellama"):
        """
        Initialize Aider executor.

        Args:
            aider_path: Path to aider command (default: "aider")
            cwd: Working directory for execution
            model: LLM model to use (default: "ollama/codellama")
        """
        self.aider_path = aider_path
        self.cwd = cwd
        self.model = model
        self._validate_installation()

    def _validate_installation(self) -> None:
        """Check if Aider is installed."""
        result = subprocess.run(
            ["aider", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.warning("Aider not installed. Run: pip install aider-chat")

    def is_available(self) -> bool:
        """
        Check if Aider is available.

        Returns:
            True if aider command is available, False otherwise
        """
        logger.debug(f"Checking Aider availability: {self.aider_path}")
        try:
            import shutil

            available = shutil.which(self.aider_path) is not None
            logger.debug(f"Aider available: {available}")
            return available
        except Exception as e:
            logger.debug(f"Aider availability check failed: {e}")
            return False

    def generate_code(self, ctx: RunContext, plan: Plan, error_feedback: str | None = None) -> ExecutorReport:
        """
        Generate code using Aider.

        Args:
            ctx: Run context
            plan: Execution plan

        Returns:
            ExecutorReport with execution results
        """
        # Journal: Aider start
        append_event(
            ctx.run_path,
            "AIDER_START",
            {
                "files": plan.files or [],
                "objective": plan.objective or "",
                "model": "aider",
            },
            trace_id=ctx.trace_id,
        )

        # Build message
        message = self._build_message(plan, error_feedback)

        # Get target files
        target_files = plan.files or []
        if not target_files:
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=False,
                files_changed=[],
                error="No target files specified",
            )

        # Resolve file paths
        resolved_files = []
        for f in target_files:
            path = PROJECT_ROOT / f
            if path.exists():
                resolved_files.append(str(path))

        if not resolved_files:
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=False,
                files_changed=[],
                error="No valid target files found",
            )

        # Create temp file for message
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(message)
            message_file = f.name

        # Construct Aider command
        cmd = [
            self.aider_path,
            "--model", self.model,
            "--yes",  # Auto-accept changes
            "--no-git",  # We handle git separately
            "--message-file", message_file,
            *resolved_files,
        ]

        # Journal: Aider command
        command_str = " ".join(cmd)
        from ..constants import PROJECT_ROOT
        code_root = ctx.run_path if (ctx.run_path / ".git").exists() else PROJECT_ROOT
        append_event(
            ctx.run_path,
            "AIDER_COMMAND",
            {
                "command": command_str,
                "cwd": str(self.cwd or code_root),
            },
            trace_id=ctx.trace_id,
        )

        # Execute command
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                cwd=str(self.cwd or code_root),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                env={**os.environ, "AIDER_NO_BROWSER": "1"},
            )
            elapsed_ms = (time.time() - start_time) * 1000
            success = result.returncode == 0

            # Clean up
            os.unlink(message_file)

            # Combine stdout and stderr
            output = result.stdout + "\n" + result.stderr

            # Journal: Aider output
            append_event(
                ctx.run_path,
                "AIDER_OUTPUT",
                {
                    "exit_code": result.returncode,
                    "stdout_length": len(result.stdout),
                    "stderr_length": len(result.stderr),
                    "duration_ms": round(elapsed_ms, 2),
                },
                trace_id=ctx.trace_id,
            )

            # Parse stdout to extract files changed
            files_changed = self._parse_changed_files(output, resolved_files)

            # Journal: Files changed
            append_event(
                ctx.run_path,
                "AIDER_FILES_CHANGED",
                {
                    "files_changed": files_changed,
                    "diff_summary": result.stdout[:500] if result.stdout else "",
                },
                trace_id=ctx.trace_id,
            )

            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=success,
                files_changed=files_changed,
                commands_run=[command_str],
                outputs={"aider": output[:1000]},
                error=output[:1000] if not success else None,
            )
        except subprocess.TimeoutExpired:
            os.unlink(message_file)
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=False,
                files_changed=[],
                error="Aider timed out",
            )
        except Exception as e:
            # Clean up message file
            try:
                os.unlink(message_file)
            except:
                pass
            # Journal: Aider error
            append_event(
                ctx.run_path,
                "AIDER_ERROR",
                {
                    "error": str(e),
                    "exit_code": -1,
                },
                trace_id=ctx.trace_id,
            )
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=False,
                files_changed=[],
                error=str(e),
            )

    def _build_message(self, plan: Plan, error_feedback: str | None = None) -> str:
        """Build message for Aider."""
        parts = []

        # Objective
        objective = plan.objective or ""
        if objective:
            parts.append(objective)

        # Steps
        steps = plan.steps or []
        if steps:
            parts.append("\nSteps:")
            for step in steps:
                parts.append(f"- {step}")

        # Error feedback
        if error_feedback:
            parts.append(f"\nFix these errors:\n{error_feedback}")

        return "\n".join(parts)

    def _parse_changed_files(self, output: str, target_files: list[str]) -> list[str]:
        """
        Parse Aider output to find changed files.

        Args:
            output: Aider command output
            target_files: List of target files that were provided

        Returns:
            List of changed file paths
        """
        changed = []

        # Look for "Applied edit to" pattern
        for line in output.split("\n"):
            if "Applied edit to" in line or "Wrote" in line:
                for f in target_files:
                    if Path(f).name in line:
                        changed.append(f)

        # If nothing found, assume all target files changed
        if not changed and "Applied" in output:
            changed = target_files

        return list(set(changed))


# Type check: AiderExecutor implements ExecutorProtocol
def _type_check() -> None:
    """Type check helper."""
    _: ExecutorProtocol = AiderExecutor()  # Type check only
