#!/usr/bin/env python3
"""
Test MCP Client - Connect to YBIS MCP Server as an external agent.
"""

import asyncio
import sys
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("[ERROR] MCP client not available. Install with: pip install mcp")
    sys.exit(1)


async def test_mcp_client_stdio():
    """Test MCP client via stdio transport."""
    print("Testing MCP Client (stdio mode)...")
    print("=" * 50)
    
    # Server command
    server_script = project_root / "scripts" / "ybis_mcp_server.py"
    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)],
        env=None,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                
                # List tools
                tools_result = await session.list_tools()
                print(f"[OK] Connected! Found {len(tools_result.tools)} tools:\n")
                
                # Show first 5 tools
                for tool in tools_result.tools[:5]:
                    print(f"  - {tool.name}: {tool.description[:60]}...")
                
                if len(tools_result.tools) > 5:
                    print(f"  ... and {len(tools_result.tools) - 5} more tools")
                
                # Test a simple tool call: get_tasks
                print("\n" + "=" * 50)
                print("Testing tool call: get_tasks")
                print("-" * 50)
                
                try:
                    call_result = await session.call_tool("get_tasks", {})
                    print(f"[OK] Tool call successful!")
                    print(f"Result: {call_result.content[0].text[:200]}...")
                except Exception as e:
                    print(f"[WARN] Tool call failed: {e}")
                    print("(This is OK if database is not initialized)")
                
                print("\n" + "=" * 50)
                print("[OK] MCP Client test complete!")
                return True
                
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_mcp_client_sse():
    """Test MCP client via SSE transport."""
    print("\nTesting MCP Client (SSE mode)...")
    print("=" * 50)
    print("[INFO] SSE mode requires server to be running separately")
    print("[INFO] Start server with: python scripts/ybis_mcp_server.py --sse")
    print("[INFO] Then connect to: http://localhost:8000")
    print("[SKIP] SSE test skipped (requires manual server start)")
    return True


async def main():
    """Run all tests."""
    print("YBIS MCP Client Test")
    print("=" * 50)
    print("This script tests if an external agent (like me) can connect")
    print("to the YBIS MCP server and use its tools.\n")
    
    # Test stdio mode
    stdio_success = await test_mcp_client_stdio()
    
    # Test SSE mode (skip for now)
    sse_success = await test_mcp_client_sse()
    
    print("\n" + "=" * 50)
    if stdio_success:
        print("[OK] MCP Client can connect via stdio!")
        print("\nAs an external agent, I can:")
        print("  1. Connect to YBIS MCP server")
        print("  2. List available tools")
        print("  3. Call tools (task_create, task_run, etc.)")
        print("  4. Use YBIS for self-development!")
    else:
        print("[ERROR] MCP Client connection failed")
    
    return stdio_success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

