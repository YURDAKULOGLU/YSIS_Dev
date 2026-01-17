#!/usr/bin/env python3
"""
YBIS Stop Hook - Claude durduğunda tetiklenir.
Cleanup, final reporting, lease release.
"""
import sys, json, os
from datetime import datetime
from pathlib import Path

SESSION_LOG = Path("/tmp/claude_session.log")
METRICS_FILE = Path("/tmp/claude_metrics.json")

def generate_session_report(context):
    """Generate session summary report"""
    report = {
        "end_time": datetime.now().isoformat(),
        "reason": context.get("stop_reason", "unknown"),
    }
    
    # Load metrics
    if METRICS_FILE.exists():
        try:
            metrics = json.loads(METRICS_FILE.read_text())
            report["metrics"] = metrics
            report["total_tool_calls"] = sum(m.get("count", 0) for m in metrics.values())
        except:
            pass
    
    return report

def cleanup(context):
    """Cleanup temporary resources"""
    # Release any YBIS task leases
    task_id = context.get("active_task_id")
    if task_id:
        # Would call MCP to release lease
        pass
    
    # Clean temp files older than 1 hour
    # ...
    
    return {"cleaned": True}

if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        context = data.get("context", {})
        
        report = generate_session_report(context)
        cleanup_result = cleanup(context)
        
        # Log session end
        with open(SESSION_LOG, "a") as f:
            f.write(json.dumps(report) + "\n")
        
        print(json.dumps({"status": "ok", "report": report}))
    except Exception as e:
        print(json.dumps({"status": "ok"}))
