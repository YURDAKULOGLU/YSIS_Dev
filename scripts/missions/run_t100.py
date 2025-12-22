"""
Execute T-100: Implement Retry Loop in OrchestratorGraph

Strategic execution using the system's own tools.
This is meta-level work: using the orchestrator to improve itself.
"""
import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.getcwd())

from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier

async def main():
    print("=" * 80)
    print("T-100: Implement Retry Loop in OrchestratorGraph")
    print("=" * 80)
    print("Strategic Mode: Using system to improve itself (dogfooding)")
    print()

    # Read task specification
    task_file = Path("Knowledge/Tasks/backlog/T-100_P0_OrchestratorGraph_Retry_Loop.md")
    if not task_file.exists():
        print(f"[ERROR] Task file not found: {task_file}")
        return 1

    task_content = task_file.read_text(encoding='utf-8')
    print(f"[INFO] Task specification loaded ({len(task_content)} chars)")
    print()

    # Initialize plugins
    print("[INFO] Initializing plugins...")
    planner = SimplePlanner()
    executor = AiderExecutor()
    verifier = SentinelVerifier()

    # Initialize orchestrator
    orchestrator = OrchestratorGraph(planner, executor, verifier)
    print("[OK] OrchestratorGraph ready")
    print()

    # Prepare task state
    initial_state = {
        "task_id": "T-100",
        "task_description": f"""
Implement retry loop in OrchestratorGraph.

FULL SPECIFICATION:
{task_content}

CRITICAL REQUIREMENTS:
1. Add conditional edge from verifier node
2. Create failed_node for terminal failure state
3. Update TaskState schema with error_history and failed_at
4. Implement should_retry_or_end routing function
5. Write tests for retry behavior
6. Ensure max_retries=3 is enforced

FILES TO MODIFY:
- src/agentic/core/graphs/orchestrator_graph.py
- src/agentic/core/protocols.py (state schema)
- tests/test_orchestrator_graph.py (new file)

ACCEPTANCE:
- Conditional edge exists
- Retry works (tests prove it)
- No infinite loops
""",
        "phase": "init",
        "retry_count": 0,
        "max_retries": 3,
        "artifacts_path": ".sandbox_hybrid/T-100",
        "started_at": datetime.now(),
        "completed_at": None,
        "plan": None,
        "code_result": None,
        "verification": None,
        "error": None
    }

    print("[START] Invoking OrchestratorGraph...")
    print()

    try:
        final_state = await orchestrator.ainvoke(initial_state)

        print()
        print("=" * 80)
        print("EXECUTION COMPLETE")
        print("=" * 80)
        print(f"Final Phase: {final_state.get('phase')}")
        print(f"Retry Count: {final_state.get('retry_count', 0)}")

        # Check results
        verification = final_state.get('verification')
        if verification:
            print()
            print("[VERIFICATION RESULTS]")
            print(f"  Tests Passed: {verification.tests_passed}")
            print(f"  Lint Passed: {verification.lint_passed}")
            print(f"  Coverage: {verification.coverage:.1%}")

            if verification.errors:
                print(f"  Errors: {len(verification.errors)}")
                for err in verification.errors[:3]:
                    print(f"    - {err}")

        # Check artifacts
        artifacts_path = Path(initial_state["artifacts_path"])
        if artifacts_path.exists():
            print()
            print("[ARTIFACTS]")
            for artifact in artifacts_path.iterdir():
                print(f"  - {artifact.name}")

        print()
        if final_state.get('phase') == 'verify' and verification.tests_passed:
            print("[SUCCESS] Retry loop implemented and verified!")
            print()
            print("[NEXT STEPS]")
            print("  1. Review artifacts: .sandbox_hybrid/T-100/")
            print("  2. Review plan: .sandbox_hybrid/T-100/PLAN.md")
            print("  3. Review changes: .sandbox_hybrid/T-100/RESULT.md")
            print("  4. Test manually if needed")
            print("  5. Move task to done/")
            return 0
        else:
            print("[WARNING] Task did not complete successfully")
            print(f"  Final phase: {final_state.get('phase')}")
            if final_state.get('error'):
                print(f"  Error: {final_state['error']}")
            return 1

    except Exception as e:
        print()
        print("=" * 80)
        print("[EXECUTION FAILED]")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
