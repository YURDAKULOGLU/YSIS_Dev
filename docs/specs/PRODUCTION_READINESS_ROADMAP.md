# YBIS Production Readiness Roadmap

**Document Version**: 1.0
**Created**: 2026-01-11
**Status**: Ready for Execution
**Target**: 100% Production Ready

---

## Executive Summary

YBIS is currently at **30% production readiness**. The core architecture is excellent but the execution path is broken. This document provides a complete roadmap with detailed specs to reach production readiness.

**Total Estimated Effort**: 150-200 developer-hours
**Timeline**: 4 weeks (with parallel execution possible)

---

## Current State Assessment

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION READINESS                      │
├─────────────────────────────────────────────────────────────┤
│  Component              │ Status │ Blocking │ Priority      │
├─────────────────────────┼────────┼──────────┼───────────────┤
│  Core Data Models       │  95%   │    No    │ -             │
│  Syscalls Enforcement   │  90%   │    No    │ -             │
│  Control Plane DB       │  85%   │    No    │ -             │
│  Orchestrator Graph     │  75%   │   YES    │ CRITICAL      │
│  CLI Interface          │   5%   │   YES    │ CRITICAL      │
│  Worker Runtime         │   0%   │   YES    │ CRITICAL      │
│  Workflow Loading       │   0%   │   YES    │ CRITICAL      │
│  Test Suite             │  10%   │   YES    │ CRITICAL      │
│  RAG/Vector Store       │   0%   │   YES    │ CRITICAL      │
│  Adapter Implementations│  20%   │ Partial  │ HIGH          │
│  MCP Integration        │  60%   │ Partial  │ HIGH          │
│  Docker Deployment      │  20%   │   YES    │ HIGH          │
│  Monitoring/Logging     │  30%   │ Partial  │ HIGH          │
│  Documentation          │  40%   │ Partial  │ MEDIUM        │
└─────────────────────────────────────────────────────────────┘
```

---

## Roadmap Overview

```
PHASE 1: CRITICAL BLOCKERS (Week 1-2)
├── CLI-001: Build Complete CLI
├── WORKER-001: Implement Worker Runtime
├── WORKFLOW-001: Connect YAML Workflows
├── TEST-001: Fix Test Infrastructure
└── RAG-001: Index Codebase for RAG (Planner Context)

PHASE 2: HIGH PRIORITY (Week 2-3)
├── ADAPTER-001: Complete Stub Adapters
├── E2E-001: End-to-End Test Suite
├── DOCKER-001: Production Deployment
└── MONITOR-001: Monitoring Stack

PHASE 3: POLISH (Week 4)
├── DOCS-001: User Documentation
├── CLEANUP-001: Legacy Code Removal
└── API-001: API Documentation

QUICK WINS (Anytime, parallel)
├── QW-001: pyproject.toml CLI entry
├── QW-002: Fix ybis_dojo.py encoding
├── QW-003: Create .env.example
├── QW-004: Fix docker-compose worker
└── QW-005: Sample task files
```

---

# PHASE 1: CRITICAL BLOCKERS

These tasks MUST be completed first. System is unusable without them.

---

## CLI-001: Build Complete CLI Interface

**Priority**: CRITICAL
**Effort**: 16 hours
**Blocking**: Users cannot interact with system
**Dependencies**: None

### Problem

Currently there's no way for users to:
- Create tasks
- Run workflows
- Monitor status
- Approve blocked runs
- Manage workers

The `scripts/ybis_run.py` exists but is incomplete and not registered as CLI entry point.

### Solution

Create a unified CLI with subcommands using Click or Typer.

### Implementation

**File**: `src/ybis/cli/__init__.py` (NEW)

```python
"""
YBIS CLI - Command Line Interface for YBIS Platform.

Usage:
    ybis task create --objective "..." [--priority HIGH|MEDIUM|LOW]
    ybis task list [--status pending|running|completed|failed]
    ybis task status <task_id>
    ybis run <task_id> [--workflow ybis_native]
    ybis worker start [--count 1]
    ybis worker status
    ybis approve <task_id> --reason "..."
    ybis health
    ybis version
"""

import click
import asyncio
import json
from pathlib import Path
from typing import Optional

from ..constants import PROJECT_ROOT
from ..control_plane import ControlPlaneDB
from ..contracts import Task


@click.group()
@click.version_option(version="0.1.0", prog_name="ybis")
def cli():
    """YBIS - AI-Native Development Platform"""
    pass


# =============================================================================
# TASK COMMANDS
# =============================================================================

@cli.group()
def task():
    """Task management commands"""
    pass


@task.command("create")
@click.option("--objective", "-o", required=True, help="Task objective")
@click.option("--title", "-t", help="Task title (optional)")
@click.option("--priority", "-p", default="MEDIUM",
              type=click.Choice(["HIGH", "MEDIUM", "LOW"]))
def task_create(objective: str, title: Optional[str], priority: str):
    """Create a new task"""
    import uuid

    task_id = f"T-{uuid.uuid4().hex[:8].upper()}"
    task_title = title or objective[:50]

    task = Task(
        task_id=task_id,
        title=task_title,
        objective=objective,
        status="pending",
        priority=priority,
    )

    async def _create():
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()
        await db.register_task(task)
        return task_id

    task_id = asyncio.run(_create())
    click.echo(f"Created task: {task_id}")
    click.echo(f"  Title: {task_title}")
    click.echo(f"  Priority: {priority}")
    click.echo(f"\nRun with: ybis run {task_id}")


@task.command("list")
@click.option("--status", "-s", help="Filter by status")
@click.option("--limit", "-l", default=20, help="Max results")
def task_list(status: Optional[str], limit: int):
    """List tasks"""
    async def _list():
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()

        # Get tasks from database
        import aiosqlite
        async with aiosqlite.connect(db.db_path) as conn:
            if status:
                cursor = await conn.execute(
                    "SELECT task_id, title, status, priority FROM tasks WHERE status = ? LIMIT ?",
                    (status, limit)
                )
            else:
                cursor = await conn.execute(
                    "SELECT task_id, title, status, priority FROM tasks LIMIT ?",
                    (limit,)
                )
            rows = await cursor.fetchall()
        return rows

    tasks = asyncio.run(_list())

    if not tasks:
        click.echo("No tasks found.")
        return

    click.echo(f"{'TASK ID':<15} {'STATUS':<12} {'PRIORITY':<10} TITLE")
    click.echo("-" * 70)
    for task_id, title, task_status, priority in tasks:
        click.echo(f"{task_id:<15} {task_status:<12} {priority:<10} {title[:35]}")


@task.command("status")
@click.argument("task_id")
def task_status(task_id: str):
    """Get task status and details"""
    async def _status():
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()
        return await db.get_task(task_id)

    task = asyncio.run(_status())

    if not task:
        click.echo(f"Task not found: {task_id}")
        return

    click.echo(f"Task ID: {task.task_id}")
    click.echo(f"Title: {task.title}")
    click.echo(f"Status: {task.status}")
    click.echo(f"Priority: {task.priority}")
    click.echo(f"Objective: {task.objective}")


# =============================================================================
# RUN COMMANDS
# =============================================================================

@cli.command("run")
@click.argument("task_id")
@click.option("--workflow", "-w", default="ybis_native", help="Workflow to use")
@click.option("--dry-run", is_flag=True, help="Show plan without executing")
def run_task(task_id: str, workflow: str, dry_run: bool):
    """Run a task through the workflow"""
    click.echo(f"Running task {task_id} with workflow: {workflow}")

    if dry_run:
        click.echo("[DRY RUN] Would execute workflow steps:")
        click.echo("  1. spec_generator")
        click.echo("  2. planner")
        click.echo("  3. executor")
        click.echo("  4. verifier")
        click.echo("  5. gate")
        return

    from ..orchestrator.graph import create_workflow_graph
    from ..contracts import Task

    async def _run():
        # Load task
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()
        task = await db.get_task(task_id)

        if not task:
            raise click.ClickException(f"Task not found: {task_id}")

        # Create and run graph
        graph = create_workflow_graph()

        # Initialize state
        initial_state = {
            "task": task,
            "spec": None,
            "plan": None,
            "patch": None,
            "verifier_report": None,
            "gate_decision": None,
            "current_step": "start",
            "error": None,
        }

        # Run workflow
        result = await graph.ainvoke(initial_state)
        return result

    try:
        result = asyncio.run(_run())

        gate_decision = result.get("gate_decision")
        if gate_decision:
            if gate_decision.approved:
                click.echo(f"\n[SUCCESS] Task completed successfully")
            else:
                click.echo(f"\n[BLOCKED] Task blocked: {gate_decision.reason}")
        else:
            click.echo(f"\n[ERROR] Workflow did not complete")

    except Exception as e:
        click.echo(f"\n[ERROR] {str(e)}")


# =============================================================================
# WORKER COMMANDS
# =============================================================================

@cli.group()
def worker():
    """Worker management commands"""
    pass


@worker.command("start")
@click.option("--count", "-c", default=1, help="Number of workers")
@click.option("--poll-interval", default=5, help="Poll interval in seconds")
def worker_start(count: int, poll_interval: int):
    """Start background worker(s)"""
    click.echo(f"Starting {count} worker(s) with poll interval {poll_interval}s...")

    from ..worker.runtime import WorkerRuntime

    async def _run_worker():
        runtime = WorkerRuntime(poll_interval=poll_interval)
        await runtime.start()

    try:
        asyncio.run(_run_worker())
    except KeyboardInterrupt:
        click.echo("\nWorker stopped.")


@worker.command("status")
def worker_status():
    """Show worker status"""
    async def _status():
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()

        # Get active leases
        import aiosqlite
        async with aiosqlite.connect(db.db_path) as conn:
            cursor = await conn.execute(
                "SELECT worker_id, task_id, expires_at FROM leases WHERE expires_at > datetime('now')"
            )
            rows = await cursor.fetchall()
        return rows

    leases = asyncio.run(_status())

    if not leases:
        click.echo("No active workers.")
        return

    click.echo(f"{'WORKER ID':<40} {'TASK ID':<15} EXPIRES")
    click.echo("-" * 70)
    for worker_id, task_id, expires_at in leases:
        click.echo(f"{worker_id:<40} {task_id:<15} {expires_at}")


# =============================================================================
# APPROVAL COMMANDS
# =============================================================================

