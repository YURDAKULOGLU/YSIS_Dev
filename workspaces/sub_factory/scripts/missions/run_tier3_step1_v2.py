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

async def run_step1_v2():
    print("🏗️ TIER 3 - STEP 1 (RETRY): LangGraph Foundation Fix")

    rag = RAGMemory()
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
        rag_memory=rag
    )

    # KESİN TALİMATLAR
    task_description = """
    CRITICAL FIX: Correctly implement LangGraph.
    The previous attempt failed due to wrong imports and NOT using the library.

    INSTRUCTIONS:
    1. Rewrite 'src/agentic/core/graphs/basic_graph.py' EXACTLY like this:

    from typing import Annotated, TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        message: Annotated[str, "The current message"]

    def node_a(state: State):
        return {"message": state["message"] + " Hello"}

    def node_b(state: State):
        return {"message": state["message"] + " World"}

    def build_basic_graph():
        workflow = StateGraph(State)
        workflow.add_node("node_a", node_a)
        workflow.add_node("node_b", node_b)
        workflow.add_edge(START, "node_a")
        workflow.add_edge("node_a", "node_b")
        workflow.add_edge("node_b", END)
        return workflow.compile()

    2. Update 'tests/test_tier3_basic.py' to use 'build_basic_graph()'.
       - Initial state: {"message": ""}
       - Expected output: " Hello World"

    OBJECTIVE:
    Proove that LangGraph library is integrated and working correctly.
    """

    task_id = "TIER3-STEP-1-FIX"

    print(f"▶️ Delegating {task_id} to Orchestrator...")
    result = await orchestrator.run_task(task_id, task_description)

    if result.phase == "done":
        print("[SUCCESS] STEP 1 FIXED. LangGraph is truly alive.")
    else:
        print(f"[ERROR] STEP 1 STILL FAILED. Phase: {result.phase}")

if __name__ == "__main__":
    asyncio.run(run_step1_v2())
