#!/usr/bin/env python3
"""
Create a simple task and run it through ybis_native workflow.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Task, Run
import uuid


async def create_and_run_task():
    """Create a simple task and run it."""
    # Initialize database
    db_path = project_root / "platform_data" / "control_plane.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    db = ControlPlaneDB(db_path)
    await db.initialize()
    
    # Create task
    task_id = f"T-{uuid.uuid4().hex[:8]}"
    task = Task(
        task_id=task_id,
        title="Basit Toplama Fonksiyonu",
        objective="Bir Python dosyası oluştur: add_numbers.py. Bu dosyada iki sayıyı toplayan bir fonksiyon olacak: def add(a, b): return a + b",
        status="pending",
        priority="MEDIUM",
    )
    await db.register_task(task)
    
    print(f"✅ Task oluşturuldu: {task_id}")
    print(f"   Title: {task.title}")
    print(f"   Objective: {task.objective}")
    print()
    print("🚀 Workflow'u başlatıyorum...")
    print()
    
    # Import and run workflow directly (avoid duplicate run registration)
    from src.ybis.data_plane import init_run_structure
    from src.ybis.orchestrator.graph import build_workflow_graph
    from src.ybis.orchestrator.logging import log_workflow_start, log_workflow_end, log_state_transition
    from src.ybis.services.adapter_bootstrap import bootstrap_adapters
    import time
    
    # Bootstrap adapters before building graph
    bootstrap_adapters()
    
    # Generate run_id and trace_id
    run_id = f"R-{uuid.uuid4().hex[:8]}"
    trace_id = f"trace-{uuid.uuid4().hex[:16]}"
    
    # Initialize workspace
    run_path = init_run_structure(task_id, run_id, trace_id=trace_id, use_git_worktree=True)
    print(f"Run path: {run_path}")
    
    # Register run
    run = Run(
        run_id=run_id,
        task_id=task_id,
        workflow="ybis_native",
        run_path=str(run_path),
        status="running",
    )
    await db.register_run(run)
    
    # Build and execute workflow graph
    graph = build_workflow_graph(workflow_name="ybis_native")
    
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
        "workflow_name": "ybis_native",
        "task_objective": task.objective,
    }
    
    # Log workflow start
    workflow_start_time = time.time()
    log_workflow_start(initial_state)
    
    print("Executing workflow...")
    previous_state = initial_state.copy()
    final_state = graph.invoke(initial_state)
    
    # Log state transitions and workflow end
    log_state_transition(previous_state, final_state)
    workflow_duration = time.time() - workflow_start_time
    log_workflow_end(final_state, final_state.get("status", "unknown"), workflow_duration)
    
    # Update run status
    import aiosqlite
    async with aiosqlite.connect(db_path) as db_conn:
        await db_conn.execute(
            "UPDATE runs SET status = ? WHERE run_id = ?",
            (final_state["status"], run_id),
        )
        await db_conn.commit()
    
    # Update task status
    if final_state["status"] == "awaiting_approval":
        task.status = "blocked"
    else:
        task.status = final_state["status"]
    await db.register_task(task)
    
    print()
    print(f"{'='*60}")
    print(f"✅ Workflow tamamlandı! Status: {final_state.get('status', 'unknown')}")
    print(f"{'='*60}")
    
    # Show failure details if failed
    if final_state.get("status") == "failed":
        print()
        print("🔍 FAILURE ANALYSIS")
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
                if decision in ["BLOCK", "REQUIRE_APPROVAL"]:
                    print(f"\n🚪 Gate Decision: {decision}")
                    print(f"   Reason: {gate_data.get('reason', 'No reason provided')}")
            
            # Check plan
            plan_path = artifacts_path / "plan.json"
            if plan_path.exists():
                plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
                steps = plan_data.get('steps', [])
                if len(steps) == 0:
                    print(f"\n⚠️ Plan has 0 steps - this is likely the root cause!")
        
        print(f"\n💡 Detaylı analiz için: python scripts/inspect_failed_run.py")


if __name__ == "__main__":
    asyncio.run(create_and_run_task())

