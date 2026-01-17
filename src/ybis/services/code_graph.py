"""
Code Graph Service - Dependency mapping using Pyan.

Generates dependency graphs for impact analysis during planning.
"""

import subprocess
from pathlib import Path


class CodeGraph:
    """
    Code dependency graph generator using Pyan.

    Provides impact analysis: "Changing file X will affect files Y and Z."
    """

    def __init__(self, project_root: Path):
        """
        Initialize code graph service.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root

    def get_dependencies(self, file_path: Path) -> list[str]:
        """
        Get list of files that depend on the given file.

        Args:
            file_path: Path to Python file

        Returns:
            List of dependent file paths (relative to project root)
        """
        try:
            # Run pyan3 to generate dependency graph
            result = subprocess.run(
                ["pyan3", str(file_path), "--dot", "--no-defines"],
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=30,
            )

            if result.returncode != 0:
                return []

            # Parse DOT output to find dependencies
            # Pyan outputs DOT format: "file1" -> "file2"
            dependent_files = []
            for line in result.stdout.split("\n"):
                if "->" in line:
                    # Extract target file (what depends on our file)
                    parts = line.split("->")
                    if len(parts) == 2:
                        target = parts[1].strip().strip('"').strip("'")
                        # Convert to relative path
                        if target and target not in dependent_files:
                            dependent_files.append(target)

            return dependent_files

        except FileNotFoundError:
            # Pyan not installed, return empty list
            return []
        except subprocess.TimeoutExpired:
            return []
        except Exception:
            return []

    def get_impact_analysis(self, file_paths: list[Path]) -> dict[str, list[str]]:
        """
        Perform impact analysis for multiple files.

        Args:
            file_paths: List of files to analyze

        Returns:
            Dictionary mapping file path to list of dependent files
        """
        impact_map: dict[str, list[str]] = {}

        for file_path in file_paths:
            if file_path.suffix == ".py":
                dependents = self.get_dependencies(file_path)
                impact_map[str(file_path.relative_to(self.project_root))] = dependents

        return impact_map

    def format_impact_warning(self, file_path: str, dependents: list[str]) -> str:
        """
        Format impact analysis warning for planner prompt.

        Args:
            file_path: File being modified
            dependents: List of dependent files

        Returns:
            Formatted warning message
        """
        if not dependents:
            return ""

        dep_list = ", ".join(dependents[:5])  # Limit to first 5
        if len(dependents) > 5:
            dep_list += f" and {len(dependents) - 5} more"

        return f"WARNING: Changing {file_path} will affect dependent files: {dep_list}"

