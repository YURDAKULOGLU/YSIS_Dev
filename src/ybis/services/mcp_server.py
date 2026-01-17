"""
MCP Server - FastMCP tool registry with a local convenience wrapper.
"""

import logging

logger = logging.getLogger(__name__)

import asyncio
import json
from collections.abc import Callable
from typing import Any

from mcp.server.fastmcp import FastMCP

from .mcp_tools import (
    agent_tools,
    artifact_tools,
    debate_tools,
    dependency_tools,
    memory_tools,
    messaging_tools,
    task_tools,
    test_tools,
    tool_search,
)

# Initialize FastMCP server
mcp = FastMCP("YBIS Platform Server")

# --- Register Tool Search Tool FIRST (for dynamic discovery) ---
# Tool Search Tool is always loaded (small, ~500 tokens)
# Other tools can be discovered on-demand
mcp.tool()(tool_search.tool_search_regex)

# --- Register Task Tools ---
mcp.tool()(task_tools.task_create)
mcp.tool()(task_tools.task_status)
mcp.tool()(task_tools.get_tasks)
mcp.tool()(task_tools.claim_task)
mcp.tool()(task_tools.claim_next_task)
mcp.tool()(task_tools.update_task_status)
mcp.tool()(task_tools.task_complete)
mcp.tool()(task_tools.task_run)

# --- Register Artifact Tools ---
mcp.tool()(artifact_tools.artifact_read)
mcp.tool()(artifact_tools.artifact_write)
mcp.tool()(artifact_tools.approval_write)

# --- Register Agent Tools ---
mcp.tool()(agent_tools.register_agent)
mcp.tool()(agent_tools.get_agents)
mcp.tool()(agent_tools.agent_heartbeat)

# --- Register Messaging Tools ---
mcp.tool()(messaging_tools.send_message)
mcp.tool()(messaging_tools.read_inbox)
mcp.tool()(messaging_tools.ack_message)

# --- Register Debate Tools ---
mcp.tool()(debate_tools.start_debate)
mcp.tool()(debate_tools.reply_to_debate)
mcp.tool()(debate_tools.ask_council)

# --- Register Dependency Tools ---
mcp.tool()(dependency_tools.dependency_scan)
mcp.tool()(dependency_tools.dependency_impact)
mcp.tool()(dependency_tools.dependency_stale)
mcp.tool()(dependency_tools.dependency_list)
mcp.tool()(dependency_tools.check_dependency_impact)
mcp.tool()(dependency_tools.find_circular_dependencies)
mcp.tool()(dependency_tools.get_critical_files)

# --- Register Memory Tools ---
mcp.tool()(memory_tools.add_to_memory)
mcp.tool()(memory_tools.search_memory)

# --- Register Test Tools ---
mcp.tool()(test_tools.run_tests)
mcp.tool()(test_tools.run_linter)
mcp.tool()(test_tools.check_test_coverage)


def _decode_payload(payload: str) -> dict[str, Any]:
    """Decode JSON responses from tool functions to keep MCPServer compatible."""
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {"raw": payload}


async def _call_tool(func: Callable[..., str], *args: Any) -> dict[str, Any]:
    """Run sync MCP tool functions safely from async contexts."""
    payload = await asyncio.to_thread(func, *args)
    return _decode_payload(payload)


class MCPServer:
    """
    Local wrapper for MCP tools (non-networked).

    Keeps existing scripts working while the canonical server is FastMCP.
    """

    def __init__(self, db_path: str | None = None) -> None:
        """Capture db_path for legacy callers (FastMCP tools use default path)."""
        self.db_path = db_path

    async def initialize(self) -> None:
        """Compatibility no-op for legacy callers."""
        return None

    async def get_tools(self) -> list[dict[str, Any]]:
        """Return FastMCP tool metadata."""
        return await mcp.list_tools()

    async def task_create(self, title: str, objective: str, priority: str = "MEDIUM") -> dict[str, Any]:
        return await _call_tool(task_tools.task_create, title, objective, priority)

    async def task_status(self, task_id: str) -> dict[str, Any]:
        return await _call_tool(task_tools.task_status, task_id)

    async def get_tasks(self, status: str | None = None) -> dict[str, Any]:
        return await _call_tool(task_tools.get_tasks, status)

    async def task_claim(self, worker_id: str) -> dict[str, Any]:
        return await _call_tool(task_tools.claim_next_task, worker_id)

    async def claim_task(self, task_id: str, worker_id: str) -> dict[str, Any]:
        return await _call_tool(task_tools.claim_task, task_id, worker_id)

    async def claim_next_task(self, worker_id: str) -> dict[str, Any]:
        return await _call_tool(task_tools.claim_next_task, worker_id)

    async def update_task_status(self, task_id: str, status: str) -> dict[str, Any]:
        return await _call_tool(task_tools.update_task_status, task_id, status)

    async def task_complete(
        self, task_id: str, run_id: str, status: str, result_summary: str, worker_id: str
    ) -> dict[str, Any]:
        return await _call_tool(
            task_tools.task_complete, task_id, run_id, status, result_summary, worker_id
        )

    async def task_run(
        self, task_id: str, workflow_name: str = "ybis_native"
    ) -> dict[str, Any]:
        return await _call_tool(task_tools.task_run, task_id, workflow_name)

    async def artifact_read(self, task_id: str, run_id: str, artifact_name: str) -> dict[str, Any]:
        return await _call_tool(artifact_tools.artifact_read, task_id, run_id, artifact_name)

    async def artifact_write(self, run_id: str, name: str, content: str) -> dict[str, Any]:
        return await _call_tool(artifact_tools.artifact_write, run_id, name, content)

    async def approval_write(self, task_id: str, run_id: str, approver: str, reason: str) -> dict[str, Any]:
        return await _call_tool(artifact_tools.approval_write, task_id, run_id, approver, reason)


if __name__ == "__main__":
    import sys

    print("[INFO] YBIS MCP Server Starting...")
    print(f"[INFO] Registered {len(mcp.list_tools())} tools")

    # Check for SSE mode
    if "--sse" in sys.argv or "--transport=sse" in sys.argv:
        print("[INFO] Starting in SSE mode (Server-Sent Events)")
        mcp.run(transport="sse")
    else:
        print("[INFO] Starting in stdio mode")
        mcp.run()
