import asyncio
import os
import sys
import argparse
from pathlib import Path

# Setup path
sys.path.insert(0, os.getcwd())

from src.agentic.core.orchestrator_v3 import OrchestratorV3
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager

async def main():
    parser = argparse.ArgumentParser(description="YBIS Hybrid Orchestrator (Orchestrator + Aider + Sentinel)")
    parser.add_argument("--task-id", help="Specific Task ID to run from BOARD", default=None)
    parser.add_argument("--description", help="Ad-hoc task description", default=None)
    parser.add_argument("--model", help="Override LLM model for Aider", default="ollama/qwen2.5:7b")
    
    args = parser.parse_args()

    # Configure Executor with Model
    executor = AiderExecutor()
    # TODO: Pass args.model to executor configuration if needed in future
    
    print(f"🚀 INITIALIZING HYBRID ENGINE...")
    print(f"   - Model: {args.model}")
    print(f"   - Accelerator: Aider")
    
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=executor,
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
        sandbox_root=".sandbox_hybrid" 
    )
    
    if args.task_id and args.description:
        # Run specific ad-hoc task
        print(f"▶️ Running Ad-Hoc Task: {args.task_id}")
        await orchestrator.run_task(args.task_id, args.description)
        
    elif args.task_id:
        # Run specific task from board (logic would be in Orchestrator.run_task if it fetched from board)
        print("Running specific board task not yet fully implemented in CLI args, running next...")
        await orchestrator.run_next_task()
        
    else:
        # Run next from board
        print(f"▶️ Polling TASK_BOARD for next task...")
        await orchestrator.run_next_task()

if __name__ == "__main__":
    asyncio.run(main())
