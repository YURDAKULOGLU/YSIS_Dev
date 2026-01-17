import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.getcwd())

from src.agentic.core.orchestrator_v3 import OrchestratorV3
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager

async def run_bootstrap_test():
    print("[INFO] STARTING BOOTSTRAP TEST: Orchestrator V3")

    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager()
    )

    task_description = """
    Create a new python file named 'src/utils/math_helper.py'.
    The file should contain:
    1. A function 'calculate_factorial(n)' that returns the factorial of n using recursion.
    2. A main block that prints 'Factorial of 5 is: {result}'.
    """

    task_id = "BOOTSTRAP-001"

    print(f"-> Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("[SUCCESS] Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_bootstrap_test())
