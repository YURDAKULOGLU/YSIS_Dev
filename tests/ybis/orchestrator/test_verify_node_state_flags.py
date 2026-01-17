"""
Test verify_node sets state flags for conditional routing.

This test verifies that verify_node correctly sets test_passed, lint_passed,
and tests_passed flags in state, which are required for repair loop routing.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.ybis.orchestrator.nodes.execution import verify_node
from src.ybis.orchestrator.graph import WorkflowState
from src.ybis.contracts import VerifierReport


@pytest.fixture
def mock_run_path(tmp_path):
    """Create a temporary run path for testing."""
    run_path = tmp_path / "workspaces" / "TEST-TASK" / "runs" / "R-test"
    run_path.mkdir(parents=True, exist_ok=True)
    artifacts_dir = run_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return run_path


@pytest.fixture
def mock_state(mock_run_path):
    """Create a mock workflow state."""
    return {
        "task_id": "TEST-TASK",
        "run_id": "R-test",
        "run_path": mock_run_path,
        "trace_id": "TEST-TASK-R-test",
        "status": "running",
        "task_objective": "Test objective",
    }


class TestVerifyNodeStateFlags:
    """Test that verify_node sets state flags correctly."""

    @patch("src.ybis.orchestrator.nodes.execution.run_verifier")
    @patch("src.ybis.orchestrator.nodes.execution.detect_task_tier")
    @patch("src.ybis.orchestrator.nodes.execution.generate_all_artifacts")
    def test_verify_node_sets_flags_when_tests_pass(
        self, mock_generate_artifacts, mock_detect_tier, mock_run_verifier, mock_state
    ):
        """Test that verify_node sets flags when tests pass."""
        # Setup mocks
        mock_detect_tier.return_value = 1  # Tier 1
        mock_generate_artifacts.return_value = {}

        # Create a passing verifier report
        verifier_report = VerifierReport(
            task_id="TEST-TASK",
            run_id="R-test",
            lint_passed=True,
            tests_passed=True,
            coverage=0.85,
        )
        mock_run_verifier.return_value = verifier_report

        # Run verify_node
        result_state = verify_node(mock_state)

        # Assert flags are set correctly
        assert result_state["test_passed"] is True
        assert result_state["lint_passed"] is True
        assert result_state["tests_passed"] is True
        assert "test_errors" in result_state
        assert "test_warnings" in result_state

    @patch("src.ybis.orchestrator.nodes.execution.run_verifier")
    @patch("src.ybis.orchestrator.nodes.execution.detect_task_tier")
    @patch("src.ybis.orchestrator.nodes.execution.generate_all_artifacts")
    def test_verify_node_sets_flags_when_tests_fail(
        self, mock_generate_artifacts, mock_detect_tier, mock_run_verifier, mock_state
    ):
        """Test that verify_node sets flags when tests fail."""
        # Setup mocks
        mock_detect_tier.return_value = 1  # Tier 1
        mock_generate_artifacts.return_value = {}

        # Create a failing verifier report
        verifier_report = VerifierReport(
            task_id="TEST-TASK",
            run_id="R-test",
            lint_passed=True,
            tests_passed=False,  # Tests failed
            coverage=0.50,
        )
        mock_run_verifier.return_value = verifier_report

        # Run verify_node
        result_state = verify_node(mock_state)

        # Assert flags are set correctly
        assert result_state["test_passed"] is False  # Overall failed
        assert result_state["lint_passed"] is True
        assert result_state["tests_passed"] is False
        assert "test_errors" in result_state
        assert "test_warnings" in result_state

    @patch("src.ybis.orchestrator.nodes.execution.run_verifier")
    @patch("src.ybis.orchestrator.nodes.execution.detect_task_tier")
    @patch("src.ybis.orchestrator.nodes.execution.generate_all_artifacts")
    def test_verify_node_sets_flags_when_lint_fails(
        self, mock_generate_artifacts, mock_detect_tier, mock_run_verifier, mock_state
    ):
        """Test that verify_node sets flags when lint fails."""
        # Setup mocks
        mock_detect_tier.return_value = 1  # Tier 1
        mock_generate_artifacts.return_value = {}

        # Create a lint-failing verifier report
        verifier_report = VerifierReport(
            task_id="TEST-TASK",
            run_id="R-test",
            lint_passed=False,  # Lint failed
            tests_passed=True,
            coverage=0.85,
        )
        mock_run_verifier.return_value = verifier_report

        # Run verify_node
        result_state = verify_node(mock_state)

        # Assert flags are set correctly
        assert result_state["test_passed"] is False  # Overall failed (lint failed)
        assert result_state["lint_passed"] is False
        assert result_state["tests_passed"] is True
        assert "test_errors" in result_state
        assert "test_warnings" in result_state

    @patch("src.ybis.orchestrator.nodes.execution.run_verifier")
    @patch("src.ybis.orchestrator.nodes.execution.detect_task_tier")
    @patch("src.ybis.orchestrator.nodes.execution.generate_all_artifacts")
    def test_verify_node_flags_enable_routing(
        self, mock_generate_artifacts, mock_detect_tier, mock_run_verifier, mock_state
    ):
        """Test that flags set by verify_node enable correct routing."""
        from src.ybis.workflows.conditional_routing import test_failed

        # Setup mocks
        mock_detect_tier.return_value = 1
        mock_generate_artifacts.return_value = {}

        # Create a failing verifier report
        verifier_report = VerifierReport(
            task_id="TEST-TASK",
            run_id="R-test",
            lint_passed=False,
            tests_passed=False,
            coverage=0.50,
        )
        mock_run_verifier.return_value = verifier_report

        # Run verify_node
        result_state = verify_node(mock_state)

        # Initialize repair retry counters for routing
        result_state["repair_retries"] = 0
        result_state["max_repair_retries"] = 3

        # Test that routing function can use the flags
        route = test_failed(result_state)

        # Should route to repair when tests fail
        assert route == "repair"

        # Verify flags are set
        assert result_state["test_passed"] is False
        assert result_state["lint_passed"] is False
        assert result_state["tests_passed"] is False


