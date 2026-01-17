#!/usr/bin/env python3
"""
Trigger Self-Improve Workflow - Proactively improve the system.

Usage:
    python scripts/trigger_self_improve.py
"""

import sys
import uuid
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Task
from src.ybis.constants import PROJECT_ROOT
import asyncio


async def create_self_improve_task() -> str:
    """Create a self-improvement task."""
    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(str(db_path))
    
    task_id = f"SELF-IMPROVE-{uuid.uuid4().hex[:8].upper()}"
    
    task = Task(
        task_id=task_id,
        title="Proactive Self-Improvement",
        objective="Reflect on system state, identify improvements, and implement them",
        status="pending",
        priority="MEDIUM",
    )
    
    await db.register_task(task)
    return task_id


def main():
    """Main entry point."""
    print("=" * 60)
    print("Triggering Self-Improve Workflow")
    print("=" * 60)
    print()
    
    try:
        task_id = asyncio.run(create_self_improve_task())
        print(f"[OK] Created self-improvement task: {task_id}")
        print()
        print("To run the workflow:")
        print(f"  python scripts/ybis_run.py {task_id} --workflow self_improve")
        print()
        print("=" * 60)
    except Exception as e:
        print(f"[ERROR] Failed to create task: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

