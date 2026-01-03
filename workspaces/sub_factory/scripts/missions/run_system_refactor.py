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

async def run_system_refactor():
    print("[INFO] STARTING SYSTEMIC REFACTOR: Single Source of Truth for Paths")

    # Initialize components
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
    SYSTEMIC REFACTOR: Implement Centralized Configuration.

    We have a recurring issue with file paths (e.g. finding 'tasks.db') being hardcoded or calculated incorrectly in multiple files.
    We need a 'Single Source of Truth'.

    INSTRUCTIONS:
    1. Create a new file 'src/agentic/core/config.py'.
       - It must dynamically detect the PROJECT_ROOT (using pathlib).
       - It must define constants:
         - DATA_DIR = PROJECT_ROOT / "Knowledge" / "LocalDB"
         - TASKS_DB_PATH = DATA_DIR / "tasks.db"
         - CHROMA_DB_PATH = DATA_DIR / "chroma_db"

    2. Refactor 'src/dashboard/app.py':
       - Import constants from 'src.agentic.core.config'.
       - REMOVE all 'os.path' calculations.
       - Use 'TASKS_DB_PATH' directly.

    3. Refactor 'src/agentic/core/plugins/task_board_manager.py':
       - Import constants from 'src.agentic.core.config'.
       - Use 'TASKS_DB_PATH' and 'PROJECT_ROOT' directly.

    4. Refactor 'src/agentic/core/plugins/rag_memory.py':
       - Import constants from 'src.agentic.core.config'.
       - Use 'CHROMA_DB_PATH' directly.

    OBJECTIVE:
    Eliminate all manual path calculations and ensure every component uses the exact same path definitions.
    """

    task_id = "REFACTOR-001"

    print(f"▶️ Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("[SUCCESS] Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_system_refactor())
