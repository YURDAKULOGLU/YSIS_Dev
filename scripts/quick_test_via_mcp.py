#!/usr/bin/env python3
"""Quick test via MCP - Just check if tools are available."""

import sys
import asyncio
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def quick_test():
    """Quick test - just list tools."""
    print("Quick MCP Test - Checking available tools...")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Add timeout for list_tools
                tools = await asyncio.wait_for(session.list_tools(), timeout=5.0)
                print(f"✅ Connected! Found {len(tools.tools)} tools")
                
                # Check for test tools
                test_tools = [t for t in tools.tools if "test" in t.name.lower()]
                print(f"\nTest tools: {len(test_tools)}")
                for tool in test_tools:
                    print(f"  - {tool.name}: {tool.description[:60]}...")
                
                return True
    except asyncio.TimeoutError:
        print("❌ Connection timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(quick_test())
    sys.exit(0 if success else 1)

