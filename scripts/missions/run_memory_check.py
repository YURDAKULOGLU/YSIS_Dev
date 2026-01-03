import asyncio
import sys
import os

# Add project root
sys.path.insert(0, os.getcwd())

from src.agentic.core.plugins.task_board_manager import TaskBoardManager

async def test_memory():
    print("[INFO] Testing Memory (TaskBoardManager)...")

    tb = TaskBoardManager()
    print(f"📂 DB Path: {tb.json_path}")

    # 1. Create Task
    print("[INFO] Creating a test task...")
    task_id = await tb.create_task("Test Memory", "Verify JSON persistence works")
    print(f"[SUCCESS] Created Task ID: {task_id}")

    # 2. Read DB directly
    print("📖 Reading DB...")
    data = await tb._read_db()

    found = False
    for t in data.get("backlog", []):
        if t["id"] == task_id:
            print(f"[SUCCESS] FOUND IT! Task {task_id} is in memory.")
            found = True
            break

    if not found:
        print("[ERROR] ERROR: Task not found in DB!")
    else:
        print("[INFO] Memory Test PASSED!")

if __name__ == "__main__":
    asyncio.run(test_memory())
