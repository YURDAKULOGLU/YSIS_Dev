#!/usr/bin/env python3
"""
Check Workflow Status - Read journal events to see what's happening.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB
import asyncio


async def check_workflow_status():
    """Check workflow status from journal events."""
    db_path = project_root / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()
    
    # Get latest run
    runs = await db.get_recent_runs(limit=1)
    if not runs:
        print("ERROR: No runs found")
        return
    
    run = runs[0]
    print(f"Task: {run.task_id}")
    print(f"Run: {run.run_id}")
    print(f"   Status: {run.status}")
    print(f"   Workflow: {run.workflow}")
    print(f"   Path: {run.run_path}")
    print()
    
    # Read journal
    journal_path = Path(run.run_path) / "journal" / "events.jsonl"
    if not journal_path.exists():
        print("ERROR: Journal not found")
        return
    
    events = []
    with open(journal_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except:
                pass
    
    print(f"Total Events: {len(events)}")
    print()
    
    # Group by event type
    event_counts = defaultdict(int)
    for event in events:
        event_type = event.get('event_type', 'UNKNOWN')
        event_counts[event_type] += 1
    
    print("Event Summary:")
    for event_type, count in sorted(event_counts.items()):
        print(f"   {event_type}: {count}")
    print()
    
    # Node execution timeline
    node_events = []
    for event in events:
        event_type = event.get('event_type', '')
        if 'NODE' in event_type:
            payload = event.get('payload', {})
            node_events.append({
                'type': event_type,
                'node': payload.get('node', 'unknown'),
                'timestamp': event.get('timestamp', ''),
                'duration': payload.get('duration'),
                'status': payload.get('status'),
                'error': payload.get('error'),
            })
    
    if node_events:
        print("Node Execution Timeline:")
        current_node = None
        for node_event in node_events:
            node = node_event['node']
            if node_event['type'] == 'NODE_START':
                current_node = node
                print(f"   [START] {node} started")
            elif node_event['type'] == 'NODE_SUCCESS':
                duration = node_event.get('duration', 0)
                status = node_event.get('status', 'unknown')
                print(f"   [SUCCESS] {node} completed ({duration:.2f}s) - status: {status}")
                current_node = None
            elif node_event['type'] == 'NODE_ERROR':
                error = node_event.get('error', 'unknown error')
                print(f"   [ERROR] {node} failed: {error}")
                current_node = None
        print()
    
    # Check for issues
    print("Issues Detected:")
    issues = []
    
    # Check for test gate blocks
    test_blocks = [e for e in events if e.get('event_type') == 'TEST_GATE_BLOCKED']
    if test_blocks:
        issues.append(f"WARNING: Test gate blocked {len(test_blocks)} times")
        for block in test_blocks[-3:]:  # Last 3
            errors = block.get('payload', {}).get('errors', [])
            if errors:
                issues.append(f"   -> {errors[0][:100]}")
    
    # Check for errors
    errors = [e for e in events if 'ERROR' in e.get('event_type', '')]
    if errors:
        issues.append(f"ERROR: {len(errors)} errors found")
        for error in errors[-3:]:  # Last 3
            error_msg = error.get('payload', {}).get('error', 'unknown error')
            issues.append(f"   -> {error_msg[:100]}")
    
    # Check workflow end
    workflow_ends = [e for e in events if e.get('event_type') == 'WORKFLOW_END']
    if not workflow_ends:
        issues.append("WARNING: Workflow has not ended (still running or stuck)")
    
    if not issues:
        print("   OK: No issues detected")
    else:
        for issue in issues:
            print(f"   {issue}")
    print()
    
    # Check debate report if exists
    debate_path = Path(run.run_path) / "artifacts" / "debate_report.json"
    if debate_path.exists():
        debate_data = json.loads(debate_path.read_text(encoding='utf-8'))
        print("Debate Report:")
        print(f"   Topic: {debate_data.get('topic', 'N/A')}")
        print(f"   Consensus: {debate_data.get('consensus', 'N/A')}")
        print(f"   Participants: {len(debate_data.get('arguments', []))}")
        for arg in debate_data.get('arguments', []):
            persona = arg.get('persona', 'Unknown')
            role = arg.get('role', 'Unknown')
            print(f"      - {persona} ({role})")
        print(f"   Summary: {debate_data.get('summary', 'N/A')[:200]}")
        print()
    
    # Last 5 events
    print("Last 5 Events:")
    for event in events[-5:]:
        event_type = event.get('event_type', 'UNKNOWN')
        payload = event.get('payload', {})
        timestamp = event.get('timestamp', '')[:19]  # Truncate to seconds
        
        if 'NODE' in event_type:
            node = payload.get('node', 'unknown')
            print(f"   [{timestamp}] {event_type}: {node}")
        elif 'TEST_GATE' in event_type:
            print(f"   [{timestamp}] {event_type}")
        elif 'COMMAND_EXEC' in event_type:
            cmd = payload.get('command', '')[:50]
            exit_code = payload.get('exit_code', '?')
            print(f"   [{timestamp}] {event_type}: {cmd} (exit: {exit_code})")
        else:
            print(f"   [{timestamp}] {event_type}")


if __name__ == "__main__":
    try:
        asyncio.run(check_workflow_status())
    except KeyboardInterrupt:
        print("\nWARNING: Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

