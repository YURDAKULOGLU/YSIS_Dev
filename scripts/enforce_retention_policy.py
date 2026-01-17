"""
Data Retention Policy Enforcement Script.

Enforces retention policies for runs, artifacts, and related data.
"""

import argparse
import json
import os
import sqlite3
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Calculate project root
PROJECT_ROOT = Path(__file__).parent.parent


class RetentionEnforcer:
    """Enforces data retention policies."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize retention enforcer.

        Args:
            dry_run: If True, only report what would be done without making changes
        """
        self.dry_run = dry_run
        self.workspaces_dir = PROJECT_ROOT / "workspaces"
        self.archive_dir = PROJECT_ROOT / "workspaces" / "archive"
        self.db_path = PROJECT_ROOT / "platform_data" / "control_plane.sqlite"
        self.audit_log = PROJECT_ROOT / "platform_data" / "retention_audit.log"

        # Load retention periods from policy/env (with defaults)
        self.retention_periods = self._load_retention_periods()
        self._ensure_retention_schema()

    def _ensure_retention_schema(self) -> None:
        """Ensure retention-related columns exist for existing databases."""
        if not self.db_path.exists():
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            def ensure_column(table: str, column: str, definition: str) -> None:
                cursor.execute(f"PRAGMA table_info({table})")
                existing = {row[1] for row in cursor.fetchall()}
                if column not in existing:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

            ensure_column("runs", "archived", "INTEGER DEFAULT 0")
            ensure_column("runs", "archived_at", "TIMESTAMP")
            ensure_column("runs", "retention_hold", "INTEGER DEFAULT 0")
            ensure_column("tasks", "protected", "INTEGER DEFAULT 0")

            conn.commit()
            conn.close()
        except Exception:
            pass

    def _load_retention_periods(self) -> Dict[str, int]:
        """
        Load retention periods from policy or environment variables.

        Returns:
            Dictionary with retention periods in days
        """
        # Default periods
        periods = {
            "successful": 90,
            "failed": 30,
            "abandoned": 7,
        }

        # Override from environment variables
        periods["successful"] = int(os.getenv("YBIS_RETENTION_SUCCESSFUL_DAYS", periods["successful"]))
        periods["failed"] = int(os.getenv("YBIS_RETENTION_FAILED_DAYS", periods["failed"]))
        periods["abandoned"] = int(os.getenv("YBIS_RETENTION_ABANDONED_DAYS", periods["abandoned"]))

        # Override from policy profile
        profile_name = os.getenv("YBIS_PROFILE", "default")
        profile_path = PROJECT_ROOT / "configs" / "profiles" / f"{profile_name}.yaml"

        if profile_path.exists():
            try:
                with open(profile_path, "r", encoding="utf-8") as f:
                    profile = yaml.safe_load(f) or {}
                    retention_config = profile.get("retention", {})
                    if retention_config:
                        periods["successful"] = retention_config.get("successful_runs_days", periods["successful"])
                        periods["failed"] = retention_config.get("failed_runs_days", periods["failed"])
                        periods["abandoned"] = retention_config.get("abandoned_runs_days", periods["abandoned"])
            except Exception:
                pass  # Fallback to defaults if policy load fails

        return periods

    def get_run_status(self, run_id: str, task_id: str) -> Optional[Dict]:
        """
        Get run status from control plane DB.

        Args:
            run_id: Run identifier
            task_id: Task identifier

        Returns:
            Run metadata or None if not found
        """
        if not self.db_path.exists():
            return None

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT run_id, task_id, status, created_at, archived FROM runs WHERE run_id = ? AND task_id = ?",
                (run_id, task_id),
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "run_id": row[0],
                    "task_id": row[1],
                    "status": row[2],
                    "created_at": row[3],
                    "archived": row[4] == 1 if row[4] else False,
                }
        except Exception:
            pass

        return None

    def is_golden_run(self, run_path: Path) -> bool:
        """
        Check if run is marked as golden.

        Args:
            run_path: Path to run directory

        Returns:
            True if golden, False otherwise
        """
        # Check artifacts for golden marker
        artifacts_dir = run_path / "artifacts"
        if artifacts_dir.exists():
            for artifact_file in artifacts_dir.glob("*.json"):
                try:
                    with open(artifact_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("metadata", {}).get("golden"):
                            return True
                except Exception:
                    continue

        return False

    def should_archive_run(self, run_path: Path, run_metadata: Optional[Dict]) -> tuple[bool, str]:
        """
        Determine if a run should be archived.

        Args:
            run_path: Path to run directory
            run_metadata: Run metadata from DB

        Returns:
            Tuple of (should_archive, reason)
        """
        # Check if already archived
        if run_metadata and run_metadata.get("archived"):
            return False, "Already archived"

        # Check if golden
        if self.is_golden_run(run_path):
            return False, "Golden run (indefinite retention)"

        # Check if retention hold is active
        if run_metadata:
            task_id = run_metadata.get("task_id")
            run_id_from_meta = run_metadata.get("run_id", run_path.name)
            if self.has_retention_hold(run_id_from_meta, task_id):
                return False, "Retention hold active (indefinite retention)"

        # Check if protected task
        if run_metadata:
            task_id = run_metadata.get("task_id")
            if self.is_protected_task(task_id):
                return False, "Protected task (indefinite retention)"

        # Determine retention period based on status
        if not run_metadata:
            # No DB metadata, check artifacts
            gate_report = run_path / "artifacts" / "gate_report.json"
            if gate_report.exists():
                try:
                    with open(gate_report, "r", encoding="utf-8") as f:
                        gate_data = json.load(f)
                        decision = gate_data.get("decision", "BLOCK")
                        if decision == "PASS":
                            status = "SUCCESS"
                        else:
                            status = "FAILED"
                except Exception:
                    status = "UNKNOWN"
            else:
                status = "ABANDONED"
        else:
            status = run_metadata.get("status", "UNKNOWN")

        # Calculate age
        if run_metadata and run_metadata.get("created_at"):
            try:
                created_at = datetime.fromisoformat(run_metadata["created_at"].replace("Z", "+00:00"))
                age_days = (datetime.now(created_at.tzinfo) - created_at).days
            except Exception:
                age_days = 999  # Unknown age, assume old
        else:
            # Use file modification time as fallback
            age_days = (datetime.now() - datetime.fromtimestamp(run_path.stat().st_mtime)).days

        # Map status to retention period
        if status in ["SUCCESS", "DONE"]:
            retention_days = self.retention_periods["successful"]
            status_key = "successful"
        elif status in ["FAILED", "BLOCK"]:
            retention_days = self.retention_periods["failed"]
            status_key = "failed"
        else:
            retention_days = self.retention_periods["abandoned"]
            status_key = "abandoned"

        if age_days > retention_days:
            return True, f"{status_key} run expired (age: {age_days} days, retention: {retention_days} days)"

        return False, f"{status_key} run within retention period (age: {age_days} days, retention: {retention_days} days)"

    def is_protected_task(self, task_id: str) -> bool:
        """
        Check if task is protected.

        Args:
            task_id: Task identifier

        Returns:
            True if protected, False otherwise
        """
        if not self.db_path.exists():
            return False

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT protected FROM tasks WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            conn.close()

            if row and row[0] == 1:
                return True
        except Exception:
            pass

        return False

    def has_retention_hold(self, run_id: str, task_id: str) -> bool:
        """
        Check if a run has an active retention hold.

        Args:
            run_id: Run identifier
            task_id: Task identifier

        Returns:
            True if hold is active, False otherwise
        """
        if not self.db_path.exists():
            return False

        self._ensure_retention_schema()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT retention_hold FROM runs WHERE run_id = ? AND task_id = ?",
                (run_id, task_id),
            )
            row = cursor.fetchone()
            conn.close()
            return bool(row[0]) if row else False
        except Exception:
            return False

    def set_retention_hold(self, run_id: str, task_id: str, enabled: bool) -> bool:
        """
        Enable or disable retention hold for a run.

        Args:
            run_id: Run identifier
            task_id: Task identifier
            enabled: True to enable hold, False to disable

        Returns:
            True if updated, False otherwise
        """
        if not self.db_path.exists():
            return False

        self._ensure_retention_schema()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE runs SET retention_hold = ? WHERE run_id = ? AND task_id = ?",
                (1 if enabled else 0, run_id, task_id),
            )
            conn.commit()
            updated = cursor.rowcount > 0
            conn.close()
            return updated
        except Exception:
            return False


    def archive_run(self, run_path: Path, task_id: str, run_id: str) -> bool:
        """
        Archive a run.

        Args:
            run_path: Path to run directory
            task_id: Task identifier
            run_id: Run identifier

        Returns:
            True if successful, False otherwise
        """
        archive_task_dir = self.archive_dir / task_id / "runs"
        archive_run_path = archive_task_dir / run_id

        try:
            # Create archive directory
            archive_task_dir.mkdir(parents=True, exist_ok=True)

            if not self.dry_run:
                # Move run to archive
                run_path.rename(archive_run_path)

                # Update DB
                if self.db_path.exists():
                    self._ensure_retention_schema()
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE runs SET archived = 1, archived_at = ? WHERE run_id = ? AND task_id = ?",
                        (datetime.now().isoformat(), run_id, task_id),
                    )
                    conn.commit()
                    conn.close()

                # Log action
                self.log_action("ARCHIVE", run_id, task_id, f"Moved to {archive_run_path}")

            return True
        except Exception as e:
            self.log_action("ARCHIVE_ERROR", run_id, task_id, f"Failed: {e}")
            return False

    def log_action(self, action: str, run_id: str, task_id: str, message: str) -> None:
        """
        Log retention action.

        Args:
            action: Action type (ARCHIVE, DELETE, etc.)
            run_id: Run identifier
            task_id: Task identifier
            message: Log message
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "run_id": run_id,
            "task_id": task_id,
            "message": message,
            "dry_run": self.dry_run,
        }

        log_line = json.dumps(log_entry) + "\n"

        if not self.dry_run:
            self.audit_log.parent.mkdir(parents=True, exist_ok=True)
            with open(self.audit_log, "a", encoding="utf-8") as f:
                f.write(log_line)
        else:
            print(f"[DRY RUN] {log_line.strip()}")

    def scan_and_enforce(self) -> Dict[str, List[str]]:
        """
        Scan workspaces and enforce retention policy.

        Returns:
            Dictionary with lists of archived runs and errors
        """
        results = {
            "archived": [],
            "errors": [],
            "skipped": [],
        }

        if not self.workspaces_dir.exists():
            return results

        # Scan all task directories
        for task_dir in self.workspaces_dir.iterdir():
            if not task_dir.is_dir() or task_dir.name == "archive":
                continue

            task_id = task_dir.name
            runs_dir = task_dir / "runs"

            if not runs_dir.exists():
                continue

            # Scan all runs
            for run_dir in runs_dir.iterdir():
                if not run_dir.is_dir():
                    continue

                run_id = run_dir.name

                # Get run metadata
                run_metadata = self.get_run_status(run_id, task_id)

                # Check if should archive
                should_archive, reason = self.should_archive_run(run_dir, run_metadata)

                if should_archive:
                    if self.archive_run(run_dir, task_id, run_id):
                        results["archived"].append(f"{task_id}/{run_id}: {reason}")
                    else:
                        results["errors"].append(f"{task_id}/{run_id}: Archive failed")
                else:
                    results["skipped"].append(f"{task_id}/{run_id}: {reason}")

        return results

    def generate_report(self, results: Dict[str, List[str]]) -> str:
        """
        Generate retention enforcement report.

        Args:
            results: Results from scan_and_enforce

        Returns:
            Markdown report
        """
        report = f"# Retention Policy Enforcement Report\n\n"
        report += f"**Date:** {datetime.now().isoformat()}\n"
        report += f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE'}\n\n"

        report += f"## Summary\n\n"
        report += f"- **Archived:** {len(results['archived'])}\n"
        report += f"- **Skipped:** {len(results['skipped'])}\n"
        report += f"- **Errors:** {len(results['errors'])}\n\n"

        if results["archived"]:
            report += f"## Archived Runs\n\n"
            for item in results["archived"]:
                report += f"- {item}\n"
            report += "\n"

        if results["errors"]:
            report += f"## Errors\n\n"
            for item in results["errors"]:
                report += f"- {item}\n"
            report += "\n"

        return report


def cleanup_archives(enforcer: RetentionEnforcer, older_than_days: int = 365) -> Dict[str, List[str]]:
    """
    Clean up archived runs older than specified days.

    Args:
        enforcer: Retention enforcer instance
        older_than_days: Delete archives older than this many days

    Returns:
        Dictionary with lists of deleted runs and errors
    """
    results = {"deleted": [], "errors": []}

    if not enforcer.archive_dir.exists():
        return results

    cutoff_date = datetime.now() - timedelta(days=older_than_days)

    # Scan archive directory
    for task_dir in enforcer.archive_dir.iterdir():
        if not task_dir.is_dir():
            continue

        task_id = task_dir.name
        runs_dir = task_dir / "runs"

        if not runs_dir.exists():
            continue

        for run_dir in runs_dir.iterdir():
            if not run_dir.is_dir():
                continue

            run_id = run_dir.name

            # Check modification time
            mod_time = datetime.fromtimestamp(run_dir.stat().st_mtime)
            if mod_time < cutoff_date:
                try:
                    if not enforcer.dry_run:
                        # Permanently delete
                        import shutil

                        shutil.rmtree(run_dir)
                        enforcer.log_action("DELETE_ARCHIVE", run_id, task_id, f"Deleted archive older than {older_than_days} days")
                    results["deleted"].append(f"{task_id}/{run_id}")
                except Exception as e:
                    results["errors"].append(f"{task_id}/{run_id}: {e}")
                    enforcer.log_action("DELETE_ARCHIVE_ERROR", run_id, task_id, f"Failed: {e}")

    return results


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Enforce data retention policy")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without executing")
    parser.add_argument("--report", type=str, help="Save report to file")
    parser.add_argument("--cleanup-archives", action="store_true", help="Clean up archived runs older than 1 year")
    parser.add_argument("--hold", type=str, help="Place retention hold on run (format: TASK_ID/RUN_ID)")
    parser.add_argument("--release", type=str, help="Release retention hold on run (format: TASK_ID/RUN_ID)")
    args = parser.parse_args()

    enforcer = RetentionEnforcer(dry_run=args.dry_run)

    # Handle retention hold operations
    if args.hold:
        parts = args.hold.split("/")
        if len(parts) != 2:
            print(f"[ERROR] Invalid format for --hold. Use TASK_ID/RUN_ID", file=sys.stderr)
            return 1
        task_id, run_id = parts
        if enforcer.set_retention_hold(run_id, task_id, enabled=True):
            print(f"[OK] Retention hold placed on {task_id}/{run_id}")
            return 0
        else:
            print(f"[ERROR] Failed to place retention hold on {task_id}/{run_id} (run may not exist)", file=sys.stderr)
            return 1

    if args.release:
        parts = args.release.split("/")
        if len(parts) != 2:
            print(f"[ERROR] Invalid format for --release. Use TASK_ID/RUN_ID", file=sys.stderr)
            return 1
        task_id, run_id = parts
        if enforcer.set_retention_hold(run_id, task_id, enabled=False):
            print(f"[OK] Retention hold released on {task_id}/{run_id}")
            return 0
        else:
            print(f"[ERROR] Failed to release retention hold on {task_id}/{run_id} (run may not exist)", file=sys.stderr)
            return 1

    # Handle archive cleanup
    if args.cleanup_archives:
        print("[INFO] Cleaning up archived runs older than 1 year...")
        cleanup_results = cleanup_archives(enforcer, older_than_days=365)
        print(f"[INFO] Deleted {len(cleanup_results['deleted'])} archived runs")
        if cleanup_results["errors"]:
            print(f"[ERROR] {len(cleanup_results['errors'])} errors during cleanup", file=sys.stderr)
        return 1 if cleanup_results["errors"] else 0

    # Normal retention enforcement
    print("[INFO] Scanning workspaces for runs to archive...")
    results = enforcer.scan_and_enforce()

    # Generate report
    report = enforcer.generate_report(results)
    print(report)

    # Save report if requested
    if args.report:
        report_path = Path(args.report)
        report_path.write_text(report, encoding="utf-8")
        print(f"[INFO] Report saved to {report_path}")

    # Return non-zero if errors occurred
    return 1 if results["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())

