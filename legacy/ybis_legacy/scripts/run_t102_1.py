"""
Execute T-102.1: Fix Plugin System Test Quality Issues

This is a DOGFOODING test of the error feedback loop:
- System will use OrchestratorGraph to fix test failures
- If Aider makes mistakes, feedback loop should auto-correct
- Tests the prevention system in a real scenario
"""

import asyncio
from datetime import datetime
from pathlib import Path
from src.agentic.core.config import PROJECT_ROOT
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced
from src.agentic.core.protocols import TaskState

async def main():
    print("="*80)
    print("T-102.1: Fix Plugin System Test Quality Issues")
    print("="*80)
    print("DOGFOODING TEST: Error feedback loop validation")
    print()

    # Load task specification
    task_file = PROJECT_ROOT / "Knowledge/Tasks/backlog/T-102.1_P1_Fix_Plugin_Tests.md"
    task_spec = task_file.read_text(encoding='utf-8')

    print(f"[INFO] Task specification loaded ({len(task_spec)} chars)")
    print()

    # Initialize plugins with ENHANCED prevention system
    print("[INFO] Initializing ENHANCED plugins with FEEDBACK LOOP...")
    planner = SimplePlanner()
    executor = AiderExecutorEnhanced()  # Uses error feedback on retry
    verifier = SentinelVerifierEnhanced()  # Catches import/emoji errors

    print("[OK] OrchestratorGraph ready with feedback loop")
    print()

    # Create orchestrator
    orchestrator = OrchestratorGraph(
        planner=planner,
        executor=executor,
        verifier=verifier
    )

    # Create task state
    task_state: TaskState = {
        "task_id": "T-102.1",
        "task_description": task_spec,
        "phase": "init",
        "plan": None,
        "code_result": None,
        "verification": None,
        "retry_count": 0,
        "max_retries": 3,  # Allow retries for feedback loop testing
        "error": None,
        "started_at": datetime.now(),
        "completed_at": None,
        "artifacts_path": str(PROJECT_ROOT / ".sandbox_hybrid/T-102.1"),
        "error_history": [],
        "failed_at": None
    }

    # Create artifacts directory
    artifacts_path = Path(task_state["artifacts_path"])
    artifacts_path.mkdir(parents=True, exist_ok=True)

    print("[START] Invoking OrchestratorGraph...")
    print()

    # Execute
    result = await orchestrator.ainvoke(task_state)

    # Report results
    print()
    print("="*80)
    print("EXECUTION COMPLETE")
    print("="*80)
    print(f"Final Phase: {result['phase']}")
    print(f"Retry Count: {result['retry_count']}")
    print()

    if result.get('verification'):
        verification = result['verification']
        print("[VERIFICATION RESULTS]")
        print(f"  Tests Passed: {verification.tests_passed}")
        print(f"  Lint Passed: {verification.lint_passed}")
        print(f"  Coverage: {verification.coverage}%")
        print()

        if verification.errors:
            print("[ERRORS]")
            for error in verification.errors:
                print(f"  - {error}")
            print()

        if verification.warnings:
            print("[WARNINGS]")
            for warning in verification.warnings:
                print(f"  - {warning}")
            print()

    # Check if feedback loop was used
    if result['retry_count'] > 0:
        print("[FEEDBACK LOOP RESULTS]")
        print(f"  Retries Used: {result['retry_count']}")
        print(f"  Error History:")
        for i, error in enumerate(result.get('error_history', []), 1):
            print(f"    {i}. {error}")
        print()

        if result['phase'] == 'verify' and result['verification'].tests_passed:
            print("[SUCCESS] Feedback loop worked! System auto-corrected errors.")
        else:
            print("[PARTIAL] Feedback loop triggered but tests still failing.")
        print()

    # Final verdict
    if result['phase'] == 'verify' and result['verification'].tests_passed:
        print("[SUCCESS] All tests fixed! T-102.1 complete.")
        print()
        print("[NEXT STEPS]")
        print(f"  1. Review artifacts: {artifacts_path}")
        print(f"  2. Run tests manually: pytest src/agentic/core/plugin_system/tests/ -v")
        print(f"  3. Move task to done/")
    elif result['phase'] == 'failed':
        print("[FAILED] Task failed after maximum retries.")
        print()
        print("[DEBUG STEPS]")
        print(f"  1. Check artifacts: {artifacts_path}")
        print(f"  2. Review error history above")
        print(f"  3. Check if prevention system caught errors")
    else:
        print(f"[UNKNOWN] Task ended in unexpected phase: {result['phase']}")

    print()

if __name__ == "__main__":
    asyncio.run(main())