@cli.command("approve")
@click.argument("task_id")
@click.option("--reason", "-r", required=True, help="Approval reason")
def approve_task(task_id: str, reason: str):
    """Approve a blocked task"""
    async def _approve():
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()

        # Record approval
        from ..contracts import Approval
        import uuid

        approval = Approval(
            approval_id=f"A-{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            approved=True,
            reason=reason,
            approver="cli_user",
        )

        await db.record_approval(approval)
        return approval.approval_id

    approval_id = asyncio.run(_approve())
    click.echo(f"Approved task {task_id}")
    click.echo(f"Approval ID: {approval_id}")


# =============================================================================
# HEALTH COMMANDS
# =============================================================================

@cli.command("health")
def health_check():
    """Run system health check"""
    from ..services.health_monitor import HealthMonitor

    monitor = HealthMonitor()
    checks = monitor.run_all_checks()
    report = monitor.generate_report(checks)

    click.echo("\nYBIS Health Check")
    click.echo("=" * 50)

    summary = report["summary"]
    click.echo(f"Healthy: {summary['healthy']}/{summary['total']}")
    click.echo(f"Degraded: {summary['degraded']}")
    click.echo(f"Unhealthy: {summary['unhealthy']}")

    click.echo("\nDetails:")
    for check in report["checks"]:
        status_icon = {"healthy": "[OK]", "degraded": "[!!]", "unhealthy": "[XX]"}
        icon = status_icon.get(check["status"], "[??]")
        click.echo(f"  {icon} {check['name']}: {check['message']}")


# =============================================================================
# MAIN ENTRY
# =============================================================================

def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
```

**File**: `src/ybis/cli/utils.py` (NEW)

```python
"""CLI utility functions"""

import click
from pathlib import Path
from typing import Any
import json


def format_json(data: Any) -> str:
    """Format data as JSON"""
    return json.dumps(data, indent=2, default=str)


def format_table(headers: list[str], rows: list[list[Any]], widths: list[int] = None) -> str:
    """Format data as table"""
    if not widths:
        widths = [max(len(str(h)), max(len(str(r[i])) for r in rows) if rows else 0)
                  for i, h in enumerate(headers)]

    lines = []
    header_line = " ".join(f"{h:<{w}}" for h, w in zip(headers, widths))
    lines.append(header_line)
    lines.append("-" * len(header_line))

    for row in rows:
        lines.append(" ".join(f"{str(c):<{w}}" for c, w in zip(row, widths)))

    return "\n".join(lines)


def ensure_db_initialized():
    """Ensure database is initialized"""
    from ..constants import PROJECT_ROOT
    from ..control_plane import ControlPlaneDB
    import asyncio

    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(str(db_path))
    asyncio.run(db.initialize())
    return db
```

**File**: Update `pyproject.toml`

Add to `pyproject.toml`:

```toml
[project.scripts]
ybis = "src.ybis.cli:main"
```

### Verification

```bash
# Test CLI installation
pip install -e .
ybis --version
ybis --help

# Test task commands
ybis task create --objective "Test task"
ybis task list
ybis task status T-XXXXXXXX

# Test run
ybis run T-XXXXXXXX --dry-run

# Test health
ybis health
```

---

## WORKER-001: Implement Worker Runtime

**Priority**: CRITICAL
**Effort**: 12 hours
**Blocking**: Background processing doesn't work
**Dependencies**: CLI-001 (partial)

### Problem

`scripts/ybis_worker.py` is empty (1 line: `pass`). Workers cannot:
- Claim pending tasks
- Execute workflows
- Renew leases
- Report results

### Solution

Implement a complete worker runtime with lease management.

### Implementation

**File**: `src/ybis/worker/__init__.py` (NEW)

```python
"""YBIS Worker Module"""

from .runtime import WorkerRuntime

__all__ = ["WorkerRuntime"]
```

**File**: `src/ybis/worker/runtime.py` (NEW)

```python
"""
YBIS Worker Runtime - Background task processor.

Workers:
1. Poll for pending tasks
2. Claim tasks with lease
3. Execute workflow
4. Renew lease during execution
5. Complete or fail task
6. Release lease
"""

import asyncio
import uuid
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import logging

from ..constants import PROJECT_ROOT
from ..control_plane import ControlPlaneDB
from ..contracts import Task, Lease
from ..orchestrator.graph import create_workflow_graph

logger = logging.getLogger(__name__)


