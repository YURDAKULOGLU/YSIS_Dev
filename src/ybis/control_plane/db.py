"""
Control Plane Database - SQLite persistence for coordination.

Handles tasks, runs, leases, and workers.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path

import aiosqlite

logger = logging.getLogger(__name__)

from ..contracts import Run, Task
from ..syscalls.journal import append_event


class ControlPlaneDB:
    """Control plane database operations."""

    def __init__(self, db_path: str | Path, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize control plane DB.

        Args:
            db_path: Path to SQLite database file
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.run_path = run_path
        self.trace_id = trace_id

    async def initialize(self) -> None:
        """
        Initialize database - create tables if they don't exist.

        Reads schema from schema.sql and executes it.
        """
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        async with aiosqlite.connect(self.db_path) as db:
            # Read and execute schema
            schema_sql = schema_path.read_text()
            await db.executescript(schema_sql)
            await self._ensure_columns(db)
            await db.commit()

    async def _ensure_columns(self, db: aiosqlite.Connection) -> None:
        """Ensure schema-compatible columns exist for existing databases."""
        await self._ensure_table_columns(
            db,
            table="tasks",
            columns={
                "protected": "INTEGER DEFAULT 0",
            },
        )
        await self._ensure_table_columns(
            db,
            table="runs",
            columns={
                "archived": "INTEGER DEFAULT 0",
                "archived_at": "TIMESTAMP",
                "retention_hold": "INTEGER DEFAULT 0",
            },
        )

    async def _ensure_table_columns(
        self, db: aiosqlite.Connection, table: str, columns: dict[str, str]
    ) -> None:
        """Add missing columns to a table without destructive migrations."""
        async with db.execute(f"PRAGMA table_info({table})") as cursor:
            existing = {row[1] async for row in cursor}

        for column, definition in columns.items():
            if column in existing:
                continue
            await db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    async def register_task(self, task: Task) -> None:
        """
        Register or update a task.

        Args:
            task: Task model to register
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO tasks
                (task_id, title, objective, status, priority, protected, schema_version, workspace_path, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    task.task_id,
                    task.title,
                    task.objective,
                    task.status,
                    task.priority,
                    1 if task.protected else 0,
                    task.schema_version,
                    task.workspace_path,
                ),
            )
            await db.commit()

            # Journal: Task created/updated
            if self.run_path:
                # Check if task exists
                async with db.execute("SELECT task_id FROM tasks WHERE task_id = ?", (task.task_id,)) as cursor:
                    exists = await cursor.fetchone()
                event_type = "DB_TASK_UPDATE" if exists else "DB_TASK_CREATE"
                append_event(
                    self.run_path,
                    event_type,
                    {
                        "task_id": task.task_id,
                        "title": task.title[:50] if task.title else "",
                    },
                    trace_id=self.trace_id,
                )

    async def register_run(self, run: Run) -> None:
        """
        Register a run (insert or update).

        Args:
            run: Run model to register
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Check if run exists
            async with db.execute(
                "SELECT run_id FROM runs WHERE run_id = ?",
                (run.run_id,),
            ) as cursor:
                exists = await cursor.fetchone()

            if exists:
                # Update existing run
                await db.execute(
                    """
                    UPDATE runs
                    SET status = ?, risk_level = ?, completed_at = ?
                    WHERE run_id = ?
                    """,
                    (
                        run.status,
                        run.risk_level,
                        run.completed_at.isoformat() if run.completed_at else None,
                        run.run_id,
                    ),
                )
            else:
                # Insert new run
                await db.execute(
                    """
                    INSERT INTO runs
                    (run_id, task_id, workflow, status, risk_level, run_path, schema_version, started_at, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run.run_id,
                        run.task_id,
                        run.workflow,
                        run.status,
                        run.risk_level,
                        str(run.run_path),
                        run.schema_version,
                        run.started_at.isoformat() if run.started_at else None,
                        run.completed_at.isoformat() if run.completed_at else None,
                    ),
                )
            await db.commit()

            # Journal: Run created/updated
            if self.run_path:
                event_type = "DB_RUN_UPDATE" if exists else "DB_RUN_CREATE"
                append_event(
                    self.run_path,
                    event_type,
                    {
                        "run_id": run.run_id,
                        "task_id": run.task_id,
                    },
                    trace_id=self.trace_id,
                )

            # Journal: Run created/updated
            if self.run_path:
                event_type = "DB_RUN_UPDATE" if exists else "DB_RUN_CREATE"
                append_event(
                    self.run_path,
                    event_type,
                    {
                        "run_id": run.run_id,
                        "task_id": run.task_id,
                    },
                    trace_id=self.trace_id,
                )

    async def get_task(self, task_id: str) -> Task | None:
        """
        Get task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task model or None if not found
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None

                # Convert row to Task model
                return Task(
                    task_id=row["task_id"],
                    title=row["title"],
                    objective=row["objective"],
                    status=row["status"],
                    priority=row["priority"],
                    protected=bool(row["protected"]) if "protected" in row.keys() else False,
                    schema_version=row["schema_version"],
                    workspace_path=row["workspace_path"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )

    async def get_run(self, run_id: str) -> Run | None:
        """
        Get run by ID.

        Args:
            run_id: Run identifier

        Returns:
            Run model or None if not found
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None

                # Convert row to Run model
                from datetime import datetime

                return Run(
                    run_id=row["run_id"],
                    task_id=row["task_id"],
                    workflow=row["workflow"],
                    status=row["status"],
                    risk_level=row["risk_level"],
                    run_path=row["run_path"],
                    schema_version=row["schema_version"],
                    started_at=datetime.fromisoformat(row["started_at"]) if row["started_at"] else None,
                    completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
                    created_at=row["created_at"],
                )

    async def claim_task(self, task_id: str, worker_id: str, duration_sec: int = 300) -> bool:
        """
        Atomically claim a task for a worker.

        Only succeeds if:
        - No active lease exists for the task, OR
        - Existing lease has expired

        Args:
            task_id: Task identifier
            worker_id: Worker identifier
            duration_sec: Lease duration in seconds

        Returns:
            True if claim successful, False otherwise
        """
        async with aiosqlite.connect(self.db_path) as db:
            expires_at = (datetime.now() + timedelta(seconds=duration_sec)).isoformat()
            lease_id = f"L-{task_id}-{worker_id}"

            # Check if lease exists and if it's expired
            async with db.execute(
                "SELECT expires_at, worker_id FROM leases WHERE task_id = ?", (task_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    existing_expires = datetime.fromisoformat(row[0])
                    existing_worker = row[1]
                    if existing_expires >= datetime.now():
                        # Active lease exists
                        return False
                    # Expired - delete old lease
                    await db.execute("DELETE FROM leases WHERE task_id = ?", (task_id,))

            # Insert new lease
            try:
                await db.execute(
                    """
                    INSERT INTO leases (lease_id, task_id, worker_id, ttl_seconds, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (lease_id, task_id, worker_id, duration_sec, expires_at),
                )
                await db.commit()
                return True
            except aiosqlite.IntegrityError:
                # Race condition - another worker claimed it
                return False

    async def release_lease(self, task_id: str, worker_id: str) -> None:
        """
        Release a lease for a task.

        Args:
            task_id: Task identifier
            worker_id: Worker identifier
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM leases WHERE task_id = ? AND worker_id = ?",
                (task_id, worker_id),
            )
            await db.commit()

    async def heartbeat(self, worker_id: str) -> None:
        """
        Update worker heartbeat timestamp.

        Args:
            worker_id: Worker identifier
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Insert or update worker heartbeat
            await db.execute(
                """
                INSERT INTO workers (worker_id, heartbeat_at)
                VALUES (?, datetime('now'))
                ON CONFLICT(worker_id) DO UPDATE SET
                    heartbeat_at = datetime('now')
                """,
                (worker_id,),
            )
            await db.commit()

    async def get_pending_tasks(self) -> list[Task]:
        """
        Get all pending tasks.

        Returns:
            List of pending tasks
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM tasks WHERE status = 'pending'") as cursor:
                rows = await cursor.fetchall()
                tasks = []
                for row in rows:
                    tasks.append(
                        Task(
                            task_id=row["task_id"],
                            title=row["title"],
                            objective=row["objective"],
                            status=row["status"],
                            priority=row["priority"],
                            schema_version=row["schema_version"],
                            workspace_path=row["workspace_path"],
                            created_at=row["created_at"],
                            updated_at=row["updated_at"],
                        )
                    )
                return tasks

    async def get_workers(self) -> list[dict]:
        """
        Get all active workers with their current task.

        Returns:
            List of worker dictionaries with id, status, current_task
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT w.worker_id, w.status, w.heartbeat_at, l.task_id
                FROM workers w
                LEFT JOIN leases l ON w.worker_id = l.worker_id
                WHERE w.status = 'active'
                ORDER BY w.heartbeat_at DESC
                """
            ) as cursor:
                rows = await cursor.fetchall()
                workers = []
                for row in rows:
                    workers.append({
                        "worker_id": row["worker_id"],
                        "status": "BUSY" if row["task_id"] else "IDLE",
                        "current_task": row["task_id"] or "None",
                        "heartbeat_at": row["heartbeat_at"],
                    })
                return workers

    async def get_blocked_tasks(self) -> list[Task]:
        """
        Get all blocked tasks.

        Returns:
            List of blocked tasks
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM tasks WHERE status = 'blocked'") as cursor:
                rows = await cursor.fetchall()
                tasks = []
                for row in rows:
                    tasks.append(
                        Task(
                            task_id=row["task_id"],
                            title=row["title"],
                            objective=row["objective"],
                            status=row["status"],
                            priority=row["priority"],
                            schema_version=row["schema_version"],
                            workspace_path=row["workspace_path"],
                            created_at=row["created_at"],
                            updated_at=row["updated_at"],
                        )
                    )
                return tasks

    async def get_recent_runs(self, task_id: str | None = None, limit: int = 5) -> list[Run]:
        """
        Get recent runs, optionally filtered by task_id.

        Args:
            task_id: Optional task ID to filter by
            limit: Number of runs to return

        Returns:
            List of recent runs
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if task_id:
                query = "SELECT * FROM runs WHERE task_id = ? ORDER BY created_at DESC LIMIT ?"
                params = (task_id, limit)
            else:
                query = "SELECT * FROM runs ORDER BY created_at DESC LIMIT ?"
                params = (limit,)

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                runs = []
                for row in rows:
                    from datetime import datetime

                    runs.append(
                        Run(
                            run_id=row["run_id"],
                            task_id=row["task_id"],
                            workflow=row["workflow"],
                            status=row["status"],
                            risk_level=row["risk_level"],
                            run_path=row["run_path"],
                            schema_version=row["schema_version"],
                            started_at=datetime.fromisoformat(row["started_at"]) if row["started_at"] else None,
                            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
                            created_at=row["created_at"],
                        )
                    )

                # Journal: Query executed
                if self.run_path:
                    append_event(
                        self.run_path,
                        "DB_QUERY",
                        {
                            "query_type": "get_recent_runs",
                            "results_count": len(runs),
                        },
                        trace_id=self.trace_id,
                    )

                return runs

    async def get_all_tasks(self, status: str | None = None, limit: int = 100) -> list[Task]:
        """
        Get all tasks, optionally filtered by status.

        Args:
            status: Optional status filter (pending, running, completed, failed, blocked)
            limit: Maximum number of tasks to return

        Returns:
            List of tasks
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if status:
                query = "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?"
                params = (status, limit)
            else:
                query = "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?"
                params = (limit,)

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                tasks = []
                for row in rows:
                    tasks.append(
                        Task(
                            task_id=row["task_id"],
                            title=row["title"],
                            objective=row["objective"],
                            status=row["status"],
                            priority=row["priority"],
                            protected=bool(row["protected"]) if "protected" in row.keys() else False,
                            schema_version=row["schema_version"],
                            workspace_path=row["workspace_path"],
                            created_at=row["created_at"],
                            updated_at=row["updated_at"],
                        )
                    )
                return tasks

