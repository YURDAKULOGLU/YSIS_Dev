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

async def run_bootstrap_phase3():
    print("🌍 BOOTSTRAP PHASE 3: Open-SWE Integration (T-104)")
    
    orchestrator = OrchestratorGraph(
        planner=RAGAwarePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier()
    )
    
    task_description = """
    IMPLEMENT Phase 3 of the Bootstrap Protocol: Open-SWE Plugin (T-104).
    
    OBJECTIVE: Grant the system the ability to interact with GitHub and solve external issues.
    
    REQUIRED DELIVERABLES:
    1. 'src/agentic/core/plugins/builtin/open_swe.py': A plugin that can:
       - Fetch GitHub issues (using PyGithub or requests).
       - Contextualize the issue for the Planner.
       - Submit a Pull Request after a successful Sentinel verification.
    2. Integration with 'src/agentic/core/auto_dispatcher.py' to handle 'external' missions.
    
    CONSTRAINTS:
    - Use 'docker_executor.py' (built in Phase 2) for running external code.
    - No mock data for logic, but use env variables for tokens (GITHUB_TOKEN).
    - Follow ARCHITECTURE_V2.md.
    """
    
    task_id = "T-104-OPEN-SWE"
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

    print(f"▶️ Starting Phase 3 construction {task_id}...")
    await orchestrator.ainvoke(state)

if __name__ == "__main__":
    asyncio.run(run_bootstrap_phase3())
