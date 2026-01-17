"""
Git syscalls - Guarded Git operations with journaling.
"""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

from ..contracts import RunContext
from .journal import append_event


def get_diff(ctx: RunContext, cwd: Path | None = None) -> str:
    """
    Get git diff.

    Args:
        ctx: Run context
        cwd: Working directory (default: run_path)

    Returns:
        Git diff output
    """
    work_dir = cwd or ctx.run_path

    result = subprocess.run(
        ["git", "diff"],
        cwd=work_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    return result.stdout


def commit(message: str, author: str, ctx: RunContext, cwd: Path | None = None) -> None:
    """
    Commit changes with journaling.

    Args:
        message: Commit message
        author: Author name
        ctx: Run context
        cwd: Working directory (default: run_path)

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    work_dir = cwd or ctx.run_path

    # Set git config for author if needed
    subprocess.run(
        ["git", "config", "user.name", author],
        cwd=work_dir,
        capture_output=True,
        check=False,
    )

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=work_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    result.check_returncode()

    # Journal event
    append_event(
        ctx.run_path,
        "GIT_COMMIT",
        {
            "message": message,
            "author": author,
            "commit_hash": _get_last_commit_hash(work_dir),
        },
    )


def _get_last_commit_hash(cwd: Path) -> str:
    """
    Get last commit hash.

    Args:
        cwd: Working directory

    Returns:
        Commit hash
    """
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    return result.stdout.strip() if result.returncode == 0 else "unknown"

