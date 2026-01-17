"""
Property-based tests for Planner.

Tests that planner handles any valid input without crashing.
"""

from hypothesis import given, strategies as st

from src.ybis.contracts import Plan, Task
from src.ybis.orchestrator.planner import LLMPlanner


@given(st.text(min_size=1, max_size=500))
def test_planner_handles_any_input(text: str) -> None:
    """
    Property: Planner should never crash on valid text input.

    This property-based test generates random text inputs and ensures
    the planner can handle them without raising exceptions.
    """
    # Create a task with the generated text
    task = Task(
        task_id="TEST-001",
        objective=text,
        status="pending",
    )

    # Planner should not crash (may return empty plan, but shouldn't error)
    planner = LLMPlanner()
    try:
        plan = planner.plan_task(task)
        # Plan should be valid Plan object (even if empty)
        assert isinstance(plan, Plan)
        assert isinstance(plan.files, list)
        assert isinstance(plan.instructions, str)
    except Exception as e:
        # Planner should handle any input gracefully
        # If it fails, it should be a controlled failure, not a crash
        assert False, f"Planner crashed on input '{text[:50]}...': {e}"


@given(st.text(min_size=1, max_size=100))
def test_plan_validation_handles_any_text(text: str) -> None:
    """
    Property: Plan validation should handle any text input.

    Even if plan content is malformed, validation should not crash.
    """
    from src.ybis.orchestrator.plan_validator import validate_plan

    # Create a minimal plan with generated text
    plan = Plan(
        objective=text,
        files=[],
        instructions=text,
        steps=[],
    )

    # Validation should not crash (may return errors, but shouldn't raise)
    try:
        result = validate_plan(plan)
        # Result should be a dict with validation info
        assert isinstance(result, dict)
    except Exception as e:
        assert False, f"Plan validation crashed on text '{text[:50]}...': {e}"


