import asyncio
import sys
import os

sys.path.insert(0, os.getcwd())

from src.agentic.core.orchestrator_v3 import OrchestratorV3
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager
from src.agentic.core.plugins.rag_memory import RAGMemory

async def run_step1():
    print("🏗️ TIER 3 - STEP 1: LangGraph Foundation")

    rag = RAGMemory()
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
        rag_memory=rag
    )

    task_description = """
    TIER 3 INITIALIZATION: Setup LangGraph Foundation.

    1. Create 'src/agentic/core/graphs/basic_graph.py':
       - Define a simple LangGraph workflow using 'StateGraph'.
       - Define a State TypedDict with a 'message' key.
       - Create two nodes: 'node_a' (appends "Hello") and 'node_b' (appends " World").
       - Connect them: START -> node_a -> node_b -> END.
       - Compile the graph.

    2. Create 'tests/test_tier3_basic.py':
       - Import the graph from 'basic_graph.py'.
       - Invoke it with an initial state.
       - Assert that the final output is "Hello World".

    OBJECTIVE:
    Verify that the LangGraph library is correctly installed and functioning within our architecture without breaking existing systems.
    """

    task_id = "TIER3-STEP-1"

    print(f"▶️ Delegating {task_id} to Orchestrator...")
    result = await orchestrator.run_task(task_id, task_description)

    if result.phase == "done":
        print("[SUCCESS] STEP 1 COMPLETE. LangGraph is alive.")
    else:
        print(f"[ERROR] STEP 1 FAILED. Phase: {result.phase}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_step1())
