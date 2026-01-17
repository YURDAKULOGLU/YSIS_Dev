"""
Node Configuration Injection - Pass config from workflow YAML to nodes.

Allows nodes to receive configuration parameters from workflow YAML.
"""

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

from ..orchestrator.graph import WorkflowState


def inject_node_config(
    node_func: Callable,
    node_config: dict[str, Any] | None,
    node_id: str,
    node_type: str,
) -> Callable:
    """
    Inject node configuration into node function.

    Args:
        node_func: Original node function
        node_config: Configuration from workflow YAML

    Returns:
        Wrapped node function with config injected
    """
    if not node_config:
        return node_func

    def wrapped_node(state: WorkflowState) -> WorkflowState:
        # Inject config into state
        if "node_config" not in state:
            state["node_config"] = {"nodes": {}, "types": {}}
        if "nodes" not in state["node_config"]:
            state["node_config"]["nodes"] = {}
        if "types" not in state["node_config"]:
            state["node_config"]["types"] = {}

        state["node_config"]["nodes"][node_id] = node_config
        # Keep a type-level view for shared defaults by node type.
        state["node_config"]["types"].setdefault(node_type, node_config)

        # Track current node identity for consumers.
        state["current_node_id"] = node_id
        state["current_node_type"] = node_type

        # Call original node function
        result = node_func(state)

        # Config persists in state for downstream nodes
        return result

    return wrapped_node


def get_node_config(
    state: WorkflowState,
    node_id: str,
    key: str,
    default: Any = None,
) -> Any:
    """
    Get node configuration value from state.

    Args:
        state: Workflow state
        node_id: Node identifier
        key: Config key
        default: Default value if not found

    Returns:
        Config value or default
    """
    node_config = state.get("node_config", {})
    nodes_config = node_config.get("nodes", {})
    types_config = node_config.get("types", {})

    if node_id in nodes_config:
        return nodes_config[node_id].get(key, default)

    # Check type-level config as fallback
    node_type = state.get("current_node_type")
    if node_type and node_type in types_config:
        return types_config[node_type].get(key, default)

    # Backward-compatible flat config
    if isinstance(node_config, dict):
        return node_config.get(key, default)

    return default


def get_current_node_config(
    state: WorkflowState,
    key: str,
    default: Any = None,
) -> Any:
    """
    Get config for the currently executing node.
    """
    node_id = state.get("current_node_id")
    if not node_id:
        return default
    return get_node_config(state, node_id, key, default)
