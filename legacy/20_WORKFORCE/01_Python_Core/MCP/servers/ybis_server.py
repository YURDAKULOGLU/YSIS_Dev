from fastmcp import FastMCP
import os
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
import warnings

# Suppress annoying Pydantic/OpenTel warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
try:
    import logging
    class NoParsableLogRecordFilter(logging.Filter):
        def filter(self, record):
             return "cannot import name 'ReadableLogRecord'" not in record.getMessage()
    logging.getLogger().addFilter(NoParsableLogRecordFilter())
except:
    pass

# YBIS Modüllerini import edebilmek için path ayarı
current_dir = os.path.dirname(os.path.abspath(__file__))
# Fix: Go up 3 levels to get to .YBIS_Dev folder which contains Agentic package
ybis_dev_root = os.path.abspath(os.path.join(current_dir, "../../../"))
if ybis_dev_root not in sys.path:
    sys.path.insert(0, ybis_dev_root) # Insert at 0 to prioritize local code

# Restore agentic_dir for tool usage
agentic_dir = os.path.join(ybis_dev_root, "Agentic")

# Araçlarımızı import edelim
from Agentic.Tools.local_rag import local_rag
# from Tools.task_manager import task_manager # DEPRECATED: Switching to TaskBoardManager
from Agentic.Tools.file_ops import file_ops
from Agentic.Tools.repo_mapper import repo_mapper
from Agentic.Core.plugins.task_board_manager import TaskBoardManager

# Initialize Board Manager
board = TaskBoardManager()

# Sunucuyu başlat
mcp = FastMCP("YBIS Agentic Server")

# --- workflow registry ---
import yaml
from pathlib import Path

class WorkflowRegistry:
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            # Default: .YBIS_Dev/Veriler/workflow-registry.yaml
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            registry_path = project_root / "Veriler" / "workflow-registry.yaml"
        self.registry_path = registry_path
        self.workflows = []
        self.load()

    def load(self):
        if not os.path.exists(self.registry_path):
            print(f"[Registry] File not found: {self.registry_path}")
            return

        with open(self.registry_path, 'r', encoding='utf-8') as f:
            self.workflows = yaml.safe_load(f) or []

    def get_suggested_workflow(self, intent_text: str) -> str:
        """Find best matching workflow based on intent keywords."""
        intent_text = intent_text.lower()

        best_match = None
        max_matches = 0

        for intent_def in self.workflows:
            keywords = intent_def.get('keywords', [])
            matches = sum(1 for k in keywords if k.lower() in intent_text)

            if matches > max_matches:
                max_matches = matches
                if intent_def.get('workflows'):
                    best_match = intent_def['workflows'][0] # Take first for MVP

        if best_match:
            return f"MATCHED WORKFLOW: {best_match['name']}\\nDESCRIPTION: {best_match.get('description')}\\nSTEPS: {best_match.get('steps')}"

        return "No standard workflow found. Defaulting to general planning."

registry = WorkflowRegistry()

# --- Supervisor / Brain Mode State ---
ORCHESTRATOR_PROCESS = None

@mcp.tool()
def search_knowledge_base(query: str, limit: int = 5) -> str:
    """
    Search the YBIS local knowledge base (RAG) for relevant documentation or code snippets.
    Use this when you need context about the project architecture, decisions, or existing code.
    """
    return local_rag.search(query, limit=limit)

@mcp.tool()
def get_repo_tree(max_depth: int = 3) -> str:
    """
    Generates a visual tree structure of the current repository, respecting .gitignore.
    Use this to understand the project's file structure and locate relevant files.
    """
    return repo_mapper.get_tree(max_depth=max_depth)

@mcp.tool()
def read_project_file(file_path: str) -> str:
    """
    Read the content of a specific file within the project.
    Use this to inspect code, documentation, or configuration files.
    """
    return file_ops.read_file(file_path)

@mcp.tool()
def write_project_file(file_path: str, content: str) -> str:
    """
    Write content to a specific file within the project.
    Use this to modify code, update documentation, or create new files.
    """
    return file_ops.write_file(file_path, content)

