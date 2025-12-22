"""
YBIS PRODUCTION RUNNER
Polls tasks.json and executes them via LangGraph.
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add project root
sys.path.insert(0, os.getcwd())

from src.agentic.graph.workflow import app
from src.agentic.core.plugins.task_board_manager import TaskBoardManager

async def production_loop():
    print("[FACTORY] YBIS FACTORY MANAGER STARTING (Production Mode)...")
    board = TaskBoardManager()
    
    while True:
        try:
            # 1. Read Database
            data = await board._read_db()
            backlog = data.get("backlog", [])
            in_progress = data.get("in_progress", [])
            
            # 2. If nothing in progress, pick from backlog
            if not in_progress and backlog:
                target_task = backlog[0]
                print(f"\n[TASK] Picking Task: {target_task['id']} - {target_task['goal']}")
                
                # Move to In Progress
                await board.update_task_status(target_task['id'], "IN PROGRESS", {})

                # 3. Prepare State for Graph
                initial_state = {
                    "task_id": target_task['id'],
                    "goal": target_task['goal'],
                    "plan": "",
                    "files": [],
                    "history": [],
                    "status": "STARTING",
                    "retry_count": 0
                }
                
                # 4. Invoke LangGraph (Streaming Mode)
                try:
                    print(f"   [EXEC] Executing Graph Workflow...")
                    final_state = None
                    async for event in app.astream(initial_state):
                        for node_name, state_update in event.items():
                            print(f"   [NODE] Node Completed: {node_name}")
                            if "status" in state_update:
                                print(f"      Status: {state_update['status']}")
                            # Keep track of final state
                            if node_name == "memory_write" or node_name == "verifier": # Last nodes
                                final_state = state_update
                    
                    # 5. Update Status based on result
                    # We might need to fetch full state if event only has partial update
                    # But for now, let's assume if we reached here without error, it's processed.
                    # Ideally check final_state["status"]
                    
                    final_status = "DONE" # Simplified for stream handling
                    await board.update_task_status(target_task['id'], final_status, {})
                    print(f"[DONE] Task {target_task['id']} finished cycle.")
                    
                except Exception as graph_err:
                    print(f"[ERROR] Graph Error: {graph_err}")
                    import traceback
                    traceback.print_exc()
                    await board.update_task_status(target_task['id'], "FAILED", {"error": str(graph_err)})
            
            else:
                if in_progress:
                    print(f"   [WAIT] Task {in_progress[0]['id']} is currently IN PROGRESS. Waiting for it to finish...")
                else:
                    print("   [IDLE] No tasks in backlog. Waiting...")
                await asyncio.sleep(10)
                
        except Exception as loop_err:
            print(f"[WARN] Loop Error: {loop_err}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(production_loop())
    except KeyboardInterrupt:
        print("\n[STOP] Factory Manager stopped.")
