"""
Test QA feedback loop with a SIMPLE task (should pass easily)
"""
import asyncio
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Agentic'))

async def main():
    print("=== QA FEEDBACK LOOP TEST ===")
    print("-" * 60)

    from Agentic.Core.orchestrator_v2 import build_v2_graph
    from Agentic.Core.state import AgentState

    # SIMPLE task that should work
    task = """Create a simple Python function that adds two numbers.

File: utils/math_helpers.py

Function signature:
def add(a: int, b: int) -> int:
    '''Add two numbers and return the result'''
    return a + b

Requirements:
- Must have type hints
- Must have docstring
- Must be syntactically correct
- No external dependencies needed"""

    print(f"\n[TASK]\n{task}\n")

    initial_state = AgentState(
        task=task,
        task_id=str(uuid.uuid4()),
        user_id="qa-loop-test",
        current_phase="init",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )

    print("[START] Testing QA feedback loop...\n")

    graph = build_v2_graph()

    try:
        async for event in graph.astream(initial_state, {"configurable": {"thread_id": "qa-loop-test"}}):
            for node_name, node_state in event.items():
                phase = node_state.get('current_phase', '')
                retry = node_state.get('retry_count', 0)
                error = node_state.get('error', '')

                if phase:
                    print(f"\n>>> {phase.upper()}", end='')
                    if retry > 0:
                        print(f" (Retry #{retry})")
                    else:
                        print()

                if error:
                    print(f"    ERROR: {error[:150]}")

        print("\n[SUCCESS] QA loop test completed!")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
