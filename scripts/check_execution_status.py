#!/usr/bin/env python3
"""Check if task was actually executed."""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from src.ybis.control_plane import ControlPlaneDB


async def check_execution():
    """Check execution status of latest run."""
    db_path = project_root / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()
    
    # Get latest task
    import aiosqlite
    async with aiosqlite.connect(db_path) as db_conn:
        db_conn.row_factory = aiosqlite.Row
        async with db_conn.execute(
            "SELECT * FROM tasks ORDER BY updated_at DESC LIMIT 1"
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                print("No tasks found")
                return
            task_id = row["task_id"]
    
    task = await db.get_task(task_id)
    if not task:
        print("Task not found")
        return
    
    print(f"Task: {task.task_id}")
    print(f"   Title: {task.title}")
    print(f"   Objective: {task.objective[:100]}...")
    print()
    
    # Get latest run
    runs = await db.get_recent_runs(task_id=task_id, limit=1)
    if not runs:
        print("No runs found")
        return
    
    run = runs[0]
    print(f"Run: {run.run_id}")
    print(f"   Status: {run.status}")
    print(f"   Workflow: {run.workflow}")
    print(f"   Path: {run.run_path}")
    print()
    
    run_path = Path(run.run_path)
    
    # Check if run path exists
    if not run_path.exists():
        print("ERROR: Run path does not exist!")
        return
    
    # Check artifacts
    artifacts_path = run_path / "artifacts"
    print(f"Artifacts directory: {artifacts_path.exists()}")
    
    if artifacts_path.exists():
        artifacts = list(artifacts_path.glob("*.json"))
        print(f"   Found {len(artifacts)} JSON artifacts:")
        for artifact in artifacts:
            print(f"     - {artifact.name}")
    
    print()
    
    # Check executor report
    executor_path = artifacts_path / "executor_report.json"
    if executor_path.exists():
        print("OK: Executor report found!")
        executor_data = json.loads(executor_path.read_text(encoding='utf-8'))
        print(f"   Success: {executor_data.get('success', False)}")
        files_changed = executor_data.get('files_changed', [])
        print(f"   Files Changed: {len(files_changed)}")
        if files_changed:
            print("   Files:")
            for file in files_changed:
                file_path = Path(file)
                exists = file_path.exists()
                print(f"     [{'OK' if exists else 'MISSING'}] {file}")
    else:
        print("ERROR: Executor report NOT found - task was NOT executed!")
    
    print()
    
    # Check plan
    plan_path = artifacts_path / "plan.json"
    if plan_path.exists():
        plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
        steps = plan_data.get('steps', [])
        print(f"Plan has {len(steps)} steps")
        if steps:
            print("   Steps:")
            for i, step in enumerate(steps, 1):
                print(f"     {i}. {step.get('action', 'N/A')[:60]}")
    else:
        print("ERROR: Plan not found!")
    
    print()
    
    # Check journal for execution events
    journal_path = run_path / "journal.jsonl"
    if journal_path.exists():
        print("Journal events:")
        with open(journal_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                event = json.loads(line)
                event_type = event.get('event_type', 'Unknown')
                if 'EXECUTE' in event_type or 'EXECUTOR' in event_type:
                    print(f"   [OK] {event_type}: {event.get('message', '')[:80]}")
                elif 'ERROR' in event_type or 'FAILED' in event_type:
                    print(f"   [ERROR] {event_type}: {event.get('message', '')[:80]}")
    else:
        print("WARNING: Journal not found")


if __name__ == "__main__":
    asyncio.run(check_execution())

