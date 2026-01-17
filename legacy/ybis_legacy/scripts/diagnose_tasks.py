#!/usr/bin/env python3
"""Diagnose why tasks are stuck in IN_PROGRESS."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic import mcp_server

def main():
    task_ids = ["TASK-New-2427", "TASK-New-2639"]
    
    print("=" * 80)
    print("TASK DIAGNOSIS REPORT")
    print("=" * 80)
    
    for task_id in task_ids:
        # Get task from MCP server
        tasks_payload = mcp_server.get_tasks()
        all_tasks = json.loads(tasks_payload).get("tasks", [])
        task = next((t for t in all_tasks if t.get("id") == task_id), None)
        
        if not task:
            print(f"\n[ERROR] Task {task_id} not found in database")
            continue
            
        print(f"\n--- {task_id} ---")
        print(f"Status: {task.get('status', 'N/A')}")
        print(f"Priority: {task.get('priority', 'N/A')}")
        print(f"Assignee: {task.get('assignee', 'N/A')}")
        print(f"Goal: {task.get('goal', 'N/A')[:60]}...")
        
        # Check workspace
        workspace = Path(f"workspaces/active/{task_id}")
        if workspace.exists():
            print(f"\nWorkspace exists: {workspace}")
            plan = workspace / "docs" / "PLAN.md"
            if plan.exists():
                content = plan.read_text(encoding="utf-8")
                if "status: DRAFT" in content or len(content.strip()) < 100:
                    print(f"  [WARN] PLAN.md is empty or DRAFT")
                else:
                    print(f"  [OK] PLAN.md exists and has content")
            else:
                print(f"  [WARN] PLAN.md missing")
        else:
            print(f"\n[WARN] Workspace does not exist: {workspace}")
        
        # Test claim attempt
        print(f"\n  Testing claim attempt...")
        claim_result = mcp_server.claim_task(task_id, "diagnosis-agent")
        print(f"  Claim result: {claim_result}")
    
    # Check orchestrator logs
    print("\n" + "=" * 80)
    print("ORCHESTRATOR LOG ANALYSIS")
    print("=" * 80)
    
    log_file = Path("Knowledge/Logs/orchestrator_cli.log")
    if log_file.exists():
        lines = log_file.read_text(encoding="utf-8").splitlines()
        recent = [l for l in lines if any(tid in l for tid in task_ids)][-10:]
        if recent:
            print("\nRecent orchestrator log entries for these tasks:")
            for line in recent:
                print(f"  {line}")
        else:
            print("\n[WARN] No orchestrator log entries found for these tasks")
            print(f"Last 5 orchestrator log entries:")
            for line in lines[-5:]:
                print(f"  {line}")
    else:
        print(f"\n[ERROR] Orchestrator log file not found: {log_file}")
    
    # Check task board logs
    print("\n" + "=" * 80)
    print("TASK BOARD LOG ANALYSIS")
    print("=" * 80)
    
    task_board_log = Path("Knowledge/Logs/task_board.log")
    if task_board_log.exists():
        lines = task_board_log.read_text(encoding="utf-8").splitlines()
        relevant = [l for l in lines if any(tid in l for tid in task_ids)][-10:]
        if relevant:
            print("\nRecent task board log entries:")
            for line in relevant:
                print(f"  {line}")
        else:
            print("\n[INFO] No task board log entries for these tasks")
    else:
        print(f"\n[ERROR] Task board log file not found: {task_board_log}")
    
    # Check for background processes
    print("\n" + "=" * 80)
    print("DIAGNOSIS SUMMARY")
    print("=" * 80)
    
    print("\n[ISSUE] Tasks are IN_PROGRESS but orchestrator cannot claim them")
    print("  Reason: _claim_specific_task() returns None when task is already IN_PROGRESS")
    print("  Solution: Release tasks and re-claim, OR modify orchestrator to handle IN_PROGRESS tasks")
    
    print("\n[RECOMMENDATION]")
    print("  1. Release stuck tasks: python scripts/ybis.py release TASK-New-2427")
    print("  2. Release stuck tasks: python scripts/ybis.py release TASK-New-2639")
    print("  3. Re-run orchestrator: python scripts/run_orchestrator.py --task-id TASK-New-2427")

if __name__ == "__main__":
    main()

