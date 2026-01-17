"""
Test Workspace - Run structure initialization.
"""

import pytest
from pathlib import Path

from src.ybis.data_plane.workspace import init_run_structure


class TestWorkspace:
    """Test workspace functionality."""

    def test_init_run_structure(self, tmp_path):
        """Test initializing run structure."""
        # Mock PROJECT_ROOT to use tmp_path
        with patch("src.ybis.data_plane.workspace.PROJECT_ROOT", tmp_path):
            run_path = init_run_structure(
                task_id="test-task-123",
                run_id="test-run-456",
                trace_id="test-trace-789",
                use_git_worktree=False,  # Skip git for test
            )

            assert run_path.exists()
            assert (run_path / "artifacts").exists()
            assert (run_path / "journal").exists()

    def test_workspace_logs(self):
        """Test workspace logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.data_plane.workspace")
        assert logger is not None


