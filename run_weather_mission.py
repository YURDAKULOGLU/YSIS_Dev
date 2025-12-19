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

async def run_mission():
    print("🌤️ STARTING NEW MISSION: Weather Stats Engine")
    
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
    Create a Weather Data Processing system.
    
    1. Create 'src/utils/weather_stats.py':
       - Define a class 'TemperatureProcessor'.
       - Method 'get_average(temps: list[float]) -> float': Returns average. Raises ValueError if list is empty.
       - Method 'get_extremes(temps: list[float]) -> tuple[float, float]': Returns (min, max). Raises ValueError if list is empty.
       
    2. Create 'tests/test_weather_stats.py':
       - Use pytest.
       - Test 'get_average' with [10, 20, 30] -> 20.0.
       - Test 'get_extremes' with [5, -2, 10] -> (-2, 10).
       - Test empty list raises ValueError for both methods.
    """
    
    task_id = "MISSION-WEATHER-001"
    
    print(f"▶️ Launching Task {task_id}...")
    await orchestrator.run_task(task_id, task_description)
    print("✅ Mission finished.")

if __name__ == "__main__":
    asyncio.run(run_mission())
