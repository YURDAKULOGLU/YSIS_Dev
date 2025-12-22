"""
TaskBoardManager - JSON-based Task Persistence.

Reads and writes tasks from/to .YBIS_Dev/Meta/Active/tasks.json (Source of Truth)
And optionally syncs to TASK_BOARD.md for visibility.
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path
from src.agentic.infrastructure.db import TaskDatabase

class TaskBoardManager:
    """Manages Task Board Persistence via SQLite."""

    def __init__(self, db_path: str = None):
        from src.agentic.core.config import DATA_DIR, PROJECT_ROOT
        
        # Determine paths
        self.db_path = db_path or str(DATA_DIR / "tasks.db")
        self.json_path = PROJECT_ROOT / "Knowledge" / "LocalDB" / "tasks.json"
        
        self.db = TaskDatabase(self.db_path)
        self._initialized = False

    async def _ensure_db(self):
        """Lazy initialization of the database."""
        if not self._initialized:
            await self.db.initialize()
            # AUTO-MIGRATION: If JSON exists, move to DB
            if os.path.exists(self.json_path):
                await self._migrate_from_json()
            self._initialized = True

    async def _migrate_from_json(self):
        """Migrate existing tasks from JSON to SQLite."""
        print(f"[TaskBoard] Migrating data from {self.json_path} to SQLite...")
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for list_name, status in [("backlog", "BACKLOG"), ("in_progress", "IN_PROGRESS"), ("done", "DONE")]:
                for task in data.get(list_name, []):
                    task['status'] = status
                    await self.db.add_task(task)
            
            # Archive the old JSON to avoid repeated migration
            os.rename(self.json_path, str(self.json_path) + ".migrated")
            print("[TaskBoard] Migration successful. JSON archived.")
        except Exception as e:
            print(f"[TaskBoard] Migration failed: {e}")

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
            "# YBIS_Dev Task Board (JSON Synced)",
            "",
            "**Protocol:** Auto-Generated from `tasks.json`",
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
            print(f"[TaskBoard] Error syncing MD: {e}")

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
