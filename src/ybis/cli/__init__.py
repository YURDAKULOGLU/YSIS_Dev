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

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import click

# Fix Windows encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from ..constants import PROJECT_ROOT
from ..contracts import Task
from ..control_plane import ControlPlaneDB


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
def task_create(objective: str, title: str | None, priority: str):
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
def task_list(status: str | None, limit: int):
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

    from ..workflows.runner import build_graph

    async def _run():
        # Load task
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))
        await db.initialize()
        task = await db.get_task(task_id)

        if not task:
            raise click.ClickException(f"Task not found: {task_id}")

        # Create and run graph
        try:
            graph = build_graph(workflow)
        except Exception as e:
            raise click.ClickException(f"Failed to build workflow '{workflow}': {e}")

        # Initialize state (using WorkflowState structure)
        initial_state = {
            "task_id": task.task_id,
            "run_id": f"R-{task.task_id[-8:]}",
            "run_path": str(PROJECT_ROOT / "workspaces" / task.task_id / "runs" / f"R-{task.task_id[-8:]}"),
            "trace_id": f"{task.task_id}-R-{task.task_id[-8:]}",
            "task_objective": task.objective,
            "status": "running",
            "retries": 0,
            "max_retries": 2,
            "error_context": None,
            "current_step": 0,
            "task_tier": None,
            "workflow_name": workflow,
        }

        # Run workflow
        result = await graph.ainvoke(initial_state)
        return result

    try:
        result = asyncio.run(_run())

        gate_decision = result.get("gate_decision")
        if gate_decision:
            if hasattr(gate_decision, 'approved') and gate_decision.approved:
                click.echo("\n[SUCCESS] Task completed successfully")
            else:
                reason = getattr(gate_decision, 'reason', 'Unknown reason')
                click.echo(f"\n[BLOCKED] Task blocked: {reason}")
        else:
            status = result.get("status", "unknown")
            if status == "completed":
                click.echo("\n[SUCCESS] Task completed")
            elif status == "failed":
                error = result.get("error", "Unknown error")
                click.echo(f"\n[ERROR] Task failed: {error}")
            else:
                click.echo(f"\n[INFO] Workflow completed with status: {status}")

    except Exception as e:
        click.echo(f"\n[ERROR] {e!s}", err=True)
        sys.exit(1)


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
    click.echo("[INFO] Worker runtime not yet implemented. Use 'python scripts/ybis_worker.py' instead.")
    # TODO: Implement when WorkerRuntime is available
    # from ..worker.runtime import WorkerRuntime
    # async def _run_worker():
    #     runtime = WorkerRuntime(poll_interval=poll_interval)
    #     await runtime.start()
    # try:
    #     asyncio.run(_run_worker())
    # except KeyboardInterrupt:
    #     click.echo("\nWorker stopped.")


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

    try:
        leases = asyncio.run(_status())

        if not leases:
            click.echo("No active workers.")
            return

        click.echo(f"{'WORKER ID':<40} {'TASK ID':<15} EXPIRES")
        click.echo("-" * 70)
        for worker_id, task_id, expires_at in leases:
            click.echo(f"{worker_id:<40} {task_id:<15} {expires_at}")
    except Exception as e:
        click.echo(f"[INFO] Worker status unavailable: {e}")


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

        # Check if task exists
        task = await db.get_task(task_id)
        if not task:
            raise click.ClickException(f"Task not found: {task_id}")

        # Record approval (simplified - using gate decision update)
        # TODO: Implement proper Approval model when available
        click.echo(f"[INFO] Approval recorded for task {task_id}")
        click.echo(f"Reason: {reason}")
        click.echo("[NOTE] Full approval workflow not yet implemented")
        return f"A-{task_id}"

    try:
        approval_id = asyncio.run(_approve())
        click.echo(f"Approved task {task_id}")
        click.echo(f"Approval ID: {approval_id}")
    except Exception as e:
        click.echo(f"[ERROR] {e!s}", err=True)
        sys.exit(1)


# =============================================================================
# HEALTH COMMANDS
# =============================================================================

