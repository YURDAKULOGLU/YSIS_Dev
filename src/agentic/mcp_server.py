"""
YBIS MCP SERVER
Exposes YBIS Skills (Spec Writer, etc.) to the world via Model Context Protocol.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.getcwd())

from mcp.server.fastmcp import FastMCP
from src.agentic.skills.spec_writer import generate_spec, SpecWriterInput

# Initialize Server
mcp = FastMCP("YBIS Factory Skills")

# --- REGISTER TOOLS ---

@mcp.tool()
def create_spec_kit(project_name: str, description: str, tech_stack: str = "Python, React") -> str:
    """
    Generates a full technical specification kit (Architecture, API, Schema).
    Use this when starting a new project.
    """
    input_data = SpecWriterInput(
        project_name=project_name,
        description=description,
        tech_stack=tech_stack
    )
    return generate_spec(input_data)

@mcp.tool()
def hello_world() -> str:
    """Simple ping check."""
    return "YBIS MCP Server is Online!"

# --- ENTRY POINT ---
if __name__ == "__main__":
    print("🚀 YBIS MCP Server Starting...")
    mcp.run()
