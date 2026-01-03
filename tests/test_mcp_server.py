import sys
import os

# Add project root
sys.path.insert(0, os.getcwd())

def test_mcp_server():
    print("🔌 Testing MCP Server...")

    try:
        from src.agentic.mcp_server import mcp

        # FastMCP internal list_tools implementation might be async or sync depending on version
        # But we can inspect the decorated tools directly for a simple check

        tools = mcp._tools # Accessing internal registry (a bit hacky but works for verify)

        print(f"   Found {len(tools)} tools.")

        tool_names = [t.name for t in tools.values() if hasattr(t, 'name')]
        # Fallback if internal structure differs
        if not tool_names:
             tool_names = list(tools.keys())

        print(f"   Tools: {tool_names}")

        if "create_spec_kit" in tool_names:
            print("[OK] 'create_spec_kit' Skill is ONLINE.")
        else:
            print("[ERROR] 'create_spec_kit' Skill NOT FOUND.")

    except ImportError as e:
        print(f"[ERROR] Import Error: {e}")
    except Exception as e:
        print(f"[ERROR] Test Error: {e}")

if __name__ == "__main__":
    test_mcp_server()
