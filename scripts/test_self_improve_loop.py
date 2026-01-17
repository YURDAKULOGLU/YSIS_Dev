#!/usr/bin/env python3
"""
Test script to verify self-improve workflow loop works correctly.

Tests:
1. Loop doesn't enter infinite recursion
2. Repair retry limits are respected
3. Conditional routing works correctly
4. State management is correct
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ybis.contracts import Task
from src.ybis.control_plane import ControlPlaneDB
from src.ybis.workflows.runner import build_graph
from src.ybis.orchestrator.graph import create_workspace


async def test_self_improve_loop():
    """Test that self-improve loop works without infinite recursion."""
    
    print("=" * 60)
    print("SELF-IMPROVE LOOP TEST")
    print("=" * 60)
    print()
    
    # Create test task
    task = Task(
        task_id="T-LOOP-TEST",
        title="Test Self-Improve Loop",
        objective="Add a simple logging statement to orchestrator/graph.py to verify loop works",
        status="pending",
        priority="MEDIUM",
    )
    
    # Initialize database
    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(str(db_path))
    await db.initialize()
    await db.register_task(task)
    
    # Create workspace
    workspace = create_workspace(task.task_id)
    run_id = f"R-{task.task_id[-8:]}"
    run_path = workspace / "runs" / run_id
    run_path.mkdir(parents=True, exist_ok=True)
    
    # Build workflow graph
    try:
        graph = build_graph("self_improve")
    except Exception as e:
        print(f"[ERROR] Failed to build graph: {e}")
        return False
    
    # Initial state
    initial_state = {
        "task_id": task.task_id,
        "run_id": run_id,
        "run_path": str(run_path),
        "status": "running",
        "repair_retries": 0,
        "max_repair_retries": 3,  # Set explicitly for testing
        "test_passed": False,
        "lint_passed": True,
        "tests_passed": True,
    }
    
    print(f"[INFO] Starting workflow for task: {task.task_id}")
    print(f"[INFO] Max repair retries: {initial_state['max_repair_retries']}")
    print()
    
    # Track execution
    node_count = {}
    max_iterations = 50  # Safety limit
    
    try:
        # Run workflow with iteration limit
        result = None
        iteration = 0
        
        async for state in graph.astream(initial_state):
            iteration += 1
            if iteration > max_iterations:
                print(f"[ERROR] Workflow exceeded {max_iterations} iterations - possible infinite loop!")
                return False
            
            # Track node execution
            current_step = state.get("current_step", "unknown")
            if current_step not in node_count:
                node_count[current_step] = 0
            node_count[current_step] += 1
            
            # Check repair retries
            repair_retries = state.get("repair_retries", 0)
            max_retries = state.get("max_repair_retries", 3)
            
            if repair_retries > max_retries:
                print(f"[ERROR] Repair retries ({repair_retries}) exceeded max ({max_retries})!")
                return False
            
            # Log progress
            if current_step in ["test", "repair", "implement"]:
                print(f"[ITER {iteration}] {current_step} - repair_retries={repair_retries}/{max_retries}")
            
            result = state
        
        print()
        print("[SUCCESS] Workflow completed without infinite recursion!")
        print()
        print("Node execution counts:")
        for node, count in sorted(node_count.items()):
            print(f"  {node}: {count}")
        print()
        
        # Check final state
        final_repair_retries = result.get("repair_retries", 0)
        final_max_retries = result.get("max_repair_retries", 3)
        test_passed = result.get("test_passed", False)
        
        print("Final state:")
        print(f"  repair_retries: {final_repair_retries}/{final_max_retries}")
        print(f"  test_passed: {test_passed}")
        print()
        
        if final_repair_retries > final_max_retries:
            print("[ERROR] Final repair retries exceeded max!")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Workflow execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_self_improve_loop())
    sys.exit(0 if success else 1)

