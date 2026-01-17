"""
Conditional Routing Functions for Workflows

These functions handle conditional routing in workflows (e.g., retry loops,
debate triggers). They are referenced by name in workflow YAML specs.
"""

import logging

from ..orchestrator.graph import RunContext, WorkflowState
from ..orchestrator.nodes import should_retry
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)


def should_continue_steps(state: WorkflowState) -> str:
    """
    Check if more steps remain in plan.

    Used in conditional routing: validate_impl -> execute (continue) or verify (done)
    """
    import json

    plan_path = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    ).plan_path

    if plan_path.exists():
        plan_data = json.loads(plan_path.read_text())
        steps = plan_data.get("steps", [])
        current_step = state.get("current_step", 0)
        if steps and current_step < len(steps):
            return "continue"  # More steps - loop back to execute
    return "done"  # No more steps - proceed to verify (not gate, verify comes before gate)


def should_retry_route(state: WorkflowState) -> str:
    """
    Route to repair if retry needed, otherwise to gate.

    Used in conditional routing: verify -> repair (retry) or gate (done)
    """
    if should_retry(state):
        return "repair"
    return "gate"


def repair_route(state: WorkflowState) -> str:
    """
    Route after repair: go back to spec/plan if needed, otherwise re-execute.

    Used in conditional routing: repair -> spec (spec repair) or plan (plan repair) or execute (re-execute)
    """
    if state.get("needs_spec_repair"):
        return "spec"  # Go back to spec generation with feedback
    if state.get("needs_plan_repair"):
        return "plan"  # Go back to plan generation with feedback
    return "execute"  # Re-execute with error context


def should_replan(state: WorkflowState) -> str:
    """
    Determine next node after repair analysis.

    Used in conditional routing: repair -> plan (replan) or execute (re-execute) or gate (no issues)

    Args:
        state: Workflow state

    Returns:
        Next node name: "plan", "execute", or "gate"
    """
    if state.get("repair_failed"):
        return "gate"  # Go to gate with failure

    if state.get("needs_replan"):
        return "plan"  # Go back to planning with feedback

    if state.get("repair_strategy") == "lint_only":
        return "execute"  # Re-execute with lint fix

    return "gate"  # No issues, go to gate


def should_debate(state: WorkflowState) -> str:
    """
    Check if debate should be triggered.

    Used in conditional routing: gate -> debate (blocked) or END (pass)
    """
    import json

    gate_path = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    ).gate_report_path

    if gate_path.exists():
        gate_data = json.loads(gate_path.read_text())
        # Decision can be a string (enum value) or nested dict
        decision = gate_data.get("decision", "")
        if isinstance(decision, dict):
            decision = decision.get("value", "")
        if decision in ["REQUIRE_APPROVAL", "BLOCK"]:
            return "debate"
    return "end"


def test_passed(state: WorkflowState) -> str:
    """
    Check if tests and linting passed.

    Used in conditional routing: test -> integrate (passed)
    NOTE: This function should ONLY return "integrate" when tests pass.
    For failures, use test_failed() function instead.
    """
    test_passed_flag = state.get("test_passed", False)
    lint_passed_flag = state.get("lint_passed", True)  # Default True if not set
    tests_passed_flag = state.get("tests_passed", True)  # Default True if not set

    if test_passed_flag and lint_passed_flag and tests_passed_flag:
        return "integrate"  # All passed - proceed to integrate

    # If tests failed, this function should not be called (test_failed handles it)
    # But if it is called, return a default that won't match any route
    # This should not happen in practice, but provides safety
    logger.warning("test_passed() called but tests failed - this should not happen")
    return "repair"  # Fallback (should not be reached if routing is correct)


def test_failed(state: WorkflowState) -> str:
    """
    Check if tests or linting failed.

    Used in conditional routing: test -> repair (failed) or integrate (passed)
    """
    run_path = state.get("run_path")
    trace_id = state.get("trace_id", f"{state.get('task_id')}-{state.get('run_id')}")

    # If max retries already reached in repair node, go to integrate
    if state.get("repair_max_retries_reached", False):
        if run_path:
            append_event(
                run_path,
                "ROUTING_DECISION",
                {
                    "from_node": "test",
                    "to_node": "integrate",
                    "condition": "repair_max_retries_reached",
                },
                trace_id=trace_id,
            )
        return "integrate"

    test_passed_flag = state.get("test_passed", False)
    lint_passed_flag = state.get("lint_passed", True)  # Default True if not set
    tests_passed_flag = state.get("tests_passed", True)  # Default True if not set

    if not test_passed_flag or not lint_passed_flag or not tests_passed_flag:
        # Check retry limits
        repair_retries = state.get("repair_retries", 0)
        max_repair_retries = state.get("max_repair_retries", 3)
        repair_max_retries_reached = state.get("repair_max_retries_reached", False)

        # If repair node already set the flag, respect it
        if repair_max_retries_reached:
            logger.info("Repair max retries flag set, proceeding to integrate")
            if run_path:
                append_event(
                    run_path,
                    "ROUTING_DECISION",
                    {
                        "from_node": "test",
                        "to_node": "integrate",
                        "condition": "repair_max_retries_reached",
                    },
                    trace_id=trace_id,
                )
            return "integrate"

        # Check if we've exceeded max retries
        if repair_retries >= max_repair_retries:
            logger.warning(f"Max repair retries ({max_repair_retries}) reached (retries={repair_retries}), proceeding to integrate")
            if run_path:
                append_event(
                    run_path,
                    "ROUTING_DECISION",
                    {
                        "from_node": "test",
                        "to_node": "integrate",
                        "condition": "max_repair_retries_reached",
                    },
                    trace_id=trace_id,
                )
            return "integrate"  # Max retries reached - proceed anyway

        # Still have retries left
        logger.info(f"Tests failed, routing to repair (attempt {repair_retries + 1}/{max_repair_retries})")
        logger.debug(f"Conditional routing state: repair_retries={repair_retries}, max={max_repair_retries}, test_passed={test_passed_flag}, lint_passed={lint_passed_flag}, tests_passed={tests_passed_flag}")
        if run_path:
            append_event(
                run_path,
                "ROUTING_DECISION",
                {
                    "from_node": "test",
                    "to_node": "repair",
                    "condition": "test_failed",
                },
                trace_id=trace_id,
            )
        return "repair"  # Tests/lint failed - go to repair

    # All passed - proceed to integrate
    if run_path:
        append_event(
            run_path,
            "ROUTING_DECISION",
            {
                "from_node": "test",
                "to_node": "integrate",
                "condition": "test_passed",
            },
            trace_id=trace_id,
        )
    return "integrate"  # All passed - proceed to integrate

