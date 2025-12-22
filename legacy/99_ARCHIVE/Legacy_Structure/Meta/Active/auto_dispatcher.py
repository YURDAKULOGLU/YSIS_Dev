#!/usr/bin/env python3
"""
Auto Task Dispatcher - Lean Protocol v3.1
Automatically assigns tasks from TASK_BOARD.md to available agents
"""
import json
import re
from datetime import datetime
from pathlib import Path

class TaskDispatcher:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.task_board = base_path / "TASK_BOARD.md"
        self.agent_status = base_path / "agent_status.json"

    def get_available_agents(self) -> list:
        """Get list of agents not currently working on tasks"""
        try:
            with open(self.agent_status) as f:
                status = json.load(f)
            return [a for a, s in status.items() if s["status"] == "idle"]
        except FileNotFoundError:
            # Default: both agents available
            return ["claude", "gemini"]

    def parse_tasks(self) -> dict:
        """Parse TASK_BOARD.md and extract tasks"""
        with open(self.task_board) as f:
            content = f.read()

        tasks = {
            "new": [],
            "in_progress": [],
            "done": [],
            "blocked": []
        }

        current_section = None

        for line in content.split('\n'):
            if line.startswith('## 📋 NEW'):
                current_section = "new"
            elif line.startswith('## 🔄 IN PROGRESS'):
                current_section = "in_progress"
            elif line.startswith('## ✅ DONE'):
                current_section = "done"
            elif line.startswith('## 🚫 BLOCKED'):
                current_section = "blocked"
            elif line.startswith('- [ ] ') and current_section:
                # Parse task
                match = re.search(r'\*\*TASK-(\d+):\*\* (.+)', line)
                if match:
                    task_id = f"TASK-{match.group(1)}"
                    description = match.group(2)
                    tasks[current_section].append({
                        "id": task_id,
                        "description": description
                    })

        return tasks

    def assign_task(self, task_id: str, agent: str):
        """Assign a task to an agent"""
        # Update task board
        with open(self.task_board) as f:
            content = f.read()

        # Move task from NEW to IN PROGRESS
        content = content.replace(
            f"- [ ] **{task_id}:**",
            f"- [x] **{task_id}:** (@{agent})"
        )

        # TODO: Implement proper section moving

        with open(self.task_board, 'w') as f:
            f.write(content)

        # Update agent status
        self.update_agent_status(agent, "working", task_id)

        # Log
        self.log_assignment(task_id, agent)

    def update_agent_status(self, agent: str, status: str, task: str = None):
        """Update agent status file"""
        try:
            with open(self.agent_status) as f:
                statuses = json.load(f)
        except FileNotFoundError:
            statuses = {}

        statuses[agent] = {
            "status": status,
            "current_task": task,
            "last_update": datetime.now().isoformat()
        }

        with open(self.agent_status, 'w') as f:
            json.dump(statuses, f, indent=2)

    def log_assignment(self, task_id: str, agent: str):
        """Log task assignment"""
        log_file = self.base_path / "communication_log.md"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n### [{timestamp}] AUTO-ASSIGN: {task_id} → @{agent}\n"

        with open(log_file, 'a') as f:
            f.write(entry)

    def auto_dispatch(self):
        """Main dispatch loop - assign NEW tasks to available agents"""
        tasks = self.parse_tasks()
        available = self.get_available_agents()

        print(f"Available agents: {available}")
        print(f"New tasks: {len(tasks['new'])}")

        for task in tasks['new']:
            if not available:
                print("No available agents, stopping dispatch")
                break

            # Simple strategy: FIFO
            agent = available.pop(0)

            print(f"Assigning {task['id']} to @{agent}")
            self.assign_task(task['id'], agent)

if __name__ == "__main__":
    base = Path(__file__).parent
    dispatcher = TaskDispatcher(base)
    dispatcher.auto_dispatch()