@mcp.tool()
async def get_next_task() -> str:
    """
    Fetch the highest priority task from the TASK_BOARD.md file.
    Returns the task description/ID or 'No tasks' message.
    """
    task = await board.get_next_task()
    if task:
        return f"{task['id']}: {task['description']}"
    return "No IN PROGRESS tasks. Please move a task from Backlog to IN PROGRESS on TASK_BOARD.md."

@mcp.tool()
async def create_new_task(title: str, description: str, priority: str = "MEDIUM") -> str:
    """
    Create a new task in the Backlog (NEW) section of TASK_BOARD.md.
    """
    task_id = await board.create_task(title, description, priority)
    return f"Created task {task_id}"

@mcp.tool()
async def update_task_status(task_id: str, status: str, result: str = "") -> str:
    """
    Update a task's status (e.g. DONE, FAILED) in TASK_BOARD.md
    """
    metadata = {}
    if result:
        metadata['error'] = result

    await board.update_task_status(task_id, status, metadata)
    return f"Updated {task_id} to {status}"

@mcp.tool()
def list_all_tasks() -> str:
    """
    Read the current content of the TASK_BOARD.md file to see all tasks (TODO, IN PROGRESS, DONE).
    """
    return file_ops.read_file(board.board_path)

@mcp.tool()
def log_agent_action(message: str) -> str:
    """
    Log a significant action or decision made by an agent to the project's central activity log.
    This helps in tracking the system's progress and debugging.
    """
    log_path = os.path.join(agentic_dir, "../Meta/Active/logs/agent_activity.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Configure Logger with Rotation if not already
    logger = logging.getLogger("ybis_agent_activity")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # 1MB max size, keep 3 backup files
        handler = RotatingFileHandler(log_path, maxBytes=1*1024*1024, backupCount=3, encoding='utf-8')
        formatter = logging.Formatter('- [%(asctime)s] AGENT ACTION: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.info(message)
    return "Action logged."

# --- Tier 4 Tools ---

@mcp.tool()
def get_suggested_workflow(intent: str) -> str:
    """
    Search the Workflow Registry for a standard process matching the user's intent.
    Example intents: 'fix bug', 'new feature', 'refactor', 'bootstrap'.
    """
    return registry.get_suggested_workflow(intent)

@mcp.tool()
def ask_user(question: str) -> str:
    """
    Simulate asking the user for permission or input.
    In "Brain Mode" (unattended), this will:
    1. Log the question.
    2. Check a heuristic (Safety Check).
    3. Return 'APPROVED' for safe actions, 'DENIED' for risky ones (MVP).
    """
    # MVP Logic:
    # If question contains "delete" or "destroy", deny.
    # Otherwise approve.
    print(f"\\n✋ [Brain] Permission Requested: {question}")

    if any(risk in question.lower() for risk in ["delete", "destroy", "wipe", "format"]):
        print("   ❌ AUTOMATICALLY DENIED (Risky Keyword)")
        return "DENIED"

    print("   ✅ AUTOMATICALLY APPROVED (Safe)")
    return "APPROVED"

@mcp.tool()
def get_recent_activities(limit: int = 10) -> str:
    """
    Get the last N logged system activities/decisions.
    """
    log_path = os.path.join(agentic_dir, "../Meta/Active/logs/agent_activity.log")
    if not os.path.exists(log_path):
        return "No activity log found."

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return "".join(lines[-limit:])
    except Exception as e:
        return f"Error reading log: {e}"

@mcp.tool()
def create_state_snapshot(snapshot_name: str = "auto") -> str:
    """
    Capture the current state of the repo (file listing, task board hash) into a snapshot file.
    Useful for 'Bootstrapper' protocol to Verify changes.
    """
    from datetime import datetime
    import hashlib

    # 1. Capture Repo Tree Hash
    tree = repo_mapper.get_tree(max_depth=5)
    tree_hash = hashlib.md5(tree.encode('utf-8')).hexdigest()

    # 2. Capture Task Board Hash
    if os.path.exists(board.board_path):
        board_content = file_ops.read_file(board.board_path)
        board_hash = hashlib.md5(board_content.encode('utf-8')).hexdigest()
    else:
        board_hash = "no_board"

    metadata = {
        "timestamp": datetime.now().isoformat(),
        "snapshot_name": snapshot_name,
        "repo_tree_hash": tree_hash,
        "task_board_hash": board_hash
    }

    snap_dir = os.path.join(agentic_dir, "../Meta/Memory/Snapshots")
    try:
         os.makedirs(snap_dir, exist_ok=True)

         filename = f"snapshot_{snapshot_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
         snap_path = os.path.join(snap_dir, filename)

         with open(snap_path, 'w', encoding='utf-8') as f:
             json.dump(metadata, f, indent=2)

         return f"Snapshot created: {filename}"
    except Exception as e:
         return f"Snapshot failed: {e}"

# --- Brain Mode Logic ---
async def supervisor_loop():
    """
    Polls TASK_BOARD.md and wakes up Orchestrator if needed.
    """
    import asyncio
    import subprocess

    print("[Brain] Supervisor Loop Started. Watching TASK_BOARD.md...")
    last_mtime = 0

    while True:
        try:
            if os.path.exists(board.board_path):
                current_mtime = os.path.getmtime(board.board_path)

                if current_mtime > last_mtime:
                    # File changed, check for tasks
                    # We only care if there is an IN PROGRESS task and Orchestrator is NOT running

                    # For MVP: We just check if there is an IN PROGRESS task
                    task = await board.get_next_task()
                    if task:
                        print(f"[Brain] Found active task: {task['id']}. Checking Orchestrator...")

                        # Simplified process check (locking via file might be better, but MVP: Just launch)
                        # We assume if we launched it, it's running. Optimally we check PID.
                        # For now, let's just log. The goal is to "Wake up".

                        # Command to run orchestrator
                        orch_path = os.path.join(agentic_dir, "graphs/orchestrator_unified.py")

                        # Launch Orchestrator as a separate process
                        # We use Popen so we don't block the supervisor
                        # We set Env Var to point to US (the Brain)
                        env = os.environ.copy()
                        env['MCP_SERVER_URL'] = "http://localhost:8000/sse" # Default for FastMCP SSE

                        print(f"[Brain] Launching Orchestrator: {orch_path}")
                        try:
                            # Use python executable running this script
                            python_exe = sys.executable
                            subprocess.Popen([python_exe, orch_path], env=env)
                            print("[Brain] Orchestrator launch successful.")
                        except Exception as launch_err:
                            print(f"[Brain] Failed to launch orchestrator: {launch_err}")

                    last_mtime = current_mtime

            await asyncio.sleep(5)
        except Exception as e:
            print(f"[Brain] Supervisor Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser()
    parser.add_argument("--brain-mode", action="store_true", help="Run as Central Brain (SSE Server + Supervisor)")
    args = parser.parse_args()

    if args.brain_mode:
        print("[Brain] Starting YBIS Server in BRAIN MODE (SSE)...")

        # Start Supervisor in background
        # Note: FastMCP run() might block. We need to schedule before or run in parallel.
        # FastMCP doesn't easily expose the loop before run.
        # However, we can use the lifespan context or just rely on the fact that we might be running under uvicorn.

        # Actually, for 'mcp.run(transport="sse")', it likely uses uvicorn.
        # We can't easily inject a background task into FastMCP's uvicorn runner without a lifespan hook.
        # But we can try to rely on 'startup' event if FastMCP supports it.
        # Looking at FastMCP docs (common pattern):
        # @mcp.on_startup
        # async def startup(): ...

        # Let's try adding a startup hook dynamically or just assuming we can't do the loop easily *inside* the same process
        # without proper hooks.
        # ALTERNATIVE: Use a separate thread for the loop.
        import threading

        def run_supervisor():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(supervisor_loop())

        t = threading.Thread(target=run_supervisor, daemon=True)
        t.start()

        # Run SSE
        # Assuming port 8000 by default or customizable
        mcp.run(transport="sse")
    else:
        # Standard Stdio Mode (for direct connecting tools)
        mcp.run()
