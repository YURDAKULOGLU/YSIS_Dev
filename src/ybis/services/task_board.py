"""
Task Board Manager - Task organization and self-healing.

Manages tasks, tracks status, and provides self-healing capabilities.
"""

from datetime import datetime
from typing import Any

from ..control_plane import ControlPlaneDB
from ..services.policy import get_policy_provider


class TaskBoard:
    """
    Task Board Manager - Organizes and manages tasks.

    Provides:
    - Task status tracking
    - Self-healing (auto-retry failed tasks)
    - Task prioritization
    - Task grouping
    """

    def __init__(self):
        """Initialize task board."""
        self.db = ControlPlaneDB()
        self.policy = get_policy_provider()

    async def get_tasks(
        self,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Get tasks from board.

        Args:
            status: Filter by status (optional)
            limit: Maximum number of tasks to return
            offset: Offset for pagination

        Returns:
            List of task dictionaries
        """
        await self.db.initialize()

        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        async with self.db.get_connection() as conn:
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()

            tasks = []
            for row in rows:
                tasks.append(dict(row))

            return tasks

    async def get_task_by_id(self, task_id: str) -> dict[str, Any] | None:
        """Get task by ID."""
        await self.db.initialize()

        async with self.db.get_connection() as conn:
            cursor = await conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = await cursor.fetchone()

            if row:
                return dict(row)
            return None

    async def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status."""
        await self.db.initialize()

        async with self.db.get_connection() as conn:
            await conn.execute(
                "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
                (status, datetime.now().isoformat(), task_id),
            )
            await conn.commit()
            return True

    async def create_task(self, objective: str, metadata: dict[str, Any] | None = None) -> str:
        """
        Create a new task.

        Args:
            objective: Task objective
            metadata: Optional metadata

        Returns:
            Task ID
        """
        await self.db.initialize()

        import uuid

        task_id = f"TASK-{uuid.uuid4().hex[:8].upper()}"

        async with self.db.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO tasks (id, objective, status, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    objective,
                    "PENDING",
                    json.dumps(metadata or {}),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )
            await conn.commit()

        return task_id

    async def self_heal(self) -> list[dict[str, Any]]:
        """
        Self-healing: Auto-retry failed tasks.

        Returns:
            List of tasks that were retried
        """
        await self.db.initialize()

        # Get failed tasks
        failed_tasks = await self.get_tasks(status="FAILED", limit=50)

        healed = []

        for task in failed_tasks:
            # Check retry count
            metadata = json.loads(task.get("metadata", "{}"))
            retry_count = metadata.get("retry_count", 0)
            max_retries = self.policy.get_policy().get("gates", {}).get("max_retries", 3)

            if retry_count < max_retries:
                # Reset task to PENDING for retry
                await self.update_task_status(task["id"], "PENDING")

                # Update retry count
                metadata["retry_count"] = retry_count + 1
                metadata["last_retry_at"] = datetime.now().isoformat()

                async with self.db.get_connection() as conn:
                    await conn.execute(
                        "UPDATE tasks SET metadata = ? WHERE id = ?",
                        (json.dumps(metadata), task["id"]),
                    )
                    await conn.commit()

                healed.append(task)

        return healed


# Global task board instance
_task_board: TaskBoard | None = None


def get_task_board() -> TaskBoard:
    """Get global task board instance."""
    global _task_board
    if _task_board is None:
        _task_board = TaskBoard()
    return _task_board


