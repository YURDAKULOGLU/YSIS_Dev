#!/usr/bin/env python3
"""Test YBIS via MCP - Use MCP tools to run tests."""

import sys
import asyncio
import json
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_via_mcp():
    """Test YBIS using MCP tools."""
    print("=" * 60)
    print("TESTING YBIS VIA MCP")
    print("=" * 60)
    print()
    
    # MCP server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                
                # List available tools
                print("Step 1: Listing available MCP tools...")
                tools = await session.list_tools()
                print(f"✅ Found {len(tools.tools)} tools")
                print()
                
                # Find test-related tools
                test_tools = [t for t in tools.tools if "test" in t.name.lower() or "run" in t.name.lower()]
                print(f"Test-related tools: {len(test_tools)}")
                for tool in test_tools[:10]:
                    print(f"  - {tool.name}: {tool.description[:60]}...")
                print()
                
                # Try to run tests using run_command if available
                print("Step 2: Looking for command execution tool...")
                run_tool = next((t for t in tools.tools if "run" in t.name.lower() and "command" in t.name.lower()), None)
                
                if run_tool:
                    print(f"✅ Found: {run_tool.name}")
                    print(f"   Description: {run_tool.description}")
                    print()
                    
                    # Run pytest
                    print("Step 3: Running tests via MCP...")
                    try:
                        result = await session.call_tool(
                            run_tool.name,
                            arguments={
                                "command": "pytest",
                                "args": ["tests/", "-v", "--tb=short"],
                                "cwd": str(project_root),
                            }
                        )
                        print(f"✅ Test execution result:")
                        print(f"   Content: {result.content[0].text[:500]}...")
                        if result.isError:
                            print(f"   ⚠️  Error: {result.content[0].text}")
                    except Exception as e:
                        print(f"❌ Failed to run tests: {e}")
                        print(f"   Tool may not support command execution")
                else:
                    print("⚠️  No command execution tool found")
                    print("   Available tools:")
                    for tool in tools.tools[:10]:
                        print(f"     - {tool.name}")
                
                # Try artifact tools
                print()
                print("Step 4: Testing artifact tools...")
                artifact_tools = [t for t in tools.tools if "artifact" in t.name.lower()]
                if artifact_tools:
                    print(f"✅ Found {len(artifact_tools)} artifact tools")
                    for tool in artifact_tools:
                        print(f"  - {tool.name}")
                else:
                    print("⚠️  No artifact tools found")
                
                # Try task tools
                print()
                print("Step 5: Testing task tools...")
                task_tools = [t for t in tools.tools if "task" in t.name.lower()]
                if task_tools:
                    print(f"✅ Found {len(task_tools)} task tools")
                    for tool in task_tools[:5]:
                        print(f"  - {tool.name}")
                    
                    # Try to get tasks
                    get_tasks_tool = next((t for t in task_tools if "get" in t.name.lower() and "task" in t.name.lower()), None)
                    if get_tasks_tool:
                        print()
                        print(f"Step 6: Getting tasks via MCP...")
                        try:
                            result = await session.call_tool(
                                get_tasks_tool.name,
                                arguments={}
                            )
                            print(f"✅ Tasks retrieved:")
                            tasks_data = json.loads(result.content[0].text)
                            # tasks_data is a dict with "tasks" key
                            tasks_list = tasks_data.get("tasks", [])
                            count = tasks_data.get("count", 0)
                            print(f"   Found {count} tasks")
                            for task in tasks_list[:3]:
                                print(f"     - {task.get('task_id', 'unknown')}: {task.get('title', 'no title')[:50]}")
                        except Exception as e:
                            print(f"❌ Failed to get tasks: {e}")
                            import traceback
                            traceback.print_exc()
                
                print()
                print("=" * 60)
                print("MCP TESTING COMPLETE")
                print("=" * 60)
                
    except Exception as e:
        print(f"❌ MCP connection failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_via_mcp())

