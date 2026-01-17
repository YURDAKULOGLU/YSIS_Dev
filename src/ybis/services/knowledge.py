"""
Knowledge Service - Codebase scanning for context awareness.

Scans the codebase to generate summaries for LLM context.
"""

import os
from pathlib import Path


def scan_codebase(root: Path, ignore_patterns: list[str] | None = None) -> str:
    """
    Scan codebase and generate a summarized file tree + key definitions text.

    Args:
        root: Root directory to scan
        ignore_patterns: List of patterns to ignore (default: .gitignore patterns)

    Returns:
        Summarized codebase structure as text
    """
    if ignore_patterns is None:
        ignore_patterns = [
            "__pycache__",
            "*.pyc",
            ".git",
            "node_modules",
            ".venv",
            "venv",
            "*.egg-info",
            ".pytest_cache",
            "platform_data",
            "workspaces",
        ]

    lines = []
    lines.append(f"Codebase Structure: {root.name}\n")
    lines.append("=" * 60)
    lines.append("")

    # Walk directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter ignored directories
        dirnames[:] = [d for d in dirnames if not _should_ignore(d, ignore_patterns)]

        rel_path = Path(dirpath).relative_to(root)
        if _should_ignore(str(rel_path), ignore_patterns):
            continue

        # Add directory header
        if rel_path != Path("."):
            indent = "  " * (len(rel_path.parts) - 1)
            lines.append(f"{indent}{rel_path.name}/")

        # Add files
        for filename in filenames:
            if _should_ignore(filename, ignore_patterns):
                continue

            file_path = Path(dirpath) / filename
            rel_file = file_path.relative_to(root)
            indent = "  " * len(rel_file.parts)

            # Extract key definitions for Python files
            if filename.endswith(".py"):
                key_info = _extract_key_definitions(file_path)
                lines.append(f"{indent}{filename}")
                if key_info:
                    lines.append(f"{indent}  # {key_info}")
            else:
                lines.append(f"{indent}{filename}")

    return "\n".join(lines)


def _should_ignore(path: str, patterns: list[str]) -> bool:
    """
    Check if path should be ignored.

    Args:
        path: Path to check
        patterns: List of ignore patterns

    Returns:
        True if path should be ignored
    """
    path_str = str(path)
    for pattern in patterns:
        if pattern in path_str or path_str.endswith(pattern):
            return True
    return False


def _extract_key_definitions(file_path: Path) -> str:
    """
    Extract key definitions from a Python file.

    Args:
        file_path: Path to Python file

    Returns:
        Summary of key definitions (classes, functions)
    """
    try:
        definitions = []
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("class "):
                    class_name = line.split("(")[0].replace("class ", "").strip()
                    definitions.append(f"class {class_name}")
                elif line.startswith("def ") and not line.startswith("def _"):  # Skip private functions
                    func_name = line.split("(")[0].replace("def ", "").strip()
                    definitions.append(f"def {func_name}")

        if definitions:
            return ", ".join(definitions[:5])  # Limit to 5 definitions
        return ""
    except Exception:
        return ""

