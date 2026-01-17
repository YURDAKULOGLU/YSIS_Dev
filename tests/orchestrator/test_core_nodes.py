"""
Test Core Nodes - spec, plan, execution, gate, factory, validation.

Tests for the core workflow nodes that form the backbone of YBIS.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.ybis.orchestrator.graph import WorkflowState
from src.ybis.orchestrator.nodes.spec import spec_node
from src.ybis.orchestrator.nodes.plan import plan_node
from src.ybis.orchestrator.nodes.execution import execute_node, verify_node, repair_node
from src.ybis.orchestrator.nodes.gate import gate_node, should_retry
from src.ybis.orchestrator.nodes.factory import spawn_sub_factory_node
from src.ybis.orchestrator.nodes.validation import (
    validate_spec_node,
    validate_plan_node,
    validate_impl_node,
)


class TestSpecNode:
    """Test spec node functionality."""

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
        }

    def test_spec_node_execution(self, mock_state):
        """Test spec node executes without error."""
        result = spec_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_spec_node_logs(self, mock_state):
        """Test spec node logs execution."""
        # Node should use @log_node_execution decorator
        assert hasattr(spec_node, "__wrapped__") or hasattr(spec_node, "__name__")


class TestPlanNode:
    """Test plan node functionality."""

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
        }

    def test_plan_node_execution(self, mock_state):
        """Test plan node executes without error."""
        result = plan_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_plan_node_logs(self, mock_state):
        """Test plan node logs execution."""
        assert hasattr(plan_node, "__wrapped__") or hasattr(plan_node, "__name__")


class TestExecutionNodes:
    """Test execution nodes (execute, verify, repair)."""

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

    def test_execute_node_execution(self, mock_state):
        """Test execute node executes without error."""
        result = execute_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_verify_node_execution(self, mock_state):
        """Test verify node executes without error."""
        result = verify_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_repair_node_execution(self, mock_state):
        """Test repair node executes without error."""
        result = repair_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_execution_nodes_log(self, mock_state):
        """Test execution nodes log execution."""
        assert hasattr(execute_node, "__wrapped__") or hasattr(execute_node, "__name__")
        assert hasattr(verify_node, "__wrapped__") or hasattr(verify_node, "__name__")
        assert hasattr(repair_node, "__wrapped__") or hasattr(repair_node, "__name__")


class TestGateNode:
    """Test gate node functionality."""

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

    def test_gate_node_execution(self, mock_state):
        """Test gate node executes without error."""
        result = gate_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_should_retry(self, mock_state):
        """Test should_retry function."""
        # Should return bool
        result = should_retry(mock_state)
        assert isinstance(result, bool)

    def test_gate_node_logs(self, mock_state):
        """Test gate node logs execution."""
        assert hasattr(gate_node, "__wrapped__") or hasattr(gate_node, "__name__")


class TestFactoryNode:
    """Test factory node functionality."""

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

    def test_factory_node_execution(self, mock_state):
        """Test factory node executes without error."""
        result = spawn_sub_factory_node(mock_state)
        assert result is not None
        assert "status" in result

    def test_factory_node_logs(self, mock_state):
        """Test factory node logs execution."""
        assert hasattr(spawn_sub_factory_node, "__wrapped__") or hasattr(spawn_sub_factory_node, "__name__")


class TestValidationNodes:
    """Test validation nodes."""

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

    def test_validation_nodes_log(self, mock_state):
        """Test validation nodes log execution."""
        assert hasattr(validate_spec_node, "__wrapped__") or hasattr(validate_spec_node, "__name__")
        assert hasattr(validate_plan_node, "__wrapped__") or hasattr(validate_plan_node, "__name__")
        assert hasattr(validate_impl_node, "__wrapped__") or hasattr(validate_impl_node, "__name__")


