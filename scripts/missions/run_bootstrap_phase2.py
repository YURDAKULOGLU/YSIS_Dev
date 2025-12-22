import asyncio
import sys
import os
from datetime import datetime

# Ensure root is in path
sys.path.insert(0, os.getcwd())

from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.rag_aware_planner import RAGAwarePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.protocols import TaskState

async def run_bootstrap_phase2():
    print("🚀 BOOTSTRAP PHASE 2: Docker Sandbox Implementation (T-103)")
    
    # Setup Orchestrator with the new RAG Aware Planner
    orchestrator = OrchestratorGraph(
        planner=RAGAwarePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier()
    )
    
    # Task Description from BOOTSTRAP_PROTOCOL.md
    task_description = """
    IMPLEMENT Phase 2 of the Bootstrap Protocol: Docker Sandbox (T-103).
    
    OBJECTIVE: Create a standardized, isolated execution environment for tasks.
    
    REQUIRED DELIVERABLES:
    1. 'docker/Dockerfile.sandbox': Python 3.12 slim with git, aider, and pytest.
    2. 'docker/docker-compose.yml': To manage the sandbox container.
    3. 'src/agentic/core/plugins/docker_executor.py': A wrapper that runs code inside the Docker container.
    4. '.sandbox/PLAN.md': Detailed execution plan for this phase.
    
    CONSTRAINTS:
    - Follow ARCHITECTURE_V2.md.
    - Use absolute paths from src.agentic.core.config.
    - No emojis.
    
    This is a self-improvement task. Use the existing Aider and Sentinel to build this.
    """
    
    task_id = "T-103-DOCKER"
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
        "max_retries": 3,
        "error_history": [],
        "artifacts_path": artifacts_path
    }

    print(f"▶️ Invoking Orchestrator for {task_id}...")
    final_state = await orchestrator.ainvoke(state)
    
    if final_state["phase"] == "done":
        print(f"✅ PHASE 2 SUCCESSFUL. Docker Sandbox is ready.")
    else:
        print(f"❌ PHASE 2 FAILED. Phase: {final_state['phase']}")
        if final_state.get("error_history"):
            print(f"Errors: {final_state['error_history'][-1]}")

if __name__ == "__main__":
    asyncio.run(run_bootstrap_phase2())
