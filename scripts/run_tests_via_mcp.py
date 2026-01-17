#!/usr/bin/env python3
"""Run YBIS tests via MCP - Use MCP tools to execute tests."""

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


async def run_tests_via_mcp():
    """Run tests using MCP tools."""
    print("=" * 60)
    print("RUNNING TESTS VIA MCP")
    print("=" * 60)
    print()
    
    # MCP server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    try:
        # Add timeout for connection (Python 3.11+)
        try:
            timeout_func = asyncio.timeout
        except AttributeError:
            # Fallback for Python < 3.11
            from asyncio import wait_for as timeout_func
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                
                # List tools
                tools = await session.list_tools()
                print(f"✅ Connected to MCP server ({len(tools.tools)} tools available)")
                print()
                
                # Find test tools
                test_tool = next((t for t in tools.tools if t.name == "run_tests"), None)
                if not test_tool:
                    print("❌ run_tests tool not found")
                    print("Available tools:")
                    for tool in tools.tools[:10]:
                        print(f"  - {tool.name}")
                    return False
                
                print(f"✅ Found test tool: {test_tool.name}")
                print(f"   Description: {test_tool.description}")
                print()
                
                # Run tests - start with a small test first
                print("Step 1: Running a quick test (tests/adapters/test_adapter_protocol.py)...")
                print("-" * 60)
                print("(This is a quick test to verify MCP works)")
                print()
                try:
                    # Run a small test first with shorter timeout
                    print("Calling run_tests tool...")
                    result = await asyncio.wait_for(
                        session.call_tool(
                            "run_tests",
                            arguments={
                                "test_path": "tests/adapters/test_adapter_protocol.py",
                                "verbose": False,  # Less verbose for speed
                                "coverage": False,
                            }
                        ),
                        timeout=30.0  # 30 second timeout for quick test
                    )
                    
                    print("✅ Tool call completed, parsing result...")
                    test_result = json.loads(result.content[0].text)
                    
                    if test_result.get("success"):
                        print("✅ Tests passed!")
                        stdout = test_result.get('stdout', '')
                        if stdout:
                            # Show last 20 lines
                            lines = stdout.split('\n')
                            print(f"\nLast {min(20, len(lines))} lines of output:")
                            print('\n'.join(lines[-20:]))
                    else:
                        print("❌ Tests failed!")
                        print(f"Exit code: {test_result.get('exit_code')}")
                        stdout = test_result.get('stdout', '')
                        if stdout:
                            lines = stdout.split('\n')
                            print(f"\nLast {min(30, len(lines))} lines of output:")
                            print('\n'.join(lines[-30:]))
                        if test_result.get("stderr"):
                            print(f"\nErrors:\n{test_result.get('stderr', '')[:500]}")
                    
                    print()
                    
                except asyncio.TimeoutError:
                    print("❌ Test execution timed out after 30 seconds")
                    print("   (This might be normal if tests take longer)")
                    print("   Try running a smaller test or increase timeout")
                    return False
                except Exception as e:
                    print(f"❌ Failed to run tests: {e}")
                    import traceback
                    traceback.print_exc()
                    return False
                
                # Run linter
                print("Step 2: Running linter...")
                print("-" * 60)
                try:
                    lint_tool = next((t for t in tools.tools if t.name == "run_linter"), None)
                    if lint_tool:
                        # Add timeout for linter (1 minute)
                        try:
                            result = await asyncio.wait_for(
                                session.call_tool(
                                    "run_linter",
                                    arguments={
                                        "path": "src/",
                                        "fix": False,
                                    }
                                ),
                                timeout=60.0
                            )
                        except asyncio.TimeoutError:
                            print("⚠️  Linter execution timed out")
                            result = None
                        
                        if result:
                            lint_result = json.loads(result.content[0].text)
                            
                            if lint_result.get("success"):
                                print("✅ Linter passed!")
                                if lint_result.get("stdout"):
                                    print(f"\nOutput:\n{lint_result.get('stdout', '')[:500]}")
                            else:
                                print("⚠️  Linter found issues")
                                print(f"\nOutput:\n{lint_result.get('stdout', '')[:1000]}")
                    else:
                        print("⚠️  Linter tool not found")
                except Exception as e:
                    print(f"⚠️  Linter check failed: {e}")
                
                print()
                print("=" * 60)
                print("TEST EXECUTION COMPLETE")
                print("=" * 60)
                
                return True
                
    except asyncio.TimeoutError:
        print("❌ Operation timed out")
        return False
    except Exception as e:
        print(f"❌ MCP connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests_via_mcp())
    sys.exit(0 if success else 1)

