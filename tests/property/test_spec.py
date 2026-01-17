"""
Property-based tests for Spec Generator.

Tests that spec generator handles any valid input without crashing.
"""

from hypothesis import given, strategies as st

from src.ybis.contracts import Task


@given(st.text(min_size=1, max_size=500))
def test_spec_generator_handles_any_input(text: str) -> None:
    """
    Property: Spec generator should never crash on valid text input.

    This property-based test generates random text inputs and ensures
    the spec generator can handle them without raising exceptions.
    """
    from src.ybis.orchestrator.spec_validator import SpecValidator

    # Create a task with the generated text
    task = Task(
        task_id="TEST-001",
        objective=text,
        status="pending",
    )

    # Spec generator should not crash
    validator = SpecValidator()
    try:
        # Spec generation may fail, but shouldn't crash
        # We're testing that it handles any input gracefully
        spec_content = validator.generate_spec(task)
        # If it succeeds, should return a string
        if spec_content:
            assert isinstance(spec_content, str)
    except Exception as e:
        # Spec generator should handle any input gracefully
        # If it fails, it should be a controlled failure, not a crash
        assert False, f"Spec generator crashed on input '{text[:50]}...': {e}"


@given(st.text(min_size=1, max_size=200))
def test_spec_parsing_handles_any_text(text: str) -> None:
    """
    Property: Spec parsing should handle any text input.

    Even if spec content is malformed, parsing should not crash.
    """
    from src.ybis.orchestrator.spec_validator import _is_structured_spec

    # Parsing should not crash (may return False for invalid, but shouldn't raise)
    try:
        result = _is_structured_spec(text)
        # Result should be boolean
        assert isinstance(result, bool)
    except Exception as e:
        assert False, f"Spec parsing crashed on text '{text[:50]}...': {e}"


