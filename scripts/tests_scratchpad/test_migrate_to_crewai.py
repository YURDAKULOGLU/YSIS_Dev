"""
DOGFOODING TEST: Orchestrator migrates itself from PydanticAI to CrewAI

Task: Replace PydanticAI wrapper agents with native CrewAI agents
Method: Use the orchestrator to refactor itself (recursive self-improvement)
"""
import asyncio
import sys
import os
import uuid

# Fix Windows encoding for Unicode output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Agentic'))

async def main():
    print("=== DOGFOODING: ORCHESTRATOR SELF-MIGRATION ===")
    print("-" * 60)

    from Agentic.Core.orchestrator_v2 import build_v2_graph
    from Agentic.Core.state import AgentState

    task = """Migrate orchestrator_v2.py from PydanticAI wrapper agents to native CrewAI agents.

CONTEXT:
- Current: Uses base_agent.py (PydanticAI wrapper) for Architect, Developer, QA
- Target: Use CrewAI Agent class directly (like in planning_crew.py)
- Reason: PydanticAI wrapper has validation issues, CrewAI is battle-tested

REQUIREMENTS:
1. Study Agentic/Workflows/planning_crew.py to understand CrewAI Agent pattern
2. Replace Agentic/Agents/architect.py with CrewAI Agent
3. Replace Agentic/Agents/developer.py with CrewAI Agent
4. Replace Agentic/Agents/qa.py with CrewAI Agent
5. Update orchestrator_v2.py to use CrewAI agents instead of PydanticAI
6. Keep LangGraph workflow intact (Init → Analyze → Execute → Lint → QA → Commit)
7. Ensure homogeneous integration: LangGraph orchestrates CrewAI agents

INTEGRATION PHILOSOPHY:
- Use ready frameworks (CrewAI > custom wrapper)
- Homogeneous integration (LangGraph state machine + CrewAI agents = seamless)
- Dogfooding (use the system to improve itself)

OUTPUT:
- Modified orchestrator_v2.py with CrewAI agents
- CrewAI-based Architect, Developer, QA agents
- Working QA feedback loop without validation errors
"""

    print(f"\n[TASK]\n{task}\n")

    initial_state = AgentState(
        task=task,
        task_id=str(uuid.uuid4()),
        user_id="self-migration",
        current_phase="init",
        status="running",
        messages=[],
        files_context=[
            "Agentic/Workflows/planning_crew.py",  # Reference for CrewAI pattern
            "Agentic/Core/orchestrator_v2.py",      # File to modify
            "Agentic/Agents/base_agent.py",         # Current wrapper to replace
        ],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )

    print("[START] Orchestrator will now refactor itself...\n")

    graph = build_v2_graph()

    try:
        async for event in graph.astream(initial_state, {"configurable": {"thread_id": "self-migration"}}):
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
                    print(f"    ERROR: {error[:200]}")

        print("\n[SUCCESS] Self-migration completed! Orchestrator now uses CrewAI agents.")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
