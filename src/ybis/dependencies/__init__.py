"""
YBIS Dependency System

Universal dependency tracking for code, docs, and configs.
"""

from .graph import ChangeImpact, DependencyGraph
from .schema import (
    Dependency,
    DependencyType,
    FileNode,
    FileType,
    extract_all_dependencies,
)

__all__ = [
    "ChangeImpact",
    "Dependency",
    "DependencyGraph",
    "DependencyType",
    "FileNode",
    "FileType",
    "extract_all_dependencies",
]
