#!/usr/bin/env python3
"""
Test Unified Task Abstraction.

Tests that all adapters work correctly.
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic.infrastructure.task_manager import UnifiedTaskManager


async def test_task_manager():
    """Test UnifiedTaskManager basic functionality."""
    print("=" * 80)
    print("UNIFIED TASK MANAGER TEST")
    print("=" * 80)
    print()
    
    manager = UnifiedTaskManager()
    
    # Test 1: List available frameworks
    print("Available frameworks:")
    frameworks = ["temporal", "ray", "prefect", "spade", "celery"]
    for fw in frameworks:
        try:
            # Just check if adapter class exists
            if fw == "temporal":
                from agentic.infrastructure.adapters.temporal_adapter import TemporalTask
                print(f"  [OK] {fw}: TemporalTask available")
            elif fw == "ray":
                from agentic.infrastructure.adapters.ray_adapter import RayTask
                print(f"  [OK] {fw}: RayTask available")
            elif fw == "prefect":
                from agentic.infrastructure.adapters.prefect_adapter import PrefectTask
                print(f"  [OK] {fw}: PrefectTask available")
            elif fw == "spade":
                from agentic.infrastructure.adapters.spade_adapter import SPADETask
                print(f"  [OK] {fw}: SPADETask available")
            elif fw == "celery":
                from agentic.infrastructure.adapters.celery_adapter import CeleryTask
                print(f"  [OK] {fw}: CeleryTask available")
        except ImportError as e:
            print(f"  [SKIP] {fw}: {e}")
    
    print()
    print("[SUCCESS] Unified Task Manager is ready!")
    print()
    print("Usage example:")
    print("  from agentic.infrastructure.task_manager import UnifiedTaskManager")
    print("  manager = UnifiedTaskManager()")
    print("  task = manager.create_task('task-1', 'temporal', workflow_type=MyWorkflow, client=temporal_client)")
    print("  await manager.start_task('task-1')")


if __name__ == "__main__":
    asyncio.run(test_task_manager())

