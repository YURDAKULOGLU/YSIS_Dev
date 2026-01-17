"""
Staleness Detector - Maintenance mode for consistency fixes.

Identifies downstream files that need updates after a core change.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..contracts import Task
from ..control_plane import ControlPlaneDB
from .code_graph import CodeGraph


class StalenessDetector:
    """
    Staleness Detector - Finds files that depend on modified core files.

    When a core file (like contracts/resources.py) changes, creates
    "Consistency Fix" tasks for all dependent files.
    """

    def __init__(self, project_root: Path | None = None):
        """
        Initialize staleness detector.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root or PROJECT_ROOT
        self.code_graph = CodeGraph(self.project_root)
        self.core_paths = [
            "src/ybis/contracts/",
            "src/ybis/syscalls/",
            "src/ybis/orchestrator/gates.py",
        ]

    def detect_staleness(self, changed_files: list[str]) -> list[dict[str, Any]]:
        """
        Detect stale files that depend on changed core files.

        Args:
            changed_files: List of file paths that were changed

        Returns:
            List of stale file information
        """
        stale_files = []

        for changed_file in changed_files:
            # Check if changed file is a core file
            is_core = any(core_path in changed_file for core_path in self.core_paths)

            if not is_core:
                continue

            # Find files that depend on this core file
            changed_path = self.project_root / changed_file
            if changed_path.exists() and changed_path.suffix == ".py":
                dependents = self.code_graph.get_dependencies(changed_path)

                for dependent in dependents:
                    # Convert dependent path to relative
                    try:
                        dependent_path = self.project_root / dependent
                        if dependent_path.exists():
                            relative_path = str(dependent_path.relative_to(self.project_root))
                            stale_files.append(
                                {
                                    "file": relative_path,
                                    "depends_on": changed_file,
                                    "reason": f"Dependent on core file {changed_file}",
                                }
                            )
                    except Exception:
                        # Skip invalid paths
                        continue

        return stale_files

    async def create_consistency_tasks(
        self, stale_files: list[dict[str, Any]], db: ControlPlaneDB
    ) -> list[str]:
        """
        Create "Consistency Fix" tasks for stale files.

        Args:
            stale_files: List of stale file information
            db: Control plane database

        Returns:
            List of created task IDs
        """
        created_tasks = []

        # Group stale files by dependency
        by_dependency: dict[str, list[str]] = {}
        for stale in stale_files:
            depends_on = stale["depends_on"]
            if depends_on not in by_dependency:
                by_dependency[depends_on] = []
            by_dependency[depends_on].append(stale["file"])

        # Create one task per dependency group
        for depends_on, files in by_dependency.items():
            import uuid

            task_id = f"T-CONSISTENCY-{uuid.uuid4().hex[:8]}"
            title = f"Consistency Fix: Update dependents of {Path(depends_on).name}"
            objective = f"Update the following files to be consistent with changes to {depends_on}:\n" + "\n".join(
                f"- {f}" for f in files[:10]  # Limit to first 10 files
            )

            task = Task(
                task_id=task_id,
                title=title,
                objective=objective,
                status="pending",
                priority="MEDIUM",
            )

            await db.register_task(task)
            created_tasks.append(task_id)

        return created_tasks

    async def check_and_create_tasks(
        self, changed_files: list[str], db: ControlPlaneDB
    ) -> list[str]:
        """
        Check for staleness and create consistency tasks if needed.

        Args:
            changed_files: List of file paths that were changed
            db: Control plane database

        Returns:
            List of created task IDs
        """
        stale_files = self.detect_staleness(changed_files)

        if not stale_files:
            return []

        # Create consistency tasks
        task_ids = await self.create_consistency_tasks(stale_files, db)

        return task_ids


class StalenessWatcher:
    """
    Watches for core file changes and auto-triggers staleness detection.

    Can be run:
    1. After each run completes
    2. On git commit hook
    3. On schedule (e.g., hourly)
    """

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or PROJECT_ROOT
        self.detector = StalenessDetector(self.project_root)
        self.last_check_file = self.project_root / "platform_data" / ".staleness_last_check"

    def get_changed_since_last_check(self) -> list[str]:
        """Get files changed since last staleness check."""
        import subprocess

        # Get last check commit
        last_commit = "HEAD~1"  # Default: compare to previous commit
        if self.last_check_file.exists():
            try:
                last_commit = self.last_check_file.read_text().strip()
            except Exception:
                pass

        # Get changed files
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", last_commit, "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        except Exception:
            pass

        return []

    def update_last_check(self) -> None:
        """Update last check marker to current HEAD."""
        import subprocess

        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                self.last_check_file.parent.mkdir(parents=True, exist_ok=True)
                self.last_check_file.write_text(result.stdout.strip())
        except Exception:
            pass

    async def check_and_create_tasks(self) -> dict[str, Any]:
        """
        Check for staleness and create consistency tasks if needed.

        Returns:
            Report of actions taken
        """
        from ..control_plane import ControlPlaneDB

        report = {
            "timestamp": datetime.now().isoformat(),
            "changed_files": [],
            "stale_files": [],
            "tasks_created": [],
        }

        # Get changed files
        changed_files = self.get_changed_since_last_check()
        report["changed_files"] = changed_files

        if not changed_files:
            return report

        # Detect staleness
        stale_files = self.detector.detect_staleness(changed_files)
        report["stale_files"] = stale_files

        if not stale_files:
            self.update_last_check()
            return report

        # Create tasks
        db_path = self.project_root / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))

        try:
            task_ids = await self.detector.create_consistency_tasks(stale_files, db)
            report["tasks_created"] = task_ids
        except Exception as e:
            report["error"] = str(e)

        # Update last check marker
        self.update_last_check()

        return report

    async def run_check(self) -> dict[str, Any]:
        """
        Convenience method to run staleness check.

        Returns:
            Staleness check report
        """
        return await self.check_and_create_tasks()

