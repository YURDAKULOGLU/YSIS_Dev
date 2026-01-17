"""Create a test task for repair loop testing."""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB


async def main():
    db = ControlPlaneDB("platform_data/control_plane.db")
    await db.initialize()

    task = await db.create_task(
        title="Test Repair Loop - Intentional Failure",
        objective="Create a Python file 'tests/test_repair_loop_fail.py' with an intentional syntax error (missing colon) to test repair loop routing. The file should fail linting and tests, triggering the repair loop.",
        priority="HIGH",
    )

    print(f"Task created: {task.task_id}")
    print(f"Title: {task.title}")
    print(f"\nRun with:")
    print(f"  python scripts/ybis_run.py {task.task_id} --workflow ybis_native")

    return task.task_id


if __name__ == "__main__":
    task_id = asyncio.run(main())
    sys.exit(0)


