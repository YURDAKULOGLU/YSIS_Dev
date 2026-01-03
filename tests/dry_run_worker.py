import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, os.getcwd())

async def test_worker_init():
    print("[DRY_RUN] Attempting to import worker modules...")
    try:
        from src.agentic.core.orchestrator_v3 import OrchestratorV3
        from src.agentic.core.plugins.sentinel import SentinelVerifier
        from src.agentic.core.plugins.aider_executor import AiderExecutor
        from src.agentic.core.plugins.simple_planner import SimplePlanner
        from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
        from src.agentic.core.plugins.task_board_manager import TaskBoardManager
        from src.agentic.core.plugins.rag_memory import RAGMemory

        print("[DRY_RUN] Imports successful.")

        print("[DRY_RUN] Initializing SentinelVerifier...")
        verifier = SentinelVerifier()
        print(f"[DRY_RUN] Sentinel Name: {verifier.name()}")

        print("[DRY_RUN] Initializing OrchestratorV3...")
        orchestrator = OrchestratorV3(
            planner=SimplePlanner(),
            executor=AiderExecutor(),
            verifier=verifier,
            artifact_gen=ArtifactGenerator(),
            task_board=TaskBoardManager(),
            rag_memory=RAGMemory(),
            sandbox_root=".sandbox_dry_run"
        )

        print("[DRY_RUN] Orchestrator Status:", orchestrator.get_status())
        print("[DRY_RUN] [OK] Worker initialization test PASSED.")

    except ImportError as e:
        print(f"[DRY_RUN] [ERROR] Import Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[DRY_RUN] [ERROR] Runtime Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_worker_init())
