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

async def run_test_fix_mission():
    print("🧹 MISSION: Core Test Health Restoration (T-103.1)")
    
    orchestrator = OrchestratorGraph(
        planner=RAGAwarePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier()
    )
    
    task_description = """
    FIX ALL BROKEN CORE TESTS in 'tests/' folder.
    
    CURRENT PROBLEMS:
    1. ImportErrors: Many tests use 'Agentic.Core' or 'Core'. Update them to use 'src.agentic.core'.
    2. Missing Async: Some async tests fail because pytest-asyncio is not configured or functions aren't decorated.
    3. Mock Inconsistencies: 'test_orchestrator_graph.py' had a signature mismatch. Ensure all mocks match 'src/agentic/core/protocols.py'.
    
    INSTRUCTIONS:
    - Focus on files in 'tests/' and 'src/agentic/core/plugin_system/tests/'.
    - DO NOT touch 'legacy/'.
    - Ensure 'pytest' runs without errors for these core files.
    """
    
    task_id = "T-103.1-TEST-FIX"
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

    print(f"▶️ Starting Test Fix Mission {task_id}...")
    await orchestrator.ainvoke(state)

if __name__ == "__main__":
    asyncio.run(run_test_fix_mission())
