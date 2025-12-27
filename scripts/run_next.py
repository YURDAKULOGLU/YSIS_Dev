import asyncio
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Setup path
sys.path.insert(0, os.getcwd())

# Import the NEW Graph Orchestrator
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.protocols import TaskState

# Plugins
from src.agentic.core.plugins.smart_planner import SmartPlanner
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.rag_memory import RAGMemory
from agentic import mcp_server

async def run_next_step():
    print(f"YBIS LANGGRAPH RUNNER STARTING...")
    
    # Initialize components
    rag_memory = RAGMemory()
    
    # Using the NEW Graph implementation
    orchestrator = OrchestratorGraph(
        planner=SmartPlanner(),
        executor=AiderExecutorEnhanced(),
        verifier=SentinelVerifierEnhanced(),
        artifact_gen=ArtifactGenerator()
    )
    
    # ATOMIC CLAIM: Race-condition safe for multi-agent systems
    import socket
    worker_id = f"claude-{socket.gethostname()}"

    target_raw = mcp_server.claim_next_task(worker_id)
    target_payload = json.loads(target_raw)
    target_task = target_payload.get("task")

    if not target_task:
        print("[IDLE] No tasks to run.")
        return

    print(f"[CLAIMED] Task: {target_task['id']} by {worker_id}")

    # Build Initial State
    sandbox_root = ".sandbox_worker"
    task_id = target_task["id"]
    
    initial_state = TaskState(
        task_id=task_id,
        task_description=target_task["goal"] + "\n" + target_task.get("details", ""),
        artifacts_path=os.path.join(sandbox_root, task_id)
    )

    try:
        # Run the Graph
        # Use model_dump() to pass a clean dict to LangGraph
        final_state = await orchestrator.run_task(initial_state.model_dump())
        
        # Update Board based on final state
        # Handle both dict and Pydantic object for robustness
        phase = getattr(final_state, "phase", "unknown") if not isinstance(final_state, dict) else final_state.get("phase", "unknown")
        
        status = "DONE" if phase == "done" else "FAILED"
        print(f"Task Finished with status: {status}")
        
        mcp_server.update_task_status(task_id, "COMPLETED" if status == "DONE" else "FAILED")
        
    except Exception as e:
        print(f"Critical Graph Failure: {e}")
        import traceback
        traceback.print_exc()
        mcp_server.update_task_status(task_id, "FAILED")

if __name__ == "__main__":
    asyncio.run(run_next_step())
