"""
Workflow Bootstrap - Register all node types with NodeRegistry.

This module registers all existing workflow nodes so they can be resolved
by type when building workflows from YAML specs.
"""

import logging
from pathlib import Path

from ..orchestrator.nodes import (
    agent_runtime_node,
    council_reviewer_node,
    debate_node,
    execute_node,
    gate_node,
    plan_node,
    repair_node,
    self_analyze_node,
    self_gate_node,
    self_integrate_node,
    self_propose_node,
    self_reflect_node,
    spec_node,
    validate_impl_node,
    validate_plan_node,
    validate_spec_node,
    verify_node,
    workflow_evolver_node,
)

logger = logging.getLogger(__name__)

# Legacy adapter-based node (deprecated) - now in self_improve.py
from ..orchestrator.self_improve import self_improve_reflect_node
from ..orchestrator.self_improve import (
    self_improve_implement_node as native_implement_node,
)
from ..orchestrator.self_improve import (
    self_improve_integrate_node as native_integrate_node,
)
from ..orchestrator.self_improve import (
    self_improve_plan_node as native_plan_node,
)
from ..orchestrator.self_improve import (
    self_improve_reflect_node as native_reflect_node,
)
from ..orchestrator.self_improve import (
    self_improve_repair_node as native_repair_node,
)
from ..orchestrator.self_improve import (
    self_improve_test_node as native_test_node,
)
from ..syscalls.journal import append_event
from .node_registry import NodeRegistry


def bootstrap_nodes(run_path: Path | None = None, trace_id: str | None = None) -> None:
    """
    Register all workflow nodes with NodeRegistry.

    This function should be called during system initialization to ensure
    all node types are available for workflow execution.

    Args:
        run_path: Optional run path for journal logging
        trace_id: Optional trace ID for journal logging
    """
    # Journal: Bootstrap start
    if run_path:
        append_event(
            run_path,
            "BOOTSTRAP_START",
            {},
            trace_id=trace_id,
        )

    node_count = 0
    # Register all node types
    # Journal: Bootstrap step
    if run_path:
        append_event(
            run_path,
            "BOOTSTRAP_STEP",
            {
                "step": "registering_nodes",
            },
            trace_id=trace_id,
        )

    NodeRegistry.register(
        "spec_generator",
        spec_node,
        description="Generates SPEC.md from task objective using Chief Architect persona",
        required_modules=["spec_validator"],
    )

    NodeRegistry.register(
        "spec_validator",
        validate_spec_node,
        description="Validates spec structure and completeness",
    )

    NodeRegistry.register(
        "planner",
        plan_node,
        description="Generates plan.json from spec using LLM planner",
        required_modules=["spec_validator"],
    )

    NodeRegistry.register(
        "plan_validator",
        validate_plan_node,
        description="Validates plan against spec requirements",
    )

    NodeRegistry.register(
        "executor",
        execute_node,
        description="Executes plan using registered executor (Aider or LocalCoder)",
    )

    NodeRegistry.register(
        "impl_validator",
        validate_impl_node,
        description="Validates implementation against spec",
    )

    NodeRegistry.register(
        "verifier",
        verify_node,
        description="Runs verifier (lint + tests) and generates verifier_report.json",
    )

    NodeRegistry.register(
        "repair",
        repair_node,
        description="Attempts to fix errors detected by verifier",
    )

    NodeRegistry.register(
        "gate",
        gate_node,
        description="Checks gates (verification + risk) and generates gate_report.json",
    )

    NodeRegistry.register(
        "debate",
        debate_node,
        description="Conducts council debate when task is blocked",
    )

    # Vendor adapter nodes (ADAPTER_INTEGRATION_PLAN.md - Phase 2)
    NodeRegistry.register(
        "workflow_evolver",
        workflow_evolver_node,
        description="Evolves workflow using EvoAgentX adapter",
        required_modules=["evoagentx"],
    )

    NodeRegistry.register(
        "agent_runtime",
        agent_runtime_node,
        description="Executes agent using reactive-agents adapter",
        required_modules=["reactive_agents"],
    )

    NodeRegistry.register(
        "council_reviewer",
        council_reviewer_node,
        description="Reviews execution using llm-council adapter",
        required_modules=["llm_council"],
    )

    # YBIS-native self-improve nodes (preferred - no external dependencies)
    NodeRegistry.register(
        "self_improve_reflect",
        native_reflect_node,
        description="Reflects on system state and identifies improvements (YBIS-native)",
        required_modules=[],
    )

    NodeRegistry.register(
        "self_improve_plan",
        native_plan_node,
        description="Plans improvements based on reflection (YBIS-native)",
        required_modules=["planner"],
    )

    NodeRegistry.register(
        "self_improve_implement",
        native_implement_node,
        description="Implements improvement plan (YBIS-native)",
        required_modules=["executor"],
    )

    NodeRegistry.register(
        "self_improve_test",
        native_test_node,
        description="Tests implementation (YBIS-native)",
        required_modules=["verifier"],
    )

    NodeRegistry.register(
        "self_improve_integrate",
        native_integrate_node,
        description="Integrates tested implementation (YBIS-native)",
        required_modules=[],
    )

    NodeRegistry.register(
        "self_improve_repair",
        native_repair_node,
        description="Repairs lint/test failures automatically (YBIS-native)",
        required_modules=["planner", "executor"],
    )

    # Legacy adapter-based nodes (fallback)
    NodeRegistry.register(
        "self_improve_reflect_adapter",
        self_improve_reflect_node,
        description="Reflects on current state using Self-Improve-Swarms adapter (legacy)",
        required_modules=["self_improve_swarms"],
    )

    # YBIS-native self-development nodes
    NodeRegistry.register(
        "self_reflect",
        self_reflect_node,
        description="Reflects on system state and identifies improvements (YBIS-native)",
    )

    NodeRegistry.register(
        "self_analyze",
        self_analyze_node,
        description="Analyzes reflection and prioritizes improvements (YBIS-native)",
    )

    NodeRegistry.register(
        "self_propose",
        self_propose_node,
        description="Proposes specific improvements as actionable tasks (YBIS-native)",
    )

    NodeRegistry.register(
        "self_gate",
        self_gate_node,
        description="Stricter gate for self-changes with additional checks (YBIS-native)",
    )

    NodeRegistry.register(
        "self_integrate",
        self_integrate_node,
        description="Integrates self-change with rollback capability (YBIS-native)",
    )

    # Count all registrations
    import re
    from pathlib import Path
    bootstrap_file = Path(__file__)
    bootstrap_content = bootstrap_file.read_text()
    node_count = len(re.findall(r'NodeRegistry\.register\(', bootstrap_content))

    # Journal: Bootstrap complete
    if run_path:
        append_event(
            run_path,
            "BOOTSTRAP_COMPLETE",
            {
                "nodes_registered": node_count,
            },
            trace_id=trace_id,
        )
