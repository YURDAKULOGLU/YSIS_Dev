"""
Dynamic Conditional Routing - Parse conditions from YAML and create routing functions.

Allows workflow YAML to define custom conditions instead of hardcoded functions.
"""

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

from ..orchestrator.graph import WorkflowState


def create_condition_function(condition_def: dict[str, Any]) -> Callable[[WorkflowState], str]:
    """
    Create a condition function from YAML definition.

    Args:
        condition_def: Condition definition from YAML
            {
                "type": "state_check",
                "field": "status",
                "operator": "eq",
                "value": "completed",
                "routes": {
                    "true": "next_node",
                    "false": "end_node"
                }
            }

    Returns:
        Condition function that takes WorkflowState and returns route key
    """
    condition_type = condition_def.get("type", "state_check")

    if condition_type == "state_check":
        return _create_state_check_condition(condition_def)
    elif condition_type == "artifact_check":
        return _create_artifact_check_condition(condition_def)
    elif condition_type == "expression":
        return _create_expression_condition(condition_def)
    else:
        raise ValueError(f"Unknown condition type: {condition_type}")


def _create_state_check_condition(condition_def: dict[str, Any]) -> Callable[[WorkflowState], str]:
    """Create condition that checks state field."""
    field = condition_def["field"]
    operator = condition_def.get("operator", "eq")
    value = condition_def["value"]
    routes = condition_def["routes"]

    def condition_func(state: WorkflowState) -> str:
        state_value = state.get(field)

        # Apply operator
        if operator == "eq":
            result = state_value == value
        elif operator == "ne":
            result = state_value != value
        elif operator == "in":
            result = state_value in value if isinstance(value, list) else False
        elif operator == "not_in":
            result = state_value not in value if isinstance(value, list) else False
        elif operator == "gt":
            result = state_value > value
        elif operator == "gte":
            result = state_value >= value
        elif operator == "lt":
            result = state_value < value
        elif operator == "lte":
            result = state_value <= value
        elif operator == "exists":
            result = state_value is not None
        elif operator == "not_exists":
            result = state_value is None
        else:
            result = False

        # Return route based on result
        return routes.get("true" if result else "false", routes.get("default", "end"))

    return condition_func


def _create_artifact_check_condition(condition_def: dict[str, Any]) -> Callable[[WorkflowState], str]:
    """Create condition that checks artifact existence/content."""
    artifact_name = condition_def["artifact"]
    check_type = condition_def.get("check", "exists")
    routes = condition_def["routes"]

    def condition_func(state: WorkflowState) -> str:
        from ..orchestrator.graph import RunContext

        ctx = RunContext(
            task_id=state["task_id"],
            run_id=state["run_id"],
            run_path=state["run_path"],
            trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
        )

        artifact_path = ctx.artifacts_dir / artifact_name

        if check_type == "exists":
            result = artifact_path.exists()
        elif check_type == "not_exists":
            result = not artifact_path.exists()
        elif check_type == "has_content":
            result = artifact_path.exists() and artifact_path.stat().st_size > 0
        else:
            result = False

        return routes.get("true" if result else "false", routes.get("default", "end"))

    return condition_func


def _create_expression_condition(condition_def: dict[str, Any]) -> Callable[[WorkflowState], str]:
    """Create condition from Python expression."""
    expression = condition_def["expression"]
    routes = condition_def["routes"]

    # Compile expression for safety (only allow state access)
    def condition_func(state: WorkflowState) -> str:
        try:
            # Safe evaluation (only state access)
            # In production, use ast.literal_eval or restricted eval
            result = eval(expression, {"__builtins__": {}}, {"state": state})
            return routes.get("true" if result else "false", routes.get("default", "end"))
        except Exception:
            # On error, use default route
            return routes.get("default", "end")

    return condition_func

