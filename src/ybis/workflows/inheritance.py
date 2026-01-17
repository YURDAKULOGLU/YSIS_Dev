"""
Workflow Inheritance - Support for extending and overriding workflows.

Allows workflows to extend base workflows and override nodes/connections.
"""

import logging

from .registry import WorkflowRegistry, WorkflowSpec

logger = logging.getLogger(__name__)


def resolve_workflow_inheritance(spec: WorkflowSpec) -> WorkflowSpec:
    """
    Resolve workflow inheritance by loading base workflow and merging.

    Args:
        spec: Workflow spec that may have 'extends' field

    Returns:
        Resolved WorkflowSpec with base workflow merged
    """
    if "extends" not in spec._raw_data:
        # No inheritance, return as-is
        return spec

    base_name = spec._raw_data["extends"]

    # Load base workflow
    try:
        base_spec = WorkflowRegistry.load_workflow(base_name)
    except FileNotFoundError:
        raise ValueError(f"Base workflow '{base_name}' not found")

    # Merge base and child specs
    merged_data = _merge_workflow_specs(base_spec._raw_data, spec._raw_data)

    # Create new merged spec
    merged_spec = WorkflowSpec(merged_data)
    return merged_spec


def _merge_workflow_specs(base: dict, child: dict) -> dict:
    """
    Merge base and child workflow specs.

    Merge strategy:
    - Nodes: Child nodes override base nodes with same ID, new nodes are added
    - Connections: Child connections override base connections (by from/to), new connections are added
    - Requirements: Child requirements extend base requirements (union)
    - Other fields: Child overrides base

    Args:
        base: Base workflow data
        child: Child workflow data

    Returns:
        Merged workflow data
    """
    merged = base.copy()

    # Override top-level fields
    merged["name"] = child["name"]
    merged["version"] = child.get("version", base.get("version", 1))
    merged["description"] = child.get("description", base.get("description", ""))

    # Merge nodes
    base_nodes = {node["id"]: node for node in base.get("nodes", [])}
    child_nodes = {node["id"]: node for node in child.get("nodes", [])}

    # Start with base nodes
    merged_nodes = list(base_nodes.values())

    # Override or add child nodes
    for child_node in child.get("nodes", []):
        node_id = child_node["id"]
        if node_id in base_nodes:
            # Override base node
            base_node = base_nodes[node_id]
            # Merge config if both have it
            if "config" in base_node and "config" in child_node:
                merged_config = base_node["config"].copy()
                merged_config.update(child_node["config"])
                child_node["config"] = merged_config

            # Replace in merged list
            merged_nodes = [n for n in merged_nodes if n["id"] != node_id]
            merged_nodes.append(child_node)
        else:
            # New node, add it
            merged_nodes.append(child_node)

    merged["nodes"] = merged_nodes

    # Merge connections
    # Connections are identified by (from, to) tuple
    base_connections = {
        (conn["from"], conn["to"]): conn
        for conn in base.get("connections", [])
    }
    child_connections = {
        (conn["from"], conn["to"]): conn
        for conn in child.get("connections", [])
    }

    # Start with base connections
    merged_connections = list(base_connections.values())

    # Override or add child connections
    for child_conn in child.get("connections", []):
        conn_key = (child_conn["from"], child_conn["to"])
        if conn_key in base_connections:
            # Override base connection
            merged_connections = [
                c for c in merged_connections
                if (c["from"], c["to"]) != conn_key
            ]
            merged_connections.append(child_conn)
        else:
            # New connection, add it
            merged_connections.append(child_conn)

    merged["connections"] = merged_connections

    # Merge requirements (union)
    base_reqs = base.get("requirements", {})
    child_reqs = child.get("requirements", {})

    merged_reqs = {}
    for key in ["modules", "artifacts", "adapters"]:
        base_list = base_reqs.get(key, [])
        child_list = child_reqs.get(key, [])
        # Union (remove duplicates, preserve order)
        merged_list = list(dict.fromkeys(base_list + child_list))
        if merged_list:
            merged_reqs[key] = merged_list

    if merged_reqs:
        merged["requirements"] = merged_reqs

    return merged

