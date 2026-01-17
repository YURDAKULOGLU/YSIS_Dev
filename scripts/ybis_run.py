#!/usr/bin/env python3
"""
YBIS Runner - Entry point for executing a task workflow.

Usage:
    python scripts/ybis_run.py TASK-123 [--workflow WORKFLOW_NAME]
    
Examples:
    python scripts/ybis_run.py TASK-123                    # Use default workflow (ybis_native)
    python scripts/ybis_run.py TASK-123 --workflow self_develop  # Use self-development workflow
    python scripts/ybis_run.py TASK-123 --workflow evo_evolve     # Use EvoAgentX workflow
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Run, Task
from src.ybis.data_plane import init_run_structure
from src.ybis.orchestrator import build_workflow_graph
from src.ybis.orchestrator.logging import log_workflow_start, log_workflow_end, log_state_transition


async def run_task(
    task_id: str,
    workflow_name: str = "ybis_native",
    db_path: str = "platform_data/control_plane.db",
) -> None:
    """
    Run a task workflow.

    Args:
        task_id: Task identifier
        db_path: Path to control plane database
    """
    # Initialize database
    db = ControlPlaneDB(db_path)
    await db.initialize()

    # Fetch task
    task = await db.get_task(task_id)
    if task is None:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)

    print(f"Running task: {task.title}")
    print(f"Objective: {task.objective}")
    print(f"Workflow: {workflow_name}")

    # Generate run_id and trace_id
    import uuid

    run_id = f"R-{uuid.uuid4().hex[:8]}"
    trace_id = f"trace-{uuid.uuid4().hex[:16]}"

    # Initialize workspace (with git worktree if available)
    run_path = init_run_structure(task_id, run_id, trace_id=trace_id, use_git_worktree=True)
    print(f"Run path: {run_path}")

    # Check if run already exists, if so update it, otherwise create new
    existing_run = await db.get_run(run_id)
    if existing_run:
        # Update existing run
        existing_run.run_path = str(run_path)
        existing_run.workflow = workflow_name
        existing_run.status = "running"
        await db.register_run(existing_run)  # register_run handles both insert and update
    else:
        # Register new run
        run = Run(
            run_id=run_id,
            task_id=task_id,
            workflow=workflow_name,  # Store workflow name in run
            run_path=str(run_path),
            status="running",
        )
        await db.register_run(run)

    # Check for approval if task is blocked
    if task.status == "blocked":
        approval_path = run_path / "artifacts" / "approval.json"
        if not approval_path.exists():
            print(f"Task {task_id} is blocked and requires approval.")
            print(f"Use MCP tool 'approval_write' or create {approval_path} to proceed.")
            sys.exit(1)
        print(f"Approval found, resuming task {task_id}...")

    # Build and execute workflow graph
    graph = build_workflow_graph(workflow_name=workflow_name)

    initial_state = {
        "task_id": task_id,
        "run_id": run_id,
        "run_path": run_path,
        "trace_id": trace_id,
        "status": "pending",
        "retries": 0,
        "max_retries": 2,
        "error_context": None,
        "current_step": 0,
        "workflow_name": workflow_name,  # Store workflow name in state
        "task_objective": task.objective,  # Add task objective for nodes
    }

    # Log workflow start
    import time
    workflow_start_time = time.time()
    log_workflow_start(initial_state)

    print("Executing workflow...")
    previous_state = initial_state.copy()
    
    try:
        final_state = graph.invoke(initial_state)
    except Exception as e:
        print(f"\n❌ Workflow execution error: {e}")
        import traceback
        traceback.print_exc()
        final_state = {"status": "failed", "error": str(e)}
    
    # Log state transitions and workflow end
    log_state_transition(previous_state, final_state)
    workflow_duration = time.time() - workflow_start_time
    log_workflow_end(final_state, final_state.get("status", "unknown"), workflow_duration)

    # Update run status
    run.status = final_state["status"]
    run.completed_at = None  # Would set to datetime.now() in real implementation
    await db.register_run(run)

    # Update task status (handle awaiting_approval -> blocked mapping)
    if final_state["status"] == "awaiting_approval":
        task.status = "blocked"
    else:
        task.status = final_state["status"]
    await db.register_task(task)

    print(f"\n{'='*60}")
    print(f"Workflow completed with status: {final_state['status']}")
    print(f"Artifacts available at: {run_path / 'artifacts'}")
    
    # Show failure/block details if not completed
    if final_state.get("status") in ["failed", "awaiting_approval"]:
        print()
        print("🔍 DETAILED ANALYSIS")
        print("-" * 60)
        
        # Check artifacts for error details
        artifacts_path = run_path / "artifacts"
        if artifacts_path.exists():
            import json
            
            # Check verifier report
            verifier_path = artifacts_path / "verifier_report.json"
            if verifier_path.exists():
                verifier_data = json.loads(verifier_path.read_text(encoding='utf-8'))
                if verifier_data.get('errors'):
                    print("\n❌ Verifier Errors:")
                    for i, error in enumerate(verifier_data['errors'][:3], 1):
                        if isinstance(error, dict):
                            print(f"  {i}. {error.get('type', 'Unknown')}: {error.get('message', 'No message')[:100]}")
                        else:
                            print(f"  {i}. {str(error)[:100]}")
            
            # Check gate report
            gate_path = artifacts_path / "gate_report.json"
            if gate_path.exists():
                gate_data = json.loads(gate_path.read_text(encoding='utf-8'))
                decision = gate_data.get('decision', {})
                if isinstance(decision, dict):
                    decision = decision.get('value', decision)
                print(f"\n🚪 Gate Decision: {decision}")
                print(f"   Reason: {gate_data.get('reason', 'No reason provided')}")
            
            # Check plan
            plan_path = artifacts_path / "plan.json"
            if plan_path.exists():
                plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
                steps = plan_data.get('steps', [])
                print(f"\n📝 Plan Steps: {len(steps)}")
                if len(steps) == 0:
                    print(f"   ⚠️ Plan has 0 steps - this may be the root cause!")
        
        print(f"\n💡 Detaylı analiz için: python scripts/inspect_failed_run.py")
    
    # Show failure details if failed
    if final_state.get("status") == "failed":
        print()
        print("=" * 60)
        print("🔍 FAILURE ANALYSIS")
        print("=" * 60)
        
        # Check artifacts for error details
        artifacts_path = run_path / "artifacts"
        if artifacts_path.exists():
            import json
            
            # Check verifier report
            verifier_path = artifacts_path / "verifier_report.json"
            if verifier_path.exists():
                verifier_data = json.loads(verifier_path.read_text(encoding='utf-8'))
                if verifier_data.get('errors'):
                    print("\n❌ Verifier Errors:")
                    for error in verifier_data['errors'][:5]:  # Show first 5
                        if isinstance(error, dict):
                            print(f"  - {error.get('type', 'Unknown')}: {error.get('message', 'No message')}")
                        else:
                            print(f"  - {str(error)}")
            
            # Check gate report
            gate_path = artifacts_path / "gate_report.json"
            if gate_path.exists():
                gate_data = json.loads(gate_path.read_text(encoding='utf-8'))
                decision = gate_data.get('decision', {})
                if isinstance(decision, dict):
                    decision = decision.get('value', decision)
                if decision in ["BLOCK", "REQUIRE_APPROVAL"]:
                    print(f"\n🚪 Gate Decision: {decision}")
                    print(f"   Reason: {gate_data.get('reason', 'No reason')}")
        
        print(f"\n💡 Detaylı analiz için: python scripts/inspect_failed_run.py")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="YBIS Runner - Execute a task workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/ybis_run.py TASK-123
  python scripts/ybis_run.py TASK-123 --workflow self_develop
  python scripts/ybis_run.py TASK-123 --workflow evo_evolve
        """,
    )
    parser.add_argument("task_id", help="Task identifier (e.g., TASK-123)")
    parser.add_argument(
        "--workflow",
        default="ybis_native",
        help="Workflow name to execute (default: ybis_native). Options: ybis_native, self_develop, evo_evolve, reactive_agent, council_review, self_improve",
    )
    parser.add_argument(
        "--db",
        default="platform_data/control_plane.db",
        help="Path to control plane database (default: platform_data/control_plane.db)",
    )

    args = parser.parse_args()

    asyncio.run(run_task(args.task_id, workflow_name=args.workflow, db_path=args.db))


if __name__ == "__main__":
    main()

