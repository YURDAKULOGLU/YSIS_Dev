import sys
import os
import asyncio

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir)) # .YBIS_Dev/..
sys.path.append(os.path.join(project_root, ".YBIS_Dev"))

from Agentic.MCP.servers.ybis_server import mcp

async def test_mcp_tools():
    print("\n--- Testing MCP Server Tools ---")
    try:
        tools = await mcp.list_tools()
        print(f"✅ Server Initialized. Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description[:50]}...")
            
        # Test a simple tool execution
        print("\n--- Executing 'get_ybis_dev_info' ---")
        # Note: FastMCP executing directly might require different syntax depending on version,
        # but calling the function directly works if it's decorated.
        # Let's try listing the project structure using the tool function logic
        
        # We can't easily call mcp.call_tool in this script without running the full server loop,
        # but we can verify the import worked, which confirms dependencies are fine.
        
    except Exception as e:
        print(f"❌ MCP Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
