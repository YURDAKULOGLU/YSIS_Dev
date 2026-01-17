"""
Node Registry - Type-based node resolution for workflows.

Nodes are registered by type (e.g., "spec_generator", "planner") and resolved
at workflow execution time. This enables data-driven workflows where node
types are specified in YAML and implementations are resolved dynamically.
"""

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)

from ..syscalls.journal import append_event


class NodeProtocol(Protocol):
    """Protocol that all workflow nodes must implement."""

    def __call__(self, state: dict) -> dict:
        """Execute node logic and return updated state."""
        ...


class NodeRegistry:
    """
    Registry for workflow node types.

    Nodes are registered by type string (e.g., "spec_generator") and resolved
    when building workflows from YAML specs.
    """

    _nodes: dict[str, Callable] = {}
    _node_metadata: dict[str, dict] = {}

    @classmethod
    def register(
        cls,
        node_type: str,
        node_func: Callable,
        description: str | None = None,
        required_modules: list[str] | None = None,
        run_path: Path | None = None,
        trace_id: str | None = None,
    ) -> None:
        """
        Register a node type.

        Args:
            node_type: Node type identifier (e.g., "spec_generator")
            node_func: Node function that takes state and returns updated state
            description: Optional human-readable description
            required_modules: Optional list of required modules
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        cls._nodes[node_type] = node_func
        cls._node_metadata[node_type] = {
            "description": description or "",
            "required_modules": required_modules or [],
        }

        # Journal: Node register
        if run_path:
            append_event(
                run_path,
                "NODE_REGISTER",
                {
                    "node_type": node_type,
                },
                trace_id=trace_id,
            )

    @classmethod
    def get(cls, node_type: str, run_path: Path | None = None, trace_id: str | None = None) -> Callable | None:
        """
        Get node implementation by type.

        Args:
            node_type: Node type identifier
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging

        Returns:
            Node function or None if not found
        """
        result = cls._nodes.get(node_type)

        # Journal: Node resolve
        if run_path:
            append_event(
                run_path,
                "NODE_RESOLVE",
                {
                    "node_type": node_type,
                    "found": result is not None,
                },
                trace_id=trace_id,
            )

        return result

    @classmethod
    def list_types(cls) -> list[str]:
        """List all registered node types."""
        return list(cls._nodes.keys())

    @classmethod
    def get_metadata(cls, node_type: str) -> dict:
        """Get metadata for a node type."""
        return cls._node_metadata.get(node_type, {})

    @classmethod
    def is_registered(cls, node_type: str) -> bool:
        """Check if a node type is registered."""
        return node_type in cls._nodes


def register_node(
    node_type: str,
    description: str | None = None,
    required_modules: list[str] | None = None,
):
    """
    Decorator to register a node function.

    Usage:
        @register_node("spec_generator", description="Generates SPEC.md")
        def spec_node(state: Dict) -> Dict:
            # Node implementation
            return state
    """
    def decorator(func: Callable) -> Callable:
        NodeRegistry.register(node_type, func, description, required_modules)
        return func
    return decorator

