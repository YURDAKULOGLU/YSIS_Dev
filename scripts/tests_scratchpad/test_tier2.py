import sys
sys.path.insert(0, 'Agentic')
from Core.orchestrator_v2 import build_v2_graph
from Core.state import AgentState
import asyncio
import uuid

async def test():
    graph = build_v2_graph()
    state = AgentState(
        task="Create hello.py with a simple hello world function",
        task_id=str(uuid.uuid4()),
        user_id="test",
        current_phase="init",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )
    print("Starting orchestrator...")
    async for event in graph.astream(state, {"configurable": {"thread_id": "test-1"}}):
        print(f"Event: {list(event.keys())}")
    print("Done!")

asyncio.run(test())
