#!/usr/bin/env python3
"""
YBIS PostToolUse Hook - Tool calistiktan SONRA tetiklenir.
Metrics, verification, logging.
"""
import sys, json, os
from datetime import datetime
from pathlib import Path

METRICS_FILE = Path("/tmp/claude_metrics.json")

def collect_metrics(tool_name, duration_ms, had_error):
    metrics = {}
    if METRICS_FILE.exists():
        try: metrics = json.loads(METRICS_FILE.read_text())
        except: pass
    key = f"tool_{tool_name}"
    if key not in metrics:
        metrics[key] = {"count": 0, "total_ms": 0, "errors": 0}
    metrics[key]["count"] += 1
    metrics[key]["total_ms"] += duration_ms
    if had_error: metrics[key]["errors"] += 1
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))

def verify_file(file_path):
    if not file_path or not Path(file_path).exists():
        return {"ok": False, "reason": "File not found"}
    if file_path.endswith(".py"):
        try:
            import ast
            ast.parse(Path(file_path).read_text())
        except SyntaxError as e:
            return {"ok": False, "reason": f"Syntax error: {e}"}
    return {"ok": True}

if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        tool = data.get("tool_name", "")
        duration = data.get("duration_ms", 0)
        output = data.get("tool_output", {})
        tool_input = data.get("tool_input", {})
        
        collect_metrics(tool, duration, bool(output.get("error")))
        
        result = {"status": "ok"}
        if tool in ["Edit", "Write"]:
            result["verification"] = verify_file(tool_input.get("file_path"))
        
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"status": "ok"}))