class WorkerRuntime:
    """
    Worker Runtime - Processes tasks from the queue.

    Lifecycle:
    1. Poll for pending tasks
    2. Attempt to claim task (acquire lease)
    3. Execute workflow
    4. Renew lease periodically during execution
    5. Complete or fail task
    6. Release lease and loop
    """

    def __init__(
        self,
        worker_id: Optional[str] = None,
        poll_interval: int = 5,
        lease_duration: int = 300,  # 5 minutes
        heartbeat_interval: int = 60,  # 1 minute
    ):
        """
        Initialize worker runtime.

        Args:
            worker_id: Unique worker identifier (generated if not provided)
            poll_interval: Seconds between polling for tasks
            lease_duration: Lease duration in seconds
            heartbeat_interval: Seconds between lease renewals
        """
        self.worker_id = worker_id or f"worker-{uuid.uuid4().hex[:8]}"
        self.poll_interval = poll_interval
        self.lease_duration = lease_duration
        self.heartbeat_interval = heartbeat_interval

        self.db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        self.db: Optional[ControlPlaneDB] = None

        self._running = False
        self._current_task: Optional[Task] = None
        self._current_lease: Optional[Lease] = None
        self._heartbeat_task: Optional[asyncio.Task] = None

    async def initialize(self):
        """Initialize worker resources."""
        self.db = ControlPlaneDB(str(self.db_path))
        await self.db.initialize()
        logger.info(f"Worker {self.worker_id} initialized")

    async def start(self):
        """Start the worker loop."""
        await self.initialize()
        self._running = True

        # Setup signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
            except NotImplementedError:
                # Windows doesn't support add_signal_handler
                pass

        logger.info(f"Worker {self.worker_id} starting...")

        while self._running:
            try:
                # Poll for pending tasks
                task = await self._poll_for_task()

                if task:
                    # Process the task
                    await self._process_task(task)
                else:
                    # No task available, wait before polling again
                    await asyncio.sleep(self.poll_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(self.poll_interval)

        logger.info(f"Worker {self.worker_id} stopped")

    async def stop(self):
        """Stop the worker gracefully."""
        logger.info(f"Worker {self.worker_id} stopping...")
        self._running = False

        # Cancel heartbeat if running
        if self._heartbeat_task:
            self._heartbeat_task.cancel()

        # Release current lease if held
        if self._current_lease:
            await self._release_lease()

    async def _poll_for_task(self) -> Optional[Task]:
        """Poll for and claim a pending task."""
        # Find pending task
        import aiosqlite
        async with aiosqlite.connect(self.db.db_path) as conn:
            cursor = await conn.execute(
                """
                SELECT task_id, title, objective, priority
                FROM tasks
                WHERE status = 'pending'
                ORDER BY
                    CASE priority
                        WHEN 'HIGH' THEN 1
                        WHEN 'MEDIUM' THEN 2
                        ELSE 3
                    END,
                    created_at ASC
                LIMIT 1
                """
            )
            row = await cursor.fetchone()

        if not row:
            return None

        task_id, title, objective, priority = row

        # Attempt to claim with lease
        lease = await self._acquire_lease(task_id)
        if not lease:
            return None

        # Load full task
        task = await self.db.get_task(task_id)
        return task

    async def _acquire_lease(self, task_id: str) -> Optional[Lease]:
        """Attempt to acquire lease on task."""
        import aiosqlite

        lease_id = f"lease-{uuid.uuid4().hex[:8]}"
        expires_at = datetime.utcnow() + timedelta(seconds=self.lease_duration)

        try:
            async with aiosqlite.connect(self.db.db_path) as conn:
                # Check if task already has active lease
                cursor = await conn.execute(
                    "SELECT lease_id FROM leases WHERE task_id = ? AND expires_at > datetime('now')",
                    (task_id,)
                )
                existing = await cursor.fetchone()

                if existing:
                    return None  # Task already claimed

                # Create lease
                await conn.execute(
                    """
                    INSERT INTO leases (lease_id, task_id, worker_id, expires_at, created_at)
                    VALUES (?, ?, ?, ?, datetime('now'))
                    """,
                    (lease_id, task_id, self.worker_id, expires_at.isoformat())
                )

                # Update task status
                await conn.execute(
                    "UPDATE tasks SET status = 'running' WHERE task_id = ?",
                    (task_id,)
                )

                await conn.commit()

            lease = Lease(
                lease_id=lease_id,
                task_id=task_id,
                worker_id=self.worker_id,
                expires_at=expires_at.isoformat(),
            )

            self._current_lease = lease
            logger.info(f"Acquired lease {lease_id} for task {task_id}")
            return lease

        except Exception as e:
            logger.error(f"Failed to acquire lease: {e}")
            return None

    async def _release_lease(self):
        """Release current lease."""
        if not self._current_lease:
            return

        import aiosqlite
        async with aiosqlite.connect(self.db.db_path) as conn:
            await conn.execute(
                "DELETE FROM leases WHERE lease_id = ?",
                (self._current_lease.lease_id,)
            )
            await conn.commit()

        logger.info(f"Released lease {self._current_lease.lease_id}")
        self._current_lease = None

    async def _renew_lease(self):
        """Renew current lease (heartbeat)."""
        if not self._current_lease:
            return

        new_expires = datetime.utcnow() + timedelta(seconds=self.lease_duration)

        import aiosqlite
        async with aiosqlite.connect(self.db.db_path) as conn:
            await conn.execute(
                "UPDATE leases SET expires_at = ? WHERE lease_id = ?",
                (new_expires.isoformat(), self._current_lease.lease_id)
            )
            await conn.commit()

        self._current_lease.expires_at = new_expires.isoformat()
        logger.debug(f"Renewed lease {self._current_lease.lease_id}")

    async def _heartbeat_loop(self):
        """Background task to renew lease periodically."""
        while self._running and self._current_lease:
            await asyncio.sleep(self.heartbeat_interval)
            try:
                await self._renew_lease()
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
                break

    async def _process_task(self, task: Task):
        """Process a single task."""
        self._current_task = task
        logger.info(f"Processing task {task.task_id}: {task.title}")

        # Start heartbeat
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        try:
            # Create workflow graph
            graph = create_workflow_graph()

            # Initialize state
            initial_state = {
                "task": task,
                "spec": None,
                "plan": None,
                "patch": None,
                "verifier_report": None,
                "gate_decision": None,
                "current_step": "start",
                "error": None,
            }

            # Execute workflow
            result = await graph.ainvoke(initial_state)

            # Determine outcome
            gate_decision = result.get("gate_decision")
            error = result.get("error")

            if error:
                await self._fail_task(task.task_id, str(error))
            elif gate_decision and gate_decision.approved:
                await self._complete_task(task.task_id, result)
            elif gate_decision and not gate_decision.approved:
                await self._block_task(task.task_id, gate_decision.reason)
            else:
                await self._fail_task(task.task_id, "Unknown workflow state")

        except Exception as e:
            logger.exception(f"Task execution failed: {e}")
            await self._fail_task(task.task_id, str(e))

        finally:
            # Stop heartbeat
            if self._heartbeat_task:
                self._heartbeat_task.cancel()
                self._heartbeat_task = None

            # Release lease
            await self._release_lease()
            self._current_task = None

    async def _complete_task(self, task_id: str, result: dict):
        """Mark task as completed."""
        import aiosqlite
        async with aiosqlite.connect(self.db.db_path) as conn:
            await conn.execute(
                "UPDATE tasks SET status = 'completed', completed_at = datetime('now') WHERE task_id = ?",
                (task_id,)
            )
            await conn.commit()
        logger.info(f"Task {task_id} completed")

    async def _fail_task(self, task_id: str, error: str):
        """Mark task as failed."""
        import aiosqlite
        async with aiosqlite.connect(self.db.db_path) as conn:
            await conn.execute(
                "UPDATE tasks SET status = 'failed', error = ? WHERE task_id = ?",
                (error, task_id)
            )
            await conn.commit()
        logger.error(f"Task {task_id} failed: {error}")

    async def _block_task(self, task_id: str, reason: str):
        """Mark task as blocked (awaiting approval)."""
        import aiosqlite
        async with aiosqlite.connect(self.db.db_path) as conn:
            await conn.execute(
                "UPDATE tasks SET status = 'blocked', block_reason = ? WHERE task_id = ?",
                (reason, task_id)
            )
            await conn.commit()
        logger.warning(f"Task {task_id} blocked: {reason}")
```

**File**: Update `scripts/ybis_worker.py`

```python
#!/usr/bin/env python
"""
YBIS Worker - Background task processor.

Usage:
    python scripts/ybis_worker.py [--count N] [--poll-interval SECONDS]
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.worker import WorkerRuntime
import click


@click.command()
@click.option("--count", "-c", default=1, help="Number of workers")
@click.option("--poll-interval", "-p", default=5, help="Poll interval in seconds")
def main(count: int, poll_interval: int):
    """Start YBIS worker(s)"""
    print(f"Starting {count} worker(s)...")

    async def run_workers():
        workers = []
        for i in range(count):
            worker = WorkerRuntime(poll_interval=poll_interval)
            workers.append(worker.start())
        await asyncio.gather(*workers)

    try:
        asyncio.run(run_workers())
    except KeyboardInterrupt:
        print("\nWorkers stopped.")


if __name__ == "__main__":
    main()
```

**File**: Update `src/ybis/contracts/__init__.py`

Add Lease contract if not exists:

```python
@dataclass
class Lease:
    """Task execution lease"""
    lease_id: str
    task_id: str
    worker_id: str
    expires_at: str
    created_at: str = ""
```

### Database Schema Update

**File**: `src/ybis/control_plane/db.py`

Ensure leases table exists in `initialize()`:

```python
await conn.execute("""
    CREATE TABLE IF NOT EXISTS leases (
        lease_id TEXT PRIMARY KEY,
        task_id TEXT NOT NULL,
        worker_id TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    )
""")
```

### Verification

```bash
# Start worker
python scripts/ybis_worker.py

# In another terminal, create task
ybis task create --objective "Test task"

# Worker should pick up and process task
# Check status
ybis task list
```

---

## WORKFLOW-001: Connect YAML Workflows to Graph

**Priority**: CRITICAL
**Effort**: 16 hours
**Blocking**: Only hardcoded workflow works
**Dependencies**: None

### Problem

- `configs/workflows/*.yaml` define workflows
- `src/ybis/workflows/registry.py` has `load_workflow()` but never called
- `src/ybis/orchestrator/graph.py` has hardcoded graph
- `--workflow` flag in CLI is ignored

### Solution

Implement dynamic workflow loading and graph building from YAML.

### Implementation

**File**: `src/ybis/workflows/loader.py` (NEW)

```python
"""
Workflow Loader - Loads workflow definitions from YAML.
"""

import yaml
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass

from ..constants import PROJECT_ROOT


@dataclass
class WorkflowNode:
    """Single node in workflow"""
    name: str
    node_type: str
    next_nodes: list[str]
    config: dict[str, Any]


@dataclass
class WorkflowDefinition:
    """Complete workflow definition"""
    name: str
    description: str
    version: str
    nodes: dict[str, WorkflowNode]
    entry_point: str
    exit_points: list[str]


class WorkflowLoader:
    """Loads workflow definitions from YAML files"""

    def __init__(self, workflows_dir: Optional[Path] = None):
        self.workflows_dir = workflows_dir or PROJECT_ROOT / "configs" / "workflows"
        self._cache: dict[str, WorkflowDefinition] = {}

    def load(self, workflow_name: str) -> WorkflowDefinition:
        """
        Load workflow definition by name.

        Args:
            workflow_name: Name of workflow (e.g., "ybis_native")

        Returns:
            WorkflowDefinition object
        """
        if workflow_name in self._cache:
            return self._cache[workflow_name]

        workflow_file = self.workflows_dir / f"{workflow_name}.yaml"

        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_file}")

        with open(workflow_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        definition = self._parse_definition(data)
        self._cache[workflow_name] = definition
        return definition

    def _parse_definition(self, data: dict) -> WorkflowDefinition:
        """Parse YAML data into WorkflowDefinition"""
        nodes = {}

        for node_data in data.get("nodes", []):
            node = WorkflowNode(
                name=node_data["name"],
                node_type=node_data["type"],
                next_nodes=node_data.get("next", []),
                config=node_data.get("config", {}),
            )
            nodes[node.name] = node

        return WorkflowDefinition(
            name=data.get("name", "unnamed"),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            nodes=nodes,
            entry_point=data.get("entry_point", "start"),
            exit_points=data.get("exit_points", ["end"]),
        )

    def list_workflows(self) -> list[str]:
        """List available workflow names"""
        workflows = []
        for f in self.workflows_dir.glob("*.yaml"):
            workflows.append(f.stem)
        return workflows


def get_workflow_loader() -> WorkflowLoader:
    """Get workflow loader singleton"""
    return WorkflowLoader()
```

**File**: `src/ybis/workflows/builder.py` (NEW)

```python
"""
Workflow Graph Builder - Builds LangGraph from workflow definition.
"""

from typing import Any, Callable
from langgraph.graph import StateGraph, END

from .loader import WorkflowDefinition, WorkflowNode
from .node_registry import get_node_function
from ..contracts import WorkflowState


class WorkflowGraphBuilder:
    """Builds executable LangGraph from workflow definition"""

    def __init__(self, definition: WorkflowDefinition):
        self.definition = definition

    def build(self) -> StateGraph:
        """
        Build LangGraph from workflow definition.

        Returns:
            Compiled StateGraph
        """
        # Create graph with state type
        graph = StateGraph(WorkflowState)

        # Add nodes
        for node_name, node in self.definition.nodes.items():
            node_func = self._get_node_function(node)
            graph.add_node(node_name, node_func)

        # Add edges
        for node_name, node in self.definition.nodes.items():
            if not node.next_nodes:
                # Terminal node
                graph.add_edge(node_name, END)
            elif len(node.next_nodes) == 1:
                # Single next node
                graph.add_edge(node_name, node.next_nodes[0])
            else:
                # Conditional routing
                router = self._create_router(node)
                graph.add_conditional_edges(node_name, router)

        # Set entry point
        graph.set_entry_point(self.definition.entry_point)

        return graph.compile()

    def _get_node_function(self, node: WorkflowNode) -> Callable:
        """Get node function from registry"""
        func = get_node_function(node.node_type)

        if func is None:
            # Fallback to passthrough
            async def passthrough(state: WorkflowState) -> WorkflowState:
                return state
            return passthrough

        # Wrap with config if needed
        if node.config:
            original_func = func
            async def configured_func(state: WorkflowState) -> WorkflowState:
                state["node_config"] = node.config
                return await original_func(state)
            return configured_func

        return func

    def _create_router(self, node: WorkflowNode) -> Callable:
        """Create conditional router for node"""
        next_nodes = node.next_nodes

        def router(state: WorkflowState) -> str:
            # Default routing logic based on state
            if state.get("error"):
                # Route to error handler if exists
                if "error_handler" in next_nodes:
                    return "error_handler"

            if state.get("gate_decision"):
                decision = state["gate_decision"]
                if not decision.approved and "repair" in next_nodes:
                    return "repair"

            # Default to first next node
            return next_nodes[0] if next_nodes else END

        return router


def build_workflow_graph(workflow_name: str) -> StateGraph:
    """
    Build workflow graph by name.

    Args:
        workflow_name: Name of workflow (e.g., "ybis_native")

    Returns:
        Compiled StateGraph
    """
    from .loader import get_workflow_loader

    loader = get_workflow_loader()
    definition = loader.load(workflow_name)
    builder = WorkflowGraphBuilder(definition)
    return builder.build()
```

**File**: `src/ybis/workflows/node_registry.py` (UPDATE)

```python
"""
Node Registry - Maps node types to implementation functions.
"""

from typing import Callable, Optional
from ..contracts import WorkflowState

# Node function registry
_NODE_REGISTRY: dict[str, Callable] = {}


def register_node(node_type: str):
    """Decorator to register node function"""
    def decorator(func: Callable):
        _NODE_REGISTRY[node_type] = func
        return func
    return decorator


def get_node_function(node_type: str) -> Optional[Callable]:
    """Get node function by type"""
    return _NODE_REGISTRY.get(node_type)


def list_node_types() -> list[str]:
    """List registered node types"""
    return list(_NODE_REGISTRY.keys())


# =============================================================================
# BUILT-IN NODE IMPLEMENTATIONS
# =============================================================================

@register_node("spec_generator")
async def spec_generator_node(state: WorkflowState) -> WorkflowState:
    """Generate spec from task"""
    from ..orchestrator.spec_generator import generate_spec

    task = state["task"]
    spec = await generate_spec(task)
    state["spec"] = spec
    state["current_step"] = "spec_generated"
    return state


@register_node("planner")
async def planner_node(state: WorkflowState) -> WorkflowState:
    """Generate plan from spec"""
    from ..orchestrator.planner import plan_task

    task = state["task"]
    plan = plan_task(task)
    state["plan"] = plan
    state["current_step"] = "planned"
    return state


@register_node("executor")
async def executor_node(state: WorkflowState) -> WorkflowState:
    """Execute plan"""
    from ..orchestrator.executor import execute_plan

    plan = state["plan"]
    task = state["task"]
    patch = await execute_plan(task, plan)
    state["patch"] = patch
    state["current_step"] = "executed"
    return state


@register_node("verifier")
async def verifier_node(state: WorkflowState) -> WorkflowState:
    """Verify execution results"""
    from ..orchestrator.verifier import verify_patch

    patch = state["patch"]
    task = state["task"]
    report = await verify_patch(task, patch)
    state["verifier_report"] = report
    state["current_step"] = "verified"
    return state


@register_node("gate")
async def gate_node(state: WorkflowState) -> WorkflowState:
    """Gate decision"""
    from ..orchestrator.gates import evaluate_gate

    task = state["task"]
    verifier_report = state["verifier_report"]
    patch = state["patch"]

    decision = await evaluate_gate(task, verifier_report, patch)
    state["gate_decision"] = decision
    state["current_step"] = "gated"
    return state


@register_node("repair")
async def repair_node(state: WorkflowState) -> WorkflowState:
    """Repair failed execution"""
    from ..orchestrator.repair import repair_execution

    task = state["task"]
    verifier_report = state["verifier_report"]

    repair_result = await repair_execution(task, verifier_report)
    state["patch"] = repair_result.patch
    state["current_step"] = "repaired"
    return state


@register_node("debate")
async def debate_node(state: WorkflowState) -> WorkflowState:
    """Multi-model debate on decision"""
    from ..orchestrator.debate import run_debate

    task = state["task"]
    gate_decision = state["gate_decision"]

    debate_result = await run_debate(task, gate_decision)
    state["debate_result"] = debate_result
    state["current_step"] = "debated"
    return state


@register_node("human_approval")
async def human_approval_node(state: WorkflowState) -> WorkflowState:
    """Wait for human approval"""
    state["awaiting_approval"] = True
    state["current_step"] = "awaiting_approval"
    return state


@register_node("passthrough")
async def passthrough_node(state: WorkflowState) -> WorkflowState:
    """Passthrough node (no-op)"""
    return state
```

**File**: Update `src/ybis/orchestrator/graph.py`

```python
"""
Orchestrator Graph - Main workflow execution.
"""

from typing import Optional
from langgraph.graph import StateGraph

from ..contracts import WorkflowState


def create_workflow_graph(workflow_name: str = "ybis_native") -> StateGraph:
    """
    Create workflow graph.

    Args:
        workflow_name: Name of workflow to load (default: ybis_native)

    Returns:
        Compiled StateGraph
    """
    from ..workflows.builder import build_workflow_graph

    try:
        return build_workflow_graph(workflow_name)
    except FileNotFoundError:
        # Fallback to hardcoded graph for backwards compatibility
        return _create_default_graph()


def _create_default_graph() -> StateGraph:
    """Create default hardcoded graph (fallback)"""
    from langgraph.graph import END
    from ..workflows.node_registry import (
        spec_generator_node,
        planner_node,
        executor_node,
        verifier_node,
        gate_node,
    )

    graph = StateGraph(WorkflowState)

    graph.add_node("spec_generator", spec_generator_node)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("gate", gate_node)

    graph.add_edge("spec_generator", "planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "verifier")
    graph.add_edge("verifier", "gate")
    graph.add_edge("gate", END)

    graph.set_entry_point("spec_generator")

    return graph.compile()
```

### Verification

```bash
# List available workflows
python -c "from src.ybis.workflows.loader import get_workflow_loader; print(get_workflow_loader().list_workflows())"

# Run with specific workflow
ybis run T-XXXXXXXX --workflow ybis_native
ybis run T-XXXXXXXX --workflow self_improve
```

---

## TEST-001: Fix Test Infrastructure

**Priority**: CRITICAL
**Effort**: 8 hours
**Blocking**: Can't run tests, can't verify changes
**Dependencies**: None

### Problem

- 16 test collection errors
- Tests import from deprecated `src.agentic` and `src.utils`
- `conftest.py` doesn't set up paths correctly
- No fixtures for database setup/teardown

### Solution

Fix imports, update conftest, create proper fixtures.

### Implementation

**File**: `tests/conftest.py` (UPDATE)

```python
"""
Pytest configuration and fixtures.
"""

import pytest
import asyncio
import sys
from pathlib import Path
import tempfile
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Now imports work
from src.ybis.constants import PROJECT_ROOT as YBIS_ROOT
from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Task


# =============================================================================
# ASYNC SUPPORT
# =============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# =============================================================================
# DATABASE FIXTURES
# =============================================================================

@pytest.fixture
async def db(tmp_path):
    """Provide a clean database for tests"""
    db_path = tmp_path / "test_control_plane.db"
    db = ControlPlaneDB(str(db_path))
    await db.initialize()
    yield db
    # Cleanup happens automatically with tmp_path


@pytest.fixture
async def db_with_task(db):
    """Database with a sample task"""
    task = Task(
        task_id="T-TEST001",
        title="Test Task",
        objective="This is a test task",
        status="pending",
        priority="MEDIUM",
    )
    await db.register_task(task)
    yield db, task


# =============================================================================
# WORKSPACE FIXTURES
# =============================================================================

@pytest.fixture
def workspace(tmp_path):
    """Provide a clean workspace directory"""
    ws = tmp_path / "workspace"
    ws.mkdir()
    yield ws


@pytest.fixture
def sample_python_file(workspace):
    """Create a sample Python file"""
    file_path = workspace / "sample.py"
    file_path.write_text("""
def hello():
    return "Hello, World!"

def add(a, b):
    return a + b
""")
    yield file_path


# =============================================================================
# MOCK FIXTURES
# =============================================================================

@pytest.fixture
def mock_llm_response(mocker):
    """Mock LLM responses"""
    def _mock(response_text: str):
        mock_completion = mocker.MagicMock()
        mock_completion.choices = [
            mocker.MagicMock(message=mocker.MagicMock(content=response_text))
        ]
        mocker.patch("litellm.completion", return_value=mock_completion)
        return mock_completion
    return _mock


# =============================================================================
# POLICY FIXTURES
# =============================================================================

@pytest.fixture
def default_policy():
    """Default test policy"""
    return {
        "sandbox": {"enabled": False, "network": False},
        "exec": {"allowlist": ["python", "pytest", "ruff"]},
        "paths": {"protected": []},
        "gates": {"require_verifier_pass": True},
    }


@pytest.fixture
def mock_policy(mocker, default_policy):
    """Mock policy provider"""
    mock_provider = mocker.MagicMock()
    mock_provider.get_policy.return_value = default_policy
    mock_provider.is_sandbox_enabled.return_value = False
    mock_provider.get_exec_allowlist.return_value = ["python", "pytest", "ruff"]

    mocker.patch(
        "src.ybis.services.policy.get_policy_provider",
        return_value=mock_provider
    )
    return mock_provider
```

**File**: `tests/unit/test_imports.py` (NEW)

```python
"""
Test that all imports work correctly.
"""

import pytest


class TestImports:
    """Test module imports"""

    def test_import_contracts(self):
        from src.ybis.contracts import Task, Plan, Spec
        assert Task is not None

    def test_import_control_plane(self):
        from src.ybis.control_plane import ControlPlaneDB
        assert ControlPlaneDB is not None

    def test_import_orchestrator(self):
        from src.ybis.orchestrator.graph import create_workflow_graph
        assert create_workflow_graph is not None

    def test_import_services(self):
        from src.ybis.services.policy import get_policy_provider
        from src.ybis.services.health_monitor import HealthMonitor
        from src.ybis.services.lesson_engine import LessonEngine
        assert get_policy_provider is not None

    def test_import_adapters(self):
        from src.ybis.adapters.registry import get_registry
        assert get_registry is not None

    def test_import_cli(self):
        from src.ybis.cli import main
        assert main is not None

    def test_import_worker(self):
        from src.ybis.worker import WorkerRuntime
        assert WorkerRuntime is not None
```

**File**: `tests/unit/test_control_plane.py` (UPDATE)

```python
"""
Tests for Control Plane database operations.
"""

import pytest
from src.ybis.contracts import Task


class TestControlPlane:
    """Control plane database tests"""

    @pytest.mark.asyncio
    async def test_register_task(self, db):
        """Test task registration"""
        task = Task(
            task_id="T-001",
            title="Test",
            objective="Test objective",
            status="pending",
            priority="HIGH",
        )
        await db.register_task(task)

        loaded = await db.get_task("T-001")
        assert loaded is not None
        assert loaded.task_id == "T-001"
        assert loaded.status == "pending"

    @pytest.mark.asyncio
    async def test_update_task_status(self, db_with_task):
        """Test task status update"""
        db, task = db_with_task

        await db.update_task_status(task.task_id, "running")

        loaded = await db.get_task(task.task_id)
        assert loaded.status == "running"

    @pytest.mark.asyncio
    async def test_get_nonexistent_task(self, db):
        """Test getting task that doesn't exist"""
        task = await db.get_task("T-NONEXISTENT")
        assert task is None
```

**Action**: Delete or fix broken test files

Remove these files that import from deprecated modules:
- `tests/regression_tests/test_code_quality.py` (imports `src.utils`)
- `tests/unit/test_ybis_messaging.py` (imports `src.agentic`)
- `tests/unit/test_local_rag.py` (imports `rag.local_rag`)
- `tests/unit/test_math_utils.py` (imports `src.utils`)

Or update their imports to use `src.ybis.*`

### Verification

```bash
# Run all tests
pytest tests/ -v

# Should see 0 collection errors
# Should see tests passing
```

---

## RAG-001: Index Codebase for RAG

**Priority**: CRITICAL
**Effort**: 8 hours
**Blocking**: Planner generates hallucinated file names without context
**Dependencies**: ChromaDB, Ollama with nomic-embed-text

### Problem

The planner queries a `"codebase"` collection that **doesn't exist**:

```python
# planner.py line 191
vector_results = self.vector_store.query("codebase", objective, top_k=3)
```

**Current state:**
- No `.chroma` directory (vector store never initialized)
- No codebase indexing script exists
- `ingest_docs_to_rag.py` only indexes external docs, NOT `src/ybis/**`
- Planner falls back to LLM hallucination (invents file names like `refactor.py`, `bootstrap.py`)

**Evidence** from `workspaces/SELF-IMPROVE-BE6D024E/runs/R-97afa1cb/artifacts/improvement_plan.json`:
```json
{
  "files": ["refactor.py", "bootstrap.py", "resilient.py"],  // DON'T EXIST!
}
```

### Solution

Create codebase indexing script and ensure it runs before planning.

### Implementation

**File**: `scripts/index_codebase.py` (NEW)

```python
#!/usr/bin/env python3
"""
Index YBIS codebase into vector store for RAG.

This enables the planner to find relevant code context
instead of hallucinating file names.

Usage:
    python scripts/index_codebase.py [--collection codebase] [--chunk-size 80]
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def extract_docstrings_and_signatures(content: str) -> list[dict]:
    """Extract docstrings and function signatures for better indexing."""
    import ast

    chunks = []
    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Get docstring
                docstring = ast.get_docstring(node) or ""

                # Get signature
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [arg.arg for arg in node.args.args]
                    signature = f"def {node.name}({', '.join(args)})"
                else:
                    signature = f"class {node.name}"

                # Get source lines
                start_line = node.lineno
                end_line = node.end_lineno or start_line + 10

                chunks.append({
                    "type": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                    "name": node.name,
                    "signature": signature,
                    "docstring": docstring,
                    "start_line": start_line,
                    "end_line": end_line,
                })
    except SyntaxError:
        pass  # Fall back to line-based chunking

    return chunks


def chunk_by_lines(content: str, chunk_size: int = 80) -> list[tuple[int, str]]:
    """Chunk content by lines."""
    lines = content.split("\n")
    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunk = "\n".join(lines[i:i + chunk_size])
        if chunk.strip():
            chunks.append((i + 1, chunk))

    return chunks


def index_codebase(
    collection: str = "codebase",
    chunk_size: int = 80,
    include_patterns: list[str] = None,
) -> int:
    """
    Index codebase into vector store.

    Args:
        collection: Vector store collection name
        chunk_size: Lines per chunk for line-based chunking
        include_patterns: Glob patterns to include (default: src/ybis/**/*.py)

    Returns:
        Number of chunks indexed
    """
    from ybis.data_plane.vector_store import VectorStore

    if include_patterns is None:
        include_patterns = [
            "src/ybis/**/*.py",
            "src/ybis/**/*.md",
        ]

    vs = VectorStore()

    docs = []
    metadata = []
    total_chunks = 0

    for pattern in include_patterns:
        for file_path in PROJECT_ROOT.glob(pattern):
            # Skip test files and __pycache__
            if "__pycache__" in str(file_path) or "test_" in file_path.name:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            rel_path = str(file_path.relative_to(PROJECT_ROOT))

            # Try AST-based extraction for Python files
            if file_path.suffix == ".py":
                ast_chunks = extract_docstrings_and_signatures(content)

                for chunk in ast_chunks:
                    # Create searchable document
                    doc_text = f"""
