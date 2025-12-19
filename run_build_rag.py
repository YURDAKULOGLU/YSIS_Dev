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

async def run_build_rag():
    print("🚀 STARTING SELF-CONSTRUCTION TASK: Build RAG Memory System")
    
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager()
    )
    
    task_description = """
    BUILD A NEW FEATURE: RAG Memory System (Vector Database).
    
    We need to enable the system to remember and search past code/docs using Vector Embeddings.
    Dependencies 'chromadb' and 'sentence-transformers' are already installed.
    
    INSTRUCTIONS:
    1. Create a new file 'src/agentic/core/plugins/rag_memory.py'.
    2. Implement a class 'RAGMemory' that:
       - Initializes a ChromaDB client (persistent, at 'Knowledge/LocalDB/chroma_db').
       - Uses 'sentence-transformers/all-MiniLM-L6-v2' for embeddings.
       - Has a method 'add_text(id: str, text: str, metadata: dict)'.
       - Has a method 'query(text: str, n_results: int = 3) -> List[str]'.
    3. Modify 'src/agentic/core/orchestrator_v3.py':
       - Import the new 'RAGMemory' class.
       - Initialize it in the Orchestrator's __init__ method (optional parameter).
       - (Just initialization for now, full integration into the loop comes later).
       
    OBJECTIVE: 
    Create the functional components for Long-Term Vector Memory.
    """
    
    task_id = "FEATURE-RAG-001"
    
    print(f"▶️ Delegating Task {task_id} to Orchestrator...")
    await orchestrator.run_task(task_id, task_description)
    print("✅ Orchestrator finished execution.")

if __name__ == "__main__":
    asyncio.run(run_build_rag())
