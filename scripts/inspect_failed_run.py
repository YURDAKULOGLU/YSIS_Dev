#!/usr/bin/env python3
"""Inspect a failed run to understand why it failed."""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from src.ybis.control_plane import ControlPlaneDB


async def inspect_failed_run():
    """Inspect the latest failed run."""
    db_path = project_root / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()
    
    # Get latest task
    import aiosqlite
    async with aiosqlite.connect(db_path) as db_conn:
        db_conn.row_factory = aiosqlite.Row
        async with db_conn.execute(
            "SELECT * FROM tasks ORDER BY updated_at DESC LIMIT 1"
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                print("No tasks found")
                return
            task_id = row["task_id"]
    
    task = await db.get_task(task_id)
    if not task:
        print("Task not found")
        return
    
    print(f"📋 Task: {task.task_id}")
    print(f"   Title: {task.title}")
    print(f"   Status: {task.status}")
    print()
    
    # Get latest run
    runs = await db.get_recent_runs(task_id=task_id, limit=1)
    if not runs:
        print("No runs found")
        return
    
    run = runs[0]
    print(f"🔍 Run: {run.run_id}")
    print(f"   Status: {run.status}")
    print(f"   Workflow: {run.workflow}")
    print()
    
    run_path = Path(run.run_path)
    artifacts_path = run_path / "artifacts"
    
    if not artifacts_path.exists():
        print("⚠️ Artifacts directory not found")
        return
    
    # Check verifier_report.json
    verifier_path = artifacts_path / "verifier_report.json"
    if verifier_path.exists():
        print("=" * 60)
        print("🔴 VERIFIER REPORT")
        print("=" * 60)
        verifier_data = json.loads(verifier_path.read_text(encoding='utf-8'))
        print(f"Success: {verifier_data.get('success', False)}")
        print(f"Errors: {len(verifier_data.get('errors', []))}")
        print(f"Warnings: {len(verifier_data.get('warnings', []))}")
        if verifier_data.get('errors'):
            print("\n❌ ERRORS:")
            for i, error in enumerate(verifier_data['errors'], 1):
                if isinstance(error, dict):
                    print(f"  {i}. {error.get('type', 'Unknown')}: {error.get('message', 'No message')}")
                    if error.get('file'):
                        print(f"     File: {error.get('file')}")
                    if error.get('line'):
                        print(f"     Line: {error.get('line')}")
                else:
                    print(f"  {i}. {error}")
        if verifier_data.get('warnings'):
            print("\n⚠️ WARNINGS:")
            for i, warning in enumerate(verifier_data['warnings'], 1):
                if isinstance(warning, dict):
                    print(f"  {i}. {warning.get('type', 'Unknown')}: {warning.get('message', 'No message')}")
                else:
                    print(f"  {i}. {warning}")
        print()
    
    # Check gate_report.json
    gate_path = artifacts_path / "gate_report.json"
    if gate_path.exists():
        print("=" * 60)
        print("🚪 GATE REPORT")
        print("=" * 60)
        gate_data = json.loads(gate_path.read_text(encoding='utf-8'))
        decision = gate_data.get('decision', {})
        if isinstance(decision, dict):
            decision = decision.get('value', decision)
        print(f"Decision: {decision}")
        reasons = gate_data.get('reasons', [])
        if reasons:
            print(f"Reasons:")
            for i, reason in enumerate(reasons, 1):
                print(f"  {i}. {reason}")
        else:
            print(f"Reason: No reason provided")
        if gate_data.get('checks'):
            print("\nChecks:")
            for check_name, check_result in gate_data['checks'].items():
                status = "✅" if check_result.get('passed', False) else "❌"
                print(f"  {status} {check_name}: {check_result.get('message', '')}")
        print()
    
    # Check debate_report.json
    debate_path = artifacts_path / "debate_report.json"
    if debate_path.exists():
        print("=" * 60)
        print("💬 DEBATE REPORT")
        print("=" * 60)
        debate_data = json.loads(debate_path.read_text(encoding='utf-8'))
        print(f"Triggered: {debate_data.get('triggered', False)}")
        if debate_data.get('outcome'):
            print(f"Outcome: {debate_data.get('outcome')}")
        print()
    
    # Check plan.json
    plan_path = artifacts_path / "plan.json"
    if plan_path.exists():
        print("=" * 60)
        print("📝 PLAN")
        print("=" * 60)
        plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
        steps = plan_data.get('steps', [])
        print(f"Steps: {len(steps)}")
        if steps:
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {step.get('action', 'N/A')}")
        else:
            print("  ⚠️ No steps in plan!")
        print()
    
    # Check executor_report.json
    executor_path = artifacts_path / "executor_report.json"
    if executor_path.exists():
        print("=" * 60)
        print("⚙️ EXECUTOR REPORT")
        print("=" * 60)
        executor_data = json.loads(executor_path.read_text(encoding='utf-8'))
        print(f"Success: {executor_data.get('success', False)}")
        files_changed = executor_data.get('files_changed', [])
        print(f"Files Changed: {len(files_changed)}")
        if files_changed:
            print("\n📁 Changed Files:")
            for i, file in enumerate(files_changed, 1):
                print(f"  {i}. {file}")
        commands_run = executor_data.get('commands_run', [])
        if commands_run:
            print(f"\n🔧 Commands Run: {len(commands_run)}")
            for i, cmd in enumerate(commands_run[:5], 1):  # Show first 5
                print(f"  {i}. {cmd[:80]}")
        if executor_data.get('error'):
            print(f"\n❌ Error: {executor_data.get('error')}")
        print()
    else:
        print("=" * 60)
        print("⚙️ EXECUTOR REPORT")
        print("=" * 60)
        print("⚠️ Executor report not found - task may not have been executed!")
        print()
    
    # Check spec_validation.json
    spec_val_path = artifacts_path / "spec_validation.json"
    if spec_val_path.exists():
        print("=" * 60)
        print("📋 SPEC VALIDATION")
        print("=" * 60)
        spec_val_data = json.loads(spec_val_path.read_text(encoding='utf-8'))
        print(f"Valid: {spec_val_data.get('valid', False)}")
        if spec_val_data.get('errors'):
            print("Errors:")
            for error in spec_val_data['errors']:
                print(f"  - {error}")
        print()
    
    # Check journal/log files
    journal_path = run_path / "journal.jsonl"
    if journal_path.exists():
        print("=" * 60)
        print("📜 JOURNAL (Last 5 events)")
        print("=" * 60)
        with open(journal_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-5:]:
                event = json.loads(line)
                print(f"  {event.get('event_type', 'Unknown')}: {event.get('message', '')[:100]}")
        print()


if __name__ == "__main__":
    asyncio.run(inspect_failed_run())

