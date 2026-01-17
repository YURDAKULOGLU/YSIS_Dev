#!/usr/bin/env python3
"""Retry self-development workflow with proper setup."""

import sys
import asyncio
import json
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.services.mcp_tools.task_tools import task_create

async def main():
    """Create task and run self-development workflow."""
    print("=" * 60)
    print("SELF-DEVELOPMENT RETRY")
    print("=" * 60)
    print()
    
    # Create new task
    print("Step 1: Creating new task...")
    task_result = await task_create(
        title="Complete EvoAgentX Integration (Retry)",
        objective="Complete EvoAgentX adapter implementation: install missing dependencies (dashscope, etc.), implement real evolution using TextGradOptimizer, complete YBIS↔EvoAgentX conversion, test end-to-end evolution",
        priority="HIGH"
    )
    
    task_data = json.loads(task_result)
    task_id = task_data["task_id"]
    
    print(f"✅ Task created: {task_id}")
    print(f"   Title: {task_data['title']}")
    print()
    
    # Show command
    print("Step 2: Run self-development workflow:")
    print(f"   python scripts/ybis_run.py {task_id} --workflow self_develop")
    print()
    print("Step 3: Check quality after completion:")
    print(f"   python scripts/check_self_development_quality.py {task_id}")
    print()
    print("=" * 60)
    print(f"Task ID: {task_id}")
    print("=" * 60)
    
    return task_id

if __name__ == "__main__":
    task_id = asyncio.run(main())
    print(f"\nReady to run: python scripts/ybis_run.py {task_id} --workflow self_develop")

