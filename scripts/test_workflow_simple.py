#!/usr/bin/env python3
"""Test workflow with a simple task."""

import sys
import asyncio
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Task
import uuid


async def main():
    """Create a test task and run it."""
    db_path = project_root / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()
    
    # Create a simple task
    task_id = f"T-{uuid.uuid4().hex[:8]}"
    task = Task(
        task_id=task_id,
        title="Test: Create hello.py",
        objective='Create a simple Python file hello.py with a function hello() that returns "Hello, World!"',
        status="pending",
        priority="MEDIUM",
    )
    
    await db.register_task(task)
    
    print(f"✅ Task created: {task.task_id}")
    print(f"📋 Title: {task.title}")
    print(f"🎯 Objective: {task.objective}")
    print()
    print(f"🚀 Run workflow:")
    print(f"   python scripts/ybis_run.py {task.task_id} --workflow ybis_native")
    
    return task.task_id


if __name__ == "__main__":
    try:
        task_id = asyncio.run(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

