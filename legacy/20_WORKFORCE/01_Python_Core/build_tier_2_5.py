"""
Tier 2.5 Builder - Using Tier 2 Orchestrator to Build Itself
This demonstrates recursive bootstrap: Tier 2 builds Tier 2.5
"""
import sys
import asyncio
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

async def build_tier_2_5():
    """Use Tier 2 orchestrator to build Tier 2.5 human-approval system"""
    print("\n" + "="*60)
    print("[RETRY] RECURSIVE BOOTSTRAP: Tier 2 Building Tier 2.5")
    print("="*60)

    try:
        from Agentic.Core.state import AgentState
        from Agentic.Core.orchestrator import build_graph

        print("\n[1] Loading Tier 2 orchestrator...")
        graph = build_graph()
        print("  ✓ Orchestrator loaded")

        # Define the Tier 2.5 task
        tier_2_5_task = """
Add human-approval checkpoints to the orchestrator before code execution.

Requirements:
1. Add a `request_approval()` function that shows the plan and waits for y/n input
2. Call this function in the execute_node before running any code
3. Add safety limits:
   - MAX_RETRIES = 3 (already exists, verify it)
   - MAX_FILES_CHANGED = 10 (new)
   - Block destructive commands (rm -rf, DROP TABLE, etc.)
4. Add detailed logging before/after approval
5. If approval denied, skip to QA with status="cancelled"

Files to modify:
- Agentic/Core/orchestrator.py (add approval checkpoint)
- Agentic/Core/state.py (add approval_requested field if needed)

Keep changes minimal - this is safety layer only.
"""

        print("\n[2] Creating Tier 2.5 build task...")
        print(f"Task: {tier_2_5_task[:100]}...")

        initial_state = AgentState(
            task=tier_2_5_task,
            task_id="tier-2.5-build",
            user_id="claude-self-improvement",
            current_phase="analyze",
            status="running",
            messages=[],
            files_context=[],
            decisions=[],
            artifacts={},
            error=None,
            retry_count=0
        )

        print("\n[3] Running orchestrator (Analyze → Execute → QA)...")
        print("="*60)

        # Run the orchestrator
        result = await graph.ainvoke(initial_state)

        print("\n" + "="*60)
        print("[4] Orchestrator finished!")
        print(f"  Status: {result['status']}")
        print(f"  Phase: {result['current_phase']}")
        print(f"  Decisions made: {len(result['decisions'])}")

        if result.get('error'):
            print(f"  [WARNING]  Error: {result['error']}")

        # Show decisions
        if result['decisions']:
            print("\n[5] Decisions made by orchestrator:")
            for i, decision in enumerate(result['decisions'], 1):
                print(f"  {i}. {decision}")

        # Show artifacts
        if result.get('artifacts'):
            print("\n[6] Artifacts created:")
            for name, content in result['artifacts'].items():
                print(f"  - {name}: {len(str(content))} chars")

        print("\n" + "="*60)

        if result['status'] == 'completed':
            print("[SUCCESS] SUCCESS: Tier 2.5 built by Tier 2!")
            print("   Recursive bootstrap working!")
        else:
            print(f"[WARNING]  Status: {result['status']}")
            print("   Review decisions and retry if needed")

        print("="*60 + "\n")

        return result

    except Exception as e:
        print(f"\n[ERROR] FAIL: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """Main entry point"""
    print("\n" + "#"*60)
    print("# TIER 2.5 BUILDER")
    print("# Using Tier 2 orchestrator to build human-approval system")
    print("#"*60)

    result = await build_tier_2_5()

    if result and result.get('status') == 'completed':
        print("\n🎉 Tier 2.5 is ready!")
        print("   Next: Test the human-approval flow")
        return 0
    else:
        print("\n[WARNING]  Build incomplete or failed")
        print("   Review errors and retry")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
