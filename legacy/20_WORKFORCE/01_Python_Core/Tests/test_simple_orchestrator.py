"""
Simple Orchestrator Test - Tier 2
Tests basic LangGraph flow without complex agents
"""
import sys
import asyncio
from pathlib import Path

# Add paths
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir.parent.parent))

async def test_simple_flow():
    """Test simple LangGraph flow"""
    print("\n" + "="*60)
    print("Testing Simple Orchestrator Flow")
    print("="*60)

    try:
        # Import components
        from Agentic.Core.state import AgentState
        from langgraph.graph import StateGraph, END

        print("\n[1] Creating simple graph...")

        # Simple test nodes
        def start_node(state: AgentState) -> AgentState:
            print("  [START] Task:", state["task"])
            state["decisions"].append("Started task")
            state["current_phase"] = "process"
            return state

        def process_node(state: AgentState) -> AgentState:
            print("  [PROCESS] Processing...")
            state["decisions"].append("Processed task")
            state["current_phase"] = "finish"
            state["status"] = "completed"
            return state

        # Build graph
        workflow = StateGraph(AgentState)
        workflow.add_node("start", start_node)
        workflow.add_node("process", process_node)

        workflow.set_entry_point("start")
        workflow.add_edge("start", "process")
        workflow.add_edge("process", END)

        graph = workflow.compile()

        print("  OK: Graph created")

        # Test execution
        print("\n[2] Running graph...")

        initial_state = AgentState(
            task="Test simple flow",
            task_id="test-1",
            user_id="test-user",
            current_phase="start",
            status="running",
            messages=[],
            files_context=[],
            decisions=[],
            artifacts={},
            error=None,
            retry_count=0
        )

        result = await graph.ainvoke(initial_state)

        print("  OK: Graph executed")
        print(f"  Status: {result['status']}")
        print(f"  Decisions: {result['decisions']}")

        assert result["status"] == "completed"
        assert len(result["decisions"]) == 2

        print("\n" + "="*60)
        print("SUCCESS: Simple orchestrator working!")
        print("="*60)
        return True

    except Exception as e:
        print(f"\nFAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_with_ollama():
    """Test with actual Ollama model"""
    print("\n" + "="*60)
    print("Testing Ollama Integration")
    print("="*60)

    try:
        from langchain_ollama import ChatOllama

        print("\n[1] Connecting to Ollama...")
        llm = ChatOllama(
            model="llama3.2:3b",
            base_url="http://localhost:11434"
        )

        print("  OK: Connected")

        print("\n[2] Testing simple completion...")
        result = await llm.ainvoke("Say 'Hello from YBIS_Dev!' in one short sentence.")

        print(f"  OK: Got response ({len(result.content)} chars)")
        print(f"  Response: {result.content[:100]}...")

        print("\n" + "="*60)
        print("SUCCESS: Ollama integration working!")
        print("="*60)
        return True

    except Exception as e:
        print(f"\nSKIP: Ollama not available - {e}")
        return None

async def main():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# YBIS_Dev Tier 2 - Orchestrator Tests")
    print("#"*60)

    results = {}

    # Test 1: Simple graph
    results["simple_graph"] = await test_simple_flow()

    # Test 2: Ollama
    results["ollama"] = await test_with_ollama()

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v is True)
    skipped = sum(1 for v in results.values() if v is None)

    for name, result in results.items():
        status = "PASS" if result is True else ("SKIP" if result is None else "FAIL")
        print(f"  {name:20s} [{status}]")

    print(f"\nPassed: {passed}/{len(results)}")
    if skipped > 0:
        print(f"Skipped: {skipped} (Ollama might not be running)")

    print("\n" + "="*60)

    if all(v in [True, None] for v in results.values()):
        print("Orchestrator is ready!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
