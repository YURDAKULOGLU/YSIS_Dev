import aiosqlite
import json
from typing import Dict, List, Optional, Any

class TaskDatabase:
    """Async SQLite Database for YBIS Task Management."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def initialize(self):
        """Create tables if they don't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    goal TEXT NOT NULL,
                    details TEXT,
                    status TEXT NOT NULL,
                    priority TEXT,
                    assignee TEXT,
                    final_status TEXT,
                    metadata TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.commit()

    async def add_task(self, task: Dict[str, Any]):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO tasks (id, goal, details, status, priority, assignee, final_status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                task['id'],
                task['goal'],
                task.get('details', ''),
                task['status'],
                task.get('priority', 'MEDIUM'),
                task.get('assignee', 'Unassigned'),
                task.get('final_status', 'UNKNOWN'),
                json.dumps(task.get('metadata', {}))
            ))
            await db.commit()

    async def get_all_tasks(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM tasks") as cursor:
                rows = await cursor.fetchall()
                tasks = []
                for row in rows:
                    t = dict(row)
                    t['metadata'] = json.loads(t['metadata']) if t['metadata'] else {}
                    tasks.append(t)
                return tasks

    async def update_task_status(self, task_id: str, status: str, final_status: str = None):
        async with aiosqlite.connect(self.db_path) as db:
            if final_status:
                await db.execute("UPDATE tasks SET status = ?, final_status = ? WHERE id = ?", (status, final_status, task_id))
            else:
                await db.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
            await db.commit()
