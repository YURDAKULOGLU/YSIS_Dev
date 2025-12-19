import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, os.getcwd())

from src.agentic.core.orchestrator_v3 import OrchestratorV3
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager
from src.agentic.core.plugins.rag_memory import RAGMemory

async def run_polish():
    print("🚀 STARTING FINAL POLISH: Config Unification & Cleanup")
    
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
    SYSTEM POLISH TASK: Eliminate Hardcoded Paths & Clean Root Directory.
    
    1. UPDATE 'src/agentic/core/config.py':
       - Add 'CONSTITUTION_PATH = PROJECT_ROOT / "00_GENESIS" / "YBIS_CONSTITUTION.md"'
       
    2. REFACTOR 'src/agentic/core/plugins/simple_planner.py':
       - Import 'CONSTITUTION_PATH' from config.
       - Use this constant instead of hardcoded strings in '_read_constitution'.
       
    3. CLEANUP ROOT DIRECTORY (Shell Command):
       - Create directory '_Archive/Legacy_Scripts'.
       - Move the following legacy files to that archive:
         'run_hybrid_test.py', 'run_meta_optimization.py', 'run_system_update.py',
         'test_capabilities.py', 'test_crew.py', 'test_mcp.py', 
         'test_migrate_to_crewai.py', 'test_orchestrator_dogfooding.py',
         'test_qa_fix.py', 'test_qa_loop.py', 'test_tier2.py', 'test_tier2_quick.py',
         'debug_ollama_models.py', 'debug_writer.py', 'error_parser.py'
       - DO NOT move 'run_build_dashboard.py', 'run_final_polish.py', 'orchestrator_main.py'.
       
    OBJECTIVE: 
    Leave the project in a pristine state with centralized configuration and zero clutter.
    """
    
    task_id = "POLISH-001"
    
    print(f"▶️ Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("✅ Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_polish())
