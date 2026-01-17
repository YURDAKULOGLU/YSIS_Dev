"""
YBIS Worker - Background process that polls for tasks and executes them.

Implements multi-worker coordination with lease-based task claiming.
"""

import asyncio
import logging
import os
import sys
import threading
import time
import uuid

logger = logging.getLogger(__name__)

from ..control_plane import ControlPlaneDB
from ..data_plane import init_run_structure


class YBISWorker:
    """
    YBIS Worker - Polls for tasks and executes workflows.

    Features:
    - Atomic task claiming via leases
    - Heartbeat thread to keep leases alive
    - Automatic lease release on completion/failure
    """

    def __init__(
        self,
        worker_id: str | None = None,
        db_path: str = "platform_data/control_plane.db",
        poll_interval: int = 5,
        heartbeat_interval: int = 60,
    ):
        """
        Initialize worker.

        Args:
            worker_id: Unique worker identifier (auto-generated if None)
            db_path: Path to control plane database
            poll_interval: Seconds between task polls
            heartbeat_interval: Seconds between heartbeats
        """
        self.worker_id = worker_id or f"worker-{uuid.uuid4().hex[:8]}"
        self.db_path = db_path
        self.poll_interval = poll_interval
        self.heartbeat_interval = heartbeat_interval
        self.running = False
        self.heartbeat_thread: threading.Thread | None = None
        self.db: ControlPlaneDB | None = None

    async def start(self) -> None:
        """Start the worker loop."""
        self.db = ControlPlaneDB(self.db_path)
        await self.db.initialize()

        self.running = True

        # Start heartbeat thread
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

        print(f"Worker {self.worker_id} started")
        print(f"Polling every {self.poll_interval} seconds")

        # Main loop
        while self.running:
            try:
                await self._poll_and_execute()
            except Exception as e:
                print(f"Error in worker loop: {e}", file=sys.stderr)
                import traceback

                traceback.print_exc()

            await asyncio.sleep(self.poll_interval)

    async def stop(self) -> None:
        """Stop the worker."""
        self.running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)
        print(f"Worker {self.worker_id} stopped")

    async def _poll_and_execute(self) -> None:
        """Poll for pending tasks and execute them."""
        if not self.db:
            return

        # Get pending tasks
        tasks = await self.db.get_pending_tasks()

        for task in tasks:
            # Try to claim task
            claimed = await self.db.claim_task(task.task_id, self.worker_id, duration_sec=300)

            if not claimed:
                # Task already claimed by another worker
                continue

            print(f"Claimed task: {task.task_id} - {task.title}")

            try:
                # Execute workflow
                await self._execute_task(task)

                # Update task status
                task.status = "completed"
                await self.db.register_task(task)

            except Exception as e:
                print(f"Task {task.task_id} failed: {e}", file=sys.stderr)
                task.status = "failed"
                await self.db.register_task(task)

            finally:
                # Release lease
                await self.db.release_lease(task.task_id, self.worker_id)

    async def _execute_task(self, task) -> None:
        """
        Execute a task workflow.

        Args:
            task: Task to execute
        """
        # Generate run_id
        run_id = f"R-{uuid.uuid4().hex[:8]}"

        # Initialize workspace
        run_path = init_run_structure(task.task_id, run_id)

        # Build and execute workflow graph (lazy import to avoid circular dependency)
        from ..orchestrator.graph import build_workflow_graph

        graph = build_workflow_graph()

        initial_state = {
            "task_id": task.task_id,
            "run_id": run_id,
            "run_path": run_path,
            "status": "pending",
        }

        # Execute workflow
        final_state = graph.invoke(initial_state)

        print(f"Task {task.task_id} completed with status: {final_state['status']}")

    def _heartbeat_loop(self) -> None:
        """Background thread that sends heartbeats."""
        while self.running:
            try:
                if self.db:
                    # Run heartbeat in async context
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.db.heartbeat(self.worker_id))
                    loop.close()
            except Exception as e:
                print(f"Heartbeat error: {e}", file=sys.stderr)

            time.sleep(self.heartbeat_interval)


async def main() -> None:
    """Main entry point for worker."""
    worker_id = os.getenv("YBIS_WORKER_ID")
    db_path = os.getenv("YBIS_DB_PATH", "platform_data/control_plane.db")

    worker = YBISWorker(worker_id=worker_id, db_path=db_path)
    try:
        await worker.start()
    except KeyboardInterrupt:
        print("\nShutting down worker...")
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())

