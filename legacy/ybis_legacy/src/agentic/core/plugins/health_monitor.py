"""
HealthMonitor - System health checks with auto-remediation task creation.

Runs at startup and periodically to detect system issues.
Creates tasks automatically when problems are found.
"""

import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from src.agentic.core.config import CHROMA_DB_PATH, PROJECT_ROOT, TASKS_DB_PATH
from src.agentic.core.utils.logging_utils import log_event


@dataclass
class HealthIssue:
    """Represents a detected health issue."""
    category: str  # RAG, EXECUTION, ENCODING, CONFIG
    severity: str  # CRITICAL, WARNING, INFO
    message: str
    auto_task: dict[str, str] | None = None  # Task to create if auto-remediation enabled
    detected_at: str = None

    def __post_init__(self):
        if not self.detected_at:
            self.detected_at = datetime.now().isoformat()


class HealthMonitor:
    """
    System health monitor with auto-remediation.

    Checks:
    - RAG index health (empty, stale)
    - Execution metrics (timeouts, failures)
    - Error patterns (encoding, repeated failures)
    - Configuration issues
    """

    def __init__(self, auto_create_tasks: bool = False):
        self.auto_create_tasks = auto_create_tasks
        self.issues: list[HealthIssue] = []
        self.metrics: dict[str, Any] = {}

    def run_all_checks(self) -> list[HealthIssue]:
        """Run all health checks and return issues found."""
        self.issues = []

        self._check_rag_health()
        self._check_recent_task_metrics()
        self._check_encoding_errors()
        self._check_config_issues()
        self._check_and_release_stale_tasks()

        # Auto-create remediation tasks if enabled
        if self.auto_create_tasks:
            self._create_remediation_tasks()

        return self.issues

    def _check_rag_health(self):
        """Check RAG/ChromaDB index health."""
        try:
            # Check if ChromaDB directory exists and has data
            chroma_path = Path(CHROMA_DB_PATH)

            if not chroma_path.exists():
                self.issues.append(HealthIssue(
                    category="RAG",
                    severity="WARNING",
                    message="ChromaDB directory does not exist",
                    auto_task={
                        "goal": "Initialize RAG index",
                        "details": "Create ChromaDB and index src/. Call local_rag.index_directory('src/')."
                    }
                ))
                return

            # Try to get document count
            try:
                from src.agentic.tools.local_rag import get_local_rag
                rag = get_local_rag()
                doc_count = rag.document_count()
                self.metrics["rag_doc_count"] = doc_count

                if doc_count == 0:
                    self.issues.append(HealthIssue(
                        category="RAG",
                        severity="WARNING",
                        message="RAG index is empty (0 documents)",
                        auto_task={
                            "goal": "Populate RAG index with codebase",
                            "details": "Index src/ into ChromaDB. Use local_rag.index_directory('src/')."
                        }
                    ))
                elif doc_count < 50:
                    self.issues.append(HealthIssue(
                        category="RAG",
                        severity="INFO",
                        message=f"RAG index has only {doc_count} documents - may need re-indexing"
                    ))

            except ImportError:
                self.issues.append(HealthIssue(
                    category="RAG",
                    severity="WARNING",
                    message="LocalRAG module not available"
                ))

        except Exception as e:
            self.issues.append(HealthIssue(
                category="RAG",
                severity="WARNING",
                message=f"RAG health check failed: {e}"
            ))

    def _check_recent_task_metrics(self):
        """Analyze recent task execution metrics."""
        try:
            if not TASKS_DB_PATH.exists():
                return

            conn = sqlite3.connect(str(TASKS_DB_PATH))
            cursor = conn.cursor()

            # Get recent failed tasks
            cursor.execute("""
                SELECT id, goal, final_status
                FROM tasks
                WHERE status IN ('FAILED', 'COMPLETED')
                AND final_status IS NOT NULL
                ORDER BY updated_at DESC
                LIMIT 20
            """)
            recent_tasks = cursor.fetchall()

            failed_count = sum(1 for t in recent_tasks if t[2] and 'FAIL' in t[2].upper())
            total_count = len(recent_tasks)

            self.metrics["recent_tasks_total"] = total_count
            self.metrics["recent_tasks_failed"] = failed_count

            if total_count > 5 and failed_count / total_count > 0.5:
                self.issues.append(HealthIssue(
                    category="EXECUTION",
                    severity="CRITICAL",
                    message=f"High failure rate: {failed_count}/{total_count} recent tasks failed",
                    auto_task={
                        "goal": "Investigate high task failure rate",
                        "details": f"Analyze {failed_count}/{total_count} failures. Check logs."
                    }
                ))

            # Check for repeated SEARCH/REPLACE failures
            cursor.execute("""
                SELECT id, final_status
                FROM tasks
                WHERE final_status LIKE '%SEARCH%' OR final_status LIKE '%REPLACE%'
                ORDER BY updated_at DESC
                LIMIT 10
            """)
            search_fails = cursor.fetchall()

            if len(search_fails) >= 3:
                self.issues.append(HealthIssue(
                    category="EXECUTION",
                    severity="WARNING",
                    message=f"Repeated SEARCH/REPLACE failures detected ({len(search_fails)} occurrences)",
                    auto_task={
                        "goal": "Enable whole-file-edits fallback for Aider",
                        "details": "Add --whole-file-edits fallback when SEARCH/REPLACE fails 2x."
                    }
                ))

            conn.close()

        except Exception as e:
            self.issues.append(HealthIssue(
                category="EXECUTION",
                severity="INFO",
                message=f"Task metrics check failed: {e}"
            ))

    def _check_encoding_errors(self):
        """Check for encoding errors in recent logs."""
        try:
            # Look for charmap codec errors in recent workspace logs
            workspaces_path = PROJECT_ROOT / "workspaces" / "active"
            if not workspaces_path.exists():
                return

            encoding_errors = 0
            for task_dir in workspaces_path.iterdir():
                if not task_dir.is_dir():
                    continue

                stderr_log = task_dir / "artifacts" / "logs" / "aider_stderr.log"
                if stderr_log.exists():
                    try:
                        content = stderr_log.read_text(encoding='utf-8', errors='ignore')
                        if 'charmap' in content.lower() or 'codec' in content.lower():
                            encoding_errors += 1
                    except Exception:
                        pass

            self.metrics["encoding_errors_count"] = encoding_errors

            if encoding_errors >= 2:
                self.issues.append(HealthIssue(
                    category="ENCODING",
                    severity="WARNING",
                    message=f"Encoding errors detected in {encoding_errors} task logs",
                    auto_task={
                        "goal": "Fix CrewAI emoji encoding issues",
                        "details": "Sanitize CrewAI output. Add ascii filter in planning_crew.py."
                    }
                ))

        except Exception:
            pass  # Non-critical check

    def _check_config_issues(self):
        """Check for configuration issues."""
        try:
            from src.agentic.core.config import AIDER_BIN

            # Check if Aider is configured
            if not AIDER_BIN:
                self.issues.append(HealthIssue(
                    category="CONFIG",
                    severity="INFO",
                    message="AIDER_BIN not set - using system aider"
                ))

            # Check Ollama availability
            try:
                import httpx
                response = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    self.metrics["ollama_models"] = len(models)
                    if not any("qwen" in m.get("name", "").lower() for m in models):
                        self.issues.append(HealthIssue(
                            category="CONFIG",
                            severity="WARNING",
                            message="qwen2.5-coder model not found in Ollama"
                        ))
            except Exception:
                self.issues.append(HealthIssue(
                    category="CONFIG",
                    severity="CRITICAL",
                    message="Ollama not responding at localhost:11434",
                    auto_task={
                        "goal": "Start Ollama service",
                        "details": "Ollama not running. Start with 'ollama serve'."
                    }
                ))

        except Exception:
            pass  # Config check is best-effort

    def _check_and_release_stale_tasks(self):
        """Check for and auto-release stale IN_PROGRESS tasks (self-healing)."""
        try:
            if not TASKS_DB_PATH.exists():
                return

            conn = sqlite3.connect(str(TASKS_DB_PATH))
            cursor = conn.cursor()

            # Find tasks stuck for more than 30 minutes
            from datetime import timedelta
            cutoff = (datetime.now() - timedelta(minutes=30)).isoformat()

            cursor.execute("""
                SELECT id FROM tasks
                WHERE status='IN_PROGRESS' AND updated_at < ?
            """, (cutoff,))
            stale_tasks = [row[0] for row in cursor.fetchall()]

            if stale_tasks:
                # Auto-release them
                cursor.execute("""
                    UPDATE tasks
                    SET status='BACKLOG', assignee=NULL
                    WHERE status='IN_PROGRESS' AND updated_at < ?
                """, (cutoff,))
                conn.commit()

                self.issues.append(HealthIssue(
                    category="EXECUTION",
                    severity="INFO",
                    message=f"Auto-released {len(stale_tasks)} stale tasks: {stale_tasks}"
                ))
                log_event(f"[SELF-HEAL] Released {len(stale_tasks)} stale tasks back to BACKLOG", component="health_monitor")

            conn.close()

        except Exception as e:
            log_event(f"Stale task check failed: {e}", component="health_monitor", level="warning")

    def _create_remediation_tasks(self):
        """Create tasks for issues that have auto_task defined."""
        if not TASKS_DB_PATH.exists():
            return

        try:
            conn = sqlite3.connect(str(TASKS_DB_PATH))
            cursor = conn.cursor()

            for issue in self.issues:
                if issue.auto_task and issue.severity in ("CRITICAL", "WARNING"):
                    task_id = f"HEALTH-{datetime.now().strftime('%Y%m%d%H%M%S')}-{issue.category}"

                    # Check if similar task already exists
                    cursor.execute(
                        "SELECT id FROM tasks WHERE goal LIKE ? AND status = 'BACKLOG'",
                        (f"%{issue.auto_task['goal'][:30]}%",)
                    )
                    if cursor.fetchone():
                        continue  # Similar task already exists

                    cursor.execute("""
                        INSERT INTO tasks (id, goal, details, status, priority)
                        VALUES (?, ?, ?, 'BACKLOG', ?)
                    """, (
                        task_id,
                        issue.auto_task["goal"],
                        issue.auto_task["details"],
                        "HIGH" if issue.severity == "CRITICAL" else "MEDIUM"
                    ))

                    log_event(f"Created remediation task: {task_id}", component="health_monitor")

            conn.commit()
            conn.close()

        except Exception as e:
            log_event(f"Failed to create remediation tasks: {e}", component="health_monitor", level="warning")

    def get_report(self) -> dict[str, Any]:
        """Get health report as dictionary."""
        return {
            "timestamp": datetime.now().isoformat(),
            "issues": [asdict(i) for i in self.issues],
            "metrics": self.metrics,
            "summary": {
                "critical": sum(1 for i in self.issues if i.severity == "CRITICAL"),
                "warning": sum(1 for i in self.issues if i.severity == "WARNING"),
                "info": sum(1 for i in self.issues if i.severity == "INFO")
            }
        }

    def print_report(self):
        """Print health report to console."""
        report = self.get_report()

        log_event("=" * 60, component="health_monitor")
        log_event("SYSTEM HEALTH REPORT", component="health_monitor")
        log_event("=" * 60, component="health_monitor")

        summary = report["summary"]
        log_event(f"Critical: {summary['critical']} | Warning: {summary['warning']} | Info: {summary['info']}", component="health_monitor")
        log_event("-" * 60, component="health_monitor")

        for issue in self.issues:
            icon = {"CRITICAL": "[!]", "WARNING": "[~]", "INFO": "[i]"}.get(issue.severity, "[?]")
            log_event(f"{icon} [{issue.category}] {issue.message}", component="health_monitor")
            if issue.auto_task:
                log_event(f"    -> Auto-task: {issue.auto_task['goal']}", component="health_monitor")

        if self.metrics:
            log_event("-" * 60, component="health_monitor")
            log_event("Metrics:", component="health_monitor")
            for k, v in self.metrics.items():
                log_event(f"  {k}: {v}", component="health_monitor")

        log_event("=" * 60, component="health_monitor")


def run_health_check(auto_create_tasks: bool = False) -> dict[str, Any]:
    """Convenience function to run health check."""
    monitor = HealthMonitor(auto_create_tasks=auto_create_tasks)
    monitor.run_all_checks()
    monitor.print_report()
    return monitor.get_report()


if __name__ == "__main__":
    import sys
    auto_create = "--auto-task" in sys.argv
    run_health_check(auto_create_tasks=auto_create)
