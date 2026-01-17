"""
Reflection Engine - Analyzes system state and identifies improvement opportunities.

This is the core of proactive self-improvement - it reflects on:
- Recent run metrics
- Error patterns
- Code quality
- Performance metrics
- System health
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

from ..constants import PROJECT_ROOT
from ..control_plane import ControlPlaneDB
from ..syscalls.journal import append_event
from .error_knowledge_base import ErrorKnowledgeBase
from .health_monitor import HealthMonitor


class ReflectionEngine:
    """
    Reflection Engine - Proactively identifies improvement opportunities.

    Unlike reactive loops that respond to failures, this engine:
    - Analyzes metrics and patterns
    - Identifies opportunities before they become problems
    - Prioritizes improvements based on impact
    """

    def __init__(self, project_root: Path | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize reflection engine.

        Args:
            project_root: Project root directory
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.project_root = project_root or PROJECT_ROOT
        self.run_path = run_path
        self.trace_id = trace_id
        self.error_kb = ErrorKnowledgeBase(run_path=run_path, trace_id=trace_id)
        self.health_monitor = HealthMonitor(run_path=run_path, trace_id=trace_id)

    def reflect(self) -> dict[str, Any]:
        """
        Reflect on system state and generate reflection report.

        Returns:
            Reflection report with issues, opportunities, and metrics
        """
        # Journal: Reflection start
        if self.run_path:
            append_event(
                self.run_path,
                "REFLECTION_START",
                {},
                trace_id=self.trace_id,
            )

        start_time = time.time()
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "system_health": self._assess_system_health(),
            "recent_metrics": self._collect_recent_metrics(),
            "error_patterns": self._analyze_error_patterns(),
            "code_quality": self._assess_code_quality(),
            "performance_metrics": self._collect_performance_metrics(),
            "issues_identified": [],
            "opportunities_identified": [],
            "priority_scores": {},
        }

        # Identify issues
        reflection["issues_identified"] = self._identify_issues(reflection)

        # Identify opportunities
        reflection["opportunities_identified"] = self._identify_opportunities(reflection)

        # Calculate priority scores
        reflection["priority_scores"] = self._calculate_priority_scores(reflection)

        elapsed_ms = (time.time() - start_time) * 1000

        # Journal: Reflection complete
        if self.run_path:
            append_event(
                self.run_path,
                "REFLECTION_COMPLETE",
                {
                    "issues_count": len(reflection["issues_identified"]),
                    "opportunities_count": len(reflection["opportunities_identified"]),
                    "duration_ms": round(elapsed_ms, 2),
                },
                trace_id=self.trace_id,
            )

        return reflection

    def _assess_system_health(self) -> dict[str, Any]:
        """Assess overall system health."""
        try:
            checks = self.health_monitor.run_all_checks()
            healthy = sum(1 for c in checks if c.status == "healthy")
            total = len(checks)
            score = healthy / total if total > 0 else 0.0
            status = "healthy" if healthy == total else "degraded" if healthy > 0 else "unhealthy"

            # Journal: Health check
            if self.run_path:
                append_event(
                    self.run_path,
                    "REFLECTION_HEALTH_CHECK",
                    {
                        "score": score,
                        "status": status,
                    },
                    trace_id=self.trace_id,
                )

            return {
                "score": score,
                "healthy_checks": healthy,
                "total_checks": total,
                "status": status,
            }
        except Exception:
            return {"score": 0.5, "status": "unknown"}

    def _collect_recent_metrics(self, days: int = 7) -> dict[str, Any]:
        """
        Collect metrics from recent runs.

        Handles async safely by checking for running event loop.
        Uses sync database access if async is not available.
        """
        try:
            db_path = self.project_root / "platform_data" / "control_plane.db"
            if not db_path.exists():
                return {"total_runs": 0, "success_rate": 0.0, "failure_rate": 0.0}

            db = ControlPlaneDB(str(db_path))

            import asyncio
            import sqlite3

            # Try async first
            try:
                loop = asyncio.get_running_loop()
                # If loop is running, try to use sync database access
                # ControlPlaneDB might have sync methods, but if not, use direct SQLite
                try:
                    # Try direct SQLite access for metrics
                    conn = sqlite3.connect(str(db_path))
                    cursor = conn.cursor()

                    # Get recent runs (last 50)
                    cursor.execute("""
                        SELECT status FROM runs
                        ORDER BY created_at DESC
                        LIMIT 50
                    """)
                    rows = cursor.fetchall()
                    conn.close()

                    if not rows:
                        return {"total_runs": 0, "success_rate": 0.0, "failure_rate": 0.0}

                    successful = sum(1 for r in rows if r[0] == "completed")
                    failed = sum(1 for r in rows if r[0] == "failed")

                    metrics = {
                        "total_runs": len(rows),
                        "success_rate": successful / len(rows) if rows else 0.0,
                        "failure_rate": failed / len(rows) if rows else 0.0,
                        "successful_runs": successful,
                        "failed_runs": failed,
                    }

                    # Journal: Metrics collected
                    if self.run_path:
                        append_event(
                            self.run_path,
                            "REFLECTION_METRICS_COLLECTED",
                            {
                                "total_runs": metrics["total_runs"],
                                "success_rate": metrics["success_rate"],
                                "failure_rate": metrics["failure_rate"],
                            },
                            trace_id=self.trace_id,
                        )

                    return metrics
                except Exception:
                    # If SQLite access fails, return defaults
                    return {"total_runs": 0, "success_rate": 0.0, "failure_rate": 0.0}
            except RuntimeError:
                # No running loop, we can use asyncio.run()
                pass

            # Use async if no loop is running
            recent_runs = asyncio.run(db.get_recent_runs(limit=50))

            if not recent_runs:
                return {
                    "total_runs": 0,
                    "success_rate": 0.0,
                    "failure_rate": 0.0,
                    "avg_execution_time": 0.0,
                }

            successful = sum(1 for r in recent_runs if r.status == "completed")
            failed = sum(1 for r in recent_runs if r.status == "failed")

            metrics = {
                "total_runs": len(recent_runs),
                "success_rate": successful / len(recent_runs),
                "failure_rate": failed / len(recent_runs),
                "successful_runs": successful,
                "failed_runs": failed,
            }

            # Journal: Metrics collected
            if self.run_path:
                append_event(
                    self.run_path,
                    "REFLECTION_METRICS_COLLECTED",
                    {
                        "total_runs": metrics["total_runs"],
                        "success_rate": metrics["success_rate"],
                        "failure_rate": metrics["failure_rate"],
                    },
                    trace_id=self.trace_id,
                )

            return metrics
        except Exception:
            return {"total_runs": 0, "success_rate": 0.0, "failure_rate": 0.0}

    def _analyze_error_patterns(self) -> dict[str, Any]:
        """Analyze error patterns from Error Knowledge Base."""
        try:
            stats = self.error_kb.get_statistics()
            patterns = self.error_kb.get_error_patterns(min_occurrences=2)

            # Deduplicate patterns by error_type and occurrences
            seen_patterns = {}
            unique_patterns = []
            for p in patterns:
                key = (p.error_type, p.occurrence_count)
                if key not in seen_patterns:
                    seen_patterns[key] = True
                    unique_patterns.append(p)

            top_patterns = [
                {
                    "error_type": p.error_type,
                    "occurrences": p.occurrence_count,
                    "affected_tasks": len(p.affected_tasks),
                }
                for p in unique_patterns[:5]
            ]

            result = {
                "total_errors": stats.get("total_errors", 0),
                "error_types": stats.get("error_types", {}),
                "patterns_detected": len(unique_patterns),
                "top_patterns": top_patterns,
            }

            # Journal: Patterns analyzed
            if self.run_path:
                top_error_type = top_patterns[0].get("error_type", "") if top_patterns else ""
                append_event(
                    self.run_path,
                    "REFLECTION_PATTERNS_ANALYZED",
                    {
                        "patterns_count": len(unique_patterns),
                        "top_error_type": top_error_type,
                    },
                    trace_id=self.trace_id,
                )

            return result
        except Exception:
            return {"total_errors": 0, "patterns_detected": 0}

    def _assess_code_quality(self) -> dict[str, Any]:
        """Assess code quality metrics."""
        # Check for common code quality issues
        issues = []

        # Check for TODO/FIXME comments (potential technical debt)
        try:
            todo_count = 0
            for py_file in (self.project_root / "src").rglob("*.py"):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    todo_count += content.count("TODO") + content.count("FIXME")
                except Exception:
                    continue

            if todo_count > 50:
                issues.append({
                    "type": "technical_debt",
                    "severity": "medium",
                    "description": f"High number of TODO/FIXME comments ({todo_count})",
                })
        except Exception:
            pass

        return {
            "issues": issues,
            "todo_count": todo_count if 'todo_count' in locals() else 0,
        }

    def _collect_performance_metrics(self) -> dict[str, Any]:
        """Collect performance-related metrics."""
        # This would ideally collect timing data from runs
        # For now, return placeholder
        return {
            "avg_verification_time": 0.0,
            "avg_gate_time": 0.0,
            "avg_execution_time": 0.0,
        }

    def _identify_issues(self, reflection: dict[str, Any]) -> list[dict[str, Any]]:
        """Identify specific issues from reflection data."""
        issues = []

        # Check system health
        health = reflection.get("system_health", {})
        if health.get("status") != "healthy":
            issues.append({
                "type": "system_health",
                "severity": "high" if health.get("status") == "unhealthy" else "medium",
                "description": f"System health is {health.get('status')}",
                "score": health.get("score", 0.0),
            })

        # Check failure rate
        metrics = reflection.get("recent_metrics", {})
        failure_rate = metrics.get("failure_rate", 0.0)
        if failure_rate > 0.2:  # More than 20% failure rate
            issues.append({
                "type": "high_failure_rate",
                "severity": "high",
                "description": f"Failure rate is {failure_rate:.1%} (threshold: 20%)",
                "failure_rate": failure_rate,
            })

        # Check error patterns
        error_patterns = reflection.get("error_patterns", {})
        if error_patterns.get("patterns_detected", 0) > 5:
            issues.append({
                "type": "recurring_errors",
                "severity": "medium",
                "description": f"{error_patterns.get('patterns_detected')} recurring error patterns detected",
            })

        return issues

    def _identify_opportunities(self, reflection: dict[str, Any]) -> list[dict[str, Any]]:
        """Identify improvement opportunities."""
        opportunities = []

        # Opportunity: Improve success rate
        metrics = reflection.get("recent_metrics", {})
        success_rate = metrics.get("success_rate", 0.0)
        if success_rate < 0.9:  # Less than 90% success rate
            opportunities.append({
                "area": "reliability",
                "priority": "high",
                "description": f"Success rate is {success_rate:.1%} - target: 90%",
                "impact": "high",
                "effort": "medium",
            })

        # Opportunity: Reduce error patterns
        error_patterns = reflection.get("error_patterns", {})
        if error_patterns.get("patterns_detected", 0) > 0:
            opportunities.append({
                "area": "error_handling",
                "priority": "medium",
                "description": f"Address {error_patterns.get('patterns_detected')} recurring error patterns",
                "impact": "medium",
                "effort": "low",
            })

        # Opportunity: Improve code quality
        code_quality = reflection.get("code_quality", {})
        if code_quality.get("todo_count", 0) > 50:
            opportunities.append({
                "area": "code_quality",
                "priority": "low",
                "description": f"Address {code_quality.get('todo_count')} TODO/FIXME comments",
                "impact": "low",
                "effort": "medium",
            })

        return opportunities

    def _calculate_priority_scores(self, reflection: dict[str, Any]) -> dict[str, Any]:
        """Calculate priority scores for improvements."""
        issues = reflection.get("issues_identified", [])
        opportunities = reflection.get("opportunities_identified", [])

        high_priority = len([i for i in issues if i.get("severity") == "high"])
        medium_priority = len([i for i in issues if i.get("severity") == "medium"])
        low_priority = len([i for i in issues if i.get("severity") == "low"])

        return {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority,
            "total_issues": len(issues),
            "total_opportunities": len(opportunities),
        }

