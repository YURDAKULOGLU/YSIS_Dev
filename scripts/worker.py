import asyncio
import os
import sys
import logging
import traceback
from pathlib import Path
from typing import Dict, Any

# Setup Path
sys.path.insert(0, os.getcwd())

# Import The Brain
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph

# Import The Body Parts (Plugins)
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.model_router import default_router

# Import Task Manager
from src.agentic.core.plugins.task_board_manager import TaskBoardManager

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [WORKER] - %(message)s',
    handlers=[
        logging.FileHandler("worker.out"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def worker_loop():
    logger.info("YBIS AUTONOMOUS WORKER STARTED (LangGraph Engine)")
    
    planner = SimplePlanner()
    executor = AiderExecutorEnhanced(router=default_router)
    verifier = SentinelVerifierEnhanced()
    artifact_gen = ArtifactGenerator()
    
    board = TaskBoardManager()
    
    while True:
        try:
            tasks_data = await board._read_db()
            active_task = None
            
            if tasks_data.get("in_progress"):
                active_task = tasks_data["in_progress"][0]
            elif tasks_data.get("backlog"):
                next_task = tasks_data["backlog"][0]
                await board.update_task_status(next_task["id"], "IN_PROGRESS", {})
                active_task = next_task
            
            if active_task:
                task_id = active_task["id"]
                goal = active_task["goal"]
                details = active_task.get("details", "")
                
                logger.info(f">>> EXECUTING TASK: {task_id}")
                
                graph_system = OrchestratorGraph(
                    planner=planner,
                    executor=executor,
                    verifier=verifier,
                    artifact_gen=artifact_gen
                )
                
                state = {
                    "task_id": task_id,
                    "task_description": f"{goal}\n{details}",
                    "phase": "PLAN",
                    "plan": None,
                    "code_result": None,
                    "verification": None,
                    "files_modified": [],
                    "error_history": [],
                    "retry_count": 0,
                    "max_retries": 3,
                    "quality_score": 0.0,
                    "artifacts_path": f".sandbox_worker/{task_id}",
                    "final_status": "UNKNOWN"
                }
                
                try:
                    final_state = await graph_system.run_task(state)
                    phase = final_state.get('phase', 'unknown')
                    
                    if phase == "done":
                        logger.info(f"<<< TASK SUCCESS: {task_id}")
                        await board.update_task_status(task_id, "DONE", {})
                    else:
                        logger.error(f"<<< TASK FAILED/INCOMPLETE: {task_id}")
                        await board.update_task_status(task_id, "FAILED", {})
                        
                except Exception as e:
                    logger.error(f"Graph Execution Error: {e}")
                    logger.error(traceback.format_exc())
                    # NO MORE DOUBLE BRACES HERE
                    await board.update_task_status(task_id, "FAILED", {})

                await asyncio.sleep(5)
            else:
                await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"CRITICAL WORKER FAILURE: {e}")
            logger.error(traceback.format_exc())
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(worker_loop())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user.")
