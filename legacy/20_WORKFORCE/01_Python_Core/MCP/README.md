# MCP (Model Context Protocol) Integration

## Overview

This directory contains MCP servers and clients for inter-agent communication in the YBIS system.

## Architecture

```
MCP/
├── servers/               # MCP Servers (expose agent capabilities)
│   ├── claude_code_server.py    # Claude Code agent server
│   └── ...
├── clients/               # MCP Clients (consume other agents)
│   └── ...
└── README.md             # This file
```

## Servers

### Claude Code Server

**Location:** `servers/claude_code_server.py`

**Capabilities:**
- `read_file` - Read file contents
- `write_file` - Write to files
- `execute_shell` - Execute shell commands
- `git_status` - Get git status
- `analyze_code` - Code analysis (placeholder)

**Usage Example:**

```python
# From another agent
import asyncio
from MCP.servers.claude_code_server import ClaudeCodeMCPServer

async def use_claude_code():
    server = ClaudeCodeMCPServer()

    # Read a file
    result = await server.handle_request(
        "read_file",
        {"path": "README.md"}
    )
    print(result)

    # Git status
    result = await server.handle_request(
        "git_status",
        {}
    )
    print(result)

asyncio.run(use_claude_code())
```

## Running Servers

### In Docker:

```bash
docker exec ybis-core python .YBIS_Dev/Agentic/MCP/servers/claude_code_server.py
```

### Locally:

```bash
cd .YBIS_Dev/Agentic/MCP
python servers/claude_code_server.py
```

## Adding New Servers

1. Create new server in `servers/` directory
2. Implement MCP interface:
   - `handle_request(method, params)`
   - `get_capabilities()`
3. Register in `AGENT_REGISTRY.json`
4. Document in this README

## Future Enhancements

- [ ] WebSocket support for real-time communication
- [ ] Authentication & authorization
- [ ] Request queue management
- [ ] Metrics & monitoring
- [ ] Rate limiting
- [ ] Load balancing across multiple agents
