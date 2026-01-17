"""
Tool Registry - Central registry for all YBIS tools.

Provides tool discovery and metadata for dynamic tool loading.
Supports Anthropic's Tool Search Tool pattern.
"""

import logging

logger = logging.getLogger(__name__)

from typing import Any

# Global tool registry (populated from MCP server)
_tool_registry: dict[str, dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    input_schema: dict[str, Any],
    defer_loading: bool = False,
    input_examples: list[dict[str, Any]] | None = None,
) -> None:
    """
    Register a tool in the registry.

    Args:
        name: Tool name
        description: Tool description (used for search)
        input_schema: JSON schema for tool inputs
        defer_loading: If True, tool is not loaded upfront (on-demand discovery)
        input_examples: Optional examples of tool usage (for Tool Use Examples)
    """
    _tool_registry[name] = {
        "name": name,
        "description": description,
        "input_schema": input_schema,
        "defer_loading": defer_loading,
        "input_examples": input_examples or [],
    }


def search_tools(query: str) -> list[dict[str, Any]]:
    """
    Search for tools by name or description.

    Args:
        query: Search query (regex pattern or plain text)

    Returns:
        List of matching tool references
    """
    import re

    try:
        pattern = re.compile(query, re.IGNORECASE)
    except re.error:
        pattern = re.compile(re.escape(query), re.IGNORECASE)

    matches = []
    for tool in _tool_registry.values():
        name = tool["name"]
        description = tool["description"]

        if pattern.search(name) or pattern.search(description):
            matches.append({
                "name": name,
                "description": description[:200],  # Truncate for token savings
                "input_schema": tool["input_schema"],
                "input_examples": tool.get("input_examples", []),
            })

    return matches


def get_tool(name: str) -> dict[str, Any] | None:
    """Get full tool definition by name."""
    return _tool_registry.get(name)


def list_tools(defer_loading: bool | None = None) -> list[dict[str, Any]]:
    """
    List all registered tools.

    Args:
        defer_loading: If True, only return deferred tools. If False, only non-deferred. If None, return all.

    Returns:
        List of tool references
    """
    tools = list(_tool_registry.values())

    if defer_loading is not None:
        tools = [t for t in tools if t.get("defer_loading", False) == defer_loading]

    return tools

