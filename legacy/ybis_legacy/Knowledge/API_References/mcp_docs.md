# MODEL CONTEXT PROTOCOL (MCP) DOCUMENTATION

## 1. Overview
Standard for connecting AI to external systems (Tools, Resources, Prompts).
- **Server:** Exposes capabilities.
- **Client:** Connects to servers (e.g. Claude Desktop, YBIS).

## 2. Python SDK
`pip install mcp`

## 3. Building a Server (FastMCP)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Demo Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

## 4. Integration with LangChain
Use `langchain-mcp-adapters` to convert MCP tools to LangChain tools.
