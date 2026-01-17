"""OpenHands adapter for SOTA autonomous code editing.

OpenHands (formerly OpenDevin) is the open-source platform for
autonomous software development agents.

Features:
- SWE-bench SOTA performance (79%+ on Verified)
- Function calling for precise edits
- Works with any LLM (Claude, GPT, Ollama)
- Sandboxed execution environment

Usage:
    adapter = OpenHandsAdapter()
    result = adapter.execute_task(ctx, plan)
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..contracts.context import RunContext
from ..contracts.evidence import ExecutorReport
from ..services.policy import get_policy_provider
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)


@dataclass
class OpenHandsConfig:
    """Configuration for OpenHands adapter."""

    model: str = "anthropic/claude-3-5-sonnet"
    max_iterations: int = 30
    timeout: int = 600  # 10 minutes
    sandbox: bool = True
    workspace_mount: bool = True

    # LLM settings
    temperature: float = 0.0
    max_tokens: int = 4096

    # API keys (from env)
    api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

    @classmethod
    def from_policy(cls, policy: dict) -> "OpenHandsConfig":
        """Create config from policy settings."""
        oh_config = policy.get("openhands", {})
        return cls(
            model=oh_config.get("model", cls.model),
            max_iterations=oh_config.get("max_iterations", cls.max_iterations),
            timeout=oh_config.get("timeout", cls.timeout),
            sandbox=oh_config.get("sandbox", cls.sandbox),
        )


class OpenHandsAdapter:
    """Adapter for OpenHands autonomous coding agent.

    This adapter provides integration with OpenHands for:
    - Autonomous code editing and generation
    - Test fixing and debugging
    - Multi-file refactoring
    - Issue resolution
    """

    def __init__(self, config: OpenHandsConfig | None = None):
        if config is None:
            policy = get_policy_provider().get_policy()
            config = OpenHandsConfig.from_policy(policy)
        self.config = config
        self._validate_installation()

    def _validate_installation(self) -> None:
        """Check if OpenHands is installed."""
        try:
            import openhands
            self.openhands = openhands
            logger.info("OpenHands adapter initialized successfully")
        except ImportError:
            logger.warning("OpenHands not installed. Run: pip install openhands-ai")
            self.openhands = None

    def is_available(self) -> bool:
        """Check if OpenHands is available."""
        return self.openhands is not None

    def execute_task(
        self,
        ctx: RunContext,
        plan: dict,
        error_feedback: str | None = None,
    ) -> ExecutorReport:
        """Execute a coding task using OpenHands.

        Args:
            ctx: Run context with paths and config
            plan: Execution plan with target files and instructions
            error_feedback: Optional feedback from previous failures

        Returns:
            ExecutorResult with files changed and status
        """
        if not self.is_available():
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=False,
                files_changed=[],
                error="OpenHands not installed. Run: pip install openhands-ai",
            )

        # 1. Environment Validation (Ruff check)
        self._verify_environment(ctx)

        # 2. Build task description (Injects Constitution)
        task_description = self._build_task_description(plan, error_feedback)

        # 3. Get target files
        target_files = plan.get("target_files", [])

        # Log start
        append_event(ctx.run_path, "OPENHANDS_START", {
            "task": task_description[:200],
            "files": target_files,
            "model": self.config.model,
        })

        try:
            # Run OpenHands
            result = self._run_openhands(
                workspace=ctx.run_path,
                task=task_description,
                files=target_files,
            )

            # Parse result
            files_changed = result.get("files_modified", [])
            log_changed = self._get_openhands_edited_files(ctx.run_path)
            if log_changed:
                files_changed = log_changed
                result["files_modified"] = files_changed
            else:
                git_changed = self._get_git_changed_files(ctx.run_path)
                if git_changed:
                    files_changed = git_changed
                    result["files_modified"] = files_changed
            success = result.get("success", False)

            # 4. Scope Enforcement (Constitution Mandate 1.2)
            scope_violation = self._check_scope_violation(target_files, files_changed)
            if scope_violation:
                logger.warning(f"SCOPE VIOLATION: {scope_violation}")
                success = False
                result["summary"] = f"CRITICAL: Scope Violation Detected. {scope_violation}"

            # Log completion
            append_event(ctx.run_path, "OPENHANDS_COMPLETE", {
                "success": success,
                "files_changed": len(files_changed),
                "scope_violation": bool(scope_violation),
                "iterations": result.get("iterations", 0),
            })

            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=success,
                files_changed=files_changed,
                commands_run=[f"openhands: {task_description[:100]}"],
                outputs={"openhands": result.get("summary", "")},
                error=None
                if success
                else (
                    result.get("summary")
                    or result.get("last_error")
                    or "OpenHands execution failed"
                ),
            )

        except Exception as e:
            logger.error(f"OpenHands execution failed: {e}", exc_info=True)
            append_event(ctx.run_path, "OPENHANDS_ERROR", {"error": str(e)})

            # Fallback to LocalCoder if OpenHands runtime/CLI is unavailable.
            try:
                from ..adapters.local_coder import LocalCoderExecutor

                append_event(
                    ctx.run_path,
                    "OPENHANDS_FALLBACK",
                    {"executor": "local_coder", "reason": str(e)},
                )
                fallback = LocalCoderExecutor()
                fallback_plan = type("PlanShim", (), {
                    "objective": plan.get("objective", ""),
                    "files": target_files,
                    "instructions": "\n".join(plan.get("steps", [])),
                    "steps": [],
                })()
                return fallback.generate_code(ctx, fallback_plan, error_context=error_feedback)
            except Exception:
                return ExecutorReport(
                    task_id=ctx.task_id,
                    run_id=ctx.run_id,
                    success=False,
                    files_changed=[],
                    error=f"OpenHands execution failed: {e}",
                )

    def generate_code(
        self,
        ctx: RunContext,
        plan,
        error_context: str | None = None,
    ) -> ExecutorReport:
        """
        ExecutorProtocol compatibility wrapper for OpenHands.
        """
        steps = []
        if getattr(plan, "steps", None):
            for step in plan.steps:
                if isinstance(step, dict):
                    action = step.get("action", "").strip()
                    description = step.get("description", "").strip()
                    if action and description:
                        steps.append(f"{action}: {description}")
                    elif action:
                        steps.append(action)
                    elif description:
                        steps.append(description)
                else:
                    steps.append(str(step))
        elif getattr(plan, "instructions", None):
            steps.append(plan.instructions)

        plan_dict = {
            "objective": getattr(plan, "objective", "Complete the task"),
            "target_files": getattr(plan, "files", []),
            "steps": steps,
        }
        return self.execute_task(ctx, plan_dict, error_feedback=error_context)

    def _build_task_description(
        self,
        plan: dict,
        error_feedback: str | None = None,
    ) -> str:
        """Build task description for OpenHands."""
        parts = []

        # Main objective
        objective = plan.get("objective", "Complete the task")
        parts.append(f"## Objective\n{objective}")

        # Target files
        files = plan.get("target_files", [])
        if files:
            parts.append(f"## Target Files\n" + "\n".join(f"- {f}" for f in files))

        # Steps
        steps = plan.get("steps", [])
        if steps:
            parts.append("## Steps")
            for i, step in enumerate(steps, 1):
                parts.append(f"{i}. {step}")

        # Error feedback (from repair loop)
        if error_feedback:
            parts.append(f"## Previous Errors to Fix\n{error_feedback}")

        # Constitutional Mandates (ASCII only; avoid Unicode log issues)
        parts.append("""
