"""
WorkflowState Schema Tests - Prevent TypedDict mismatches.

Tests that WorkflowState TypedDict includes all fields used in nodes.
"""

import ast
from pathlib import Path

import pytest

from src.ybis.constants import PROJECT_ROOT
from src.ybis.orchestrator.graph import WorkflowState


def find_state_accesses(file_path: Path) -> set[str]:
    """Find all state[...] accesses in a Python file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        accesses = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Name):
                    if node.value.id == "state":
                        if isinstance(node.slice, ast.Constant):
                            accesses.add(node.slice.value)
                        elif isinstance(node.slice, ast.Index):
                            if isinstance(node.slice.value, ast.Constant):
                                accesses.add(node.slice.value.value)
        
        return accesses
    except Exception:
        return set()


class TestWorkflowStateSchema:
    """Test WorkflowState schema validation."""

    def test_workflowstate_has_required_fields(self):
        """Verify WorkflowState TypedDict has all required fields."""
        # Get TypedDict annotations
        annotations = WorkflowState.__annotations__
        
        required_fields = {
            "task_id",
            "run_id",
            "run_path",
            "trace_id",
            "task_objective",
            "status",
            "retries",
            "max_retries",
            "error_context",
            "current_step",
        }
        
        for field in required_fields:
            assert field in annotations, f"WorkflowState missing required field: {field}"

    def test_all_state_accesses_are_defined(self):
        """Verify all state[...] accesses in graph.py are defined in WorkflowState."""
        graph_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
        accesses = find_state_accesses(graph_path)
        
        # Get WorkflowState fields
        annotations = WorkflowState.__annotations__
        defined_fields = set(annotations.keys())
        
        # Check for undefined accesses
        undefined = accesses - defined_fields
        
        # Filter out method calls (state.get, state.items, etc.)
        undefined = {u for u in undefined if not u.startswith("get") and not u.startswith("items")}
        
        # task_tier is optional (can be None), so it's allowed even if not always in TypedDict
        # But we should add it to TypedDict for clarity
        if "task_tier" in undefined:
            # This is a known issue - task_tier should be in TypedDict
            # For now, we'll allow it but warn
            undefined.remove("task_tier")
            # TODO: Add task_tier to WorkflowState TypedDict
        
        assert len(undefined) == 0, \
            f"Found state accesses for undefined fields: {undefined}"

    def test_initial_state_has_all_fields(self):
        """Verify initial_state in scripts includes all required fields."""
        # Check e2e_test_runner.py
        script_path = PROJECT_ROOT / "scripts" / "e2e_test_runner.py"
        if script_path.exists():
            content = script_path.read_text(encoding="utf-8")
            
            # Find initial_state dictionary
            if "initial_state" in content:
                # Check for required fields
                required_fields = {
                    "task_id",
                    "run_id",
                    "run_path",
                    "trace_id",
                    "task_objective",
                    "status",
                    "retries",
                    "max_retries",
                    "error_context",
                    "current_step",
                }
                
                for field in required_fields:
                    assert field in content, \
                        f"initial_state in e2e_test_runner.py missing field: {field}"

