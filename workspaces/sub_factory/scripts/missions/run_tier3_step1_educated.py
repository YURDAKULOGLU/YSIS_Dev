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

async def run_step1_educated():
    print("🎓 TIER 3 - STEP 1 (EDUCATED): Teaching LangGraph to Aider")

    rag = RAGMemory()
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
        rag_memory=rag
    )

    # LangGraph Kılavuzu
    langgraph_docs = """
    LIBRARY DOCUMENTATION (LangGraph):
    ----------------------------------
    LangGraph is a library for building stateful, multi-actor applications with LLMs.

    Key Concepts:
    1. State: A TypedDict that holds the graph's memory.
    2. Nodes: Functions that take the State and return an update to the State.
    3. Edges: Connect nodes. 'START' is the entry point, 'END' is the exit.

    Minimal Example Code:
    ```python
    from typing import TypedDict, Annotated
    from langgraph.graph import StateGraph, START, END

    # 1. Define State
    class GraphState(TypedDict):
        log: list[str]

    # 2. Define Nodes
    def step_1(state: GraphState):
        return {"log": ["Step 1 Done"]}

    def step_2(state: GraphState):
        return {"log": ["Step 2 Done"]}

    # 3. Build Graph
    def build_graph():
        builder = StateGraph(GraphState)
        builder.add_node("step_1", step_1)
        builder.add_node("step_2", step_2)
        builder.add_edge(START, "step_1")
        builder.add_edge("step_1", "step_2")
        builder.add_edge("step_2", END)
        return builder.compile()
    ```
    ----------------------------------
    """

    task_description = f"""
    {langgraph_docs}

    TASK:
    Based on the DOCUMENTATION above (do not ignore it), create a valid LangGraph implementation.

    1. Overwrite 'src/agentic/core/graphs/basic_graph.py':
       - Create a graph with State containing 'message' (str).
       - Node 'node_a': appends " Hello" to message.
       - Node 'node_b': appends " World" to message.
       - Edges: START -> node_a -> node_b -> END.
       - Export a function 'build_basic_graph()' that returns the compiled app.

    2. Overwrite 'tests/test_tier3_basic.py':
       - Import 'build_basic_graph'.
       - Run: app = build_basic_graph()
       - Run: result = app.invoke({{"message": ""}})
       - Assert result["message"] == " Hello World".

    OBJECTIVE:
    Demonstrate that the system can learn new libraries from context.
    """

    task_id = "TIER3-STEP-1-EDU"

    print(f"▶️ Delegating {task_id} to Orchestrator...")
    result = await orchestrator.run_task(task_id, task_description)

    if result.phase == "done":
        print("[SUCCESS] STEP 1 SUCCESSFUL. Aider learned LangGraph.")
    else:
        print(f"[ERROR] STEP 1 FAILED. Phase: {result.phase}")

if __name__ == "__main__":
    asyncio.run(run_step1_educated())
