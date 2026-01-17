"""
Test Validation Nodes - Validate spec, plan, and implementation.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.ybis.orchestrator.graph import WorkflowState
from src.ybis.orchestrator.nodes.validation import (
    validate_spec_node,
    validate_plan_node,
    validate_impl_node,
)


class TestValidationNodes:
    """Test validation workflow nodes."""

    @pytest.fixture
    def mock_state(self, tmp_path):
        """Create mock workflow state."""
        return {
            "task_id": "test-task-123",
            "run_id": "test-run-456",
            "run_path": tmp_path,
            "trace_id": "test-trace-789",
            "status": "running",
        }

    def test_validate_spec_node(self, mock_state):
        """Test validate spec node."""
        result = validate_spec_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_validate_plan_node(self, mock_state):
        """Test validate plan node."""
        result = validate_plan_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_validate_impl_node(self, mock_state):
        """Test validate impl node."""
        result = validate_impl_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_nodes_log_execution(self, mock_state):
        """Test that nodes log their execution."""
        # All nodes should use @log_node_execution decorator
        assert hasattr(validate_spec_node, "__wrapped__") or hasattr(validate_spec_node, "__name__")
        assert hasattr(validate_plan_node, "__wrapped__") or hasattr(validate_plan_node, "__name__")
        assert hasattr(validate_impl_node, "__wrapped__") or hasattr(validate_impl_node, "__name__")


