import asyncio
import json
import os
import sys
import logging
import time
from datetime import datetime

# Path Setup
sys.path.insert(0, os.getcwd())

from src.agentic.core.plugins.task_board_manager import TaskBoardManager
from scripts.worker import worker_loop

# LOGGING SETUP
LOG_FILE = "logs/stress_test_report.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [STRESS_TEST] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("StressTest")

async def monitor_logs():
    """Reads worker.out in real-time to capture evidence"""
    try:
        with open("worker.out", "r") as f:
            f.seek(0, 2) # Go to end
            while True:
                line = f.readline()
                if line:
                    logger.info(f"WORKER LOG: {line.strip()}")
                else:
                    await asyncio.sleep(0.1)
    except Exception:
        pass

async def inject_tasks(board: TaskBoardManager):
    """Injects a series of tasks into the system with specific IDs"""
    tasks = [
        ("STRESS-A", "Create a file named src/stress_a.py that prints 'Stress Test A'"),
        ("STRESS-B", "Create a file named src/stress_b.py with a function calculate_sum(a,b)"),
        ("STRESS-C", "Modify src/stress_b.py to add a docstring to calculate_sum")
    ]

    # Read current DB
    data = await board._read_db()

    for tid, goal in tasks:
        logger.info(f"Injecting Task: {tid} - {goal}")

        # Check if already exists
        exists = False
        for lst in data.values():
            for t in lst:
                if t["id"] == tid:
                    exists = True
                    break

        if not exists:
            new_task = {
                "id": tid,
                "goal": goal,
                "details": "Created by Stress Test",
                "assignee": "StressTestBot",
                "priority": "HIGH"
            }
            data.setdefault("backlog", []).append(new_task)
            logger.info(f"Task {tid} added to backlog.")
        else:
            logger.info(f"Task {tid} already exists. Skipping injection.")

    # Save DB
    await board._save_db(data)

async def run_stress_test():
    logger.info("Starting GRAND SYSTEM STRESS TEST")

    # 1. Clear State (Optional, but good for stress test)
    # For now we append to existing state to simulate real usage

    board = TaskBoardManager()

    # 2. Start Worker in Background
    logger.info("Launching Background Worker...")
    worker_task = asyncio.create_task(worker_loop())

    # 3. Inject Tasks
    await inject_tasks(board)

    # 4. Monitor Loop
    # Wait for all injected tasks to become 'DONE'
    start_time = time.time()
    max_wait = 300 # 5 minutes max

    while time.time() - start_time < max_wait:
        data = await board._read_db()

        # Check if our specific tasks are done
        target_ids = ["STRESS-A", "STRESS-B", "STRESS-C"]
        completed = [t["id"] for t in data.get("done", [])]

        pending = [tid for tid in target_ids if tid not in completed]

        if not pending:
            logger.info("SUCCESS: All stress tasks completed!")
            break

        logger.info(f"Waiting for tasks: {pending}")
        await asyncio.sleep(10)

    if pending:
        logger.error(f"TIMEOUT: Tasks {pending} did not finish in time.")

    # Stop Worker
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        logger.info("Worker shut down gracefully.")

if __name__ == "__main__":
    # Ensure logs dir exists
    os.makedirs("logs", exist_ok=True)
    try:
        asyncio.run(run_stress_test())
    except KeyboardInterrupt:
        pass