@cli.command("health")
def health_check():
    """Run system health check"""
    try:
        from ..services.health_monitor import HealthMonitor

        monitor = HealthMonitor()
        checks = monitor.run_all_checks()
        report = monitor.generate_report(checks)

        click.echo("\nYBIS Health Check")
        click.echo("=" * 50)

        summary = report.get("summary", {})
        click.echo(f"Healthy: {summary.get('healthy', 0)}/{summary.get('total', 0)}")
        click.echo(f"Degraded: {summary.get('degraded', 0)}")
        click.echo(f"Unhealthy: {summary.get('unhealthy', 0)}")

        click.echo("\nDetails:")
        for check in report.get("checks", []):
            status_icon = {"healthy": "[OK]", "degraded": "[!!]", "unhealthy": "[XX]"}
            icon = status_icon.get(check.get("status", "unknown"), "[??]")
            click.echo(f"  {icon} {check.get('name', 'unknown')}: {check.get('message', '')}")
    except Exception as e:
        click.echo(f"[ERROR] Health check failed: {e}", err=True)
        sys.exit(1)


# =============================================================================
# RAG COMMANDS
# =============================================================================

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
        [sys.executable, "scripts/index_codebase.py", "--collection", collection],
        cwd=PROJECT_ROOT,
    )
    sys.exit(result.returncode)


@rag.command("verify")
def rag_verify():
    """Verify RAG is working"""
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/verify_rag.py"],
        cwd=PROJECT_ROOT,
    )
    sys.exit(result.returncode)


@rag.command("query")
@click.argument("query")
@click.option("--top-k", default=5, help="Number of results")
def rag_query(query: str, top_k: int):
    """Query the codebase"""
    try:
        from ..data_plane.vector_store import VectorStore

        vs = VectorStore()
        results = vs.query("codebase", query, top_k=top_k)

        if not results:
            click.echo("No results found. Run 'ybis rag index' first.")
            return

        for i, result in enumerate(results, 1):
            click.echo(f"\n--- Result {i} (distance: {result.get('distance', 0):.4f}) ---")
            metadata = result.get('metadata', {})
            click.echo(f"File: {metadata.get('file', 'unknown')}")
            click.echo(result.get('document', '')[:500])

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# =============================================================================
# DATABASE COMMANDS
# =============================================================================

@cli.group()
def db():
    """Database management commands"""
    pass


@db.command()
def migrate():
    """Run pending migrations"""
    from ..migrations import run_migrations, migration_status

    status = migration_status()
    if status["pending_count"] == 0:
        click.echo("No pending migrations.")
        return

    click.echo(f"Running {status['pending_count']} migrations...")
    applied = run_migrations()
    for name in applied:
        click.echo(f"  Applied: {name}")
    click.echo("Done.")


@db.command()
def status():
    """Show migration status"""
    from ..migrations import migration_status

    status = migration_status()
    click.echo(f"Current version: {status['current_version']}")
    click.echo(f"Latest version: {status['latest_version']}")
    click.echo(f"Pending: {status['pending_count']}")

    if status["pending"]:
        click.echo("\nPending migrations:")
        for m in status["pending"]:
            click.echo(f"  {m['version']}: {m['name']}")


@db.command()
@click.argument("version", type=int)
def rollback(version: int):
    """Rollback to specific version"""
    from ..migrations import rollback as do_rollback

    click.echo(f"Rolling back to version {version}...")
    applied = do_rollback(version)
    for name in applied:
        click.echo(f"  {name}")
    click.echo("Done.")


# =============================================================================
# BACKUP COMMANDS
# =============================================================================

@cli.group()
def backup():
    """Backup and recovery commands"""
    pass


@backup.command()
@click.option("--include-workspaces", is_flag=True, help="Include workspace artifacts")
def create(include_workspaces: bool):
    """Create a backup"""
    from ..services.backup import BackupService

    service = BackupService()
    path = service.create_backup(include_workspaces=include_workspaces)
    click.echo(f"Backup created: {path}")


@backup.command()
def list():
    """List available backups"""
    from ..services.backup import BackupService

    service = BackupService()
    backups = service.list_backups()

    if not backups:
        click.echo("No backups found.")
        return

    for b in backups:
        click.echo(f"{b['timestamp']} - {', '.join(b['components'])}")


@backup.command()
@click.argument("backup_path", type=click.Path(exists=True))
@click.option("--component", multiple=True, help="Specific component to restore")
def restore(backup_path: str, component: tuple):
    """Restore from backup"""
    from pathlib import Path
    from ..services.backup import BackupService

    service = BackupService()
    components = list(component) if component else None
    result = service.restore_backup(Path(backup_path), components)
    click.echo(f"Restored: {', '.join(result['restored'])}")


@backup.command()
@click.option("--keep", default=5, help="Number of backups to keep")
def cleanup(keep: int):
    """Remove old backups"""
    from ..services.backup import BackupService

    service = BackupService()
    service.cleanup_old_backups(keep_count=keep)
    click.echo(f"Cleanup complete. Kept {keep} most recent backups.")


# =============================================================================
# MAIN ENTRY
# =============================================================================

def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()

