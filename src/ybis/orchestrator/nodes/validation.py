"""
Validation Nodes - Validate spec, plan, and implementation.

Includes:
- validate_spec_node: Validates spec structure and completeness
- validate_plan_node: Validates plan against spec requirements
- validate_impl_node: Validates implementation against spec
"""

import json
import logging

from ...contracts import RunContext
from ...syscalls import write_file
from ..graph import WorkflowState
from ..logging import log_node_execution
from ..spec_validator import (
    generate_spec_validation_artifact,
    validate_implementation_against_spec,
    validate_plan_against_spec,
    validate_spec,
)

logger = logging.getLogger(__name__)


@log_node_execution("validate_spec")
def validate_spec_node(state: WorkflowState) -> WorkflowState:
    """
    Validate spec node - validates spec structure and completeness.

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

    logger.info(f"Validate spec node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Validate spec
    validation_result = validate_spec(ctx)

    # Write validation result
    validation_path = ctx.run_path / "artifacts" / "spec_structure_validation.json"
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    write_file(validation_path, json.dumps(validation_result, indent=2), ctx)

    state["status"] = "running"
    return state


@log_node_execution("validate_plan")
def validate_plan_node(state: WorkflowState) -> WorkflowState:
    """
    Validate plan node - validates plan against spec requirements.

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

    logger.info(f"Validate plan node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Validate plan against spec
    validation_result = validate_plan_against_spec(ctx)

    # Write validation result
    validation_path = ctx.run_path / "artifacts" / "plan_validation.json"
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    write_file(validation_path, json.dumps(validation_result, indent=2), ctx)

    state["status"] = "running"
    return state


@log_node_execution("validate_impl")
def validate_impl_node(state: WorkflowState) -> WorkflowState:
    """
    Validate implementation node - validates implementation against spec.

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

    logger.info(f"Validate impl node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Validate implementation against spec (only if executor report exists)
    executor_path = ctx.executor_report_path
    if executor_path.exists():
        validation_result = validate_implementation_against_spec(ctx)

        # Write validation result
        validation_path = ctx.run_path / "artifacts" / "implementation_validation.json"
        validation_path.parent.mkdir(parents=True, exist_ok=True)
        write_file(validation_path, json.dumps(validation_result, indent=2), ctx)

        # Generate comprehensive spec validation artifact (for gates)
        generate_spec_validation_artifact(ctx)
    else:
        # No executor report yet - skip validation (will be validated after execution)
        # Just create a stub validation result
        validation_result = {
            "executor_report_exists": False,
            "compliance_score": None,
            "messages": ["Executor report not found - validation skipped"],
        }
        validation_path = ctx.run_path / "artifacts" / "implementation_validation.json"
        validation_path.parent.mkdir(parents=True, exist_ok=True)
        write_file(validation_path, json.dumps(validation_result, indent=2), ctx)

    state["status"] = "running"
    return state