File: {rel_path}
{chunk['type'].title()}: {chunk['signature']}

{chunk['docstring']}
"""
                    docs.append(doc_text.strip())
                    metadata.append({
                        "file": rel_path,
                        "type": chunk["type"],
                        "name": chunk["name"],
                        "start_line": chunk["start_line"],
                        "end_line": chunk["end_line"],
                    })

            # Also do line-based chunking for full context
            for start_line, chunk in chunk_by_lines(content, chunk_size):
                doc_text = f"File: {rel_path} (lines {start_line}-{start_line + chunk_size})\n\n{chunk}"
                docs.append(doc_text)
                metadata.append({
                    "file": rel_path,
                    "start_line": start_line,
                    "type": "code_chunk",
                })

            # Batch insert
            if len(docs) >= 50:
                vs.add_documents(collection, docs, metadata)
                total_chunks += len(docs)
                print(f"  Indexed {total_chunks} chunks...")
                docs, metadata = [], []

    # Final batch
    if docs:
        vs.add_documents(collection, docs, metadata)
        total_chunks += len(docs)

    return total_chunks


def main():
    parser = argparse.ArgumentParser(description="Index codebase for RAG")
    parser.add_argument(
        "--collection",
        default="codebase",
        help="Vector store collection name (default: codebase)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=80,
        help="Lines per chunk (default: 80)",
    )

    args = parser.parse_args()

    print("=" * 50)
    print("YBIS Codebase Indexer")
    print("=" * 50)
    print()
    print("Prerequisites:")
    print("  1. ChromaDB installed: pip install chromadb")
    print("  2. Ollama running with nomic-embed-text:")
    print("     ollama pull nomic-embed-text")
    print()

    try:
        total = index_codebase(
            collection=args.collection,
            chunk_size=args.chunk_size,
        )
        print()
        print(f"[SUCCESS] Indexed {total} chunks into '{args.collection}' collection")
        print(f"[INFO] Vector store saved to: .chroma/")
        return 0

    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        print()
        print("Install with:")
        print("  pip install chromadb litellm")
        return 1

    except Exception as e:
        print(f"[ERROR] Indexing failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**File**: `scripts/verify_rag.py` (NEW)

```python
#!/usr/bin/env python3
"""
Verify RAG is working by querying the codebase collection.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def verify_rag():
    from ybis.data_plane.vector_store import VectorStore

    print("Checking RAG status...")
    print()

    # Check if .chroma exists
    chroma_dir = PROJECT_ROOT / ".chroma"
    if not chroma_dir.exists():
        print("[FAIL] .chroma directory not found")
        print("       Run: python scripts/index_codebase.py")
        return False

    print(f"[OK] .chroma directory exists")

    # Try to query
    try:
        vs = VectorStore()
        results = vs.query("codebase", "dependency graph analysis", top_k=3)

        if not results:
            print("[FAIL] No results returned - collection may be empty")
            print("       Run: python scripts/index_codebase.py")
            return False

        print(f"[OK] Query returned {len(results)} results")
        print()
        print("Sample result:")
        print("-" * 40)
        print(results[0]["document"][:300] + "...")
        print("-" * 40)
        print()
        print("[SUCCESS] RAG is working!")
        return True

    except Exception as e:
        print(f"[FAIL] Query failed: {e}")
        return False


