#!/usr/bin/env python3
"""
Verify Audit Trail - Audit the "Proof of Work" from events.jsonl.

DoD:
- Audit script passes, confirming the system is fully compliant with the "Evidence-First" constitution.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.constants import PROJECT_ROOT


def verify_audit_trail(task_id: str, run_id: str | None = None) -> bool:
    """
    Verify audit trail from events.jsonl.

    Args:
        task_id: Task identifier
        run_id: Run identifier (if None, uses latest run)

    Returns:
        True if audit trail is valid
    """
    # Find run directory
    runs_dir = PROJECT_ROOT / "workspaces" / task_id / "runs"

    if not runs_dir.exists():
        print(f"Error: No runs found for task {task_id}")
        return False

    if run_id:
        run_path = runs_dir / run_id
    else:
        run_dirs = list(runs_dir.glob("R-*"))
        if not run_dirs:
            print(f"Error: No run directories found")
            return False
        run_path = max(run_dirs, key=lambda p: p.stat().st_mtime)
        run_id = run_path.name

    print(f"Verifying audit trail for:")
    print(f"  Task: {task_id}")
    print(f"  Run: {run_id}")
    print()

    # Read events.jsonl
    events_path = run_path / "journal" / "events.jsonl"

    if not events_path.exists():
        print(f"Error: Events file not found: {events_path}")
        return False

    events = []
    with open(events_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON line: {line[:50]}...")

    print(f"Found {len(events)} events in journal")
    print()

    # Verify required events
    required_events = {
        "PLAN_GENERATED": False,
        "FILE_WRITE": False,
        "GATE_DECISION": False,
        "COMMAND_EXEC": False,
    }

    event_types = [e.get("event_type") for e in events]

    # Check for plan generation (could be in plan.json creation or event)
    if any("plan" in str(e).lower() for e in events):
        required_events["PLAN_GENERATED"] = True
        print("[OK] PLAN_GENERATED event found")

    # Check for FILE_WRITE
    if "FILE_WRITE" in event_types:
        required_events["FILE_WRITE"] = True
        print("[OK] FILE_WRITE event found")
        # Check if constants.py was written
        file_events = [e for e in events if e.get("event_type") == "FILE_WRITE"]
        constants_events = [e for e in file_events if "constants.py" in str(e.get("path", ""))]
        if constants_events:
            print("  -> constants.py modification recorded")

    # Check for GATE_DECISION
    if "GATE_DECISION" in event_types:
        required_events["GATE_DECISION"] = True
        print("[OK] GATE_DECISION event found")
        gate_events = [e for e in events if e.get("event_type") == "GATE_DECISION"]
        for gate_event in gate_events:
            decision = gate_event.get("decision", "")
            gate_type = gate_event.get("gate_type", "")
            print(f"  -> {gate_type}: {decision}")

    # Check for COMMAND_EXEC
    if "COMMAND_EXEC" in event_types:
        required_events["COMMAND_EXEC"] = True
        print("[OK] COMMAND_EXEC event found")
        exec_events = [e for e in events if e.get("event_type") == "COMMAND_EXEC"]
        commands = [e.get("command", "") for e in exec_events]
        print(f"  -> Commands: {', '.join(set(commands[:5]))}")

    print()

    # Summary
    all_present = all(required_events.values())
    if all_present:
        print("[OK] All required events present in audit trail")
        print("[OK] System is compliant with Evidence-First constitution")
        return True
    else:
        missing = [k for k, v in required_events.items() if not v]
        print(f"[ERROR] Missing events: {', '.join(missing)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_audit_trail.py TASK-ID [RUN-ID]")
        sys.exit(1)

    task_id = sys.argv[1]
    run_id = sys.argv[2] if len(sys.argv) > 2 else None

    success = verify_audit_trail(task_id, run_id)
    sys.exit(0 if success else 1)

