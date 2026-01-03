"""
TaskBoardManager - SQLite-based Task Persistence.

Can sync TASK_BOARD.md for visibility.
"""

from typing import Optional, Dict, Any, List
from src.agentic.infrastructure.db import TaskDatabase
from src.agentic.core.utils.logging_utils import log_event

class TaskBoardManager:
    """Manages Task Board Persistence via SQLite."""

    def __init__(self, db_path: str = None):
        from src.agentic.core.config import DATA_DIR, PROJECT_ROOT

        # Determine paths
        self.db_path = db_path or str(DATA_DIR / "tasks.db")
        self.db = TaskDatabase(self.db_path)
        self._initialized = False

    async def _ensure_db(self):
        """Lazy initialization of the database."""
        if not self._initialized:
            await self.db.initialize()
            self._initialized = True

    async def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get next available task (Priority to IN_PROGRESS, then BACKLOG)."""
        await self._ensure_db()
        tasks = await self.db.get_all_tasks()

        # Sort by status priority
        in_prog = [t for t in tasks if t['status'] == "IN_PROGRESS"]
        if in_prog:
            return in_prog[0]

        backlog = [t for t in tasks if t['status'] == "BACKLOG"]
        if backlog:
            return backlog[0]

        return None

    async def claim_next_task(self, worker_id: str = "default-worker") -> Optional[Dict[str, Any]]:
        """
        ATOMIC: Claim next available BACKLOG task.
        Race-condition safe for multi-agent systems (Claude + Gemini).
        """
        await self._ensure_db()
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row

            # First check for existing IN_PROGRESS for this worker
            async with conn.execute(
                "SELECT * FROM tasks WHERE status='IN_PROGRESS' AND assignee=? LIMIT 1",
                (worker_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)

            # Atomic claim: Single SQL transaction
            async with conn.execute(
                """
                UPDATE tasks
                SET status='IN_PROGRESS', assignee=?
                WHERE id = (
                    SELECT id FROM tasks
                    WHERE status='BACKLOG'
                    ORDER BY
                        CASE priority
                            WHEN 'HIGH' THEN 1
                            WHEN 'MEDIUM' THEN 2
                            ELSE 3
                        END,
                        id
                    LIMIT 1
                )
                RETURNING *
                """,
                (worker_id,)
            ) as cursor:
                row = await cursor.fetchone()

            # Commit after cursor is closed
            await conn.commit()
            return dict(row) if row else None

    async def create_task(self, title: str, description: str, priority: str = "MEDIUM") -> str:
        """Create new task in database."""
        await self._ensure_db()
        import random
        task_id = f"TASK-New-{random.randint(100,999)}"

        new_task = {
            "id": task_id,
            "goal": title,
            "details": description,
            "assignee": "Unassigned",
            "priority": priority,
            "status": "BACKLOG"
        }
        await self.db.add_task(new_task)
        return task_id

    async def update_task_status(self, task_id: str, status: str, metadata: Dict[str, Any]) -> None:
        """Update task status in database."""
        await self._ensure_db()
        status = status.upper()
        final_status = "UNKNOWN"

        if status in ["DONE", "COMPLETED"]:
            final_status = "SUCCESS"
            status = "DONE"
        elif status == "FAILED":
            final_status = "FAILED"
            status = "DONE"
        elif status == "IN_PROGRESS":
            status = "IN_PROGRESS"

        await self.db.update_task_status(task_id, status, final_status)

    async def _read_db(self) -> Dict[str, Any]:
        """Backward compatibility for worker.py loop."""
        await self._ensure_db()
        tasks = await self.db.get_all_tasks()
        return {
            "backlog": [t for t in tasks if t['status'] == "BACKLOG"],
            "in_progress": [t for t in tasks if t['status'] == "IN_PROGRESS"],
            "done": [t for t in tasks if t['status'] == "DONE"]
        }

    def _sync_to_markdown(self, data: Dict[str, Any]):
        """Generate TASK_BOARD.md from data."""
        lines = [
            "# YBIS_Dev Task Board (DB Synced)",
            "",
            "**Protocol:** Auto-Generated from `tasks.db`",
            f"**Last Update:** {self._get_timestamp()}",
            "",
            "---",
            "",
            "## [NEW] (Backlog)",
            ""
        ]

        # Backlog
        for task in data.get("backlog", []):
            lines.append(f"- [ ] **{task['id']}:** {task['goal']}")
            lines.append(f"  - **Goal:** {task.get('details', '')}")
            lines.append(f"  - **Assignee:** {task.get('assignee', 'Unassigned')}")
            lines.append(f"  - **Priority:** {task.get('priority', 'MEDIUM')}")

        lines.append("")
        lines.append("## [IN PROGRESS]")
        lines.append("")

        # In Progress
        for task in data.get("in_progress", []):
            lines.append(f"- [ ] **{task['id']}:** {task['goal']}")
            lines.append(f"  - **Goal:** {task.get('details', '')}")
            if "scope" in task:
                 lines.append(f"  - **Scope:** {task['scope']}")
            lines.append(f"  - **Assignee:** {task.get('assignee', 'Unassigned')}")
            lines.append(f"  - **Priority:** {task.get('priority', 'HIGH')}")
            lines.append(f"  - **Status:** IN PROGRESS")

        lines.append("")
        lines.append("## [DONE]")
        lines.append("")

        # Done
        for task in data.get("done", []):
             lines.append(f"- [x] **{task['id']}:** {task['goal']}")

        lines.append("")
        lines.append("---")

        try:
            with open(self.md_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
        except Exception as e:
            log_event(f"Error syncing MD: {e}", component="task_board", level="warning")

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    async def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get first task from in_progress."""
        data = await self._read_db()
        in_progress = data.get("in_progress", [])

        if not in_progress:
            return None

        task = in_progress[0]
        return {
            "id": task["id"],
            "description": task["goal"], # Mapping goal -> description for orchestrator compatibility
            "status": "IN PROGRESS"
        }

    async def create_task(self, title: str, description: str, priority: str = "MEDIUM") -> str:
        """Create new task in Backlog."""
        data = await self._read_db()

        # Generate ID (Simple increment or random)
        import random
        task_id = f"TASK-New-{random.randint(100,999)}"

        new_task = {
            "id": task_id,
            "goal": title,
            "details": description,
            "assignee": "Unassigned",
            "priority": priority,
            "status": "BACKLOG"
        }
        await self.db.add_task(new_task)
        return task_id

    async def update_task_status(self, task_id: str, status: str, metadata: Dict[str, Any]) -> None:
        """Update task status in database."""
        await self._ensure_db()
        status = status.upper()
        final_status = "UNKNOWN"

        if status in ["DONE", "COMPLETED"]:
            final_status = "SUCCESS"
            status = "DONE"
        elif status == "FAILED":
            final_status = "FAILED"
            status = "DONE"

        await self.db.update_task_status(task_id, status, final_status)