if __name__ == "__main__":
    success = verify_rag()
    sys.exit(0 if success else 1)
```

### CLI Integration

**File**: Update `src/ybis/cli/__init__.py`

Add RAG commands:

```python
@cli.group()
def rag():
    """RAG/Vector store commands"""
    pass


@rag.command("index")
@click.option("--collection", default="codebase", help="Collection name")
def rag_index(collection: str):
    """Index codebase for RAG"""
    import subprocess
    result = subprocess.run(
        ["python", "scripts/index_codebase.py", "--collection", collection],
        cwd=PROJECT_ROOT,
    )
    sys.exit(result.returncode)


@rag.command("verify")
def rag_verify():
    """Verify RAG is working"""
    import subprocess
    result = subprocess.run(
        ["python", "scripts/verify_rag.py"],
        cwd=PROJECT_ROOT,
    )
    sys.exit(result.returncode)


@rag.command("query")
@click.argument("query")
@click.option("--top-k", default=5, help="Number of results")
def rag_query(query: str, top_k: int):
    """Query the codebase"""
    from ..data_plane.vector_store import VectorStore

    try:
        vs = VectorStore()
        results = vs.query("codebase", query, top_k=top_k)

        for i, result in enumerate(results, 1):
            click.echo(f"\n--- Result {i} (distance: {result['distance']:.4f}) ---")
            click.echo(f"File: {result['metadata'].get('file', 'unknown')}")
            click.echo(result['document'][:500])

    except Exception as e:
        click.echo(f"Error: {e}")
```

### Automatic Indexing on First Run

**File**: Update `src/ybis/orchestrator/planner.py`

Add auto-index check:

```python
def _ensure_codebase_indexed(self):
    """Ensure codebase is indexed before planning."""
    if not self.vector_store:
        return

    try:
        # Quick check if collection has documents
        results = self.vector_store.query("codebase", "test", top_k=1)
        if not results:
            import logging
            logging.warning(
                "RAG codebase collection is empty. "
                "Run 'python scripts/index_codebase.py' for better planning."
            )
    except Exception:
        pass  # Vector store may not be available
```

Call in `plan()` method:

```python
def plan(self, task: Task) -> Plan:
    # Check RAG is ready
    self._ensure_codebase_indexed()

    # ... rest of method
```

### Verification

```bash
# 1. Pull embedding model
ollama pull nomic-embed-text

# 2. Index codebase
python scripts/index_codebase.py

# Expected output:
# Indexed 50 chunks...
# Indexed 100 chunks...
# [SUCCESS] Indexed 342 chunks into 'codebase' collection

# 3. Verify
python scripts/verify_rag.py

# Expected output:
# [OK] .chroma directory exists
# [OK] Query returned 3 results
# [SUCCESS] RAG is working!

# 4. Test query
python -c "
from src.ybis.data_plane.vector_store import VectorStore
vs = VectorStore()
results = vs.query('codebase', 'how to analyze dependencies', top_k=3)
for r in results:
    print(r['metadata'].get('file'), r['distance'])
"

# Expected: Real files like src/ybis/dependencies/graph.py
```

### Impact

After RAG-001:
- Planner gets real codebase context
- No more hallucinated file names
- Self-improvement plans reference actual modules
- Better code generation with relevant examples

---

# PHASE 2: HIGH PRIORITY

Complete after Phase 1. System works but with limited features.

---

## ADAPTER-001: Complete Stub Adapters

**Priority**: HIGH
**Effort**: 24 hours
**Dependencies**: Phase 1 complete

### Problem

6 adapters have stub implementations:
- `aiwaves_agents.py` - 5 TODOs
- `llm_council.py` - Multi-model review not implemented
- `reactive_agents.py` - Framework integration missing
- `evoagentx.py` - Evolution logic not implemented
- `self_improve_swarms.py` - 5+ TODOs
- `llamaindex_adapter.py` - RAG integration missing

### Solution

Implement each adapter or create functional in-house alternatives.

### Implementation Priority

1. **llamaindex_adapter.py** - RAG is important for context
2. **llm_council.py** - Multi-model consensus adds reliability
3. **self_improve_swarms.py** - Core to self-improvement
4. Others - Lower priority, can remain stubs

### Spec: llamaindex_adapter.py

**File**: `src/ybis/adapters/llamaindex_adapter.py`

```python
"""
LlamaIndex Adapter - RAG integration for codebase understanding.
"""

