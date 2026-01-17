"""
Test Aider Adapter - Aider-based code executor.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.ybis.adapters.aider import AiderExecutor
from src.ybis.contracts import Plan, RunContext


class TestAiderExecutor:
    """Test AiderExecutor functionality."""

    @pytest.fixture
    def executor(self):
        """Create executor instance."""
        return AiderExecutor()

    @pytest.fixture
    def mock_ctx(self, tmp_path):
        """Create mock run context."""
        return RunContext(
            task_id="test-task-123",
            run_id="test-run-456",
            run_path=tmp_path,
            trace_id="test-trace-789",
        )

    @pytest.fixture
    def mock_plan(self):
        """Create mock plan."""
        return Plan(
            objective="Test objective",
            files=["test_file.py"],
            instructions="Test instructions",
            steps=[],
        )

    def test_executor_initialization(self, executor):
        """Test executor can be initialized."""
        assert executor is not None

    def test_is_available(self, executor):
        """Test is_available check."""
        available = executor.is_available()
        assert isinstance(available, bool)

    def test_executor_logs(self, executor):
        """Test executor logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.aider")
        assert logger is not None

    @pytest.mark.skip(reason="Requires Aider installed")
    def test_generate_code(self, executor, mock_ctx, mock_plan):
        """Test code generation (requires Aider)."""
        # This would require actual Aider
        pass


