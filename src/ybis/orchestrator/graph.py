"""
LangGraph Skeleton - State machine for Build workflow.

Defines WorkflowState and LangGraph nodes for the canonical workflow.

Note: All workflow nodes have been moved to src/ybis/orchestrator/nodes/
This file now only contains:
- WorkflowState: TypedDict definition
- _save_experience_to_memory: Helper function for saving run experience
- build_workflow_graph: Function to build workflow graph from YAML
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph

logger = logging.getLogger(__name__)

from ..constants import PROJECT_ROOT
from ..contracts import RunContext


class WorkflowState(TypedDict, total=False):
    """Workflow state - extends RunContext with status.

    Note: total=False allows optional keys for flexibility.
    """

    task_id: str
    run_id: str
    run_path: Path
    trace_id: str  # Distributed tracing ID
    task_objective: str  # Task objective (passed from initial state)
    status: str  # "pending", "running", "completed", "failed", "awaiting_approval"
    retries: int  # Number of retry attempts
    max_retries: int  # Maximum retry attempts
    error_context: str | None  # Error context from previous attempts
    current_step: int  # Current step index in multi-step plan
    task_tier: int | None  # Task tier (0, 1, 2) for cost optimization (optional)
    workflow_name: str | None  # Workflow name (e.g., "ybis_native") for artifact enforcement
    # Self-improve workflow specific state
    repair_retries: int  # Number of repair attempts in self-improve workflow
    max_repair_retries: int  # Maximum repair retry attempts
    repair_failed: bool  # Flag indicating repair failed
    repair_max_retries_reached: bool  # Flag indicating max repair retries reached
    test_passed: bool  # Flag indicating tests passed
    lint_passed: bool  # Flag indicating lint passed
    tests_passed: bool  # Flag indicating unit tests passed


def _save_experience_to_memory(ctx: RunContext, state: WorkflowState, success: bool) -> None:
    """
    Save run experience to vector store memory.

    Args:
        ctx: Run context
        state: Workflow state
        success: Whether the run was successful
    """
    try:
        from ..data_plane.vector_store import VectorStore
        from ..services.policy import get_policy_provider

        policy_provider = get_policy_provider()
        features = policy_provider.get_policy().get("features", {})
        memory_mode = features.get("memory", "auto")
        memory_mode = "required" if memory_mode is True else "disabled" if memory_mode is False else str(memory_mode).lower()
        if memory_mode in {"disabled", "off", "false", "0"}:
            return

        try:
            vector_store = VectorStore()
        except ImportError:
            if memory_mode in {"required", "strict"}:
                raise
            return
        collection = "experience"

        # Load plan if available
        plan_path = ctx.plan_path
        plan_summary = ""
        if plan_path.exists():
            import json

            plan_data = json.loads(plan_path.read_text())
            plan_summary = f"Objective: {plan_data.get('objective', '')}\nFiles: {plan_data.get('files', [])}"

        # Load executor report if available
        executor_path = ctx.executor_report_path
        executor_summary = ""
        if executor_path.exists():
            import json

            executor_data = json.loads(executor_path.read_text())
            executor_summary = f"Files changed: {executor_data.get('files_changed', [])}\nCommands: {executor_data.get('commands_run', [])}"

        # Create experience document
        if success:
            experience_text = f"SUCCESSFUL TASK:\nTask ID: {ctx.task_id}\n{plan_summary}\n\nSolution:\n{executor_summary}"
        else:
            # Load gate report for failure reason
            gate_path = ctx.gate_report_path
            failure_reason = ""
            if gate_path.exists():
                import json

                gate_data = json.loads(gate_path.read_text())
                failure_reason = f"Failure reasons: {gate_data.get('reasons', [])}"

            experience_text = f"FAILED TASK:\nTask ID: {ctx.task_id}\n{plan_summary}\n\nWhat NOT to do:\n{failure_reason}"

        # Save to vector store
        vector_store.add_documents(
            collection,
            [experience_text],
            [
                {
                    "task_id": ctx.task_id,
                    "run_id": ctx.run_id,
                    "success": success,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ],
        )

        # Journal event
        from ..syscalls.journal import append_event

        append_event(
            ctx.run_path,
            "EXPERIENCE_SAVED",
            {
                "collection": collection,
                "success": success,
                "task_id": ctx.task_id,
            },
            trace_id=ctx.trace_id,
        )

    except Exception as e:
        # Don't fail the workflow if memory save fails
        print(f"Failed to save experience to memory: {e}")


def build_workflow_graph(workflow_name: str = "ybis_native") -> StateGraph:
    """
    Build the workflow graph from YAML specification.

    Args:
        workflow_name: Name of workflow to load (default: "ybis_native")
                      Must be a valid YAML workflow in configs/workflows/

    Returns:
        Compiled LangGraph

    Raises:
        FileNotFoundError: If workflow YAML file not found
        ValueError: If workflow spec is invalid or nodes not registered
    """
    from ..services.adapter_bootstrap import bootstrap_adapters
    from ..workflows import WorkflowRunner, bootstrap_nodes

    bootstrap_adapters()
    bootstrap_nodes()  # Register all node types

    # Load workflow from YAML (mandatory, no fallback)
    runner = WorkflowRunner().load_workflow(workflow_name)
    return runner.build_graph()
