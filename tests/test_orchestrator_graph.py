"""
Tests for LangGraph Skeleton.

DoD:
- The graph compiles and runs end-to-end
- All artifacts (plan.json, executor_report.json, verifier_report.json, gate_report.json) are found in the run folder after execution
"""

import json
import tempfile
import warnings
from pathlib import Path

import pytest

# Suppress third-party library warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="httpx")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")

from src.ybis.contracts import RunContext
from src.ybis.data_plane import init_run_structure
from src.ybis.orchestrator import build_workflow_graph


def test_graph_execution():
    """Test that graph compiles and runs end-to-end."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock PROJECT_ROOT
        import src.ybis.data_plane.workspace as ws_module

        original_root = ws_module.PROJECT_ROOT
        ws_module.PROJECT_ROOT = Path(tmpdir)

        try:
            task_id = "T-001"
            run_id = "R-001"

            # Initialize run structure
            run_path = init_run_structure(task_id, run_id)

            # Build graph
            graph = build_workflow_graph()

            # Create initial state (with all required fields)
            initial_state: dict = {
                "task_id": task_id,
                "run_id": run_id,
                "run_path": run_path,
                "trace_id": f"trace-{task_id}-{run_id}",
                "task_objective": "Test objective",
                "status": "pending",
                "retries": 0,
                "max_retries": 2,
                "error_context": None,
                "current_step": 0,
            }

            # Run graph
            final_state = graph.invoke(initial_state)

            # Verify final state
            assert final_state["status"] in ["completed", "failed"]
            assert final_state["task_id"] == task_id
            assert final_state["run_id"] == run_id

            # Verify all artifacts exist
            ctx = RunContext(
                task_id=task_id,
                run_id=run_id,
                run_path=run_path,
                trace_id=f"trace-{task_id}-{run_id}",
            )

            assert ctx.plan_path.exists(), "plan.json should exist"
            assert ctx.executor_report_path.exists(), "executor_report.json should exist"
            assert ctx.verifier_report_path.exists(), "verifier_report.json should exist"
            assert ctx.gate_report_path.exists(), "gate_report.json should exist"

            # Verify artifacts are valid JSON
            plan_data = json.loads(ctx.plan_path.read_text())
            assert plan_data["task_id"] == task_id

            executor_data = json.loads(ctx.executor_report_path.read_text())
            assert "success" in executor_data

            verifier_data = json.loads(ctx.verifier_report_path.read_text())
            assert "lint_passed" in verifier_data

            gate_data = json.loads(ctx.gate_report_path.read_text())
            assert "decision" in gate_data

        finally:
            ws_module.PROJECT_ROOT = original_root
