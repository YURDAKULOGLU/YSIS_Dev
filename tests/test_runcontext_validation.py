"""
RunContext Validation Tests - Prevent missing required fields.

Tests that all RunContext creations include required fields (especially trace_id).
"""

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.ybis.constants import PROJECT_ROOT
from src.ybis.contracts.context import RunContext


def find_runcontext_creations(file_path: Path) -> list[dict]:
    """Find all RunContext(...) calls in a Python file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        creations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == "RunContext":
                        # Get line number and check arguments
                        args = []
                        for arg in node.args:
                            if isinstance(arg, ast.keyword):
                                args.append(arg.arg)
                            elif isinstance(arg, ast.Constant):
                                args.append("positional")
                        
                        creations.append({
                            "line": node.lineno,
                            "args": args,
                        })
        
        return creations
    except Exception:
        return []


class TestRunContextValidation:
    """Test RunContext creation validation."""

    def test_runcontext_requires_trace_id(self):
        """Verify RunContext requires trace_id field."""
        # This should fail without trace_id
        with pytest.raises(ValidationError):
            RunContext(
                task_id="T-123",
                run_id="R-456",
                run_path=Path("/tmp/test"),
                # trace_id missing - should fail
            )
        
        # This should succeed with trace_id
        ctx = RunContext(
            task_id="T-123",
            run_id="R-456",
            run_path=Path("/tmp/test"),
            trace_id="trace-789",
        )
        assert ctx.trace_id == "trace-789"

    def test_all_runcontext_creations_include_trace_id(self):
        """Verify all RunContext creations in graph.py include trace_id."""
        graph_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
        assert graph_path.exists(), "graph.py not found"
        
        content = graph_path.read_text(encoding="utf-8")
        creations = find_runcontext_creations(graph_path)
        
        # Check each creation - look at multi-line context
        violations = []
        lines = content.split("\n")
        for creation in creations:
            line_num = creation["line"]
            # Check current line and next 5 lines for trace_id
            context_lines = lines[max(0, line_num - 1):min(len(lines), line_num + 5)]
            context = "\n".join(context_lines)
            
            # Check if trace_id is in the context
            if "trace_id" not in context:
                violations.append({
                    "line": line_num,
                    "content": lines[line_num - 1].strip()[:80],
                })
        
        assert len(violations) == 0, \
            f"Found {len(violations)} RunContext creations without trace_id: {violations}"

    def test_runcontext_creations_use_state_trace_id(self):
        """Verify RunContext creations use state.get('trace_id', ...) pattern."""
        graph_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
        content = graph_path.read_text(encoding="utf-8")
        
        # Find RunContext creations
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "RunContext(" in line:
                # Check if trace_id uses state.get pattern
                # Look ahead a few lines for trace_id
                context = "\n".join(lines[max(0, i-2):min(len(lines), i+5)])
                if "trace_id" in context:
                    # Should use state.get("trace_id", ...) pattern
                    assert "state.get" in context or "state[\"trace_id\"]" in context or f"{state['task_id']}-{state['run_id']}" in context, \
                        f"RunContext at line {i+1} should use state.get('trace_id', ...) pattern"

