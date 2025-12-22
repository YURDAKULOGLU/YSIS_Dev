"""
Dogfooding: Use orchestrator_v2.py to integrate CrewAI into itself
"""
import asyncio
import sys
import os
import uuid

# Add Agentic to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Agentic'))

async def main():
    print("=== Dogfooding: orchestrator_v2 integrates CrewAI ===")
    print("-" * 60)

    from Agentic.Core.orchestrator_v2 import build_v2_graph
    from Agentic.Core.state import AgentState

    task = """Integrate CrewAI into orchestrator_v2.py analyze_node().

Add this code to analyze_node() BEFORE architect_agent.analyze():

```python
# Optional: Use CrewAI for requirement analysis
try:
    from Crews.planning_crew import PlanningCrew
    crew = PlanningCrew()
    crew_result = crew.run(state['task'])
    print(f"   [CrewAI] {str(crew_result)[:100]}...")
    full_context += f"\\n--- CREW ANALYSIS ---\\n{crew_result}\\n"
except Exception as e:
    print(f"   [CrewAI] Skipped: {e}")
```

Files: Agentic/Core/orchestrator_v2.py (line ~85, in analyze_node)
"""

    print(f"\n[TASK]\n{task}\n")

    initial_state = AgentState(
        task=task,
        task_id=str(uuid.uuid4()),
        user_id="claude",
        current_phase="init",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )

    print("[START] Running orchestrator_v2...\n")

    graph = build_v2_graph()

    try:
        async for event in graph.astream(initial_state, {"configurable": {"thread_id": "dogfood-1"}}):
            # Print phase transitions
            for node_name, node_state in event.items():
                if 'current_phase' in node_state:
                    print(f">>> Phase: {node_state['current_phase']}")

        print("\n[SUCCESS] Orchestrator workflow completed!")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
