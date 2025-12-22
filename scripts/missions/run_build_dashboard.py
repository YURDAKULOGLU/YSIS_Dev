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

async def run_build_dashboard():
    print("🚀 STARTING SELF-CONSTRUCTION TASK: YSIS Control Center (Full Stack)")
    
    # Initialize full stack orchestrator
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
    BUILD A WEB DASHBOARD: 'YSIS Control Center'.
    
    We need a Full-Stack interface to monitor the system status.
    Dependencies: 'flask' is installed.
    
    INSTRUCTIONS:
    1. Create a new directory structure: 'src/dashboard/' and 'src/dashboard/templates/'.
    2. Create 'src/dashboard/app.py':
       - A Flask application running on port 5000.
       - A route '/' that reads the 'Knowledge/LocalDB/tasks.json' file directly.
       - Passes the task data (backlog, in_progress, done) to the template.
    3. Create 'src/dashboard/templates/index.html':
       - A modern, dark-themed HTML dashboard.
       - Use CSS Grid/Flexbox to display 3 columns: Backlog, In Progress, Done.
       - Display tasks as cards within these columns.
       - Add a header "YSIS Control Center".
       - Add a footer showing "Powered by Agentic Core".
       
    OBJECTIVE: 
    Create a functional, visual dashboard to view the system's memory state.
    """
    
    task_id = "FEATURE-DASHBOARD-001"
    
    print(f"▶️ Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("✅ Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_build_dashboard())
