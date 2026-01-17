#!/usr/bin/env python3
"""
YBIS Top - Factory Dashboard (CLI).

A top-like CLI tool to visualize the state of the factory (Tasks, Workers, Leases).
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Error: rich library not installed")
    print("Install with: pip install rich")
    sys.exit(1)

from src.ybis.constants import PROJECT_ROOT
from src.ybis.control_plane import ControlPlaneDB


class FactoryDashboard:
    """Factory dashboard with live updates."""

    def __init__(self, db_path: Path):
        """Initialize dashboard."""
        self.db = ControlPlaneDB(db_path)
        self.console = Console()

    async def initialize(self) -> None:
        """Initialize database connection."""
        await self.db.initialize()

    def create_workers_panel(self, workers: list[dict]) -> Panel:
        """Create workers panel."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Worker ID", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Current Task", style="yellow")
        table.add_column("Last Heartbeat", style="dim")

        for worker in workers:
            status_color = "green" if worker["status"] == "IDLE" else "yellow"
            table.add_row(
                worker["worker_id"],
                f"[{status_color}]{worker['status']}[/]",
                worker["current_task"],
                worker["heartbeat_at"] or "N/A",
            )

        if not workers:
            table.add_row("No active workers", "", "", "")

        return Panel(table, title="[bold cyan]Workers[/]", border_style="cyan")

    def create_queue_panel(self, pending: list, blocked: list) -> Panel:
        """Create queue panel."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Priority", style="dim")

        # Add pending tasks
        for task in pending[:10]:  # Limit to 10
            table.add_row(
                task.task_id,
                task.title[:40] + "..." if len(task.title) > 40 else task.title,
                "[green]TODO[/]",
                task.priority or "MEDIUM",
            )

        # Add blocked tasks
        for task in blocked[:5]:  # Limit to 5
            table.add_row(
                task.task_id,
                task.title[:40] + "..." if len(task.title) > 40 else task.title,
                "[red]BLOCKED[/]",
                task.priority or "MEDIUM",
            )

        if not pending and not blocked:
            table.add_row("No tasks in queue", "", "", "")

        return Panel(table, title="[bold cyan]Queue[/]", border_style="cyan")

    def create_runs_panel(self, runs: list) -> Panel:
        """Create recent runs panel."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Run ID", style="cyan")
        table.add_column("Task ID", style="yellow")
        table.add_column("Status", style="white")
        table.add_column("Workflow", style="dim")

        for run in runs:
            status_color = "green" if run.status == "completed" else "red" if run.status == "failed" else "yellow"
            status_text = run.status.upper()
            if run.status == "awaiting_approval":
                status_text = "AWAITING_APPROVAL"
            table.add_row(
                run.run_id,
                run.task_id,
                f"[{status_color}]{status_text}[/]",
                run.workflow or "build",
            )

        if not runs:
            table.add_row("No recent runs", "", "", "")

        return Panel(table, title="[bold cyan]Recent Runs[/]", border_style="cyan")

    def create_layout(self, workers: list[dict], pending: list, blocked: list, runs: list) -> Layout:
        """Create dashboard layout."""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
        )

        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )

        layout["left"].split_column(
            Layout(name="workers", ratio=1),
            Layout(name="queue", ratio=1),
        )

        layout["right"].split_column(
            Layout(name="runs", ratio=1),
        )

        # Header
        header_text = Text("YBIS Factory Dashboard", style="bold white on blue", justify="center")
        layout["header"].update(Panel(header_text, border_style="blue"))

        # Panels
        layout["workers"].update(self.create_workers_panel(workers))
        layout["queue"].update(self.create_queue_panel(pending, blocked))
        layout["runs"].update(self.create_runs_panel(runs))

        return layout

    async def update_data(self) -> tuple[list[dict], list, list, list]:
        """Fetch latest data from database."""
        workers = await self.db.get_workers()
        pending = await self.db.get_pending_tasks()
        blocked = await self.db.get_blocked_tasks()
        runs = await self.db.get_recent_runs(limit=5)

        return workers, pending, blocked, runs

    async def run(self) -> None:
        """Run dashboard with live updates."""
        await self.initialize()

        with Live(auto_refresh=False, console=self.console, screen=True) as live:
            while True:
                try:
                    workers, pending, blocked, runs = await self.update_data()
                    layout = self.create_layout(workers, pending, blocked, runs)
                    live.update(layout, refresh=True)
                    await asyncio.sleep(2)  # Refresh every 2 seconds
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/]")
                    await asyncio.sleep(2)


async def main() -> None:
    """Main entry point."""
    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    dashboard = FactoryDashboard(db_path)

    print("Starting YBIS Factory Dashboard...")
    print("Press Ctrl+C to quit")
    print()

    try:
        await dashboard.run()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")


if __name__ == "__main__":
    asyncio.run(main())

