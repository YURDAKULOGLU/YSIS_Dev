import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.getcwd())

from src.agentic.core.orchestrator_v3 import OrchestratorV3
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager

async def run_memory_fix():
    print("[INFO] STARTING SELF-REPAIR TASK: Memory System Fix")

    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager() # This is currently broken, but we are fixing it!
    )

    task_description = """
    CRITICAL FIX for 'src/agentic/core/plugins/task_board_manager.py'.

    The current implementation has a HARDCODED absolute path ('c:/Projeler/YBIS/...') which is WRONG.
    It causes [TaskBoard] JSON DB not found errors.

    INSTRUCTIONS:
    1. Edit 'src/agentic/core/plugins/task_board_manager.py'.
    2. In the __init__ method:
       - Remove the hardcoded 'self.meta_dir' path.
       - Use 'os.getcwd()' to find the project root dynamically.
       - Set the new database path to: project_root / 'Knowledge' / 'LocalDB'.
       - Ensure the directory 'Knowledge/LocalDB' exists (create it if missing using os.makedirs).
       - Set 'self.db_path' to 'tasks.db' inside that directory.
       - Set 'self.md_path' to 'TASK_BOARD.md' inside that directory.

    OBJECTIVE:
    Enable the system to reliably save and load tasks from a local JSON database within the project structure.
    """

    task_id = "SELF-REPAIR-001"

    print(f"-> Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("[SUCCESS] Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_memory_fix())
