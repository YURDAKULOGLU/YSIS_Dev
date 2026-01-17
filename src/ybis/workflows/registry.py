"""
Workflow Registry - Load and manage workflow specifications.

Workflows are defined as YAML files in `configs/workflows/` and loaded
via the registry. The registry validates workflow specs against the schema
and provides discovery and loading capabilities.
"""

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

from ..constants import PROJECT_ROOT
from ..syscalls.journal import append_event


class WorkflowSpec:
    """Workflow specification loaded from YAML."""

    def __init__(self, data: dict):
        self.name = data["name"]
        self.version = data.get("version", 1)
        self.description = data.get("description", "")
        self.nodes = data["nodes"]
        self.connections = data["connections"]
        self.requirements = data.get("requirements", {})
        self._raw_data = data

    def get_node(self, node_id: str) -> dict | None:
        """Get node by ID."""
        for node in self.nodes:
            if node["id"] == node_id:
                return node
        return None

    def get_connections_from(self, node_id: str) -> list[dict]:
        """Get all connections from a node."""
        return [c for c in self.connections if c["from"] == node_id]

    def get_connections_to(self, node_id: str) -> list[dict]:
        """Get all connections to a node."""
        return [c for c in self.connections if c["to"] == node_id]


class WorkflowRegistry:
    """
    Registry for workflow specifications.

    Workflows are loaded from YAML files in `configs/workflows/` and
    cached for performance. The registry validates workflows against
    the schema before returning them.
    """

    _workflows: dict[str, WorkflowSpec] = {}
    _workflow_dir = PROJECT_ROOT / "configs" / "workflows"

    @classmethod
    def load_workflow(cls, name: str, run_path: Path | None = None, trace_id: str | None = None) -> WorkflowSpec:
        """
        Load workflow by name.

        Args:
            name: Workflow name (e.g., "ybis_native")
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging

        Returns:
            WorkflowSpec instance

        Raises:
            FileNotFoundError: If workflow file not found
            ValueError: If workflow spec is invalid
        """
        # Check cache first
        if name in cls._workflows:
            # Journal: Workflow get
            if run_path:
                append_event(
                    run_path,
                    "WORKFLOW_GET",
                    {
                        "workflow_name": name,
                        "from_cache": True,
                    },
                    trace_id=trace_id,
                )
            return cls._workflows[name]

        # Load from file
        workflow_path = cls._workflow_dir / f"{name}.yaml"
        if not workflow_path.exists():
            raise FileNotFoundError(f"Workflow '{name}' not found at {workflow_path}")

        with open(workflow_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Validate basic structure
        if "name" not in data:
            raise ValueError(f"Workflow '{name}' missing 'name' field")
        if "nodes" not in data:
            raise ValueError(f"Workflow '{name}' missing 'nodes' field")
        if "connections" not in data:
            raise ValueError(f"Workflow '{name}' missing 'connections' field")

        # Validate workflow name matches
        if data["name"] != name:
            raise ValueError(f"Workflow name mismatch: file has '{data['name']}', expected '{name}'")

        spec = WorkflowSpec(data)

        # Resolve inheritance if present
        if "extends" in data:
            from .inheritance import resolve_workflow_inheritance
            spec = resolve_workflow_inheritance(spec)

        cls._workflows[name] = spec

        # Journal: Workflow register
        if run_path:
            append_event(
                run_path,
                "WORKFLOW_REGISTER",
                {
                    "workflow_name": name,
                    "nodes_count": len(spec.nodes),
                },
                trace_id=trace_id,
            )

        return spec

    @classmethod
    def list_workflows(cls) -> list[str]:
        """
        List all available workflows.

        Returns:
            List of workflow names
        """
        if not cls._workflow_dir.exists():
            return []

        workflows = []
        for yaml_file in cls._workflow_dir.glob("*.yaml"):
            if yaml_file.name == "schema.yaml":
                continue
            workflow_name = yaml_file.stem
            workflows.append(workflow_name)

        return sorted(workflows)

    @classmethod
    def reload_workflow(cls, name: str) -> WorkflowSpec:
        """Reload workflow from disk (clears cache)."""
        if name in cls._workflows:
            del cls._workflows[name]
        return cls.load_workflow(name)

    @classmethod
    def clear_cache(cls) -> None:
        """Clear workflow cache."""
        cls._workflows.clear()


def load_workflow(name: str) -> WorkflowSpec:
    """
    Convenience function to load a workflow.

    Args:
        name: Workflow name

    Returns:
        WorkflowSpec instance
    """
    return WorkflowRegistry.load_workflow(name)

