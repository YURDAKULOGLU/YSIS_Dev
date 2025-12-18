# YBIS MCP Server: Multi-Client Connection Guide

Our `ybis_server.py` is a universal tool provider. Here is how to connect various AI tools to it.

## 1. Cursor IDE (Cursor + Codex/Claude)

Cursor now supports MCP natively (in Beta).

1.  Open **Cursor Settings** (Ctrl+,).
2.  Go to **Features** > **MCP**.
3.  Click **+ Add New MCP Server**.
4.  Enter the following details:
    *   **Name:** `ybis-core`
    *   **Type:** `command`
    *   **Command:** `C:\Projeler\YBIS\.YBIS_Dev\Agentic\.venv\Scripts\python.exe`
    *   **Arguments:** `C:\Projeler\YBIS\.YBIS_Dev\Agentic\MCP\servers\ybis_server.py`

**Result:** Now, when you chat with Cursor (`Ctrl+L` or `Ctrl+K`), it can see and use `search_knowledge_base`, `get_repo_tree`, `read_project_file`, `write_project_file`, `get_next_task`, `list_all_tasks`, `log_agent_action` tools automatically!

---

## 2. VS Code (Github Copilot / Codex)

VS Code uses extensions to support MCP.

1.  Install the **"Model Context Protocol"** extension (if available/official) or use the `vs-code-mcp` bridge.
2.  Edit your `.vscode/settings.json` in the project root:

```json
{
  "mcp.servers": {
    "ybis-core": {
      "command": "C:\\Projeler\\YBIS\\.YBIS_Dev\\Agentic\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Projeler\\YBIS\\.YBIS_Dev\\Agentic\\MCP\\servers\\ybis_server.py"]
    },
    "ybis-filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Projeler\\YBIS"
      ]
    }
  }
}
```

---

## 3. Gemini / Custom Python Scripts

Since Gemini doesn't have a native "Desktop App" with MCP support yet, you act as the client using our Python SDK.

In your python script (or `orchestrator.py`), you are already doing this! But to connect to the *Server* specifically:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="C:\\Projeler\\YBIS\\.YBIS_Dev\\Agentic\\.venv\\Scripts\\python.exe",
    args=["C:\\Projeler\\YBIS\\.YBIS_Dev\\Agentic\\MCP\\servers\\ybis_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Call the tool
        result = await session.call_tool("get_next_task", arguments={})
        print(result)
```

---

## 4. Claude Desktop (Already Configured)

Copy the contents of `claude_config_example.json` to:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
**(Ensure the paths inside the JSON are absolute and correct for your system)**

```
