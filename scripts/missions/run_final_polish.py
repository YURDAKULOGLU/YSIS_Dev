import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, os.getcwd())

from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.rag_aware_planner import RAGAwarePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.protocols import TaskState

async def run_final_polish():
    print("[SUCCESS] BOOTSTRAP PHASE 4: Final Polish & Dashboard (T-105)")

    orchestrator = OrchestratorGraph(
        planner=RAGAwarePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier()
    )

    task_description = """
    FINAL POLISH for Beta Release.

    OBJECTIVE: Make the system visually representable and stable.

    REQUIRED DELIVERABLES:
    1. 'src/dashboard/app.py': Enhanced Streamlit UI.
       - Show 'Current Mission' status.
       - Show 'Sentinel Logs' (Warnings/Errors).
       - Live graph visualization of Orchestrator state.
    2. 'SYSTEM_STATE.md': Update with the completed Phase 1, 2, 3 and current Phase 4.
    3. 'tests/test_tier4_e2e.py': A simple end-to-end test that ensures the Graph can run.

    CONSTRAINTS:
    - No placeholders in Dashboard.
    - Sentinel will verify this. Ensure tests pass.
    """

    task_id = "T-105-POLISH"
    artifacts_path = os.path.join(".sandbox", "hybrid", task_id)
    os.makedirs(artifacts_path, exist_ok=True)

    state: TaskState = {
        "task_id": task_id,
        "task_description": task_description,
        "phase": "init",
        "plan": None,
        "code_result": None,
        "verification": None,
        "retry_count": 0,
        "max_retries": 2,
        "error_history": [],
        "artifacts_path": artifacts_path
    }

    print(f"-> Executing Final Polish {task_id}...")
    await orchestrator.ainvoke(state)

if __name__ == "__main__":
    asyncio.run(run_final_polish())