from pathlib import Path
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class LlamaIndexAdapter:
    """
    LlamaIndex integration for advanced RAG.

    Provides:
    - Codebase indexing
    - Semantic search
    - Context retrieval for planning
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._index = None
        self._available = False
        self._initialize()

    def _initialize(self):
        """Initialize LlamaIndex if available"""
        try:
            from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
            from llama_index.core.node_parser import CodeSplitter
            self._available = True
        except ImportError:
            logger.warning("LlamaIndex not installed. RAG features disabled.")
            self._available = False

    def is_available(self) -> bool:
        """Check if LlamaIndex is available"""
        return self._available

    def index_codebase(self, directories: list[str] = None) -> bool:
        """
        Index codebase for semantic search.

        Args:
            directories: List of directories to index (default: src/ybis)

        Returns:
            True if indexing successful
        """
        if not self._available:
            return False

        try:
            from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
            from llama_index.core.node_parser import CodeSplitter

            dirs = directories or ["src/ybis"]
            all_docs = []

            for dir_path in dirs:
                full_path = self.project_root / dir_path
                if full_path.exists():
                    reader = SimpleDirectoryReader(
                        input_dir=str(full_path),
                        recursive=True,
                        required_exts=[".py", ".md", ".yaml"],
                    )
                    docs = reader.load_data()
                    all_docs.extend(docs)

            if not all_docs:
                logger.warning("No documents found to index")
                return False

            # Create index with code-aware splitting
            splitter = CodeSplitter(
                language="python",
                chunk_lines=40,
                chunk_lines_overlap=15,
            )

            self._index = VectorStoreIndex.from_documents(
                all_docs,
                transformations=[splitter],
            )

            logger.info(f"Indexed {len(all_docs)} documents")
            return True

        except Exception as e:
            logger.error(f"Indexing failed: {e}")
            return False

    def query_codebase(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Query codebase for relevant context.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of relevant documents with metadata
        """
        if not self._available or not self._index:
            return []

        try:
            query_engine = self._index.as_query_engine(similarity_top_k=top_k)
            response = query_engine.query(query)

            results = []
            for node in response.source_nodes:
                results.append({
                    "document": node.text,
                    "file_path": node.metadata.get("file_path", ""),
                    "score": node.score,
                })

            return results

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []

    def get_file_context(self, file_path: str) -> Optional[str]:
        """
        Get context for a specific file.

        Args:
            file_path: Path to file

        Returns:
            File content with context
        """
        if not self._available:
            return None

        full_path = self.project_root / file_path
        if not full_path.exists():
            return None

        try:
            return full_path.read_text(encoding="utf-8")
        except Exception:
            return None
```

### Spec: llm_council.py

**File**: `src/ybis/adapters/llm_council.py`

```python
"""
LLM Council Adapter - Multi-model consensus for critical decisions.
"""

import asyncio
from typing import Any
import logging

logger = logging.getLogger(__name__)


class LLMCouncilAdapter:
    """
    Multi-model council for consensus-based decisions.

    Uses multiple LLMs to review and vote on decisions,
    reducing single-model bias and improving reliability.
    """

    def __init__(self, models: list[str] = None):
        """
        Initialize council.

        Args:
            models: List of model names (default: diverse set)
        """
        self.models = models or [
            "ollama/llama3.2:3b",
            "ollama/qwen2.5-coder:7b",
            "ollama/mistral:7b",
        ]

    async def review(
        self,
        prompt: str,
        candidates: list[str],
        criteria: str = "quality and correctness",
    ) -> dict[str, Any]:
        """
        Get council review and ranking of candidates.

        Args:
            prompt: Context/question for review
            candidates: List of candidate responses/solutions
            criteria: Evaluation criteria

        Returns:
            Council decision with rankings and rationale
        """
        try:
            import litellm
        except ImportError:
            return {"error": "litellm not installed", "winner": candidates[0] if candidates else None}

        votes = []
        rationales = []

        review_prompt = f"""
You are evaluating candidates based on: {criteria}

Context: {prompt}

Candidates:
{chr(10).join(f'{i+1}. {c}' for i, c in enumerate(candidates))}

Which candidate is best? Respond with JSON:
{{"winner": <number>, "rationale": "<brief explanation>"}}
"""

        # Query each model
        tasks = []
        for model in self.models:
            tasks.append(self._query_model(model, review_prompt))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Aggregate votes
        for result in results:
            if isinstance(result, dict) and "winner" in result:
                votes.append(result["winner"])
                rationales.append(result.get("rationale", ""))

        if not votes:
            return {"error": "No valid votes", "winner": candidates[0] if candidates else None}

        # Determine winner by majority
        from collections import Counter
        vote_counts = Counter(votes)
        winner_idx = vote_counts.most_common(1)[0][0]

        return {
            "winner": candidates[winner_idx - 1] if 0 < winner_idx <= len(candidates) else None,
            "winner_index": winner_idx,
            "vote_counts": dict(vote_counts),
            "rationales": rationales,
            "models_voted": len(votes),
            "consensus": vote_counts.most_common(1)[0][1] / len(votes) if votes else 0,
        }

    async def _query_model(self, model: str, prompt: str) -> dict:
        """Query single model"""
        try:
            import litellm
            import json

            response = await asyncio.to_thread(
                litellm.completion,
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                timeout=30,
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            logger.warning(f"Model {model} failed: {e}")
            return {"error": str(e)}

    async def debate(
        self,
        topic: str,
        positions: list[str],
        rounds: int = 2,
    ) -> dict[str, Any]:
        """
        Run multi-round debate between models.

        Args:
            topic: Debate topic
            positions: Initial positions to debate
            rounds: Number of debate rounds

        Returns:
            Debate transcript and final consensus
        """
        transcript = []
        current_positions = positions.copy()

        for round_num in range(rounds):
            round_responses = []

            for i, model in enumerate(self.models[:len(positions)]):
                position = current_positions[i % len(current_positions)]

                debate_prompt = f"""
Topic: {topic}
Your position: {position}
Other positions: {[p for j, p in enumerate(current_positions) if j != i]}

Defend your position or update it based on the debate. Respond with:
{{"position": "<your current position>", "argument": "<your argument>"}}
"""

                response = await self._query_model(model, debate_prompt)
                round_responses.append({
                    "model": model,
                    "response": response,
                })

                if isinstance(response, dict) and "position" in response:
                    current_positions[i % len(current_positions)] = response["position"]

            transcript.append({
                "round": round_num + 1,
                "responses": round_responses,
            })

        # Final vote
        final_review = await self.review(
            f"After debate on '{topic}'",
            current_positions,
            "strongest argument and position",
        )

        return {
            "transcript": transcript,
            "final_positions": current_positions,
            "consensus": final_review,
        }
```

### Remaining Adapters

For `self_improve_swarms.py`, `evoagentx.py`, `aiwaves_agents.py`, and `reactive_agents.py`:

Create minimal in-house implementations that:
1. Use existing YBIS services (Health Monitor, Error KB, Lesson Engine)
2. Don't require external packages
3. Provide basic functionality

See `docs/specs/SELF_IMPROVEMENT_LOOP_SPECS.md` for self-improve implementation details.

---

## E2E-001: End-to-End Test Suite

**Priority**: HIGH
**Effort**: 20 hours
**Dependencies**: Phase 1 complete

### Implementation

**File**: `tests/e2e/test_golden_path.py` (NEW)

```python
"""
End-to-end golden path tests.

Tests complete workflow: create → run → verify → complete
"""

import pytest
import asyncio
from pathlib import Path

from src.ybis.contracts import Task
from src.ybis.control_plane import ControlPlaneDB
from src.ybis.orchestrator.graph import create_workflow_graph


class TestGoldenPath:
    """End-to-end workflow tests"""

    @pytest.fixture
    async def setup_db(self, tmp_path):
        """Setup test database"""
        db_path = tmp_path / "test.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()
        return db

    @pytest.mark.asyncio
    async def test_create_and_run_simple_task(self, setup_db, tmp_path):
        """Test creating and running a simple task"""
        db = setup_db

        # Create task
        task = Task(
            task_id="T-E2E-001",
            title="Create hello.py",
            objective="Create a file hello.py that prints 'Hello, World!'",
            status="pending",
            priority="MEDIUM",
        )
        await db.register_task(task)

        # Verify task created
        loaded = await db.get_task("T-E2E-001")
        assert loaded is not None
        assert loaded.status == "pending"

        # Run workflow (with mocked executor)
        graph = create_workflow_graph("ybis_native")

        initial_state = {
            "task": task,
            "spec": None,
            "plan": None,
            "patch": None,
            "verifier_report": None,
            "gate_decision": None,
            "current_step": "start",
            "error": None,
        }

        # Note: This will use real LLM unless mocked
        # For CI, we'd mock the LLM responses

    @pytest.mark.asyncio
    async def test_task_lifecycle(self, setup_db):
        """Test complete task lifecycle"""
        db = setup_db

        # 1. Create
        task = Task(
            task_id="T-LIFECYCLE",
            title="Lifecycle Test",
            objective="Test task lifecycle",
            status="pending",
            priority="HIGH",
        )
        await db.register_task(task)

        # 2. Claim (simulate worker)
        await db.update_task_status("T-LIFECYCLE", "running")

        # 3. Complete
        await db.update_task_status("T-LIFECYCLE", "completed")

        # Verify
        final = await db.get_task("T-LIFECYCLE")
        assert final.status == "completed"

    @pytest.mark.asyncio
    async def test_blocked_task_approval(self, setup_db):
        """Test approval flow for blocked task"""
        db = setup_db

        # Create and block task
        task = Task(
            task_id="T-BLOCKED",
            title="Protected Path Edit",
            objective="Edit src/ybis/contracts/resources.py",
            status="blocked",
            priority="HIGH",
        )
        await db.register_task(task)

        # Record approval
        from src.ybis.contracts import Approval
        approval = Approval(
            approval_id="A-001",
            task_id="T-BLOCKED",
            approved=True,
            reason="Reviewed and safe",
            approver="test_user",
        )
        await db.record_approval(approval)

        # Verify approval recorded
        # (Implementation depends on db schema)
```

**File**: `tests/e2e/test_worker.py` (NEW)

```python
"""
Worker integration tests.
"""

import pytest
import asyncio

from src.ybis.worker import WorkerRuntime
from src.ybis.contracts import Task
from src.ybis.control_plane import ControlPlaneDB


class TestWorker:
    """Worker runtime tests"""

    @pytest.mark.asyncio
    async def test_worker_claims_task(self, tmp_path):
        """Test worker claiming a pending task"""
        # Setup
        db_path = tmp_path / "test.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()

        # Create pending task
        task = Task(
            task_id="T-WORKER-001",
            title="Worker Test",
            objective="Test worker claim",
            status="pending",
            priority="MEDIUM",
        )
        await db.register_task(task)

        # Create worker (won't start loop, just test methods)
        worker = WorkerRuntime(poll_interval=1)
        worker.db = db

        # Poll for task
        claimed = await worker._poll_for_task()

        assert claimed is not None
        assert claimed.task_id == "T-WORKER-001"

    @pytest.mark.asyncio
    async def test_worker_lease_renewal(self, tmp_path):
        """Test lease renewal"""
        db_path = tmp_path / "test.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()

        # Create and claim task
        task = Task(
            task_id="T-LEASE-001",
            title="Lease Test",
            objective="Test lease renewal",
            status="pending",
            priority="MEDIUM",
        )
        await db.register_task(task)

        worker = WorkerRuntime(lease_duration=60)
        worker.db = db

        # Claim
        claimed = await worker._poll_for_task()
        assert worker._current_lease is not None

        original_expires = worker._current_lease.expires_at

        # Renew
        await worker._renew_lease()

        assert worker._current_lease.expires_at != original_expires
```

---

## DOCKER-001: Production Deployment

**Priority**: HIGH
**Effort**: 16 hours
**Dependencies**: Worker implementation

### Implementation

**File**: `docker-compose.yml` (UPDATE)

```yaml
version: '3.8'

services:
  # Main YBIS API/MCP Server
  ybis:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - YBIS_PROFILE=default
      - DATABASE_URL=sqlite:///platform_data/control_plane.db
    volumes:
      - ./platform_data:/app/platform_data
      - ./workspaces:/app/workspaces
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # YBIS Worker
  worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
    environment:
      - YBIS_PROFILE=default
      - DATABASE_URL=sqlite:///platform_data/control_plane.db
      - WORKER_COUNT=2
      - POLL_INTERVAL=5
    volumes:
      - ./platform_data:/app/platform_data
      - ./workspaces:/app/workspaces
    depends_on:
      - ybis
    restart: unless-stopped
    deploy:
      replicas: 2

  # Redis (for event bus)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  # Neo4j (optional - for dependency graph)
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:-ybis-graph-2025}
    volumes:
      - neo4j_data:/data
    profiles:
      - full
    restart: unless-stopped

