#!/usr/bin/env python3
"""Run a single test file via MCP - Quick test."""

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


async def test_single():
    """Run a single test file via MCP."""
    test_file = sys.argv[1] if len(sys.argv) > 1 else "tests/adapters/test_adapter_protocol.py"
    
    print(f"Running test: {test_file}")
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
                
                print("✅ Connected to MCP server")
                print(f"Calling run_tests tool with: {test_file}")
                print()
                
                print("Waiting for test execution (this may take a while)...")
                try:
                    result = await asyncio.wait_for(
                        session.call_tool(
                            "run_tests",
                            arguments={
                                "test_path": test_file,
                                "verbose": True,
                                "coverage": False,
                            }
                        ),
                        timeout=180.0  # 3 minute timeout (tests can be slow)
                    )
                    print("✅ Tool call completed!")
                    
                    # Debug output
                    raw_text = result.content[0].text
                    print(f"DEBUG: Full JSON response ({len(raw_text)} chars):")
                    print(raw_text)
                    print("=" * 60)
                    
                    test_result = json.loads(raw_text)
                    
                    print("=" * 60)
                    if test_result.get("success"):
                        print("✅ TESTS PASSED")
                    else:
                        print("❌ TESTS FAILED")
                        print(f"Exit code: {test_result.get('exit_code')}")
                    
                    print("=" * 60)
                    print("\nFull output:")
                    print(test_result.get('stdout', ''))
                    
                    if test_result.get("stderr"):
                        print("\nErrors:")
                        print(test_result.get('stderr', ''))
                    
                    return test_result.get("success", False)
                    
                except asyncio.TimeoutError:
                    print("❌ Test execution timed out")
                    return False
                except Exception as e:
                    print(f"❌ Error: {e}")
                    import traceback
                    traceback.print_exc()
                    return False
                    
    except Exception as e:
        print(f"❌ MCP connection failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_single())
    sys.exit(0 if success else 1)

