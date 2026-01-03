"""
Execute TASK-New-206: Project Structure Cleanup & Standardization

DOGFOODING DEMONSTRATION:
- System cleans itself using its own tools
- OrchestratorGraph → SimplePlanner → AiderExecutor → SentinelVerifier
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
    print("DOGFOODING: TASK-New-206 - Project Structure Cleanup")
    print("=" * 80)
    print("System will clean itself using:")
    print("  - SimplePlanner: Plan cleanup steps")
    print("  - AiderExecutor: Generate cleanup bash script")
    print("  - SentinelVerifier: Verify structure integrity")
    print()

    # Read detailed plan
    task_file = Path("Knowledge/Tasks/backlog/TASK-New-206_DETAILED_PLAN.md")
    if not task_file.exists():
        print(f"[ERROR] Task file not found: {task_file}")
        return 1

    task_content = task_file.read_text(encoding='utf-8')
    print(f"[INFO] Cleanup plan loaded ({len(task_content)} chars)")
    print()

    # Initialize plugins
    print("[INFO] Initializing orchestration plugins...")
    planner = SimplePlanner()
    executor = AiderExecutor()
    verifier = SentinelVerifier()

    # Initialize orchestrator
    orchestrator = OrchestratorGraph(planner, executor, verifier)
    print("[OK] OrchestratorGraph ready")
    print()

    # Prepare task state
    initial_state = {
        "task_id": "TASK-New-206",
        "task_description": f"""
Project Structure Cleanup & Standardization

OBJECTIVE:
Clean root directory, move files to proper locations, achieve professional repo structure.

FULL CLEANUP PLAN:
{task_content}

CRITICAL APPROACH:
1. Create a bash script (scripts/cleanup_structure.sh) that performs all moves
2. Script must be SAFE (check before move, create dirs, handle errors)
3. Script must be IDEMPOTENT (can run multiple times safely)
4. Include dry-run mode (--dry-run flag)

SCRIPT TEMPLATE:
```bash
#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=${{1:-false}}

# Function to safely move
safe_move() {{
    src=$1
    dst=$2
    if [ "$DRY_RUN" = "--dry-run" ]; then
        echo "[DRY-RUN] Would move: $src -> $dst"
    else
        mkdir -p "$(dirname "$dst")"
        if [ -e "$src" ]; then
            mv "$src" "$dst"
            echo "[MOVED] $src -> $dst"
        fi
    fi
}}

# Phase 1: Root cleanup
safe_move "brain_debug.txt" "logs/archive/brain_debug.txt"
safe_move "error_plan.json" "logs/archive/error_plan.json"
# ... (rest of moves from plan)

echo "[SUCCESS] Cleanup complete!"
```

DELIVERABLES:
1. scripts/cleanup_structure.sh (executable bash script)
2. Updated .gitignore
3. Verification that tests still pass

ACCEPTANCE CRITERIA:
- Root has ≤10 top-level items
- All loose files moved
- .gitignore prevents future clutter
- Tests pass after cleanup
""",
        "phase": "init",
        "retry_count": 0,
        "max_retries": 3,
        "artifacts_path": ".sandbox_hybrid/TASK-New-206",
        "started_at": datetime.now(),
        "completed_at": None,
        "plan": None,
        "code_result": None,
        "verification": None,
        "error": None,
        "error_history": [],
        "failed_at": None
    }

    print("[START] Invoking OrchestratorGraph for self-cleanup...")
    print()

    try:
        final_state = await orchestrator.ainvoke(initial_state)

        print()
        print("=" * 80)
        print("DOGFOODING EXECUTION COMPLETE")
        print("=" * 80)
        print(f"Final Phase: {final_state.get('phase')}")
        print(f"Retry Count: {final_state.get('retry_count', 0)}")

        # Check verification
        verification = final_state.get('verification')
        if verification:
            print()
            print("[VERIFICATION RESULTS]")
            print(f"  Tests Passed: {verification.tests_passed}")
            print(f"  Lint Passed: {verification.lint_passed}")

            if verification.errors:
                print(f"\n  Errors: {len(verification.errors)}")
                for err in verification.errors[:3]:
                    print(f"    - {err}")

        # Check for generated script
        cleanup_script = Path("scripts/cleanup_structure.sh")
        if cleanup_script.exists():
            print()
            print("[SUCCESS] Cleanup script generated!")
            print(f"  Location: {cleanup_script}")
            print()
            print("[NEXT STEPS]")
            print("  1. Review script: cat scripts/cleanup_structure.sh")
            print("  2. Dry-run: bash scripts/cleanup_structure.sh --dry-run")
            print("  3. Execute: bash scripts/cleanup_structure.sh")
            print("  4. Verify: python -m pytest tests/ -v")
            return 0
        else:
            print("[WARNING] Cleanup script not generated")
            print(f"  Final phase: {final_state.get('phase')}")
            if final_state.get('error'):
                print(f"  Error: {final_state['error']}")
            return 1

    except Exception as e:
        print()
        print("=" * 80)
        print("[DOGFOODING FAILED]")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
