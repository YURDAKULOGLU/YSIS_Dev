"""
Tool Search Tool - Dynamic tool discovery for MCP.

Implements Anthropic's Tool Search Tool pattern for on-demand tool discovery.
Reduces context bloat by only loading tools when needed.
"""

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def _get_mcp():
    """Lazy import of mcp to avoid circular import."""
    from ...services.mcp_server import mcp
    return mcp


async def tool_search_regex(query: str) -> str:
    """
    Search for MCP tools using regex pattern matching.

    This implements Anthropic's Tool Search Tool pattern, allowing agents
    to discover tools on-demand instead of loading all tool definitions upfront.

    Args:
        query: Search query (regex pattern or plain text)

    Returns:
        JSON string with matching tool references
    """
    # Get all registered tools from FastMCP (lazy import to avoid circular import)
    mcp = _get_mcp()
    all_tools = await mcp.list_tools()

    # Convert query to regex pattern (case-insensitive)
    try:
        # Try to compile as regex
        pattern = re.compile(query, re.IGNORECASE)
    except re.error:
        # If not valid regex, treat as plain text search
        pattern = re.compile(re.escape(query), re.IGNORECASE)

    # Search in tool names and descriptions
    matching_tools = []
    for tool in all_tools:
        name = tool.get("name", "")
        description = tool.get("description", "")

        # Check if query matches name or description
        if pattern.search(name) or pattern.search(description):
            # Return tool reference (not full definition to save tokens)
            matching_tools.append({
                "name": name,
                "description": description[:200],  # Truncate for token savings
                "input_schema": tool.get("inputSchema", {}),
            })

    return json.dumps({
        "query": query,
        "matches": matching_tools,
        "count": len(matching_tools),
    }, indent=2)


# Note: Tool registration is done in mcp_server.py to avoid circular import
# This module only defines the tool function, registration happens when mcp_server imports it

