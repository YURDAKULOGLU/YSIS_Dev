#!/usr/bin/env python3
"""
First Contact Demo - Create a task that requires changing a YBIS core file.

Expected: Task should reach AWAITING_APPROVAL status because it touches src/ybis/.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.contracts import Task
from src.ybis.control_plane import ControlPlaneDB


async def create_and_run_task() -> None:
    """Create task and run it."""
    db_path = "platform_data/control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()

    # Create task
    import uuid

    task_id = f"T-FIRST-{uuid.uuid4().hex[:8]}"

    task = Task(
        task_id=task_id,
        title="Document Journal Directory",
        objective="In src/ybis/constants.py, add a comment or docstring to JOURNAL_DIR explaining its purpose.",
        status="pending",
    )

    await db.register_task(task)

    print(f"Created task: {task_id}")
    print(f"Title: {task.title}")
    print(f"Objective: {task.objective}")
    print()

    # Run the task
    print("Running workflow...")
    import subprocess

    result = subprocess.run(
        [sys.executable, "scripts/ybis_run.py", task_id],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Check task status
    updated_task = await db.get_task(task_id)
    if updated_task:
        print(f"\nTask status: {updated_task.status}")

        if updated_task.status == "blocked":
            print("[OK] Task is BLOCKED as expected. Awaiting approval.")
        else:
            print(f"[WARN] Task status: {updated_task.status} (expected: blocked)")

        # Check gate report
        from src.ybis.constants import PROJECT_ROOT

        run_dirs = list((PROJECT_ROOT / "workspaces" / task_id / "runs").glob("R-*"))
        if run_dirs:
            latest_run = max(run_dirs, key=lambda p: p.stat().st_mtime)
            gate_report_path = latest_run / "artifacts" / "gate_report.json"

            if gate_report_path.exists():
                import json

                gate_data = json.loads(gate_report_path.read_text())
                decision = gate_data.get("decision")
                print(f"Gate decision: {decision}")

                if decision == "REQUIRE_APPROVAL":
                    print("[OK] Gate report contains REQUIRE_APPROVAL as expected.")
                else:
                    print(f"[WARN] Gate decision: {decision} (expected: REQUIRE_APPROVAL)")


if __name__ == "__main__":
    asyncio.run(create_and_run_task())

