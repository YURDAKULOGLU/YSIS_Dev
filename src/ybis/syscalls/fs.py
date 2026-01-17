"""
Filesystem syscalls - File operations with protection and journaling.
"""

import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from ..contracts import RunContext
from ..services.policy import get_policy_provider


def _is_protected(path: Path) -> bool:
    """
    Check if path is protected.

    Args:
        path: Path to check (can be relative or absolute)

    Returns:
        True if path is protected
    """
    from ..constants import PROJECT_ROOT as PROJ_ROOT

    # Get protected paths from policy
    policy_provider = get_policy_provider()
    protected_paths = policy_provider.get_protected_paths()

    # Convert to absolute path for comparison
    if not path.is_absolute():
        abs_path = (PROJ_ROOT / path).resolve()
    else:
        abs_path = path.resolve()

    path_str = str(abs_path)
    for protected in protected_paths:
        # Check if protected path is in the absolute path
        protected_abs = (PROJ_ROOT / protected).resolve()
        protected_str = str(protected_abs)
        if protected_str in path_str or path_str.startswith(protected_str):
            return True
    return False


def write_file(path: Path, content: str, ctx: RunContext) -> None:
    """
    Write file with protection check and journaling.

    Args:
        path: Path to file to write
        content: Content to write
        ctx: Run context

    Raises:
        PermissionError: If path is protected
    """
    # Check if path is protected
    if _is_protected(path):
        raise PermissionError(f"Protected path: {path}")

    # Write file
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    # Journal event
    from .journal import append_event

    # Calculate content hash and length for journal
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    append_event(
        ctx.run_path,
        "FILE_WRITE",
        {
            "path": str(path),
            "content_length": len(content),
            "content_hash": content_hash,
        },
    )

