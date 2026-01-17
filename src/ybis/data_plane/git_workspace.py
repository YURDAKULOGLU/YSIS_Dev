"""
Git Worktree Management - Per-run git isolation.

Follows Port Architecture: Uses GitPython adapter, core never imports git directly.
"""

import logging
import shutil
from pathlib import Path

from ..constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


def _sync_uncommitted_files(worktree_path: Path, project_root: Path) -> list[str]:
    """
    Sync uncommitted/untracked files from project root to worktree.

    This ensures files that haven't been committed yet are available
    in the worktree for execution.

    Args:
        worktree_path: Path to worktree
        project_root: Main project root

    Returns:
        List of synced file paths
    """
    try:
        from git import Repo
    except ImportError:
        return []

    synced = []
    repo = Repo(project_root)

    # Get untracked files
    untracked = repo.untracked_files

    # Get modified but uncommitted files
    modified = [item.a_path for item in repo.index.diff(None)]

    # Get staged but uncommitted files
    staged = [item.a_path for item in repo.index.diff("HEAD")]

    all_uncommitted = set(untracked + modified + staged)

    for file_path in all_uncommitted:
        source = project_root / file_path
        dest = worktree_path / file_path

        if source.exists() and source.is_file():
            # Skip large files and non-essential
            if source.stat().st_size > 10 * 1024 * 1024:  # 10MB
                continue

            # Skip virtual env and cache
            skip_patterns = [".venv", "__pycache__", ".git", "node_modules", ".chroma"]
            if any(p in str(file_path) for p in skip_patterns):
                continue

            # Copy file
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            synced.append(file_path)

    return synced


def init_git_worktree(
    task_id: str, run_id: str, run_path: Path, trace_id: str | None = None
) -> Path:
    """
    Create git worktree for isolated execution.

    Follows Port Architecture: Uses GitPython, not git CLI directly.

    Args:
        task_id: Task identifier
        run_id: Run identifier
        run_path: Path where worktree will be created
        trace_id: Optional trace ID for journaling

    Returns:
        Path to worktree directory

    Raises:
        ImportError: If GitPython not installed
        Exception: If git worktree creation fails
    """
    try:
        from git import GitCommandError, Repo
    except ImportError:
        raise ImportError(
            "GitPython not installed. Install with: pip install GitPython"
        )

    # Ensure we're in a git repository
    repo = Repo(PROJECT_ROOT)
    if not repo.git_dir:
        # Not a git repo, return regular path
        run_path.mkdir(parents=True, exist_ok=True)
        # Lazy import to avoid circular dependency
        from ..syscalls.journal import append_event
        append_event(
            run_path,
            "GIT_WORKTREE_SKIPPED",
            {
                "reason": "Not a git repository",
                "task_id": task_id,
                "run_id": run_id,
            },
            trace_id=trace_id,
        )
        return run_path

    # Create branch name
    branch_name = f"task-{task_id}-run-{run_id}"

    try:
        branch_exists = any(head.name == branch_name for head in repo.heads)
        if branch_exists:
            # Create worktree from existing branch
            repo.git.worktree("add", str(run_path), branch_name)
        else:
            # Create new branch and worktree
            repo.git.worktree("add", "-b", branch_name, str(run_path))

        # NEW: Sync uncommitted files
        synced_files = _sync_uncommitted_files(run_path, PROJECT_ROOT)

        # Journal event (lazy import to avoid circular dependency)
        from ..syscalls.journal import append_event
        append_event(
            run_path,
            "GIT_WORKTREE_CREATED",
            {
                "branch_name": branch_name,
                "worktree_path": str(run_path),
                "task_id": task_id,
                "run_id": run_id,
            },
            trace_id=trace_id,
        )

        if synced_files:
            append_event(
                run_path,
                "WORKTREE_FILES_SYNCED",
                {
                    "synced_count": len(synced_files),
                    "files": synced_files[:20],  # First 20 for log
                },
                trace_id=trace_id,
            )

        return run_path

    except GitCommandError as e:
        # If worktree already exists or branch exists, handle gracefully
        if "already exists" in str(e).lower() or "already checked out" in str(e).lower():
            # Use existing worktree
            from ..syscalls.journal import append_event
            append_event(
                run_path,
                "GIT_WORKTREE_REUSED",
                {
                    "branch_name": branch_name,
                    "worktree_path": str(run_path),
                    "task_id": task_id,
                    "run_id": run_id,
                    "reason": str(e),
                },
                trace_id=trace_id,
            )
            return run_path
        else:
            # Other error - fallback to regular directory
            run_path.mkdir(parents=True, exist_ok=True)
            from ..syscalls.journal import append_event
            append_event(
                run_path,
                "GIT_WORKTREE_FAILED",
                {
                    "branch_name": branch_name,
                    "error": str(e),
                    "fallback": "regular_directory",
                },
                trace_id=trace_id,
            )
            return run_path

    except Exception as e:
        # Fallback to regular directory
        run_path.mkdir(parents=True, exist_ok=True)
        from ..syscalls.journal import append_event
        append_event(
            run_path,
            "GIT_WORKTREE_ERROR",
            {
                "error": str(e),
                "fallback": "regular_directory",
            },
            trace_id=trace_id,
        )
        return run_path


def cleanup_git_worktree(
    worktree_path: Path, trace_id: str | None = None, force: bool = False
) -> None:
    """
    Remove git worktree.

    Args:
        worktree_path: Path to worktree to remove
        trace_id: Optional trace ID for journaling
        force: Force removal even if there are uncommitted changes
    """
    try:
        from git import GitCommandError, Repo
    except ImportError:
        # GitPython not available, just remove directory
        import shutil

        if worktree_path.exists():
            shutil.rmtree(worktree_path, ignore_errors=True)
        return

    try:
        repo = Repo(PROJECT_ROOT)
        if not repo.git_dir:
            # Not a git repo, just remove directory
            import shutil

            if worktree_path.exists():
                shutil.rmtree(worktree_path, ignore_errors=True)
            return

        # Remove worktree
        if force:
            repo.git.worktree("remove", "--force", str(worktree_path))
        else:
            repo.git.worktree("remove", str(worktree_path))

        # Journal event (lazy import to avoid circular dependency)
        from ..syscalls.journal import append_event
        append_event(
            worktree_path,
            "GIT_WORKTREE_REMOVED",
            {
                "worktree_path": str(worktree_path),
                "force": force,
            },
            trace_id=trace_id,
        )

    except GitCommandError as e:
        # If worktree doesn't exist or can't be removed, just delete directory
        import shutil

        if worktree_path.exists():
            shutil.rmtree(worktree_path, ignore_errors=True)

        from ..syscalls.journal import append_event
        append_event(
            worktree_path,
            "GIT_WORKTREE_REMOVE_FAILED",
            {
                "worktree_path": str(worktree_path),
                "error": str(e),
                "fallback": "directory_deleted",
            },
            trace_id=trace_id,
        )

    except Exception as e:
        # Fallback: just delete directory
        import shutil

        if worktree_path.exists():
            shutil.rmtree(worktree_path, ignore_errors=True)

        from ..syscalls.journal import append_event
        append_event(
            worktree_path,
            "GIT_WORKTREE_CLEANUP_ERROR",
            {
                "error": str(e),
                "fallback": "directory_deleted",
            },
            trace_id=trace_id,
        )

