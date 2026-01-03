import asyncio
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.getcwd())

from src.agentic.core.plugins.rag_aware_planner import RAGAwarePlanner
from src.agentic.core.protocols import Plan

# Mock classes to avoid real API calls
class MockPlanner:
    async def plan(self, task, context):
        print(f"[MockPlanner] Received context keys: {list(context.keys())}")
        if "relevant_history" in context:
            print(f"[MockPlanner] RAG Context found: {context['relevant_history'][:50]}...")
        return Plan(objective="Test", steps=[], files_to_modify=[])

    def name(self): return "MockPlanner"

class MockRAG:
    def query(self, text, n_results=3):
        return ["Previously we solved this by using X", "Another similar task was Y"]

async def test_rag_integration():
    print("Testing RAG Aware Planner Integration...")

    # Setup
    mock_planner = MockPlanner()
    mock_rag = MockRAG()
    rag_planner = RAGAwarePlanner(base_planner=mock_planner, rag_memory=mock_rag)

    # Execute
    task = "Fix the login bug"
    context = {"user": "tester"}

    await rag_planner.plan(task, context)
    print("Test Complete.")

if __name__ == "__main__":
    asyncio.run(test_rag_integration())
