"""
Debate Manager Module.
Autonomous deliberation for framework intake and architectural changes.
"""
import os
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event
from src.agentic import mcp_server

class DebateManager:
    def __init__(self, agent_id: str = "steward"):
        self.agent_id = agent_id
        self.keywords = [
            "framework", "integration", "adapter", "plugin", "langgraph",
            "openhands", "aider", "crewai", "metagpt", "langfuse",
            "opentelemetry", "litellm", "council", "consensus"
        ]

    def is_architectural_task(self, description: str) -> bool:
        """Determines if a task requires architectural debate."""
        lowered = description.lower()
        return any(word in lowered for word in self.keywords)

    async def maybe_start_debate(self, task_id: str, description: str, docs_dir: Path) -> str | None:
        """Starts a debate if the task is architectural and no debate exists."""
        if not self.is_architectural_task(description):
            return None

        marker_path = docs_dir / "DEBATE.md"
        if marker_path.exists():
            return None

        proposal = (
            f"Architectural Debate for {task_id}.\n\n"
            "This task involves framework intake or core system changes.\n"
            "Questions for the Council:\n"
            "1. Does this introduce new external dependencies?\n"
            "2. Is the implementation homogeneous with existing adapters?\n"
            "3. Are there deterministic gates for this change?\n"
        )

        debate_id = None
        try:
            # Try to use MCP server to initiate debate
            result = mcp_server.start_debate(
                topic=f"Framework Intake: {task_id}", 
                proposal=proposal, 
                agent_id=self.agent_id
            )
            if isinstance(result, str) and "ID:" in result:
                debate_id = result.split("ID:")[-1].strip()
        except Exception as e:
            log_event(f"Debate initiation failed: {e}", component="debate_manager", level="warning")

        if debate_id:
            marker_path.write_text(f"debate_id: {debate_id}\n", encoding="utf-8")
        
        return debate_id
