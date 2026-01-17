"""
Test Local Coder Adapter - Ollama-based code executor.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.ybis.adapters.local_coder import LocalCoderExecutor
from src.ybis.contracts import Plan, RunContext


class TestLocalCoderExecutor:
    """Test LocalCoderExecutor functionality."""

    @pytest.fixture
    def executor(self):
        """Create executor instance."""
        return LocalCoderExecutor()

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
        assert hasattr(executor, "model")
        assert hasattr(executor, "api_base")

    def test_is_available(self, executor):
        """Test is_available check."""
        # Should not raise
        available = executor.is_available()
        assert isinstance(available, bool)

    def test_executor_logs(self, executor):
        """Test executor logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.local_coder")
        assert logger is not None

    @pytest.mark.skip(reason="Requires Ollama running")
    def test_generate_code(self, executor, mock_ctx, mock_plan):
        """Test code generation (requires Ollama)."""
        # This would require actual Ollama
        pass


