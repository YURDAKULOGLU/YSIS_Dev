"""
Task Management MCP Tools.

Tools for task creation, status, claiming, and completion.
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ...constants import PROJECT_ROOT

logger = logging.getLogger(__name__)
from ...contracts import Run, Task
from ...control_plane import ControlPlaneDB
from ...data_plane import init_run_structure
from ...syscalls.journal import append_event


async def get_db(run_path: Path | None = None, trace_id: str | None = None) -> ControlPlaneDB:
    """Get initialized database connection."""
    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(str(db_path), run_path=run_path, trace_id=trace_id)
    await db.initialize()
    return db


async def task_create(title: str, objective: str, priority: str = "MEDIUM", run_path: Path | None = None, trace_id: str | None = None) -> str:
    """
    Create a new task.

    Args:
        title: Task title
        objective: Task objective
        priority: Task priority (LOW, MEDIUM, HIGH)
        run_path: Optional run path for journal logging
        trace_id: Optional trace ID for journal logging

    Returns:
        JSON string with task information

    Examples:
        Minimal usage:
        ```json
        {"title": "Fix bug", "objective": "Fix login bug", "priority": "MEDIUM"}
        ```

        Full usage:
        ```json
        {"title": "Add feature", "objective": "Add user authentication", "priority": "HIGH"}
        ```

    Tool Use Examples (for Anthropic API):
        - Minimal: {"title": "Fix bug", "objective": "Fix login bug"}
        - Typical: {"title": "Add feature", "objective": "Add user authentication", "priority": "HIGH"}
        - Complex: {"title": "Refactor module", "objective": "Refactor orchestrator for better performance", "priority": "MEDIUM"}
    """
    db = await get_db(run_path=run_path, trace_id=trace_id)
    task_id = f"T-{uuid.uuid4().hex[:8]}"
    task = Task(
        task_id=task_id,
        title=title,
        objective=objective,
        status="pending",
        priority=priority,
    )
    await db.register_task(task)

    # Journal: MCP task create
    if run_path:
        append_event(
            run_path,
            "MCP_TASK_CREATE",
            {
                "task_id": task_id,
                "title": title[:50],
            },
            trace_id=trace_id,
        )

    return json.dumps(
        {
            "task_id": task_id,
            "title": title,
            "objective": objective,
            "status": "pending",
            "priority": priority,
        },
        indent=2,
    )


async def task_status(task_id: str) -> str:
    """
    Get task status and latest run information.

    Args:
        task_id: Task identifier

    Returns:
        JSON string with task and run status
    """
    db = await get_db()
    task = await db.get_task(task_id)
    if not task:
        return json.dumps({"error": f"Task {task_id} not found"}, indent=2)

    # Get latest run for this task
    # Note: get_recent_runs doesn't take task_id, so we need to filter manually
    all_runs = await db.get_recent_runs(limit=100)
    task_runs = [r for r in all_runs if r.task_id == task_id]
    latest_run = task_runs[0] if task_runs else None

    result = {
        "task_id": task.task_id,
        "title": task.title,
        "objective": task.objective,
        "status": task.status,
        "priority": task.priority,
    }

    if latest_run:
        result["latest_run"] = {
            "run_id": latest_run.run_id,
            "status": latest_run.status,
            "risk_level": latest_run.risk_level,
        }

    return json.dumps(result, indent=2)


async def get_tasks(status: str | None = None, limit: int = 100) -> str:
    """
    Get tasks from database.

    Args:
        status: Filter by status (pending, running, completed, failed, blocked). If None, returns all.
        limit: Maximum number of tasks to return (default 100)

    Returns:
        JSON string with list of tasks
    """
    db = await get_db()
    tasks = await db.get_all_tasks(status=status, limit=limit)

    task_list = []
    for task in tasks:
        task_list.append({
            "task_id": task.task_id,
            "title": task.title,
            "objective": task.objective[:100] + "..." if len(task.objective) > 100 else task.objective,
            "status": task.status,
            "priority": task.priority,
            "protected": task.protected,
            "created_at": str(task.created_at) if task.created_at else None,
        })

    return json.dumps({
        "tasks": task_list,
        "count": len(task_list),
        "filter": status or "all",
    }, indent=2)


async def claim_task(task_id: str, worker_id: str) -> str:
    """
    Claim a task atomically.

    Args:
        task_id: Task ID to claim
        worker_id: Worker claiming the task

    Returns:
        Success/failure message
    """
    db = await get_db()
    task = await db.get_task(task_id)
    if not task:
        return f"ERROR: Task {task_id} not found"

    if task.status != "pending":
        return f"ERROR: Task {task_id} is already {task.status}"

    # Claim task with lease
    claimed = await db.claim_task(task_id, worker_id, duration_sec=300)
    if not claimed:
        return f"ERROR: Task {task_id} was claimed by another worker"

    # Initialize run structure
    run_id = f"R-{uuid.uuid4().hex[:8]}"
    run_path = init_run_structure(task_id, run_id)

    # Register run
    run = Run(
        run_id=run_id,
        task_id=task_id,
        run_path=str(run_path),
        status="running",
        started_at=datetime.now(),
    )
    await db.register_run(run)

    return f"SUCCESS: Task {task_id} claimed by {worker_id}. Run ID: {run_id}"


async def claim_next_task(worker_id: str) -> str:
    """
    Claim the next available pending task (atomic).

    Args:
        worker_id: Worker claiming the task

    Returns:
        JSON string with claimed task or message when empty
    """
    db = await get_db()
    pending_tasks = await db.get_pending_tasks()

    if not pending_tasks:
        return json.dumps({"task": None, "message": "No pending tasks available"}, indent=2)

    # Try to claim the first pending task
    task = pending_tasks[0]
    claimed = await db.claim_task(task.task_id, worker_id, duration_sec=300)

    if not claimed:
        return json.dumps({"task": None, "message": "Failed to claim task (may be already claimed)"}, indent=2)

    # Initialize run structure
    run_id = f"R-{uuid.uuid4().hex[:8]}"
    run_path = init_run_structure(task.task_id, run_id)

    # Register run
    run = Run(
        run_id=run_id,
        task_id=task.task_id,
        run_path=str(run_path),
        status="running",
        started_at=datetime.now(),
    )
    await db.register_run(run)

    return json.dumps(
        {
            "task": {
                "task_id": task.task_id,
                "title": task.title,
                "objective": task.objective,
                "status": "claimed",
            },
            "run_id": run_id,
            "run_path": str(run_path),
        },
        indent=2,
    )


async def update_task_status(task_id: str, status: str) -> str:
    """
    Update task status.

    Args:
        task_id: Task ID
        status: New status (pending, running, completed, failed)

    Returns:
        Success/failure message
    """
    db = await get_db()
    task = await db.get_task(task_id)
    if not task:
        return f"ERROR: Task {task_id} not found"

    task.status = status
    await db.register_task(task)

    return f"SUCCESS: Task {task_id} updated to {status}"


async def task_complete(task_id: str, run_id: str, status: str, result_summary: str, worker_id: str) -> str:
    """
    Mark a task as complete and release the lease.

    Args:
        task_id: Task identifier
        run_id: Run identifier
        status: Final status (completed, failed, etc.)
        result_summary: Summary of the execution result
        worker_id: Worker identifier

    Returns:
        JSON string with completion confirmation
    """
    db = await get_db()

    # Update task status
    task = await db.get_task(task_id)
    if task:
        task.status = status
        await db.register_task(task)

    # Update run status
    run = await db.get_run(run_id)
    if run:
        run.status = status
        run.completed_at = datetime.now()
        await db.register_run(run)

    # Release lease
    await db.release_lease(task_id, worker_id)

    return json.dumps(
        {
            "task_id": task_id,
            "run_id": run_id,
            "status": status,
            "result_summary": result_summary,
            "lease_released": True,
        },
        indent=2,
    )


async def task_run(task_id: str, workflow_name: str = "ybis_native") -> str:
    """
    Run a task workflow immediately (no worker lease).

    Args:
        task_id: Task identifier
        workflow_name: Workflow spec name to execute

    Returns:
        JSON string with run status and artifacts path
    """
    db = await get_db()
    task = await db.get_task(task_id)
    if not task:
        return json.dumps({"error": f"Task {task_id} not found"}, indent=2)

    run_id = f"R-{uuid.uuid4().hex[:8]}"
    trace_id = f"trace-{uuid.uuid4().hex[:16]}"
    run_path = init_run_structure(
        task_id, run_id, trace_id=trace_id, use_git_worktree=True
    )

    run = Run(
        run_id=run_id,
        task_id=task_id,
        run_path=str(run_path),
        status="running",
    )
    await db.register_run(run)

    from ...orchestrator import build_workflow_graph

    initial_state: dict[str, Any] = {
        "task_id": task_id,
        "run_id": run_id,
        "run_path": run_path,
        "trace_id": trace_id,
        "status": "pending",
        "retries": 0,
        "max_retries": 2,
        "error_context": None,
        "current_step": 0,
        "workflow_name": workflow_name,
    }

    graph = build_workflow_graph(workflow_name=workflow_name)
    final_state = graph.invoke(initial_state)

    run.status = final_state.get("status", "unknown")
    run.completed_at = datetime.now()
    await db.register_run(run)

    task.status = run.status
    await db.register_task(task)

    return json.dumps(
        {
            "task_id": task_id,
            "run_id": run_id,
            "workflow": workflow_name,
            "status": run.status,
            "artifacts_path": str(run_path / "artifacts"),
        },
        indent=2,
    )


