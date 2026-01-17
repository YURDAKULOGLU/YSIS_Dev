"""
Execute T-102: Plugin Architecture Core

Uses ENHANCED executor/verifier with prevention system:
- AiderExecutorEnhanced (injects CODE_STANDARDS, API refs)
- SentinelVerifierEnhanced (checks imports, emojis)
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.getcwd())

from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced

async def main():
    print("=" * 80)
    print("T-102: Plugin Architecture Core + Infrastructure")
    print("=" * 80)
    print("Prevention System: ACTIVE")
    print("  - Emoji check: ENABLED")
    print("  - Import check: ENABLED")
    print("  - API reference injection: ENABLED")
    print("  - Test-first enforcement: ENABLED")
    print()

    # Read task specification
    task_file = Path("Knowledge/Tasks/backlog/T-102_P0_Plugin_Architecture_Core.md")
    if not task_file.exists():
        print(f"[ERROR] Task file not found: {task_file}")
        return 1

    task_content = task_file.read_text(encoding='utf-8')
    print(f"[INFO] Task specification loaded ({len(task_content)} chars)")
    print()

    # Initialize ENHANCED plugins
    print("[INFO] Initializing ENHANCED plugins...")
    planner = SimplePlanner()
    executor = AiderExecutorEnhanced()  # Enhanced!
    verifier = SentinelVerifierEnhanced()  # Enhanced!

    # Initialize orchestrator
    orchestrator = OrchestratorGraph(planner, executor, verifier)
    print("[OK] OrchestratorGraph ready with enhanced prevention system")
    print()

    # Prepare task state
    initial_state = {
        "task_id": "T-102",
        "task_description": f"""
Implement Plugin Architecture Core.

FULL SPECIFICATION:
{task_content}

CRITICAL REQUIREMENTS (from ARCHITECTURE_PRINCIPLES.md):
1. Plugin-first architecture
2. Free & open-source only
3. ToolProtocol interface (<500 lines core)
4. ToolRegistry for registration/invocation
5. Built-in plugins: @math/calculator, @file/read, @git/status
6. LangFuse integration (self-hosted observability)
7. LiteLLM integration (LLM proxy)

FILES TO CREATE:
- src/agentic/core/plugin_system/protocol.py
- src/agentic/core/plugin_system/registry.py
- src/agentic/core/plugin_system/loader.py
- src/agentic/core/plugin_system/observability.py
- src/agentic/core/plugin_system/llm_proxy.py
- src/agentic/core/plugins/builtin/calculator.py
- src/agentic/core/plugins/builtin/file_ops.py
- src/agentic/core/plugins/builtin/git_ops.py
- tests/plugin_system/test_*.py

MANDATORY APPROACH (enforced by enhanced executor):
1. Write tests FIRST
2. Implement to pass tests
3. NO EMOJIS in code
4. Correct API usage (LangGraph, etc.)
5. All imports must be present

ACCEPTANCE:
- ToolProtocol defined
- ToolRegistry works
- 3+ built-in plugins functional
- All tests pass
- NO emojis found
- NO missing imports
""",
        "phase": "init",
        "retry_count": 0,
        "max_retries": 3,
        "artifacts_path": ".sandbox_hybrid/T-102",
        "started_at": datetime.now(),
        "completed_at": None,
        "plan": None,
        "code_result": None,
        "verification": None,
        "error": None,
        "error_history": [],
        "failed_at": None
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

            # Show enhanced checks
            logs = verification.logs
            print()
            print("[ENHANCED CHECKS]")
            print(f"  Emoji Check: {logs.get('emoji_check', 'N/A')}")
            print(f"  Import Check: {logs.get('import_check', 'N/A')}")

            if verification.errors:
                print(f"\n  Errors: {len(verification.errors)}")
                for err in verification.errors:
                    print(f"    - {err}")

            if verification.warnings:
                print(f"\n  Warnings: {len(verification.warnings)}")
                for warn in verification.warnings[:3]:
                    print(f"    - {warn}")

        # Check artifacts
        artifacts_path = Path(initial_state["artifacts_path"])
        if artifacts_path.exists():
            print()
            print("[ARTIFACTS]")
            for artifact in artifacts_path.iterdir():
                print(f"  - {artifact.name}")

        print()
        if final_state.get('phase') == 'verify' and verification and verification.tests_passed:
            print("[SUCCESS] Plugin architecture implemented and verified!")
            print()
            print("[PREVENTION SYSTEM RESULTS]")
            print(f"  Emoji violations: {0 if logs.get('emoji_check') == 'PASSED' else 1}")
            print(f"  Import violations: {0 if logs.get('import_check') == 'PASSED' else 1}")
            print()
            print("[NEXT STEPS]")
            print("  1. Review artifacts: .sandbox_hybrid/T-102/")
            print("  2. Test plugins manually")
            print("  3. Move task to done/")
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
