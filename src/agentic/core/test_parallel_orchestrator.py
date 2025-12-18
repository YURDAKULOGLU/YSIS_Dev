import pytest
import asyncio
from .parallel_orchestrator import ParallelOrchestrator

@pytest.mark.asyncio
async def test_parallel_execution():
    orch = ParallelOrchestrator()
    tasks = [
        {"id": "task_1", "desc": "FE Work"},
        {"id": "task_2", "desc": "BE Work"}
    ]
    
    results = await orch.run_parallel(tasks)
    
    assert len(results) == 2
    assert results[0] == "Done"
    assert results[1] == "Done"
