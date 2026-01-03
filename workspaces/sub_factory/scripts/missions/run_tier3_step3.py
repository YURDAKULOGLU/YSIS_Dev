import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, os.getcwd())

from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager
from src.agentic.core.plugins.rag_memory import RAGMemory

async def run_new_brain():
    print("[INFO] TIER 3 - STEP 3: Awakening the Graph")

    # Init Plugins
    planner = SimplePlanner()
    executor = AiderExecutor()
    verifier = SentinelVerifier()

    # Init Graph
    orchestrator = OrchestratorGraph(planner, executor, verifier)

    # Prepare Input State (TypedDict compatible)
    initial_state = {
        "task_id": "TIER3-TEST",
        "task_description": "Create a file 'src/hello_graph.py' that prints 'Hello from LangGraph'.",
        "phase": "init",
        "retry_count": 0,
        "max_retries": 3,
        "artifacts_path": ".sandbox/TIER3-TEST",
        "started_at": datetime.now(),
        "completed_at": None,
        "plan": None,
        "code_result": None,
        "verification": None,
        "error": None
    }

    print(f"▶️ Invoking Graph for task: {initial_state['task_description']}")

    try:
        final_state = await orchestrator.ainvoke(initial_state)
        print("\n[SUCCESS] GRAPH EXECUTION COMPLETE!")
        print(f"Final Phase: {final_state.get('phase')}")

        if final_state.get('verification') and final_state['verification'].tests_passed:
             print("🎉 SUCCESS: Verification Passed.")
        else:
             print("⚠️ WARNING: Verification didn't pass or run (check logs).")

    except Exception as e:
        print(f"[ERROR] GRAPH CRASHED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_new_brain())
