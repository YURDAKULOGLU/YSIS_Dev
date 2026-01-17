"""
Artifact Management MCP Tools.

Tools for reading and writing artifacts.
"""

import json
from pathlib import Path

from ...constants import PROJECT_ROOT
from ...syscalls.journal import append_event


async def artifact_read(task_id: str, run_id: str, artifact_name: str, run_path: Path | None = None, trace_id: str | None = None) -> str:
    """
    Read an artifact from a run.

    Args:
        task_id: Task identifier (e.g., "T-12345678")
        run_id: Run identifier (e.g., "run-abc123")
        artifact_name: Artifact name (e.g., "plan.json", "verifier_report.json", "executor_report.json")
        run_path: Optional run path for journal logging
        trace_id: Optional trace ID for journal logging

    Returns:
        JSON string with artifact content

    Tool Use Examples:
        - Read plan: {"task_id": "T-12345678", "run_id": "run-abc123", "artifact_name": "plan.json"}
        - Read verifier report: {"task_id": "T-12345678", "run_id": "run-abc123", "artifact_name": "verifier_report.json"}
        - Read executor report: {"task_id": "T-12345678", "run_id": "run-abc123", "artifact_name": "executor_report.json"}
    """
    artifact_run_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    artifact_path = artifact_run_path / "artifacts" / artifact_name

    if not artifact_path.exists():
        return json.dumps({"error": f"Artifact {artifact_name} not found for run {run_id}"}, indent=2)

    # Journal: MCP artifact read
    if run_path:
        append_event(
            run_path,
            "MCP_ARTIFACT_READ",
            {
                "artifact_name": artifact_name,
                "run_id": run_id,
            },
            trace_id=trace_id,
        )

    try:
        content = artifact_path.read_text(encoding="utf-8")
        # Try to parse as JSON
        try:
            data = json.loads(content)
            return json.dumps({"content": data, "raw": content}, indent=2)
        except json.JSONDecodeError:
            return json.dumps({"content": content, "raw": content}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to read artifact: {e!s}"}, indent=2)


async def artifact_write(run_id: str, name: str, content: str, run_path: Path | None = None, trace_id: str | None = None) -> str:
    """
    Write an artifact to a run's artifacts directory.

    Args:
        run_id: Run identifier (e.g., "run-abc123")
        name: Artifact name (e.g., "executor_report.json", "custom_analysis.json")
        content: Artifact content (string, can be JSON stringified)

    Returns:
        JSON string with write confirmation

    Tool Use Examples:
        - Write JSON artifact: {"run_id": "run-abc123", "name": "analysis.json", "content": "{\"result\": \"success\"}"}
        - Write text artifact: {"run_id": "run-abc123", "name": "notes.txt", "content": "Task completed successfully"}
        - Write report: {"run_id": "run-abc123", "name": "custom_report.json", "content": "{\"status\": \"done\", \"files_changed\": 3}"}
    """
    from datetime import datetime

    from ...control_plane import ControlPlaneDB

    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(str(db_path))
    await db.initialize()

    # Get run to find task_id
    run = await db.get_run(run_id)
    if not run:
        return json.dumps({"error": f"Run {run_id} not found"}, indent=2)

    # Construct artifact path
    artifact_path = PROJECT_ROOT / "workspaces" / run.task_id / "runs" / run_id / "artifacts" / name

    # Write artifact
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(content, encoding="utf-8")

    # Journal: MCP artifact create
    if run_path:
        append_event(
            run_path,
            "MCP_ARTIFACT_CREATE",
            {
                "artifact_name": name,
                "run_id": run_id,
            },
            trace_id=trace_id,
        )

    # Record FILE_WRITE event in journal
    journal_path = PROJECT_ROOT / "workspaces" / run.task_id / "runs" / run_id / "journal" / "events.jsonl"
    journal_path.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "FILE_WRITE",
        "payload": {
            "path": str(artifact_path),
            "source": "remote-worker",
            "artifact_name": name,
        },
    }

    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return json.dumps(
        {
            "run_id": run_id,
            "artifact_name": name,
            "artifact_path": str(artifact_path),
            "status": "written",
        },
        indent=2,
    )


async def approval_write(task_id: str, run_id: str, approver: str, reason: str) -> str:
    """
    Write an approval record for a blocked run.

    Args:
        task_id: Task identifier
        run_id: Run identifier
        approver: Approver identifier
        reason: Approval reason

    Returns:
        JSON string with approval confirmation
    """
    from datetime import datetime

    run_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    approval_path = run_path / "artifacts" / "approval.json"

    approval_data = {
        "task_id": task_id,
        "run_id": run_id,
        "approver": approver,
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
    }

    approval_path.parent.mkdir(parents=True, exist_ok=True)
    approval_path.write_text(json.dumps(approval_data, indent=2), encoding="utf-8")

    return json.dumps(
        {
            "task_id": task_id,
            "run_id": run_id,
            "approver": approver,
            "status": "approved",
        },
        indent=2,
    )