volumes:
  redis_data:
  neo4j_data:
```

**File**: `Dockerfile` (NEW or UPDATE)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY configs/ configs/
COPY pyproject.toml .

# Install package
RUN pip install -e .

# Create directories
RUN mkdir -p platform_data workspaces

# Default command (MCP server)
CMD ["python", "-m", "src.ybis.services.mcp_server"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import src.ybis; print('OK')"
```

**File**: `Dockerfile.worker` (NEW)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY configs/ configs/
COPY scripts/ scripts/
COPY pyproject.toml .

# Install package
RUN pip install -e .

# Create directories
RUN mkdir -p platform_data workspaces

# Default command (worker)
CMD ["python", "scripts/ybis_worker.py", "--count", "${WORKER_COUNT:-1}", "--poll-interval", "${POLL_INTERVAL:-5}"]
```

**File**: `.env.example` (NEW)

```bash
# YBIS Environment Configuration

# Profile
YBIS_PROFILE=default

# Database
DATABASE_URL=sqlite:///platform_data/control_plane.db

# Worker
WORKER_COUNT=2
POLL_INTERVAL=5

# Redis (event bus)
REDIS_URL=redis://localhost:6379

# Neo4j (optional)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=ybis-graph-2025

# LLM
OLLAMA_BASE_URL=http://localhost:11434

# Observability (optional)
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# E2B Sandbox (optional)
E2B_API_KEY=
```

---

## MONITOR-001: Monitoring Stack

**Priority**: HIGH
**Effort**: 16 hours
**Dependencies**: Docker deployment

### Implementation

Add structured logging, metrics, and tracing.

**File**: `src/ybis/services/logging_config.py` (NEW)

```python
"""
Logging Configuration - Structured JSON logging.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


def setup_logging(level: str = "INFO", json_format: bool = True):
    """
    Setup logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        json_format: Use JSON format (True for production)
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    if json_format:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))

    root_logger.addHandler(handler)

    # Set levels for noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("litellm").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get logger with extra fields support"""
    return logging.getLogger(name)
```

**File**: `src/ybis/services/metrics.py` (NEW)

```python
"""
Metrics Collection - Prometheus-compatible metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import threading


@dataclass
class Counter:
    """Simple counter metric"""
    name: str
    value: int = 0
    labels: Dict[str, str] = field(default_factory=dict)

    def inc(self, amount: int = 1):
        self.value += amount


@dataclass
class Gauge:
    """Simple gauge metric"""
    name: str
    value: float = 0.0
    labels: Dict[str, str] = field(default_factory=dict)

    def set(self, value: float):
        self.value = value

    def inc(self, amount: float = 1.0):
        self.value += amount

    def dec(self, amount: float = 1.0):
        self.value -= amount


@dataclass
class Histogram:
    """Simple histogram metric"""
    name: str
    buckets: List[float] = field(default_factory=lambda: [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0])
    observations: List[float] = field(default_factory=list)
    labels: Dict[str, str] = field(default_factory=dict)

    def observe(self, value: float):
        self.observations.append(value)


class MetricsRegistry:
    """Central metrics registry"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._metrics = {}
        return cls._instance

    def counter(self, name: str, labels: Dict[str, str] = None) -> Counter:
        """Get or create counter"""
        key = f"counter:{name}:{labels}"
        if key not in self._metrics:
            self._metrics[key] = Counter(name=name, labels=labels or {})
        return self._metrics[key]

    def gauge(self, name: str, labels: Dict[str, str] = None) -> Gauge:
        """Get or create gauge"""
        key = f"gauge:{name}:{labels}"
        if key not in self._metrics:
            self._metrics[key] = Gauge(name=name, labels=labels or {})
        return self._metrics[key]

    def histogram(self, name: str, labels: Dict[str, str] = None) -> Histogram:
        """Get or create histogram"""
        key = f"histogram:{name}:{labels}"
        if key not in self._metrics:
            self._metrics[key] = Histogram(name=name, labels=labels or {})
        return self._metrics[key]

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []

        for key, metric in self._metrics.items():
            if isinstance(metric, Counter):
                labels_str = ",".join(f'{k}="{v}"' for k, v in metric.labels.items())
                lines.append(f"{metric.name}{{{labels_str}}} {metric.value}")
            elif isinstance(metric, Gauge):
                labels_str = ",".join(f'{k}="{v}"' for k, v in metric.labels.items())
                lines.append(f"{metric.name}{{{labels_str}}} {metric.value}")
            elif isinstance(metric, Histogram):
                # Simplified histogram export
                labels_str = ",".join(f'{k}="{v}"' for k, v in metric.labels.items())
                count = len(metric.observations)
                total = sum(metric.observations) if metric.observations else 0
                lines.append(f"{metric.name}_count{{{labels_str}}} {count}")
                lines.append(f"{metric.name}_sum{{{labels_str}}} {total}")

        return "\n".join(lines)


def get_metrics() -> MetricsRegistry:
    """Get metrics registry singleton"""
    return MetricsRegistry()


# Pre-defined metrics
TASKS_CREATED = get_metrics().counter("ybis_tasks_created_total")
TASKS_COMPLETED = get_metrics().counter("ybis_tasks_completed_total")
TASKS_FAILED = get_metrics().counter("ybis_tasks_failed_total")
ACTIVE_WORKERS = get_metrics().gauge("ybis_active_workers")
WORKFLOW_DURATION = get_metrics().histogram("ybis_workflow_duration_seconds")
```

---

# PHASE 3: POLISH

Complete after Phase 2. System is functional, needs refinement.

---

## DOCS-001: User Documentation

**Priority**: MEDIUM
**Effort**: 12 hours

### Files to Create

1. **README.md** (UPDATE) - Quick start, installation, basic usage
2. **docs/QUICK_START.md** (NEW) - Step-by-step getting started guide
3. **docs/USER_GUIDE.md** (NEW) - Complete usage documentation
4. **docs/DEPLOYMENT.md** (NEW) - Production deployment guide
5. **docs/TROUBLESHOOTING.md** (NEW) - Common issues and solutions

### README.md Template

```markdown
# YBIS - AI-Native Development Platform

YBIS is a self-improving AI development platform that uses structured workflows,
evidence-based decision making, and policy governance.

## Quick Start

```bash
# Install
pip install -e .

# Create a task
ybis task create --objective "Create a hello world function"

# Run the task
ybis run T-XXXXXXXX

# Check status
ybis task status T-XXXXXXXX
```

## Features

- **Structured Workflows**: Spec → Plan → Execute → Verify → Gate
- **Self-Improvement**: Learns from failures, updates policies automatically
- **Policy Governance**: Protected paths, approval workflows, audit trails
- **Multi-Model Support**: Ollama, OpenAI, Anthropic via LiteLLM
- **MCP Integration**: Use with Claude, VS Code, and other MCP clients

## Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [User Guide](docs/USER_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment](docs/DEPLOYMENT.md)

## Requirements

