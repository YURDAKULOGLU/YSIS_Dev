"""
YBIS Platform - Governed agent runtime with workflows, syscalls, evidence, and MCP.
"""

__version__ = "0.1.0"

# Export constants
from .constants import ARTIFACTS_DIR, JOURNAL_DIR, PROJECT_ROOT, VENDORS_DIR

__all__ = [
    "ARTIFACTS_DIR",
    "JOURNAL_DIR",
    "PROJECT_ROOT",
    "VENDORS_DIR",
]

