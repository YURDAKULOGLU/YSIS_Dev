import asyncio
import os
import sys
import argparse
from pathlib import Path

# Setup path
sys.path.insert(0, os.getcwd())

from src.agentic.core.plugins.task_board_manager import TaskBoardManager

async def main():
    parser = argparse.ArgumentParser(description="Add a task to the YBIS Task Board")
    parser.add_argument("goal", help="The high-level goal of the task")
    parser.add_argument("details", help="Detailed description/instructions", nargs='?', default="")
    parser.add_argument("--priority", help="Task priority (LOW, MEDIUM, HIGH)", default="MEDIUM")

    args = parser.parse_args()

    board = TaskBoardManager()

    print(f"📝 Adding task: {args.goal}")
    task_id = await board.create_task(args.goal, args.details, args.priority)

    print(f"[SUCCESS] Created {task_id}")
    print(f"[INFO] Worker will pick it up shortly.")

if __name__ == "__main__":
    asyncio.run(main())
