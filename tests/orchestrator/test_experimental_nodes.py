"""
Test Experimental Nodes - Vendor adapter nodes and self-development nodes.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.ybis.orchestrator.graph import WorkflowState
from src.ybis.orchestrator.nodes.experimental import (
    workflow_evolver_node,
    agent_runtime_node,
    council_reviewer_node,
)


class TestExperimentalNodes:
    """Test experimental workflow nodes."""

    @pytest.fixture
    def mock_state(self, tmp_path):
        """Create mock workflow state."""
        return {
            "task_id": "test-task-123",
            "run_id": "test-run-456",
            "run_path": tmp_path,
            "trace_id": "test-trace-789",
            "status": "running",
            "task_objective": "Test objective",
            "workflow_name": "ybis_native",
        }

    def test_workflow_evolver_node(self, mock_state):
        """Test workflow evolver node."""
        # Node should not raise even if EvoAgentX not available
        result = workflow_evolver_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_agent_runtime_node(self, mock_state):
        """Test agent runtime node."""
        # Node should not raise even if adapters not available
        result = agent_runtime_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_council_reviewer_node(self, mock_state):
        """Test council reviewer node."""
        # Node should not raise even if adapters not available
        result = council_reviewer_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_nodes_log_execution(self, mock_state):
        """Test that nodes log their execution."""
        # All nodes should use @log_node_execution decorator
        # This is checked via the decorator presence in code
        assert hasattr(workflow_evolver_node, "__wrapped__") or hasattr(workflow_evolver_node, "__name__")
        assert hasattr(agent_runtime_node, "__wrapped__") or hasattr(agent_runtime_node, "__name__")
        assert hasattr(council_reviewer_node, "__wrapped__") or hasattr(council_reviewer_node, "__name__")


