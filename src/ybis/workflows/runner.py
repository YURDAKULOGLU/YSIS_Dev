"""
Workflow Runner - Execute workflows from YAML specifications.

The WorkflowRunner loads workflow specs, resolves node types via NodeRegistry,
and builds LangGraph StateGraph instances for execution.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from langgraph.graph import END, START, StateGraph

from ..orchestrator.graph import WorkflowState
from ..syscalls.journal import append_event
from .conditional_routing import (
    should_replan,
    repair_route,
    should_continue_steps,
    should_debate,
    should_retry_route,
    test_failed,
    test_passed,
)
from .dynamic_conditions import create_condition_function
from .node_config import inject_node_config
from .node_registry import NodeRegistry
from .registry import WorkflowRegistry, WorkflowSpec


class WorkflowRunner:
    """
    Runner for workflow specifications.

    Loads workflow YAML, resolves nodes via registry, and builds LangGraph
    StateGraph for execution.
    """

    def __init__(self, workflow_spec: WorkflowSpec | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize workflow runner.

        Args:
            workflow_spec: Optional WorkflowSpec instance. If None, must call
                         load_workflow() before building graph.
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.spec = workflow_spec
        self.node_registry = NodeRegistry
        self.run_path = run_path
        self.trace_id = trace_id

    def load_workflow(self, name: str) -> "WorkflowRunner":
        """
        Load workflow by name.

        Args:
            name: Workflow name (e.g., "ybis_native")

        Returns:
            Self for chaining
        """
        self.spec = WorkflowRegistry.load_workflow(name)

        # Journal: Workflow loaded
        if self.run_path:
            append_event(
                self.run_path,
                "WORKFLOW_LOAD",
                {
                    "workflow_name": name,
                },
                trace_id=self.trace_id,
            )

        return self

    def build_graph(self) -> StateGraph:
        """
        Build LangGraph StateGraph from workflow spec.

        Returns:
            Compiled StateGraph ready for execution

        Raises:
            ValueError: If workflow spec not loaded or nodes not registered
        """
        if self.spec is None:
            raise ValueError("Workflow spec not loaded. Call load_workflow() first.")

        # Create graph
        graph = StateGraph(WorkflowState)

        # Add nodes
        for node_def in self.spec.nodes:
            node_id = node_def["id"]
            node_type = node_def["type"]

            # Resolve node implementation
            node_func = self.node_registry.get(node_type)
            if node_func is None:
                raise ValueError(
                    f"Node type '{node_type}' (node '{node_id}') not registered. "
                    f"Available types: {self.node_registry.list_types()}"
                )

            def _wrap_with_identity(func, node_id=node_id, node_type=node_type):
                def wrapped(state: WorkflowState) -> WorkflowState:
                    state["current_node_id"] = node_id
                    state["current_node_type"] = node_type
                    return func(state)
                return wrapped

            node_func = _wrap_with_identity(node_func)

            # Inject node config if available
            node_config = node_def.get("config", {})
            if node_config:
                node_func = inject_node_config(
                    node_func,
                    node_config,
                    node_id=node_id,
                    node_type=node_type,
                )

            # Add node to graph
            graph.add_node(node_id, node_func)

        # Add edges
        # First, collect all unconditional and conditional edges
        unconditional_edges = []
        conditional_edges = []

        for conn in self.spec.connections:
            if "condition" in conn:
                conditional_edges.append(conn)
            else:
                unconditional_edges.append(conn)

        # Group unconditional edges by source to detect parallel execution
        # LangGraph automatically executes parallel nodes when multiple edges
        # are added from the same source
        unconditional_by_source = {}
        for conn in unconditional_edges:
            source = conn["from"]
            if source not in unconditional_by_source:
                unconditional_by_source[source] = []
            unconditional_by_source[source].append(conn)

        # Add unconditional edges (parallel execution is automatic)
        for conn in unconditional_edges:
            from_node = conn["from"]
            to_node = conn["to"]

            # Handle START/END special nodes
            if from_node == "START":
                from_node = START
            elif from_node not in [n["id"] for n in self.spec.nodes]:
                raise ValueError(f"Connection from unknown node: {from_node}")

            if to_node == "END":
                to_node = END
            elif to_node not in [n["id"] for n in self.spec.nodes]:
                raise ValueError(f"Connection to unknown node: {to_node}")

            # Add edge (LangGraph handles parallel execution automatically)
            graph.add_edge(from_node, to_node)

        # Handle conditional edges (requires special routing functions)
        if conditional_edges:
            # Group conditional edges by source node
            conditional_by_source = {}
            for conn in conditional_edges:
                source = conn["from"]
                if source not in conditional_by_source:
                    conditional_by_source[source] = []
                conditional_by_source[source].append(conn)

            # Add conditional edges
            for source, conns in conditional_by_source.items():
                # Check if condition is a function name (legacy) or YAML definition (new)
                first_conn = conns[0]
                condition_def = first_conn.get("condition")

                if isinstance(condition_def, str):
                    # Legacy: Function name (e.g., "should_continue_steps")
                    condition_map = {
                        "should_continue_steps": should_continue_steps,
                        "should_retry_route": should_retry_route,
                        "repair_route": repair_route,
                        "should_debate": should_debate,
                        "test_passed": test_passed,
                        "test_failed": test_failed,
                        "should_replan": should_replan,
                    }

                    if condition_def not in condition_map:
                        raise ValueError(f"Unknown condition function: {condition_def}")

                    routing_func = condition_map[condition_def]
                elif isinstance(condition_def, dict):
                    # New: YAML-defined condition
                    routing_func = create_condition_function(condition_def)
                else:
                    raise ValueError(f"Invalid condition definition: {condition_def}")

                # Build routing map from connections
                routing_map = {}
                for conn in conns:
                    target = conn["to"]
                    if target == "END":
                        target = END

                    # Get route key from connection (if specified) or infer from target
                    route_key = conn.get("route", None)

                    if route_key:
                        # Route key explicitly specified in YAML
                        routing_map[route_key] = target
                    elif isinstance(condition_def, dict):
                        # Dynamic condition - route key comes from condition definition
                        routes = condition_def.get("routes", {})
                        # Find which route this target belongs to
                        for key, route_target in routes.items():
                            if route_target == target or (target == END and route_target == "END"):
                                routing_map[key] = target
                                break
                    else:
                        # Legacy: Infer route key from target node name
                        # For should_continue_steps: "continue" -> execute, "done" -> verify
                        if condition_def == "should_continue_steps":
                            if target == "execute":
                                routing_map["continue"] = target
                            elif target == "verify":
                                routing_map["done"] = target
                        # For should_retry_route: "repair" -> repair, "gate" -> gate
                        elif condition_def == "should_retry_route":
                            if "repair" in str(target):
                                routing_map["repair"] = target
                            elif "gate" in str(target):
                                routing_map["gate"] = target
                        # For repair_route: "spec" -> spec, "plan" -> plan, "execute" -> execute
                        elif condition_def == "repair_route":
                            if "spec" in str(target):
                                routing_map["spec"] = target
                            elif "plan" in str(target):
                                routing_map["plan"] = target
                            elif "execute" in str(target):
                                routing_map["execute"] = target
                        # For should_debate: "debate" -> debate, "end" -> END
                        elif condition_def == "should_debate":
                            if "debate" in str(target):
                                routing_map["debate"] = target
                            elif target == END:
                                routing_map["end"] = END
                        # For test_passed: "integrate" -> integrate, "repair" -> repair
                        elif condition_def == "test_passed":
                            if "integrate" in str(target):
                                routing_map["integrate"] = target
                            elif "repair" in str(target):
                                routing_map["repair"] = target
                        # For test_failed: "repair" -> repair, "integrate" -> integrate
                        elif condition_def == "test_failed":
                            if "repair" in str(target):
                                routing_map["repair"] = target
                            elif "integrate" in str(target):
                                routing_map["integrate"] = target

                # Add conditional edge
                if source == "START":
                    source = START
                elif source not in [n["id"] for n in self.spec.nodes]:
                    raise ValueError(f"Conditional edge from unknown node: {source}")

                graph.add_conditional_edges(source, routing_func, routing_map)

        # Validate: Gate node must exist (gate or self_gate)
        gate_nodes = [n for n in self.spec.nodes if n["type"] in ("gate", "self_gate")]
        if not gate_nodes:
            raise ValueError("Workflow must include at least one 'gate' or 'self_gate' node")

        compiled_graph = graph.compile()

        # Journal: Workflow execute
        if self.run_path:
            append_event(
                self.run_path,
                "WORKFLOW_EXECUTE",
                {
                    "workflow_name": self.spec.name if hasattr(self.spec, "name") else "unknown",
                    "nodes_count": len(self.spec.nodes),
                },
                trace_id=self.trace_id,
            )

        return compiled_graph

    def validate_workflow(self) -> tuple[bool, list[str]]:
        """
        Validate workflow spec.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if self.spec is None:
            return False, ["Workflow spec not loaded"]

        # Check all nodes are registered
        for node_def in self.spec.nodes:
            node_type = node_def["type"]
            if not self.node_registry.is_registered(node_type):
                errors.append(f"Node type '{node_type}' (node '{node_def['id']}') not registered")

        # Check all connections reference valid nodes
        node_ids = {n["id"] for n in self.spec.nodes}
        for conn in self.spec.connections:
            from_node = conn["from"]
            to_node = conn["to"]

            if from_node != "START" and from_node not in node_ids:
                errors.append(f"Connection from unknown node: {from_node}")
            if to_node != "END" and to_node not in node_ids:
                errors.append(f"Connection to unknown node: {to_node}")

        # Check gate node exists (gate or self_gate)
        gate_nodes = [n for n in self.spec.nodes if n["type"] in ("gate", "self_gate")]
        if not gate_nodes:
            errors.append("Workflow must include at least one 'gate' or 'self_gate' node")

        return len(errors) == 0, errors
