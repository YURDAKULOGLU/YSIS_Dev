"""
Services - Background services (worker, MCP server, policy).
"""
from typing import TYPE_CHECKING

from .policy import PolicyProvider, get_policy_provider

if TYPE_CHECKING:
    from .mcp_server import MCPServer
    from .worker import YBISWorker

__all__ = [
    "MCPServer",
    "PolicyProvider",
    "YBISWorker",
    "get_policy_provider",
]


def __getattr__(name: str):
    if name == "MCPServer":
        from .mcp_server import MCPServer

        return MCPServer
    if name == "YBISWorker":
        from .worker import YBISWorker

        return YBISWorker
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
