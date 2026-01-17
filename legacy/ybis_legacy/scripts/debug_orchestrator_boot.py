import sys
import os

# Add current directory to path so we can import src
sys.path.insert(0, os.getcwd())

print("Attempting to import OrchestratorV3...")
try:
    from src.agentic.core.orchestrator_v3 import OrchestratorV3
    from src.agentic.core.plugins.simple_planner import SimplePlanner
    from src.agentic.core.plugins.aider_executor import AiderExecutor
    from src.agentic.core.plugins.sentinel import SentinelVerifier
    from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
    from src.agentic.core.plugins.task_board_manager import TaskBoardManager

    print("Imports successful!")

    print("Initializing Orchestrator...")
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager()
    )
    print("Orchestrator initialized successfully!")
    print("Core System Status: ONLINE")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
