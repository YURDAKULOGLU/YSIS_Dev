import asyncio
import os
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, os.getcwd())

from Agentic.Core.orchestrator_v3 import OrchestratorV3
from Agentic.Core.plugins.simple_planner import SimplePlanner
from Agentic.Core.plugins.aider_executor import AiderExecutor
from Agentic.Core.plugins.sentinel import SentinelVerifier
from Agentic.Core.plugins.artifact_generator import ArtifactGenerator
from Agentic.Core.plugins.task_board_manager import TaskBoardManager

async def main():
    print("🚀 INITIALIZING HYBRID SYSTEM (Orchestrator + Aider + Sentinel)...")
    
    # 1. Initialize Hybrid Components
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),         # Brain: Simple for now
        executor=AiderExecutor(),        # Hands: Aider (The Specialist)
        verifier=SentinelVerifier(),     # Eyes: Sentinel (The Guardian)
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
        sandbox_root=".sandbox_hybrid"   # Distinct sandbox
    )
    
    print(f"✅ System Ready: {orchestrator.get_status()}")
    
    # 2. Define a Test Task
    task_id = "TASK-HYBRID-001"
    description = "Create a python file named 'hybrid_success.py' that prints 'Hybrid System Online!'."
    
    # 3. Run the Task
    print(f"\n▶️ Running Task: {description}")
    result = await orchestrator.run_task(task_id, description)
    
    # 4. Report
    if result.phase == "done":
        print(f"\n✅ SUCCESS! Task completed. Artifacts in {result.artifacts_path}")
    else:
        print(f"\n❌ FAILURE! Task failed with error: {result.error}")

if __name__ == "__main__":
    asyncio.run(main())
