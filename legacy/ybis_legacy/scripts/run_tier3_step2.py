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

async def run_step2():
    print("[INFO] TIER 3 - STEP 2: The Brain Transplant (Orchestrator -> LangGraph)")

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
    IMPLEMENT LangGraph NODES in 'src/agentic/core/graphs/orchestrator_graph.py'.

    We want to port the logic from 'OrchestratorV3._phase_plan', '_phase_execute', '_phase_verify' into LangGraph nodes.

    INSTRUCTIONS:
    1. Edit 'src/agentic/core/graphs/orchestrator_graph.py'.
    2. Add imports:
       from src.agentic.core.protocols import TaskState
       from datetime import datetime
    3. Implement async node methods inside 'OrchestratorGraph' class:

       async def planner_node(self, state: TaskState):
           # Call self.planner.plan(...)
           # Update state.plan
           # Return {"plan": state.plan} (LangGraph merges dicts)

       async def executor_node(self, state: TaskState):
           # Call self.executor.execute(...)
           # Update state.code_result

       async def verifier_node(self, state: TaskState):
           # Call self.verifier.verify(...)
           # Update state.verification

    4. Implement '_build_graph(self)':
       - builder = StateGraph(TaskState)
       - Add nodes: 'planner', 'executor', 'verifier'
       - Add edges: START -> 'planner' -> 'executor' -> 'verifier' -> END
       - return builder.compile()

    5. Implement 'invoke(self, input_state: TaskState)':
       - return await self.workflow.ainvoke(input_state)

    OBJECTIVE:
    Wrap our existing plugins in a LangGraph workflow.
    """

    task_id = "TIER3-STEP-2"

    print(f"-> Delegating {task_id} to Orchestrator...")
    result = await orchestrator.run_task(task_id, task_description)

    if result.phase == "done":
        print("[SUCCESS] STEP 2 SUCCESSFUL. Nodes are wired.")
    else:
        print(f"[ERROR] STEP 2 FAILED. Phase: {result.phase}")

if __name__ == "__main__":
    asyncio.run(run_step2())
