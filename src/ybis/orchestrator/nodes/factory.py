"""
Factory Node - Spawns sub-factory structure for complex tasks.
"""

from ...contracts import RunContext
from ...syscalls.journal import append_event
from ..graph import WorkflowState
from ..logging import log_node_execution
from ..logging import log_node_execution


@log_node_execution("factory")
def spawn_sub_factory_node(state: WorkflowState) -> WorkflowState:
    """
    Spawn sub-factory node - creates nested YBIS structure for complex tasks.

    Args:
        state: Workflow state

    Returns:
        Updated state
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    # Check if task is marked as sub-factory
    # For now, we'll check if objective contains "complex" or "sub-factory"
    # In production, this would check task.is_sub_factory

    # Create sub-factory structure
    sub_factory_path = ctx.run_path / "sub_factory"
    sub_factory_path.mkdir(parents=True, exist_ok=True)

    # Initialize minimal YBIS structure
    (sub_factory_path / "src" / "ybis").mkdir(parents=True, exist_ok=True)
    (sub_factory_path / "workspaces").mkdir(exist_ok=True)
    (sub_factory_path / "platform_data").mkdir(exist_ok=True)

    # Write a marker file
    marker_path = sub_factory_path / ".ybis_sub_factory"
    marker_path.write_text(f"Sub-factory for task {state['task_id']}\n", encoding="utf-8")

    # Journal event
    append_event(
        ctx.run_path,
        "SUB_FACTORY_SPAWNED",
        {
            "sub_factory_path": str(sub_factory_path),
            "task_id": state["task_id"],
        },
    )

    state["status"] = "running"
    return state

