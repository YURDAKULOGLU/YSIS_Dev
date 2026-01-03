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

async def run_step1_v3():
    print("🏗️ TIER 3 - STEP 1 (FINAL ATTEMPT): LangGraph Clean Slate")

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
    Create two NEW files from scratch. DO NOT reuse old broken code.

    1. File: 'src/agentic/core/graphs/basic_graph.py'
    Content:
    from typing import Annotated, TypedDict
    from langgraph.graph import StateGraph, START, END

    class State(TypedDict):
        message: str

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

    2. File: 'tests/test_tier3_basic.py'
    Content:
    import pytest
    from src.agentic.core.graphs.basic_graph import build_basic_graph

    def test_hello_world_graph():
        graph = build_basic_graph()
        initial_state = {"message": ""}
        result = graph.invoke(initial_state)
        assert result["message"] == " Hello World"
    """

    task_id = "TIER3-STEP-1-FINAL"

    print(f"▶️ Delegating {task_id} to Orchestrator...")
    result = await orchestrator.run_task(task_id, task_description)

    if result.phase == "done":
        print("[SUCCESS] STEP 1 SUCCESSFUL. LangGraph is integrated.")
    else:
        print(f"[ERROR] STEP 1 FAILED. Phase: {result.phase}")

if __name__ == "__main__":
    asyncio.run(run_step1_v3())
