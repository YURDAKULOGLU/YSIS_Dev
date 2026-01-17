#!/usr/bin/env python3
"""Check the latest run results."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from src.ybis.control_plane import ControlPlaneDB


async def check_latest_run():
    """Check the latest run."""
    db_path = project_root / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()
    
    # Get latest task (query directly)
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
    print(f"Latest Task: {task.task_id}")
    print(f"  Title: {task.title}")
    print(f"  Status: {task.status}")
    print()
    
    # Get latest run for this task
    runs = await db.get_recent_runs(task_id=task.task_id, limit=1)
    if not runs:
        print("No runs found for this task")
        return
    
    run = runs[0]
    print(f"Latest Run: {run.run_id}")
    print(f"  Status: {run.status}")
    print(f"  Workflow: {run.workflow}")
    print(f"  Run Path: {run.run_path}")
    print()
    
    # Check artifacts
    run_path = Path(run.run_path)
    artifacts_path = run_path / "artifacts"
    
    if artifacts_path.exists():
        print("=== ARTIFACTS ===")
        for artifact in sorted(artifacts_path.glob("*")):
            size = artifact.stat().st_size if artifact.is_file() else 0
            print(f"  ✅ {artifact.name} ({size} bytes)")
    else:
        print("⚠️ Artifacts directory not found")
    
    # Check for created files
    print()
    print("=== CREATED FILES (Python) ===")
    py_files = list(run_path.rglob("*.py"))
    if py_files:
        for py_file in sorted(py_files)[:10]:  # Show first 10
            rel_path = py_file.relative_to(run_path)
            print(f"  📄 {rel_path}")
        if len(py_files) > 10:
            print(f"  ... and {len(py_files) - 10} more")
    else:
        print("  No Python files found")
    
    # Check for SPEC.md
    spec_path = artifacts_path / "SPEC.md"
    if spec_path.exists():
        print()
        print("=== SPEC.md (first 300 chars) ===")
        print(spec_path.read_text(encoding='utf-8')[:300])
    
    # Check for plan.json
    plan_path = artifacts_path / "plan.json"
    if plan_path.exists():
        import json
        print()
        print("=== plan.json ===")
        plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
        print(f"  Steps: {len(plan_data.get('steps', []))}")
        if plan_data.get('steps'):
            print(f"  First step: {plan_data['steps'][0].get('action', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(check_latest_run())