## AI SYSTEM CONSTITUTION (MANDATORY)
You MUST follow these rules or the run will be terminated:
1. **Startup**: State "Context loaded, constitutional protocols active" as your first action.
2. **Surgical Edits**: Use the editor tool (`str_replace_editor`) for targeted edits. Use `str_replace` only (do NOT use `insert`). PROHIBITED: sed/grep/find and rewriting files entirely unless necessary.
3. **Scope Control**: Only modify the target files listed above. Unplanned writes to config files or legacy directories trigger a Security Violation.
4. **Sentinel Compliance**:
    - All Python functions MUST have type hints.
    - All changes MUST pass `ruff check <files>` when lint is required.
5. **No Placeholders**: Do not use "TASK-1234" or "TODO" for critical logic. Use the current task context.
6. **Shell Commands**: Use `execute_bash` only. Powershell is not available.
""")

        return "\n\n".join(parts)

    def _verify_environment(self, ctx: RunContext) -> None:
        """Ensure critical tools are available in the sandbox."""
        # Note: In docker mode, we might need to run this INSIDE the sandbox later.
        # But as an adapter, we can at least check if ruff is in the current Python environment
        # which is usually where OpenHands starts its runtime.
        try:
            subprocess.run(["ruff", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Ruff not found in environment. Sentinel duties may fail.")
            # We don't block here because OpenHands might have it in its internal sandbox
            # But we log it for observability.

    def _check_scope_violation(self, planned: list[str], actual: list[str]) -> str | None:
        """Check if the agent modified unauthorized files."""
        if not planned:
            return None

        planned_set = {str(Path(p).as_posix()) for p in planned}
        # Ignore temporary files created by OpenHands/Git
        actual_set = {
            str(Path(p).as_posix())
            for p in actual
            if not p.endswith((".log", ".tmp", "TASK_BOARD.md", "executor_report.json"))
            and ".sandbox_worker" not in p
        }

        unauthorized = actual_set - planned_set
        if unauthorized:
            return f"Unauthorized file modifications: {', '.join(unauthorized)}"

        return None

    def _get_git_changed_files(self, workspace: Path) -> list[str]:
        """Return git-tracked changes in the run workspace."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=workspace,
                capture_output=True,
                text=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []

        changed_files: list[str] = []
        for line in result.stdout.splitlines():
            if not line:
                continue
            entry = line[3:]
            if " -> " in entry:
                entry = entry.split(" -> ", 1)[1]
            changed_files.append(entry.replace("\\", "/"))
        return changed_files

    def _get_openhands_edited_files(self, workspace: Path) -> list[str]:
        """Return files edited by OpenHands based on its local log."""
        log_path = workspace / "openhands.log"
        if not log_path.exists():
            return []

        edited_files: list[str] = []
        try:
            with log_path.open("r", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if "The file /workspace/" not in line or "has been edited" not in line:
                        continue
                    start = line.find("The file /workspace/")
                    if start == -1:
                        continue
                    start += len("The file /workspace/")
                    end = line.find(" has been edited", start)
                    if end == -1:
                        continue
                    edited_files.append(line[start:end].strip())
        except OSError:
            return []

        return sorted(set(edited_files))

    def _run_openhands(
        self,
        workspace: Path,
        task: str,
        files: list[str],
    ) -> dict[str, Any]:
        """Run OpenHands agent on task.

        This uses the OpenHands Python API for integration.
        """
        if not self.openhands:
            raise RuntimeError("OpenHands not available")

        try:
            os.environ.setdefault("LOG_LEVEL", "DEBUG")
            os.environ.setdefault("DEBUG_RUNTIME", "true")
            if self.config.sandbox and os.name == "nt":
                os.environ.setdefault("OPENHANDS_FORCE_DOCKER", "1")

            from openhands.core.config import LLMConfig, OpenHandsConfig, SandboxConfig
            from openhands.core.logger import openhands_logger
            from openhands.core.main import auto_continue_response, run_controller
            from openhands.core.schema import AgentState
            from openhands.events.action import MessageAction
            from openhands.utils.async_utils import call_async_from_sync

            self._attach_openhands_log_handler(openhands_logger, workspace)

            llm_config = LLMConfig(
                model=self.config.model,
                api_key=self.config.api_key or None,
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
            )
            if self.config.model.startswith(("ollama/", "ollama:")):
                llm_config.ollama_base_url = (
                    os.getenv("OLLAMA_API_BASE") or os.getenv("OLLAMA_BASE_URL")
                )

            sandbox_config = SandboxConfig()
            config = OpenHandsConfig(
                llms={"llm": llm_config},
                max_iterations=self.config.max_iterations,
                sandbox=sandbox_config,
            )

            use_docker = self.config.sandbox and (
                os.name != "nt" or os.getenv("OPENHANDS_FORCE_DOCKER") == "1"
            )
            if use_docker:
                config.runtime = "docker"
                config.workspace_mount_path_in_sandbox = "/workspace"
                config.workspace_mount_path = str(workspace)
                if os.name != "nt":
                    sandbox_config.volumes = f"{workspace}:/workspace:rw"
            else:
                config.runtime = "local"
                config.workspace_base = str(workspace)

            initial_action = MessageAction(content=task)
            state = call_async_from_sync(
                run_controller,
                self.config.timeout,
                config=config,
                initial_user_action=initial_action,
                fake_user_response_fn=auto_continue_response,
            )
            summary = ""
            agent_state = None
            last_error = None
            if state is not None:
                agent_state = getattr(state, "agent_state", None)
                last_error = getattr(state, "last_error", None)
                last_message = state.get_last_agent_message()
                if last_message and getattr(last_message, "content", None):
                    summary = last_message.content

            return {
                "success": agent_state == AgentState.FINISHED,
                "files_modified": self._collect_git_changes(workspace),
                "summary": summary,
                "iterations": None,
                "cost": None,
                "agent_state": agent_state,
                "last_error": last_error,
            }
        except ImportError:
            # Fallback: Use CLI if API not available
            logger.warning("OpenHands API not available, falling back to CLI")
            return self._run_openhands_cli(workspace, task, files)

    def _run_openhands_cli(
        self,
        workspace: Path,
        task: str,
        files: list[str],
    ) -> dict[str, Any]:
        """Fallback: Run OpenHands via CLI."""
        # Create task file
        task_file = workspace / "openhands_task.md"
        task_file.write_text(task, encoding="utf-8")

        # Run OpenHands CLI
        cmd = [
            "openhands",
            "--task", str(task_file),
            "--workspace", str(workspace),
            "--model", self.config.model,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                cwd=str(workspace),
            )

            # Parse output (simplified)
            success = result.returncode == 0
            files_modified = files if success else []

            return {
                "success": success,
                "files_modified": files_modified,
                "summary": result.stdout[:500] if result.stdout else "",
                "iterations": 0,
                "cost": 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "files_modified": [],
                "summary": "OpenHands timed out",
                "iterations": 0,
                "cost": 0,
            }

    def fix_lint_errors(
        self,
        ctx: RunContext,
        errors: list[dict],
    ) -> ExecutorReport:
        """Specifically fix lint errors.

        For simple lint fixes, we can use ruff --fix first,
        then fall back to OpenHands for complex issues.
        """
        # Try ruff --fix first
        fixable_files = list(set(e.get("file") for e in errors if e.get("fixable")))

        if fixable_files:
            subprocess.run(
                ["python", "-m", "ruff", "check", "--fix", *fixable_files],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
            )

        # Check if issues remain
        result = subprocess.run(
            ["python", "-m", "ruff", "check", "--output-format=json", *fixable_files],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=True,
                files_changed=fixable_files,
                commands_run=["ruff check --fix"],
                outputs={"ruff": "Lint errors fixed by ruff --fix"},
            )

        # Fall back to OpenHands for remaining issues
        remaining_errors = json.loads(result.stdout) if result.stdout else []

        if remaining_errors:
            plan = {
                "objective": "Fix the remaining lint errors",
                "target_files": fixable_files,
                "steps": [f"Fix {e['code']}: {e['message']}" for e in remaining_errors[:10]],
            }
            return self.execute_task(ctx, plan)

        return ExecutorReport(
            task_id=ctx.task_id,
            run_id=ctx.run_id,
            success=True,
            files_changed=fixable_files,
            commands_run=["ruff check --fix"],
            outputs={"ruff": "All lint errors fixed"},
        )

    def _collect_git_changes(self, workspace: Path) -> list[str]:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(workspace),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []
        files: list[str] = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            path = line[3:]
            if "->" in path:
                path = path.split("->")[-1].strip()
            files.append(path)
        return files

    def _attach_openhands_log_handler(
        self, logger: logging.Logger, workspace: Path
    ) -> None:
        log_path = workspace / "openhands.log"
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler) and getattr(
                handler, "baseFilename", None
            ) == str(log_path):
                return
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s:%(levelname)s: %(filename)s:%(lineno)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)


# Adapter registry entry
ADAPTER_CONFIG = {
    "name": "openhands",
    "class": OpenHandsAdapter,
    "description": "OpenHands autonomous coding agent (SWE-bench SOTA)",
    "default_enabled": True,
    "priority": 10,  # Higher priority than LocalCoder
    "capabilities": [
        "code_generation",
        "code_editing",
        "test_fixing",
        "refactoring",
        "debugging",
    ],
    "requirements": [
        "openhands-ai==1.2.1",
    ],
}
