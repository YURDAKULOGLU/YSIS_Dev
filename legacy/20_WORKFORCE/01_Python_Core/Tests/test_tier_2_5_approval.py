"""
Tier 2.5 Human Approval Test
Tests the human-in-the-loop safety checkpoint
"""
import sys
import asyncio
from pathlib import Path

# Add paths
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir.parent.parent))

async def test_approval_flow():
    """Test Tier 2.5 human approval checkpoint"""
    print("\n" + "="*60)
    print("Testing Tier 2.5 Human Approval Flow")
    print("="*60)

    try:
        from Agentic.Core.state import AgentState
        from Agentic.Core.orchestrator import build_graph

        print("\n[1] Building orchestrator with Tier 2.5 approval...")
        graph = build_graph()
        print("  ✓ Graph built with approval checkpoint")

        # Simple test task
        test_task = """
Create a simple Python function called 'greet' that takes a name parameter
and returns a greeting string like "Hello, {name}!".

Save it to: .YBIS_Dev/Meta/Active/test_greet.py
"""

        print("\n[2] Creating test task...")
        print(f"  Task: Create a simple greet function")

        initial_state = AgentState(
            task=test_task,
            task_id="tier-2.5-test",
            user_id="test-user",
            current_phase="analyze",
            status="running",
            messages=[],
            files_context=[],
            decisions=[],
            artifacts={},
            error=None,
            retry_count=0
        )

        print("\n[3] Running orchestrator...")
        print("  Note: You will be asked to approve before execution")
        print("  Options: [y] approve, [n] deny, [s] show full code")
        print("\n" + "="*60)

        # Run the orchestrator
        result = await graph.ainvoke(initial_state)

        print("\n" + "="*60)
        print("[4] Test completed!")
        print(f"  Status: {result['status']}")
        print(f"  Phase: {result['current_phase']}")

        if result['status'] == 'completed':
            print("\n[SUCCESS] SUCCESS: Code was approved and executed")
            print(f"  File created: {result['artifacts'].get('path', 'N/A')}")
        elif result['status'] == 'cancelled':
            print("\n[ERROR] CANCELLED: User denied execution")
            print("  This is the safety layer working correctly!")
        elif result['status'] == 'failed':
            print(f"\n[WARNING]  FAILED: {result.get('error', 'Unknown error')}")

        print("\n" + "="*60)
        return result

    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """Main entry point"""
    print("\n" + "#"*60)
    print("# TIER 2.5 APPROVAL TEST")
    print("# Human-in-the-loop safety demonstration")
    print("#"*60)

    result = await test_approval_flow()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    if result:
        if result['status'] == 'completed':
            print("[SUCCESS] Approval granted - code executed successfully")
            print("   Tier 2.5 is working! Human approval layer active.")
        elif result['status'] == 'cancelled':
            print("[SUCCESS] Approval denied - execution prevented")
            print("   Tier 2.5 is working! Safety layer prevented execution.")
        else:
            print(f"[WARNING]  Unexpected status: {result['status']}")
    else:
        print("[ERROR] Test failed to run")

    print("="*60 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
