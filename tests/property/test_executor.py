"""
Property-based tests for Executor.

Tests that executor handles errors gracefully.
"""

from hypothesis import given, strategies as st

from src.ybis.contracts import Plan, RunContext
from pathlib import Path


@given(st.lists(st.text(min_size=1, max_size=100), min_size=0, max_size=10))
def test_executor_handles_any_file_list(files: list[str]) -> None:
    """
    Property: Executor should handle any file list without crashing.

    Even if files don't exist or are invalid, executor should handle gracefully.
    """
    from src.ybis.executors.registry import get_executor_registry

    # Create a plan with generated file list
    plan = Plan(
        objective="Test objective",
        files=files,
        instructions="Test instructions",
        steps=[],
    )

    # Create a minimal run context
    ctx = RunContext(
        task_id="TEST-001",
        run_id="run-001",
        run_path=Path("workspaces/TEST-001/runs/run-001"),
        trace_id="trace-001",
    )

    # Executor should not crash (may skip invalid files, but shouldn't error)
    executor_registry = get_executor_registry()
    executor = executor_registry.get_executor()

    try:
        # Executor should handle any file list gracefully
        # It may skip invalid files, but shouldn't crash
        report = executor.execute(ctx, plan)
        # Report should be valid (even if no files changed)
        assert report is not None
        assert hasattr(report, "success")
        assert hasattr(report, "files_changed")
    except Exception as e:
        # Executor should handle any input gracefully
        assert False, f"Executor crashed on file list {files[:3]}: {e}"


