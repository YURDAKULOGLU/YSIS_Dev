import sys
import os
import asyncio
import uuid

# Path setup to import YBIS modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Agentic.Core.orchestrator import build_graph
from Agentic.Core.state import AgentState

async def run_scenario():
    print("\n" + "="*60)
    print("🧪 YBIS-OS v2 SCENARIO TEST: Data Analysis Script")
    print("="*60)
    
    # Complex Task Definition
    task = "Create a Python script named 'data_analyst.py' that creates a dummy CSV file with employees and calculates average salary per department."
    
    print(f"📋 TASK:\n{task}\n")
    
    # Initialize Graph
    graph = build_graph()
    
    # Constructing state manually to avoid weird TypedDict issues
    initial_state = {
        "task": task,
        "task_id": str(uuid.uuid4()),
        "user_id": "test_user_v2",
        "current_phase": "analyze",
        "status": "running",
        "messages": [],
        "files_context": [],
        "decisions": [],
        "artifacts": {},
        "error": None,
        "retry_count": 0
    }
    
    config = {"configurable": {"thread_id": "scenario-test-1"}}
    
    print("[SYSTEM] Starting Autonomous Loop (Architect -> Dev -> QA)...")
    
    async for event in graph.astream(initial_state, config):
        pass
        
    print("\n" + "="*60)
    print("[SUCCESS] SCENARIO COMPLETED")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_scenario())