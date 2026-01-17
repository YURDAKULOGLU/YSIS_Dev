"""
Unit tests for Conditional Routing Functions.

Tests test_passed and test_failed routing functions.
"""

import pytest
from unittest.mock import Mock
import sys
from pathlib import Path

# Direct import to avoid circular import issues
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

# Import directly from module, not through package __init__
from ybis.workflows.conditional_routing import test_passed as routing_test_passed, test_failed as routing_test_failed
from ybis.orchestrator.graph import WorkflowState


class TestTestPassed:
    """Tests for test_passed routing function."""

    def test_test_passed_all_passed(self):
        """Test routing when all tests pass."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": True,
            "lint_passed": True,
            "tests_passed": True,
        }

        result = routing_test_passed(state)
        assert result == "integrate"

    def test_test_passed_lint_failed(self):
        """Test routing when lint fails."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "lint_passed": False,
            "tests_passed": True,
        }

        result = routing_test_passed(state)
        assert result == "repair"  # Fallback (should not happen in practice)

    def test_test_passed_tests_failed(self):
        """Test routing when tests fail."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "lint_passed": True,
            "tests_passed": False,
        }

        result = routing_test_passed(state)
        assert result == "repair"  # Fallback (should not happen in practice)

    def test_test_passed_defaults(self):
        """Test routing with default values."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
        }

        result = routing_test_passed(state)
        assert result == "repair"  # Fallback (should not happen in practice)


class TestTestFailed:
    """Tests for test_failed routing function."""

    def test_test_failed_all_passed(self):
        """Test routing when all tests pass."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": True,
            "lint_passed": True,
            "tests_passed": True,
        }

        result = routing_test_failed(state)
        assert result == "integrate"

    def test_test_failed_lint_failed(self):
        """Test routing when lint fails."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "lint_passed": False,
            "tests_passed": True,
            "repair_retries": 0,
            "max_repair_retries": 3,
        }

        result = routing_test_failed(state)
        assert result == "repair"

    def test_test_failed_tests_failed(self):
        """Test routing when tests fail."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "lint_passed": True,
            "tests_passed": False,
            "repair_retries": 0,
            "max_repair_retries": 3,
        }

        result = routing_test_failed(state)
        assert result == "repair"

    def test_test_failed_max_retries_reached(self):
        """Test routing when max retries reached."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "lint_passed": False,
            "tests_passed": False,
            "repair_retries": 3,
            "max_repair_retries": 3,
        }

        result = routing_test_failed(state)
        assert result == "integrate"  # Max retries reached, proceed anyway

    def test_test_failed_repair_max_retries_reached_flag(self):
        """Test routing when repair_max_retries_reached flag is set."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "lint_passed": False,
            "tests_passed": False,
            "repair_max_retries_reached": True,
        }

        result = routing_test_failed(state)
        assert result == "integrate"  # Flag set, proceed to integrate

    def test_test_failed_defaults(self):
        """Test routing with default values."""
        state: WorkflowState = {
            "task_id": "T-test",
            "run_id": "R-test",
            "run_path": Mock(),
            "trace_id": "T-test-R-test",
            "status": "running",
            "task_objective": "Test",
            "test_passed": False,
            "repair_retries": 0,
            "max_repair_retries": 3,
        }

        result = routing_test_failed(state)
        assert result == "repair"  # Defaults assume failure

