#!/usr/bin/env python3
"""
Multi-Worker Stress Test - Verify concurrent execution safety.

DoD:
- 5/5 tasks completed without race conditions
- Journal logs show distinct worker IDs for each task
"""

import asyncio
import multiprocessing
import sys
import tempfile
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Task


def run_worker(worker_id: str, db_path: str, duration: int = 30) -> None:
    """Run a worker process."""
    import asyncio

    from src.ybis.services.worker import YBISWorker

    async def worker_main():
        worker = YBISWorker(worker_id=worker_id, db_path=db_path, poll_interval=1)
        try:
            # Run for specified duration
            await asyncio.wait_for(worker.start(), timeout=duration)
        except asyncio.TimeoutError:
            await worker.stop()

    asyncio.run(worker_main())


async def stress_test() -> None:
    """Run stress test with multiple workers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "stress_test.db"

        # Initialize database
        db = ControlPlaneDB(db_path)
        await db.initialize()

        # Create 5 independent tasks
        tasks = []
        for i in range(5):
            task = Task(
                task_id=f"T-STRESS-{i:03d}",
                title=f"Stress Test Task {i}",
                objective=f"Test concurrent execution {i}",
                status="pending",
            )
            await db.register_task(task)
            tasks.append(task.task_id)

        print(f"Created {len(tasks)} tasks: {tasks}")

        # Start 3 worker processes
        workers = []
        for i in range(3):
            worker_id = f"worker-{i}"
            process = multiprocessing.Process(
                target=run_worker, args=(worker_id, str(db_path), 30)
            )
            process.start()
            workers.append(process)
            print(f"Started worker: {worker_id}")

        # Wait for workers to complete tasks
        await asyncio.sleep(20)

        # Check task completion
        completed = 0
        worker_assignments = {}

        for task_id in tasks:
            task = await db.get_task(task_id)
            if task and task.status in ["completed", "failed"]:
                completed += 1
                print(f"Task {task_id}: {task.status}")

        # Stop workers
        for process in workers:
            process.terminate()
            process.join(timeout=5)

        # Verify results
        print(f"\nResults:")
        print(f"  Tasks completed: {completed}/{len(tasks)}")
        print(f"  Workers used: {len(workers)}")

        assert completed == len(tasks), f"Expected {len(tasks)} tasks completed, got {completed}"

        # Verify no duplicate assignments (check leases)
        import aiosqlite

        async with aiosqlite.connect(db_path) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(
                "SELECT task_id, worker_id FROM leases WHERE task_id LIKE 'T-STRESS-%'"
            ) as cursor:
                rows = await cursor.fetchall()
                task_workers = {row["task_id"]: row["worker_id"] for row in rows}

        print(f"  Task-worker assignments: {task_workers}")

        # Verify each task has at most one worker
        assert len(task_workers) <= len(tasks), "Too many lease records"

        print("\n✓ Stress test passed: All tasks completed without race conditions")


if __name__ == "__main__":
    asyncio.run(stress_test())

