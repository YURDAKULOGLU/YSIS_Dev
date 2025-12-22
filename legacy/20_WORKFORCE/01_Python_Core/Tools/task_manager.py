"""Task Manager - Simple task queue"""
import json
from pathlib import Path
from datetime import datetime

class TaskManagerTool:
    def __init__(self):
        self.tasks_file = Path(__file__).parent.parent.parent / "Meta/Active/tasks.json"
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.tasks_file.exists():
            self.tasks_file.write_text("[]")

    def pick_next_task(self) -> str | None:
        """Get next task"""
        try:
            tasks = json.loads(self.tasks_file.read_text())
            pending = [t for t in tasks if t.get("status") == "pending"]
            return pending[0]["description"] if pending else None
        except:
            return None

    def add_task(self, description: str) -> str:
        """Add task"""
        tasks = json.loads(self.tasks_file.read_text() or "[]")
        task_id = f"task-{len(tasks)+1}"
        tasks.append({"id": task_id, "description": description, "status": "pending"})
        self.tasks_file.write_text(json.dumps(tasks, indent=2))
        return task_id

task_manager = TaskManagerTool()
