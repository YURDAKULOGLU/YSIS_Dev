"""
Syscalls - Single enforcement point for all mutating operations.
"""

from .exec import run_command
from .fs import write_file
from .git import commit, get_diff
from .journal import append_event

__all__ = [
    "append_event",
    "commit",
    "get_diff",
    "run_command",
    "write_file",
]
