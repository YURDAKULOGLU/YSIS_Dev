"""
Workspace management - Physical directory structure for immutable runs.

Follows Port Architecture: Uses git worktree adapter when available.
"""

import logging
from pathlib import Path

from ..constants import ARTIFACTS_DIR, JOURNAL_DIR, PROJECT_ROOT
from .git_workspace import init_git_worktree

logger = logging.getLogger(__name__)


def init_run_structure(
    task_id: str, run_id: str, trace_id: str | None = None, use_git_worktree: bool = True
) -> Path:
    """
    Initialize immutable run structure with optional git worktree.

    Creates:
    - workspaces/<task_id>/runs/<run_id>/ (git worktree if enabled)
    - workspaces/<task_id>/runs/<run_id>/artifacts/
    - workspaces/<task_id>/runs/<run_id>/journal/

    Args:
        task_id: Task identifier
        run_id: Run identifier
        trace_id: Optional trace ID for journaling
        use_git_worktree: If True, create git worktree (default: True)

    Returns:
        Path to run directory
    """
    run_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id

    # Try git worktree if enabled
    if use_git_worktree:
        try:
            run_path = init_git_worktree(task_id, run_id, run_path, trace_id)
        except Exception:
            # Fallback to regular directory
            run_path.mkdir(parents=True, exist_ok=True)
    else:
        # Regular directory
        run_path.mkdir(parents=True, exist_ok=True)

    # Create artifacts and journal directories
    (run_path / ARTIFACTS_DIR).mkdir(exist_ok=True)
    (run_path / JOURNAL_DIR).mkdir(exist_ok=True)

    return run_path

