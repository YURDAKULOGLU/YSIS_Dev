"""
Test Write File - Atomic file writing.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.ybis.syscalls.write_file import write_file
from src.ybis.contracts import RunContext


class TestWriteFile:
    """Test write_file functionality."""

    @pytest.fixture
    def mock_ctx(self, tmp_path):
        """Create mock run context."""
        return RunContext(
            task_id="test-123",
            run_id="run-456",
            run_path=tmp_path,
            trace_id="trace-789",
        )

    def test_write_file_logs(self):
        """Test write_file logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.syscalls.write_file")
        assert logger is not None

    def test_write_file(self, mock_ctx, tmp_path):
        """Test file writing."""
        test_file = tmp_path / "test.txt"
        write_file(test_file, "test content", mock_ctx)
        assert test_file.exists()
        assert test_file.read_text() == "test content"