- Python 3.11+
- Ollama (for local LLM)
- Redis (optional, for event bus)
- Neo4j (optional, for dependency graph)
```

---

## CLEANUP-001: Legacy Code Removal

**Priority**: MEDIUM
**Effort**: 8 hours

### Tasks

1. Archive `src/agentic/` to `legacy/src_agentic/`
2. Remove `src/utils/` (deprecated)
3. Update all imports in remaining code
4. Remove broken test files
5. Clean up unused config files

---

## API-001: API Documentation

**Priority**: MEDIUM
**Effort**: 8 hours

### Tasks

1. Add docstrings to all public classes/functions
2. Generate API reference with pdoc or mkdocs
3. Document all MCP tools with examples
4. Document all CLI commands

---

# QUICK WINS

Can be done anytime, 1-4 hours each.

## QW-001: Add CLI Entry Point to pyproject.toml

**File**: `pyproject.toml`

Add:

```toml
[project.scripts]
ybis = "src.ybis.cli:main"
```

## QW-002: Fix ybis_dojo.py Encoding Error

**File**: `scripts/ybis_dojo.py`

Replace Unicode emojis with ASCII text or add encoding declaration.

## QW-003: Create .env.example

See DOCKER-001 section for content.

## QW-004: Fix docker-compose Worker Service

See DOCKER-001 section for content.

## QW-005: Create Sample Task Files

**File**: `examples/tasks/simple_task.json`

```json
{
  "task_id": "T-EXAMPLE-001",
  "title": "Create Hello World",
  "objective": "Create a Python file hello.py that prints 'Hello, World!'",
  "priority": "MEDIUM"
}
```

---

# EXECUTION CHECKLIST

## Week 1

- [ ] QW-001: pyproject.toml CLI entry
- [ ] QW-003: .env.example
- [ ] CLI-001: Build complete CLI
- [ ] TEST-001: Fix test infrastructure
- [ ] RAG-001: Index codebase for RAG

## Week 2

- [ ] WORKER-001: Implement worker runtime
- [ ] WORKFLOW-001: Connect YAML workflows
- [ ] QW-002: Fix ybis_dojo.py
- [ ] QW-004: Fix docker-compose

## Week 3

- [ ] ADAPTER-001: Complete stub adapters (llamaindex, council)
- [ ] E2E-001: End-to-end tests
- [ ] DOCKER-001: Production deployment

## Week 4

- [ ] MONITOR-001: Monitoring stack
- [ ] DOCS-001: User documentation
- [ ] CLEANUP-001: Legacy code removal
- [ ] API-001: API documentation
- [ ] QW-005: Sample task files

---

# SUCCESS CRITERIA

After completing all tasks:

1. **Users can run end-to-end workflows** via CLI
2. **Workers process tasks** in background
3. **Workflows are configurable** via YAML
4. **Tests pass** with >80% coverage
5. **RAG provides real codebase context** to planner (no hallucinations)
5. **Docker deployment** works out of the box
6. **Documentation** enables self-service onboarding
7. **Monitoring** provides visibility into system health

**Target: 100% Production Ready**

1) “Ben worker/lease/orchestrator yazmayayım” → Temporal

Neyi çözer?

Worker runtime + task claim/lease/heartbeat mantığı (Temporal’ın Worker/Task Queue modeliyle)

Uzun süren işlerin dayanıklılığı, retry, state, visibility

Approval akışları için “signal/update/query” tarzı etkileşim (workflow stateful web-service gibi davranır)

YBIS roadmap’e etkisi

WORKER-001 ve lease DB tablosu gibi şeylerin çoğu Temporal’a taşınır (senin yazacağın worker döngüsü minimal olur).

WORKFLOW-001 için YAML’ı yine tutabilirsin ama “graph builder” yerine Temporal workflow tanımlarına map edersin.

Ne zaman seçilir?

“Prod’da sağlamlık > her şey” diyorsan ve ileride dağıtık/multi-worker büyüyeceksen.

2) “Python’da hızlı prod-orchestration + UI istiyorum” → Prefect (OSS)

Neyi çözer?

Flow orchestration, state tracking, retry, scheduling, gözlemlenebilirlik/izleme deneyimi

YBIS roadmap’e etkisi

WORKER-001’in büyük kısmı: Prefect agent/worker modeline kayar.

WORKFLOW-001: YAML workflow’ları istersen tutarsın ama Prefect’in Python decorator/flow yaklaşımıyla “workflow loading” ihtiyacı azalır.

CLI yine gerekir ama “run/list/status” gibi komutlar Prefect API’sine bağlanır.

Ne zaman seçilir?

“4 haftada prod demo + görünürlük + hızlı iterasyon” hedefinde, özellikle tek repo/tek ekip.

3) “Klasik queue + basit worker istiyorum” → Celery veya Dramatiq (+ Redis/RabbitMQ)

Neyi çözer?

Background task processing’i hazır alırsın; claim/lease yerine broker + ack/retry semantiğiyle ilerlersin

YBIS roadmap’e etkisi

WORKER-001 custom loop yerine Celery/Dramatiq worker’a dönüşür.

DB “leases” tablosu çoğu senaryoda gereksizleşir; “task state” broker ve result backend ile tutulur.

Orchestrator graph yine sende kalır (LangGraph gibi).

Ne zaman seçilir?

“Basit, bilinen, hızlı” istiyorsan. (Temporal kadar “durable workflow engine” değil.)

YBIS’in “agentic graph + YAML” tarafı için

Sen zaten LangGraph çizgisine yakınsın. LangGraph; state, conditional edges, döngüler, debugging/deployment gibi agent workflow ihtiyaçlarını hedefliyor.

Özet: Orchestrator’ı LangGraph’ta tutup, worker/orchestration’ı Temporal/Prefect/Celery ile “platformlaştırmak” en pragmatik yol.

RAG/Vector Store için “hazır” tercihler

Chroma (lokal hızlı prototip) vs Qdrant (prod vector DB olarak daha yaygın tercih edilen çizgi)

İstersen LlamaIndex veya LangChain entegrasyonlarıyla indeksleme + retrieval’i paket gibi alırsın (senin index_codebase.py yine değerli ama “ürünleştirme” yükü düşer).

Observability / tracing (LLM odaklı)

Arize Phoenix: open-source LLM tracing/eval/observability
Bu, senin MONITOR-001 için “LLM tarafını” ciddi hızlandırır (OTEL ile de iyi gider).

CLI için “hazır”

Click yazmışsın; Typer aynı ekosistemde, type-hint ile daha hızlı CLI çıkartır (Click üzerinde çalışır).

CLI-001’i Typer’a çekmek genelde daha çabuk ve temiz oluyor.

En net öneri (roadmap’e göre)

Eğer “gerçek prod dayanıklılığı” istiyorsan: Temporal + LangGraph + (Qdrant) + Phoenix + Typer

Eğer “4 haftada en hızlı prod-ready demo” istiyorsan: Prefect + LangGraph + (Chroma/Qdrant) + Phoenix + Typer

Eğer “minimal bağımlılık, klasik yaklaşım” istiyorsan: Dramatiq/Celery + LangGraph + (Chroma/Qdrant) + Phoenix + Typer

Tamam—roadmap’in zaten “iskele” kısmını çok iyi kapatıyor. Benim ekstra önerilerim, prod’a geçince en çok can yakan boşlukları önceden kapatmaya yönelik:

0) “Prod-ready” tanımını kilitle

Readiness rubric: 0–100 puanlık checklist (Security, Reliability, Operability, Testability, UX). Her PR bu rubriğe dokunsun.

Release gate: “pytest + ruff + mypy + e2e smoke + docker build” geçmeden main’e merge yok.

1) SQLite ile worker/lease riskini azalt

SQLite + çoklu worker + lease tablosu = kilitlenme/yarış ihtimali.

Lease acquire için tek SQL statement ile atomiklik (INSERT…WHERE NOT EXISTS / transaction + immediate lock).

“stale lease cleanup” job.

Uzun vadede: Postgres (mümkünse Week 3’e koy, yoksa Week 4).

2) İdempotency + retry stratejisi (en kritik)

Worker retry yapınca aynı task iki kere uygulanmasın:

Her run’a run_id ve her patch’e patch_id ver.

“apply_patch” idempotent olsun (aynı patch tekrar uygulanınca no-op).

External side-effect’ler (git push, file write, tool call) için idempotency key.

3) Run artifact standardı

Şu an artifacts var ama standartlaştır:

runs/<run_id>/artifacts/{spec.json, plan.json, patch.diff, verifier.json, gate.json, logs.jsonl}

Her node “input snapshot + output snapshot” yazsın (debugging 10x kolay).

4) Config & profiles (dev/staging/prod)

configs/profiles/{dev.yaml,prod.yaml} + env override

“policy”, “model listesi”, “vector store backend”, “workspace root”, “protected paths” hepsi config’ten gelsin.

5) LLM çağrı katmanı: determinism + cost + rate limit

Tek bir LLMClient wrapper: timeout, retry, backoff, token/cost logging, response caching.

“model fallback” (local model çökünce küçük bir fallback).

Prompt’ları kodun içinden çıkar: configs/prompts/*.md + versiyonlama.

6) Test stratejisini 3 katman yap

Unit: contracts/db/workflow builder

Integration: worker lease + graph + vector store mock

Golden path: tamamen deterministik (LLM mock + fixed fixtures)
Ek: CI’da gerçek LLM koşmasın; sadece nightly’de koşsun.

7) “Safe execution” / sandbox netliği

Executor zaten kritik:

Protected paths + approval gate tamam; ek olarak:

Tool allowlist + cwd sandbox

File write guard (yalnızca workspace)

Network default kapalı (açılınca policy’ye bağlanmış olsun)

8) Observability’yi “workflow-native” yap

Loglar yetmiyor:

Her run için: run_duration, node_duration, token_in/out, tool_calls, gate_outcome metrikleri

Minimal: Prometheus text endpoint + JSON logs. Sonra OTEL.

9) “Queue semantics” netleştir

Task durumları güzel ama bir de:

pending → running → completed/failed/blocked

blocked için TTL / reminder / auto-expire

running stuck olursa: watchdog “lease expired → back to pending” (ama idempotency şart)

10) DX (developer experience) hızlı kazanımlar

make setup, make test, make lint, make run-worker

pre-commit + ruff format + mypy (hafif strict)

examples/ klasörü: 5 hazır task + 2 workflow yaml örneği

11) Packaging düzeltmesi (pyproject)

Senin örnekte ybis = "src.ybis.cli:main" var; pratikte çoğu projede paket yolu ybis.cli:main olur (src-layout doğru ayarlanmalı).
Bunu “pip install -e .” sonrası gerçekten import edilebilir hale getir.

12) “Self-improve” döngüsü için minimal gerçekçilik

Self-improve çok güçlü ama prod’da riskli:

İlk sürümde self-improve sadece öneri üretir, otomatik apply yok.

“policy update proposal” + “human approve” şartı (audit trail ile).

Eğer 1–2 tane seçmem gerekse (en yüksek ROI)

Idempotency + retry + run artifacts standardı

SQLite concurrency/lease atomikliği + watchdog

LLMClient wrapper (timeout/retry/cost/logging)
