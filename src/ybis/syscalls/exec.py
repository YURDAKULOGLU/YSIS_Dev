"""
Execution syscalls - Command execution with allowlist and journaling.

Follows Port Architecture: Uses E2B sandbox adapter when policy enables it.
"""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

from ..contracts import ExecutorReport, RunContext
from ..services.policy import get_policy_provider


def _is_allowed(cmd: list[str]) -> bool:
    """
    Check if command is in allowlist.

    Args:
        cmd: Command as list of strings

    Returns:
        True if command is allowed
    """
    if not cmd:
        return False

    # Get allowlist from policy
    policy_provider = get_policy_provider()
    allowed_commands = policy_provider.get_exec_allowlist()

    base_cmd = cmd[0]
    # Remove path if present (e.g., "/usr/bin/python" -> "python")
    # Also handle Windows paths like "C:\Python\python.exe" -> "python"
    base_cmd = Path(base_cmd).stem  # Use stem to remove .exe extension on Windows

    return base_cmd in allowed_commands


def run_command(
    cmd: list[str],
    ctx: RunContext,
    cwd: Path | None = None,
    is_primary_execution: bool = False,
    use_sandbox: bool | None = None,
) -> subprocess.CompletedProcess:
    """
    Run command with allowlist check and journaling.

    Follows Port Architecture: Uses E2B sandbox adapter when policy enables it.

    Args:
        cmd: Command as list of strings
        ctx: Run context
        cwd: Working directory (default: run_path)
        is_primary_execution: If True, writes executor_report.json
        use_sandbox: Override policy sandbox setting (None = use policy)

    Returns:
        CompletedProcess result (or mock result for sandbox execution)

    Raises:
        PermissionError: If command is not in allowlist
    """
    # Check allowlist
    if not _is_allowed(cmd):
        raise PermissionError(f"Command not in allowlist: {cmd[0]}")

    # Check if sandbox should be used
    policy_provider = get_policy_provider()
    if use_sandbox is None:
        use_sandbox = policy_provider.is_sandbox_enabled()

    # Use E2B sandbox if enabled
    sandbox_used = False
    if use_sandbox and policy_provider.get_sandbox_type() == "e2b":
        if not policy_provider.is_network_allowed():
            from .journal import append_event

            append_event(
                ctx.run_path,
                "SANDBOX_FALLBACK",
                {
                    "reason": "Sandbox network disabled by policy",
                    "fallback": "local_subprocess",
                },
            )
        else:
            try:
                from ..adapters.e2b_sandbox import E2BSandboxAdapter

                with E2BSandboxAdapter(ctx) as sandbox:
                    # Execute in sandbox
                    result_dict = sandbox.execute_command(cmd, cwd=str(cwd) if cwd else None)

                    # Convert to CompletedProcess-like object
                    class SandboxResult:
                        def __init__(self, result_dict):
                            self.returncode = result_dict["exit_code"]
                            self.stdout = result_dict["stdout"]
                            self.stderr = result_dict["stderr"]

                    result = SandboxResult(result_dict)
                    sandbox_used = True

            except (ImportError, ValueError, Exception) as e:
                # Fallback to local execution if E2B not available
                from .journal import append_event

                append_event(
                    ctx.run_path,
                    "SANDBOX_FALLBACK",
                    {
                        "reason": str(e),
                        "fallback": "local_subprocess",
                    },
                )

                # Continue with local execution
                sandbox_used = False

    # Local execution (fallback or policy setting)
    if not sandbox_used:
        work_dir = cwd or ctx.run_path
        result = subprocess.run(
            cmd,
            cwd=work_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    # Journal event
    from .journal import append_event

    append_event(
        ctx.run_path,
        "COMMAND_EXEC",
        {
            "command": " ".join(cmd),
            "exit_code": result.returncode,
            "stdout_length": len(result.stdout),
            "stderr_length": len(result.stderr),
            "stdout_summary": result.stdout[:200] if result.stdout else "",
            "stderr_summary": result.stderr[:200] if result.stderr else "",
            "sandbox_used": sandbox_used,
        },
    )

    # Write executor_report.json if this was a primary execution
    if is_primary_execution:
        report = ExecutorReport(
            task_id=ctx.task_id,
            run_id=ctx.run_id,
            success=(result.returncode == 0),
            commands_run=[" ".join(cmd)],
            outputs={" ".join(cmd): result.stdout[:1000]},
            error=result.stderr[:1000] if result.returncode != 0 else None,
        )

        report_path = ctx.artifacts_dir / "executor_report.json"
        report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")

    return result

