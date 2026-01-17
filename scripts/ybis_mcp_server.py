#!/usr/bin/env python3
"""
YBIS MCP Server Entry Point.

Runs the FastMCP server with all registered tools.
Supports both stdio and SSE transport modes.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.services.mcp_server import mcp

if __name__ == "__main__":
    import asyncio
    
    # Print to stderr to avoid breaking JSON-RPC protocol on stdout
    print("[INFO] YBIS FastMCP Server Starting...", file=sys.stderr)
    
    # Get tool count (async)
    async def get_tool_count():
        tools = await mcp.list_tools()
        return len(tools)
    
    try:
        tool_count = asyncio.run(get_tool_count())
        print(f"[INFO] Registered {tool_count} tools", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] Could not list tools: {e}", file=sys.stderr)
        print("[INFO] Starting server anyway...", file=sys.stderr)

    # Check for SSE mode
    if "--sse" in sys.argv or "--transport=sse" in sys.argv:
        print("[INFO] Starting in SSE mode (Server-Sent Events)", file=sys.stderr)
        print("[INFO] Server will be available at http://localhost:8000", file=sys.stderr)
        mcp.run(transport="sse")
    else:
        print("[INFO] Starting in stdio mode", file=sys.stderr)
        mcp.run()


