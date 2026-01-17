#!/usr/bin/env python3
"""
YBIS Integration Plugin - Limit Test
Full-featured plugin demonstrating ALL plugin capabilities.
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

# ============================================================================
# PLUGIN CONFIGURATION
# ============================================================================

class PluginConfig:
    def __init__(self, config: dict):
        self.db_path = Path(config.get("ybis_db_path", "platform_data/control_plane.db"))
        self.workspace_root = Path(config.get("workspace_root", "workspaces"))
        self.default_workflow = config.get("default_workflow", "ybis_native")
        self.auto_claim = config.get("auto_claim", False)
        self.max_retries = config.get("max_retries", 3)

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

TOOLS = [
    {
        "name": "ybis_quick_task",
        "description": "Create and immediately run a YBIS task in one step",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "objective": {"type": "string", "description": "Task objective"},
                "auto_run": {"type": "boolean", "default": True},
            },
            "required": ["title", "objective"]
        }
    },
    {
        "name": "ybis_workspace_status",
        "description": "Get detailed status of all active workspaces",
        "parameters": {
            "type": "object",
            "properties": {
                "include_artifacts": {"type": "boolean", "default": False},
            }
        }
    },
    {
        "name": "ybis_artifact_search",
        "description": "Search across all YBIS artifacts (PLAN, RESULT, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "artifact_type": {"type": "string", "enum": ["PLAN", "RESULT", "all"]},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["query"]
        }
    },
    {
        "name": "ybis_workflow_visualize",
        "description": "Generate ASCII visualization of workflow execution",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "run_id": {"type": "string"},
            }
        }
    }
]

# ============================================================================
# TOOL HANDLERS
# ============================================================================

async def handle_ybis_quick_task(params: dict, config: PluginConfig) -> dict:
    """Create and run task in one step"""
    import uuid

    task_id = f"T-{uuid.uuid4().hex[:8]}"
    title = params["title"]
    objective = params["objective"]
    auto_run = params.get("auto_run", True)

    # Create task in DB
    conn = sqlite3.connect(config.db_path)
    conn.execute(
        "INSERT INTO tasks (task_id, title, objective, status, priority, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (task_id, title, objective, "pending", "MEDIUM", datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    result = {
        "task_id": task_id,
        "title": title,
        "status": "created",
    }

    if auto_run:
        result["status"] = "queued_for_execution"
        result["message"] = f"Task {task_id} created and queued"

    return result

async def handle_ybis_workspace_status(params: dict, config: PluginConfig) -> dict:
    """Get workspace status"""
    active_dir = config.workspace_root / "active"
    workspaces = []

    if active_dir.exists():
        for ws in active_dir.iterdir():
            if ws.is_dir():
                ws_info = {
                    "task_id": ws.name,
                    "path": str(ws),
                    "has_plan": (ws / "docs" / "PLAN.md").exists(),
                    "has_result": (ws / "artifacts" / "RESULT.md").exists(),
                }

                if params.get("include_artifacts"):
                    artifacts = list((ws / "artifacts").glob("*")) if (ws / "artifacts").exists() else []
                    ws_info["artifacts"] = [a.name for a in artifacts]

                workspaces.append(ws_info)

    return {
        "active_workspaces": len(workspaces),
        "workspaces": workspaces,
    }

async def handle_ybis_artifact_search(params: dict, config: PluginConfig) -> dict:
    """Search artifacts"""
    query = params["query"].lower()
    artifact_type = params.get("artifact_type", "all")
    limit = params.get("limit", 10)

    results = []
    active_dir = config.workspace_root / "active"

    if active_dir.exists():
        for ws in active_dir.iterdir():
            if ws.is_dir():
                if artifact_type in ["PLAN", "all"]:
                    plan_path = ws / "docs" / "PLAN.md"
                    if plan_path.exists():
                        content = plan_path.read_text()
                        if query in content.lower():
                            results.append({
                                "task_id": ws.name,
                                "type": "PLAN",
                                "path": str(plan_path),
                                "snippet": content[:200],
                            })

                if artifact_type in ["RESULT", "all"]:
                    result_path = ws / "artifacts" / "RESULT.md"
                    if result_path.exists():
                        content = result_path.read_text()
                        if query in content.lower():
                            results.append({
                                "task_id": ws.name,
                                "type": "RESULT",
                                "path": str(result_path),
                                "snippet": content[:200],
                            })

    return {
        "query": query,
        "count": len(results[:limit]),
        "results": results[:limit],
    }

async def handle_ybis_workflow_visualize(params: dict, config: PluginConfig) -> dict:
    """Visualize workflow"""
    task_id = params.get("task_id", "N/A")

    viz = f"""
    +-------------+
    |   START     |
    +------+------+
           |
    +------v------+
    |   PLAN      | <-- Task: {task_id}
    +------+------+
           |
    +------v------+
    |  EXECUTE    |
    +------+------+
           |
    +------v------+
    |   VERIFY    |
    +------+------+
           |
    +------v------+
    |    GATE     |
    +------+------+
           |
    +------v------+
    |    END      |
    +-------------+
    """

    return {"visualization": viz, "task_id": task_id}

# ============================================================================
# PLUGIN INTERFACE
# ============================================================================

class YBISIntegrationPlugin:
    """Main plugin class"""

    def __init__(self, config: dict):
        self.config = PluginConfig(config)
        self.tools = TOOLS

    async def handle_tool(self, tool_name: str, params: dict) -> dict:
        """Route tool calls to handlers"""
        handlers = {
            "ybis_quick_task": handle_ybis_quick_task,
            "ybis_workspace_status": handle_ybis_workspace_status,
            "ybis_artifact_search": handle_ybis_artifact_search,
            "ybis_workflow_visualize": handle_ybis_workflow_visualize,
        }

        if tool_name in handlers:
            return await handlers[tool_name](params, self.config)

        return {"error": f"Unknown tool: {tool_name}"}

    def get_tools(self) -> list:
        """Return tool definitions"""
        return self.tools

# Export
plugin = YBISIntegrationPlugin
