"""
Health Monitor Service - System health checks and telemetry.

Provides health monitoring capabilities with auto-remediation suggestions.
This is a service (not core) and should be used via adapters.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..services.event_bus import Events, get_event_bus
from ..services.policy import get_policy_provider
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)


class HealthCheck:
    """Individual health check result."""

    def __init__(
        self,
        name: str,
        status: str,  # "healthy", "degraded", "unhealthy"
        message: str,
        details: dict[str, Any] | None = None,
    ):
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()


class HealthMonitor:
    """
    Health Monitor - System health checks with telemetry.

    Checks:
    - Database connectivity
    - Adapter availability
    - Disk space
    - Configuration validity
    - Run artifacts integrity
    """

    def __init__(self, auto_create_tasks: bool = False, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize health monitor.

        Args:
            auto_create_tasks: If True, auto-create remediation tasks for issues
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.auto_create_tasks = auto_create_tasks
        self.policy = get_policy_provider()
        self.event_bus = get_event_bus()
        self.run_path = run_path
        self.trace_id = trace_id

    def run_all_checks(self) -> list[HealthCheck]:
        """
        Run all health checks.

        Returns:
            List of health check results
        """
        checks = []

        # Check database connectivity
        checks.append(self._check_database())

        # Check adapter availability
        checks.append(self._check_adapters())

        # Check disk space
        checks.append(self._check_disk_space())

        # Check configuration
        checks.append(self._check_configuration())

        # Check run artifacts integrity
        checks.append(self._check_artifacts_integrity())

        # Publish health check event
        healthy_count = sum(1 for c in checks if c.status == "healthy")
        total_count = len(checks)

        # Journal: Health check
        if self.run_path:
            append_event(
                self.run_path,
                "HEALTH_CHECK",
                {
                    "healthy": healthy_count,
                    "total": total_count,
                },
                trace_id=self.trace_id,
            )

        if healthy_count < total_count:
            # Publish event
            self.event_bus.publish(
                Events.HEALTH_DEGRADED,
                {
                    "healthy": healthy_count,
                    "total": total_count,
                    "checks": [c.__dict__ for c in checks],
                },
            )

            # Trigger self-healing
            healer = SelfHealHandler(self)
            recovery_report = healer.handle_degradation(checks)

            # Publish recovery event
            self.event_bus.publish(
                Events.HEALTH_RECOVERED if recovery_report["success"] else Events.HEALTH_RECOVERY_FAILED,
                recovery_report,
            )
        else:
            self.event_bus.publish(
                Events.HEALTH_CHECK,
                {
                    "healthy": healthy_count,
                    "total": total_count,
                },
            )

        return checks

    def _check_database(self) -> HealthCheck:
        """Check database connectivity."""
        try:
            from ..control_plane import ControlPlaneDB

            db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
            db = ControlPlaneDB(str(db_path))

            # Try to initialize (will create if not exists)
            import asyncio

            asyncio.run(db.initialize())

            return HealthCheck(
                name="database",
                status="healthy",
                message="Database connection successful",
            )
        except Exception as e:
            return HealthCheck(
                name="database",
                status="unhealthy",
                message=f"Database connection failed: {e!s}",
            )

    def _check_adapters(self) -> HealthCheck:
        """Check adapter availability."""
        from ..adapters.registry import get_registry

        registry = get_registry()
        adapters = registry.list_adapters()

        enabled_adapters = [a for a in adapters if a["enabled"]]
        available_adapters = [a for a in enabled_adapters if a["available"]]

        if len(enabled_adapters) == 0:
            return HealthCheck(
                name="adapters",
                status="healthy",
                message="No adapters enabled (expected for minimal setup)",
            )

        if len(available_adapters) < len(enabled_adapters):
            missing = [a["name"] for a in enabled_adapters if not a["available"]]
            return HealthCheck(
                name="adapters",
                status="degraded",
                message=f"Some adapters unavailable: {', '.join(missing)}",
                details={"missing": missing},
            )

        return HealthCheck(
            name="adapters",
            status="healthy",
            message=f"All {len(available_adapters)} enabled adapters available",
        )

    def _check_disk_space(self) -> HealthCheck:
        """Check disk space."""
        try:
            import shutil

            total, used, free = shutil.disk_usage(PROJECT_ROOT)

            # Check if free space is less than 1GB
            free_gb = free / (1024**3)
            if free_gb < 1.0:
                return HealthCheck(
                    name="disk_space",
                    status="unhealthy",
                    message=f"Low disk space: {free_gb:.2f} GB free",
                    details={"free_gb": free_gb},
                )
            elif free_gb < 5.0:
                return HealthCheck(
                    name="disk_space",
                    status="degraded",
                    message=f"Disk space getting low: {free_gb:.2f} GB free",
                    details={"free_gb": free_gb},
                )

            return HealthCheck(
                name="disk_space",
                status="healthy",
                message=f"Disk space adequate: {free_gb:.2f} GB free",
                details={"free_gb": free_gb},
            )
        except Exception as e:
            return HealthCheck(
                name="disk_space",
                status="degraded",
                message=f"Could not check disk space: {e!s}",
            )

    def _check_configuration(self) -> HealthCheck:
        """Check configuration validity."""
        try:
            policy = self.policy.get_policy()

            # Check required sections
            required_sections = ["sandbox", "exec", "paths", "gates"]
            missing = [s for s in required_sections if s not in policy]

            if missing:
                return HealthCheck(
                    name="configuration",
                    status="degraded",
                    message=f"Missing policy sections: {', '.join(missing)}",
                    details={"missing": missing},
                )

            return HealthCheck(
                name="configuration",
                status="healthy",
                message="Configuration valid",
            )
        except Exception as e:
            return HealthCheck(
                name="configuration",
                status="unhealthy",
                message=f"Configuration check failed: {e!s}",
            )

    def _check_artifacts_integrity(self) -> HealthCheck:
        """Check run artifacts integrity."""
        try:
            workspaces_dir = PROJECT_ROOT / "workspaces"
            if not workspaces_dir.exists():
                return HealthCheck(
                    name="artifacts",
                    status="healthy",
                    message="No workspaces directory (expected for new setup)",
                )

            # Check for recent runs with missing artifacts
            issues = []
            for task_dir in workspaces_dir.iterdir():
                if not task_dir.is_dir():
                    continue

                runs_dir = task_dir / "runs"
                if not runs_dir.exists():
                    continue

                for run_dir in runs_dir.iterdir():
                    if not run_dir.is_dir():
                        continue

                    artifacts_dir = run_dir / "artifacts"
                    if not artifacts_dir.exists():
                        issues.append(f"{task_dir.name}/{run_dir.name}: missing artifacts/")
                        continue

                    # Check for required artifacts (if run is completed)
                    journal_dir = run_dir / "journal"
                    if journal_dir.exists():
                        events_file = journal_dir / "events.jsonl"
                        if events_file.exists():
                            # Check if run has completion event
                            try:
                                events = events_file.read_text(encoding="utf-8").strip().split("\n")
                                if events:
                                    last_event = json.loads(events[-1])
                                    if last_event.get("event_type") in ["RUN_COMPLETED", "RUN_FAILED"]:
                                        # Check for required artifacts
                                        required = ["gate_report.json"]
                                        missing_artifacts = [
                                            a for a in required if not (artifacts_dir / a).exists()
                                        ]
                                        if missing_artifacts:
                                            issues.append(
                                                f"{task_dir.name}/{run_dir.name}: missing {', '.join(missing_artifacts)}"
                                            )
                            except Exception:
                                pass  # Skip if can't parse events

            if issues:
                return HealthCheck(
                    name="artifacts",
                    status="degraded",
                    message=f"Found {len(issues)} artifact integrity issues",
                    details={"issues": issues[:10]},  # Limit to 10
                )

            return HealthCheck(
                name="artifacts",
                status="healthy",
                message="Artifact integrity check passed",
            )
        except Exception as e:
            return HealthCheck(
                name="artifacts",
                status="degraded",
                message=f"Artifact check failed: {e!s}",
            )

    def generate_report(self, checks: list[HealthCheck]) -> dict[str, Any]:
        """
        Generate health report.

        Args:
            checks: List of health check results

        Returns:
            Health report dictionary
        """
        healthy = sum(1 for c in checks if c.status == "healthy")
        degraded = sum(1 for c in checks if c.status == "degraded")
        unhealthy = sum(1 for c in checks if c.status == "unhealthy")

        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "healthy": healthy,
                "degraded": degraded,
                "unhealthy": unhealthy,
                "total": len(checks),
            },
            "checks": [c.__dict__ for c in checks],
        }


