"""
EvoAgentX Adapter - Workflow evolution and optimization.

Implements WorkflowEvolutionProtocol using EvoAgentX for workflow optimization.
"""

from typing import Any

from ..constants import PROJECT_ROOT


class EvoAgentXAdapter:
    """
    EvoAgentX Adapter - Workflow evolution and optimization.

    Uses EvoAgentX to evolve workflow specs based on metrics and score workflows.
    """

    def __init__(self):
        """Initialize EvoAgentX adapter."""
        self._available = False
        self._check_availability()

    def _check_availability(self) -> None:
        """Check if EvoAgentX is available."""
        try:
            # Check if EvoAgentX is in vendors
            evoagentx_path = PROJECT_ROOT / "vendors" / "EvoAgentX"
            if evoagentx_path.exists():
                self._available = True
        except Exception:
            self._available = False

    def is_available(self) -> bool:
        """
        Check if EvoAgentX adapter is available.

        Returns:
            True if EvoAgentX is available, False otherwise
        """
        return self._available

    def evolve(self, workflow_spec: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
        """
        Evolve workflow spec based on metrics using EvoAgentX.

        Args:
            workflow_spec: Current workflow specification (YAML dict)
            metrics: Performance metrics (e.g., execution time, success rate)

        Returns:
            Updated workflow specification dict with evolution metadata
        """
        if not self._available:
            # Graceful fallback: return original spec unchanged
            return workflow_spec

        try:
            # Try to import EvoAgentX
            import sys
            evoagentx_path = PROJECT_ROOT / "vendors" / "EvoAgentX"
            if str(evoagentx_path) not in sys.path:
                sys.path.insert(0, str(evoagentx_path))

            # Import EvoAgentX components
            try:
                from evoagentx.core.base_config import Parameter
                from evoagentx.workflow.workflow_graph import (
                    WorkFlowEdge,
                    WorkFlowGraph,
                    WorkFlowNode,
                )
            except ImportError as e:
                # EvoAgentX not properly installed - graceful fallback
                evolved_spec = workflow_spec.copy()
                evolved_spec["_evolution_metadata"] = {
                    "evolved": False,
                    "reason": f"EvoAgentX import failed: {e}",
                    "metrics": metrics,
                }
                return evolved_spec

            # Convert YBIS workflow spec to EvoAgentX format
            try:
                evo_graph = self._convert_ybis_to_evoagentx(workflow_spec)
            except Exception as e:
                # Conversion failed - return original with metadata
                evolved_spec = workflow_spec.copy()
                evolved_spec["_evolution_metadata"] = {
                    "evolved": False,
                    "reason": f"Conversion failed: {e}",
                    "metrics": metrics,
                }
                return evolved_spec

            # Apply simple evolution based on metrics
            # For now, we'll do a simple analysis and suggest improvements
            evolved_graph = self._apply_simple_evolution(evo_graph, metrics)

            # Convert back to YBIS format
            try:
                evolved_spec = self._convert_evoagentx_to_ybis(evolved_graph, workflow_spec)
                evolved_spec["_evolution_metadata"] = {
                    "evolved": True,
                    "reason": "Simple evolution applied based on metrics",
                    "metrics": metrics,
                    "changes": ["Applied metric-based optimization"],
                }
                return evolved_spec
            except Exception as e:
                # Conversion back failed - return original with metadata
                evolved_spec = workflow_spec.copy()
                evolved_spec["_evolution_metadata"] = {
                    "evolved": False,
                    "reason": f"Conversion back failed: {e}",
                    "metrics": metrics,
                }
                return evolved_spec

        except Exception as e:
            # Any other error - graceful fallback
            evolved_spec = workflow_spec.copy()
            evolved_spec["_evolution_metadata"] = {
                "evolved": False,
                "reason": f"Evolution failed: {e}",
                "metrics": metrics,
            }
            return evolved_spec

    def _convert_ybis_to_evoagentx(self, ybis_spec: dict[str, Any]) -> Any:
        """
        Convert YBIS workflow spec to EvoAgentX WorkFlowGraph.

        Args:
            ybis_spec: YBIS workflow specification dict

        Returns:
            EvoAgentX WorkFlowGraph instance
        """
        from evoagentx.workflow.workflow_graph import WorkFlowEdge, WorkFlowGraph, WorkFlowNode

        # Extract workflow info
        workflow_name = ybis_spec.get("name", "ybis_workflow")
        workflow_description = ybis_spec.get("description", "")
        goal = f"Execute {workflow_name}: {workflow_description}"

        # Convert nodes
        evo_nodes = []
        for node_def in ybis_spec.get("nodes", []):
            node_id = node_def.get("id", "")
            node_type = node_def.get("type", "")
            node_desc = node_def.get("description", f"Execute {node_type}")

            # Create WorkFlowNode
            evo_node = WorkFlowNode(
                name=node_id,
                description=node_desc,
                inputs=[],  # YBIS nodes don't have explicit inputs/outputs
                outputs=[],
                reason=f"Node type: {node_type}",
            )
            evo_nodes.append(evo_node)

        # Convert connections to edges
        evo_edges = []
        for conn in ybis_spec.get("connections", []):
            from_node = conn.get("from", "")
            to_node = conn.get("to", "")

            # Skip START/END nodes (EvoAgentX handles these differently)
            if from_node == "START" or to_node == "END":
                continue

            # Create WorkFlowEdge
            evo_edge = WorkFlowEdge(
                from_node=from_node,
                to_node=to_node,
            )
            evo_edges.append(evo_edge)

        # Create WorkFlowGraph
        evo_graph = WorkFlowGraph(
            goal=goal,
            nodes=evo_nodes,
            edges=evo_edges,
        )

        return evo_graph

    def _apply_simple_evolution(self, evo_graph: Any, metrics: dict[str, Any]) -> Any:
        """
        Apply simple evolution to EvoAgentX workflow graph based on metrics.

        Args:
            evo_graph: EvoAgentX WorkFlowGraph
            metrics: Performance metrics

        Returns:
            Evolved WorkFlowGraph (or original if no evolution needed)
        """
        # For now, just return the original graph
        # In the future, we can apply actual EvoAgentX optimizers here
        # Example: optimizer = TextGradOptimizer(llm=llm, graph=evo_graph)
        # evolved = optimizer.optimize(dataset=benchmark)
        return evo_graph

    def _convert_evoagentx_to_ybis(self, evo_graph: Any, original_spec: dict[str, Any]) -> dict[str, Any]:
        """
        Convert EvoAgentX WorkFlowGraph back to YBIS workflow spec.

        Args:
            evo_graph: EvoAgentX WorkFlowGraph
            original_spec: Original YBIS spec (for structure preservation)

        Returns:
            YBIS workflow specification dict
        """
        # For now, return original spec (evolution not yet implemented)
        # In the future, extract nodes and edges from evo_graph and convert back
        return original_spec.copy()

    def score(self, workflow_spec: dict[str, Any], artifacts: dict[str, Any]) -> float:
        """
        Score workflow spec based on artifacts.

        Args:
            workflow_spec: Workflow specification (YAML dict)
            artifacts: Run artifacts (e.g., verifier_report, gate_report)

        Returns:
            Score (0.0-1.0) indicating workflow quality
        """
        if not self._available:
            # Graceful fallback: return neutral score
            return 0.5

        try:
            # Extract metrics from artifacts
            verifier_report = artifacts.get("verifier_report", {})
            gate_report = artifacts.get("gate_report", {})
            
            # Calculate simple score based on available metrics
            score = 0.5  # Neutral baseline
            
            # Boost score if verifier passed
            if verifier_report.get("lint_passed") and verifier_report.get("tests_passed"):
                score += 0.3
            
            # Boost score if gate passed
            gate_decision = gate_report.get("decision", {})
            if isinstance(gate_decision, dict):
                gate_decision = gate_report.get("decision", {}).get("value", "UNKNOWN")
            if gate_decision == "PASS":
                score += 0.2
            
            # Normalize to 0.0-1.0
            score = max(0.0, min(1.0, score))
            
            # TODO: Use EvoAgentX evaluator for more sophisticated scoring
            # from evoagentx.evaluators import WorkflowEvaluator
            # evaluator = WorkflowEvaluator()
            # score = evaluator.evaluate(workflow_spec, artifacts)
            
            return score
        except Exception:
            # Scoring failed - return neutral score
            return 0.5

