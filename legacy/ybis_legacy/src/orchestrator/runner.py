#!/usr/bin/env python3
"""
Modular Orchestrator Runner.
Entry point for the YBIS Autonomous Factory.
Feature-complete successor to scripts/run_orchestrator.py.
"""
import sys
import os
import asyncio
import argparse
from pathlib import Path
from rich.console import Console

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Filter stderr to hide specific library noises (Legacy Feature Restoration)
class StderrFilter:
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr

    def write(self, message):
        if "posthog" in message or "telemetry" in message or "ClientStartEvent" in message:
            return
        self.original_stderr.write(message)

    def flush(self):
        self.original_stderr.flush()

    def isatty(self):
        return getattr(self.original_stderr, "isatty", lambda: False)()

sys.stderr = StderrFilter(sys.stderr)

# Imports
from src.orchestrator.config import PROJECT_ROOT, USE_CREWAI, USE_POETIQ, EXECUTOR_MODE
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.simple_planner_v2 import SimplePlannerV2
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.patch_executor import PatchExecutor
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced
from src.agentic.infrastructure.db import TaskDatabase
from src.agentic.core.plugins.git_manager import GitWorktreeManager, GitManager
from src.agentic.core.utils.logging_utils import log_event

# Optional CrewAI Import
try:
    from src.agentic.crews.planning_crew import PlanningCrew
except ImportError:
    PlanningCrew = None

console = Console()

async def run_single_task(task_data: dict, db: TaskDatabase, worktree_manager: GitWorktreeManager = None):
    """Executes a single task with full isolation and context."""
    task_id = task_data['id']
    console.print(f"[bold green]Starting Task: {task_id}[/bold green]")
    
    # 1. Worktree Isolation (Legacy Feature)
    worktree_path = None
    original_code_root = os.environ.get("YBIS_CODE_ROOT")
    
    if worktree_manager:
        try:
            console.print("[cyan]Creating Isolated Worktree...[/cyan]")
            worktree_path, branch = worktree_manager.ensure_worktree(task_id)
            os.environ["YBIS_CODE_ROOT"] = str(worktree_path)
            console.print(f"[cyan]Worktree Active: {worktree_path}[/cyan]")
        except Exception as e:
            console.print(f"[bold red]Worktree Failed: {e}[/bold red]")
            return "FAILED"

    try:
        # 2. Update Status
        await db.update_task_status(task_id, "IN_PROGRESS")

        # 3. Select Planner
        if USE_CREWAI and PlanningCrew:
            console.print("[bold cyan]Planning Engine: CrewAI Squad[/bold cyan]")
            planner = PlanningCrew()
        else:
            console.print("[bold cyan]Planning Engine: SimplePlannerV2[/bold cyan]")
            planner = SimplePlannerV2()

        # 4. Initialize Components
        # Note: GitManager needs to know about the worktree if active
        current_root = worktree_path or PROJECT_ROOT
        git_manager = GitManager(repo_root=current_root)
        
        # Select Executor based on Config
        if EXECUTOR_MODE == "patch":
            console.print("[bold yellow]Executor: PatchExecutor[/bold yellow]")
            executor = PatchExecutor()
        else:
            console.print("[bold yellow]Executor: AiderExecutorEnhanced[/bold yellow]")
            executor = AiderExecutorEnhanced()
        
        verifier = SentinelVerifierEnhanced()

        orchestrator = OrchestratorGraph(
            planner=planner, 
            executor=executor, 
            verifier=verifier,
            git_manager=git_manager
        )

        # 5. Build Initial State
        initial_state = {
            "task_id": task_id,
            "task_description": task_data['goal'],
            "context": task_data.get('metadata', {}),
            "phase": "init",
            "retry_count": 0,
            "error_history": []
        }

        # 6. Run Graph
        result = await orchestrator.run_task(initial_state)
        
        # 7. Finalize
        final_status = "DONE" if result.final_status == "SUCCESS" else "FAILED"
        await db.update_task_status(task_id, final_status, final_status=result.final_status)
        
        console.print(f"[bold blue]Task Finished: {final_status}[/bold blue]")
        
        # 8. Merge Worktree (If successful)
        if worktree_manager and final_status == "DONE":
            console.print("[cyan]🔀 Merging Worktree...[/cyan]")
            # Logic to merge would go here (GitManager can handle this via PR or merge)
            # For now, we leave the worktree for review
            pass

    except Exception as e:
        console.print(f"[bold red]💥 Critical Failure: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        await db.update_task_status(task_id, "FAILED", final_status="CRITICAL_ERROR")
    finally:
        # 9. Cleanup
        if original_code_root:
            os.environ["YBIS_CODE_ROOT"] = original_code_root
        else:
            os.environ.pop("YBIS_CODE_ROOT", None)
            
        if worktree_manager:
            console.print("[cyan]🧹 Cleaning up Worktree...[/cyan]")
            # worktree_manager.remove_worktree(task_id) # Optional: keep for debug

async def main():
    parser = argparse.ArgumentParser(description="YBIS Orchestrator")
    parser.add_argument("--task", help="Direct task input")
    parser.add_argument("--loop", action="store_true", help="Run in continuous loop mode")
    args = parser.parse_args()

    console.print("[bold green]🤖 YBIS Factory Starting...[/bold green]")

    # Initialize DB
    db = TaskDatabase(str(PROJECT_ROOT / "Knowledge/LocalDB/tasks.db"))
    await db.initialize()
    
    # Initialize Worktree Manager
    # Only use worktrees if not in direct CLI task mode (optional preference)
    use_worktrees = os.getenv("YBIS_USE_WORKTREES", "true").lower() == "true"
    wt_manager = GitWorktreeManager(PROJECT_ROOT) if use_worktrees else None

    if args.task:
        # Direct task mode
        task_data = {
            "id": "CLI-TASK-" + os.urandom(4).hex(),
            "goal": args.task,
            "metadata": {"source": "cli"}
        }
        await run_single_task(task_data, db, wt_manager)
    
    elif args.loop:
        console.print("[yellow]Starting Infinite Loop... (Press Ctrl+C to stop)[/yellow]")
        while True:
            tasks = await db.get_all_tasks()
            pending = [t for t in tasks if t['status'] == 'BACKLOG']
            
            if pending:
                await run_single_task(pending[0], db, wt_manager)
            else:
                await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        # Fix Windows Unicode issues
        if sys.platform == "win32":
            os.environ["PYTHONUTF8"] = "1"
            # Force console to utf-8 if possible
            try:
                sys.stdout.reconfigure(encoding='utf-8')
                sys.stderr.reconfigure(encoding='utf-8')
            except Exception:
                pass
                
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red]Factory Shutdown.[/red]")

