#!/usr/bin/env python3
"""
Approval & Resume Demo - Manually approve blocked task and resume it.

Expected: Task should bypass gate and finish with SUCCESS.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.constants import PROJECT_ROOT
from src.ybis.control_plane import ControlPlaneDB


async def approve_and_resume(task_id: str) -> None:
    """Approve blocked task and resume it."""
    db_path = "platform_data/control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()

    # Get task
    task = await db.get_task(task_id)
    if not task:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)

    print(f"Task: {task_id} - {task.title}")
    print(f"Current status: {task.status}")
    print()

    # Find latest run
    runs_dir = PROJECT_ROOT / "workspaces" / task_id / "runs"
    if not runs_dir.exists():
        print(f"Error: No runs found for task {task_id}")
        sys.exit(1)

    run_dirs = list(runs_dir.glob("R-*"))
    if not run_dirs:
        print(f"Error: No run directories found")
        sys.exit(1)

    latest_run = max(run_dirs, key=lambda p: p.stat().st_mtime)
    run_id = latest_run.name

    print(f"Latest run: {run_id}")
    print(f"Run path: {latest_run}")

    # Write approval
    approval_path = latest_run / "artifacts" / "approval.json"
    approval_data = {
        "task_id": task_id,
        "run_id": run_id,
        "approver": "demo-script",
        "reason": "Demo approval for first contact test",
        "timestamp": None,  # Would use datetime.now().isoformat()
    }

    approval_path.parent.mkdir(parents=True, exist_ok=True)
    approval_path.write_text(json.dumps(approval_data, indent=2), encoding="utf-8")

    print(f"[OK] Approval written to: {approval_path}")
    print()

    # Re-run the task
    print("Re-running workflow with approval...")
    import subprocess

    result = subprocess.run(
        [sys.executable, "scripts/ybis_run.py", task_id],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Check final status
    updated_task = await db.get_task(task_id)
    if updated_task:
        print(f"\nFinal task status: {updated_task.status}")

        if updated_task.status == "completed":
            print("[OK] Task completed successfully!")

            # Verify file was modified
            constants_path = PROJECT_ROOT / "src" / "ybis" / "constants.py"
            if constants_path.exists():
                content = constants_path.read_text()
                if "JOURNAL_DIR" in content and "events.jsonl" in content:
                    print("[OK] src/ybis/constants.py was modified as expected")
                else:
                    print("[WARN] File exists but modification not verified")
        else:
            print(f"[WARN] Task status: {updated_task.status} (expected: completed)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/demo_approve_and_resume.py TASK-ID")
        sys.exit(1)

    task_id = sys.argv[1]
    asyncio.run(approve_and_resume(task_id))

