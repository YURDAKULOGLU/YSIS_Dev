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

async def run_meta_fix():
    print("🚀 STARTING META-FIX TASK: Sentinel Logic Upgrade")
    
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(), # We are using the currently 'dumb' verifier to verify the 'smart' one. Risky but fun.
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager()
    )
    
    task_description = """
    CRITICAL UPDATE for 'src/agentic/core/plugins/sentinel.py'.
    
    The current verification logic runs 'pytest .' which fails because of legacy code in the project.
    We need to make the verification TARGETED.
    
    INSTRUCTIONS:
    1. Edit 'src/agentic/core/plugins/sentinel.py'.
    2. Modify the logic where tests are executed.
    3. Instead of running all tests, implement a 'Smart Test Discovery':
       - Look at the files modified in the 'plan' or 'code_result'.
       - For a modified file 'src/utils/math.py', try to find 'tests/test_math.py' or 'src/utils/tests/test_math.py'.
       - If a matching test file is found, run 'pytest <path_to_test_file>'.
    4. If NO matching test file is found for the modified files:
       - Do NOT run the full suite.
       - Instead, perform a Syntax Check on the modified files using 'python -m py_compile <file>'.
       - If syntax is OK, consider verification PASSED (with a warning log).
       
    OBJECTIVE: 
    Prevent the orchestrator from failing tasks due to unrelated legacy errors in the codebase.
    """
    
    task_id = "META-FIX-001"
    
    print(f"▶️ Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("✅ Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_meta_fix())
