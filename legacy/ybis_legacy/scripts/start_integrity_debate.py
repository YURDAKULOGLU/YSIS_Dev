import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path.cwd() / "src"))

from agentic import mcp_server

agent_id = "gemini-cli"
topic = "SYSTEM INTEGRITY ALERT: The Missing Links (Audit Report)"

proposal = """
## THE GRAND AUDIT REPORT

Status: Frankenstein is alive but disconnected.

### CRITICAL GAPS (Immediate Action Required)

1) THE PHANTOM BRIDGE (Council)
- Issue: tools/llm-council exists but src/agentic/bridges/council_bridge.py is missing.
- Impact: Council logic is inaccessible; decisions are manual.
- Assignment: Claude to build the bridge or document why it is deferred.

2) THE BLIND BRAIN (LangGraph)
- Issue: OrchestratorGraph does not call dependency impact or memory read.
- Impact: Plans are made without impact context or memory.
- Proposal: Inject MCP client or add a planner hook.

3) DATA ANEMIA (Neo4j)
- Issue: Graph import edges are sparse.
- Impact: Dependency graph under-represents reality.
- Assignment: Claude to review ingest_graph.py import scanner.

## EXECUTION PLAN

Claude:
- Confirm bridge status and fix ingest scanner.

Codex:
- Confirm React app data expectations for the subgraph API.

Gemini:
- Design MCP injection pattern for LangGraph.
"""

result = mcp_server.send_message(
    to="all",
    subject=topic,
    content=proposal,
    from_agent=agent_id,
    message_type="debate",
    priority="HIGH",
    reply_to=None,
    tags="debate"
)

print(result)
