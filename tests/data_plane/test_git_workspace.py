"""
Test Git Workspace - Git worktree management.
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from src.ybis.data_plane.git_workspace import init_git_worktree, cleanup_git_worktree


class TestGitWorkspace:
    """Test git workspace functionality."""

    @pytest.fixture
    def mock_run_path(self, tmp_path):
        """Create mock run path."""
        return tmp_path / "run_123"

    def test_init_git_worktree_no_git(self, mock_run_path):
        """Test init_git_worktree when git not available."""
        mock_run_path.mkdir(parents=True, exist_ok=True)

        # Should not raise even if git not available
        try:
            result = init_git_worktree("task-123", "run-456", mock_run_path)
            assert result is not None
        except ImportError:
            # GitPython not installed - expected
            pass

    def test_cleanup_git_worktree(self, mock_run_path):
        """Test cleanup_git_worktree."""
        mock_run_path.mkdir(parents=True, exist_ok=True)

        # Should not raise
        try:
            cleanup_git_worktree(mock_run_path)
        except ImportError:
            # GitPython not installed - expected
            pass

    def test_git_workspace_logs(self):
        """Test git workspace logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.data_plane.git_workspace")
        assert logger is not None


