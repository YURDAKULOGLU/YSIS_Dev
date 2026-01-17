"""
Syscall journaling - Wrapper for journal writer with automatic metadata.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from ..data_plane import JournalWriter


def append_event(run_path: Path, event_type: str, event_data: dict[str, Any], trace_id: str | None = None) -> None:
    """
    Append syscall event to journal with automatic metadata.

    Args:
        run_path: Path to run directory
        event_type: Event type (e.g., "FILE_WRITE", "COMMAND_EXEC")
        event_data: Event-specific data
        trace_id: Optional trace ID (if None, will try to extract from run_path or artifacts)
    """
    journal_path = run_path / "journal" / "events.jsonl"
    writer = JournalWriter(journal_path)

    # Extract trace_id if not provided
    if trace_id is None:
        try:
            import json


            # Try to get trace_id from plan.json or other artifact
            plan_path = run_path / "artifacts" / "plan.json"
            if plan_path.exists():
                plan_data = json.loads(plan_path.read_text())
                trace_id = plan_data.get("trace_id")
            
            # Fallback: extract from run_path
            if not trace_id:
                parts = run_path.parts
                if "workspaces" in parts and "runs" in parts:
                    task_idx = parts.index("workspaces") + 1
                    run_idx = parts.index("runs") + 1
                    if task_idx < len(parts) and run_idx < len(parts):
                        task_id = parts[task_idx]
                        run_id = parts[run_idx]
                        trace_id = f"{task_id}-{run_id}"
                    else:
                        trace_id = f"trace-{run_path.name}"
                else:
                    trace_id = f"trace-{run_path.name}"
        except Exception:
            trace_id = f"trace-{run_path.name}"

    # Add automatic metadata
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "trace_id": trace_id,
        "payload": event_data,
    }

    writer.append_event(event)

