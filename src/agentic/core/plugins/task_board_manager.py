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

class TaskBoardManager:
    """Manages Task Board Persistence via JSON"""

    def __init__(self, board_path: str = None):
        from src.agentic.core.config import DATA_DIR

        self.meta_dir = DATA_DIR
        
        # Ensure directory exists
        if not self.meta_dir.exists():
            try:
                os.makedirs(self.meta_dir, exist_ok=True)
                print(f"[TaskBoard] Created DB directory: {self.meta_dir}")
            except Exception as e:
                print(f"[TaskBoard] Error creating DB dir: {e}")
        
        from src.agentic.core.config import TASKS_DB_PATH

        self.json_path = TASKS_DB_PATH
        self.md_path = DATA_DIR / "TASK_BOARD.md"
        # Backward compatibility for ybis_server.list_all_tasks
        self.board_path = str(self.md_path)

    async def _read_db(self) -> Dict[str, Any]:
        """Read JSON DB."""
        if not self.json_path.exists():
            print(f"[TaskBoard] JSON DB not found: {self.json_path}")
            return {"backlog": [], "in_progress": [], "done": []}
            
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[TaskBoard] Error reading JSON: {e}")
            return {"backlog": [], "in_progress": [], "done": []}

    async def _save_db(self, data: Dict[str, Any]):
        """Save JSON DB and Sync MD."""
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # Sync to Markdown
            self._sync_to_markdown(data)
        except Exception as e:
            print(f"[TaskBoard] Error saving JSON: {e}")

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
            "priority": priority
        }
        
        data.setdefault("backlog", []).append(new_task)
        await self._save_db(data)
        return task_id

    async def update_task_status(self, task_id: str, status: str, metadata: Dict[str, Any]) -> None:
        """Move task between lists."""
        data = await self._read_db()
        
        # Find task and remove from current list
        target_task = None
        source_list = None
        
        for list_name in ["backlog", "in_progress", "done"]:
            lst = data.get(list_name, [])
            for i, task in enumerate(lst):
                if task["id"] == task_id:
                    target_task = task
                    source_list = list_name
                    del lst[i]
                    break
            if target_task:
                break
        
        if not target_task:
            print(f"[TaskBoard] Task {task_id} not found.")
            return

        # Prepare for moving
        status = status.upper()
        
        if status == "DONE" or status == "COMPLETED":
            data.setdefault("done", []).append(target_task)
        elif status == "IN PROGRESS":
             data.setdefault("in_progress", []).append(target_task)
        else:
             # Default back to backlog or fail? Let's assume backlog if failed/stopped
             data.setdefault("backlog", []).append(target_task)
             
        await self._save_db(data)
