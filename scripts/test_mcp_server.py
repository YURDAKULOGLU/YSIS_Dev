#!/usr/bin/env python3
"""
Test MCP Server - Check if MCP server is working.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.services.mcp_server import mcp


async def test_mcp_server():
    """Test MCP server tools."""
    print("Testing MCP Server...")
    print("=" * 50)
    
    # List tools
    try:
        tools = await mcp.list_tools()
        print(f"[OK] MCP Server has {len(tools)} tools registered:\n")
        
        # Group by category
        tool_categories = {}
        for tool in tools:
            # Tool is a Pydantic model, use attribute access
            name = getattr(tool, "name", "unknown") if hasattr(tool, "name") else str(tool)
            # Categorize by prefix
            if name.startswith("task_"):
                category = "Task Management"
            elif name.startswith("artifact_"):
                category = "Artifact Management"
            elif name.startswith("agent_"):
                category = "Agent Management"
            elif name.startswith("send_") or name.startswith("read_") or name.startswith("ack_"):
                category = "Messaging"
            elif name.startswith("start_") or name.startswith("reply_") or name.startswith("ask_"):
                category = "Debate"
            elif "dependency" in name or "circular" in name or "critical" in name:
                category = "Dependency Analysis"
            elif "memory" in name or "search" in name or "add_to" in name:
                category = "Memory"
            else:
                category = "Other"
            
            if category not in tool_categories:
                tool_categories[category] = []
            tool_categories[category].append(name)
        
        # Print categorized
        for category, tool_names in sorted(tool_categories.items()):
            print(f"\n{category}:")
            for tool_name in sorted(tool_names):
                print(f"  - {tool_name}")
        
        print("\n" + "=" * 50)
        print("[OK] MCP Server is ready!")
        print("\nTo start server:")
        print("  python scripts/ybis_mcp_server.py")
        print("\nTo start in SSE mode:")
        print("  python scripts/ybis_mcp_server.py --sse")
        
    except Exception as e:
        print(f"[ERROR] Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)

