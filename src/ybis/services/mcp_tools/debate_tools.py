"""
Debate MCP Tools.

Tools for debate system integration and council consultation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from ...constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


def _debate_archive_dir() -> Path:
    """Get debate archive directory."""
    base = PROJECT_ROOT / "platform_data" / "knowledge" / "Messages" / "debates"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _write_debate(debate_id: str, topic: str, initiator: str, proposal: str) -> None:
    """Write debate archive file."""
    payload = {
        "id": debate_id,
        "topic": topic,
        "initiator": initiator,
        "proposal": proposal,
        "messages": [],
        "status": "open",
        "started_at": datetime.now().isoformat(),
    }
    path = _debate_archive_dir() / f"{debate_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _append_debate_message(debate_id: str, agent_id: str, content: str) -> bool:
    """Append message to debate archive."""
    path = _debate_archive_dir() / f"{debate_id}.json"
    if not path.exists():
        return False

    debate = json.loads(path.read_text(encoding="utf-8"))
    debate["messages"].append(
        {
            "from": agent_id,
            "timestamp": datetime.now().isoformat(),
            "content": content,
        }
    )
    path.write_text(json.dumps(debate, indent=2), encoding="utf-8")
    return True


async def start_debate(topic: str, proposal: str, agent_id: str = "mcp-client") -> str:
    """
    Start a debate: archive in platform_data/knowledge/Messages/debates and broadcast via MCP.

    Args:
        topic: Debate topic
        proposal: Initial proposal
        agent_id: ID of agent starting the debate

    Returns:
        Success message with debate ID
    """
    from .messaging_tools import send_message

    try:
        debate_id = f"DEBATE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        _write_debate(debate_id, topic, agent_id, proposal)
        from .messaging_tools import send_message
        await send_message(
            to="all",
            subject=debate_id,
            content=f"Debate started: {debate_id}\nTopic: {topic}\n\n{proposal}",
            from_agent=agent_id,
            message_type="debate",
            priority="HIGH",
            reply_to=None,
            tags="debate",
        )
        return f"SUCCESS: Debate started. ID: {debate_id}"
    except Exception as e:
        return f"ERROR: Failed to start debate: {e!s}"


async def reply_to_debate(debate_id: str, content: str, agent_id: str = "mcp-client") -> str:
    """
    Reply to a debate: append to archive and notify via MCP.

    Args:
        debate_id: Debate ID to reply to
        content: Reply content
        agent_id: ID of agent replying

    Returns:
        Success/failure message
    """
    from .messaging_tools import send_message

    try:
        if not _append_debate_message(debate_id, agent_id, content):
            return f"ERROR: Debate {debate_id} not found"
        from .messaging_tools import send_message
        await send_message(
            to="all",
            subject=debate_id,
            content=f"Reply from {agent_id}:\n\n{content}",
            from_agent=agent_id,
            message_type="debate",
            priority="NORMAL",
            reply_to=None,
            tags="debate",
        )
        return f"SUCCESS: Reply posted to {debate_id}"
    except Exception as e:
        return f"ERROR: Failed to reply to debate: {e!s}"


async def ask_council(
    question: str,
    agent_id: str = "mcp-client",
    use_local: bool = False,
    return_stages: bool = False,
) -> str:
    """
    Ask the LLM Council for consensus decision on important questions.

    Uses 3-stage deliberation:
    - Stage 1: Multiple LLMs provide individual responses
    - Stage 2: Anonymous peer review and ranking
    - Stage 3: Chairman synthesizes final consensus

    Args:
        question: The question to deliberate on
        agent_id: ID of agent asking (for logging)
        use_local: Use local Ollama models (True) or OpenRouter (False)
        return_stages: Return full deliberation details (False for just answer)

    Returns:
        Consensus answer from the council, or error message

    Example:
        ask_council("Should we use Cognee or MemGPT for memory?")
    """
    try:
        # Try to import council bridge (adapter-based)
        from ...adapters.council_bridge import CouncilBridgeAdapter

        bridge = CouncilBridgeAdapter(use_local=use_local)
        result = bridge.ask_council(question, return_stages=return_stages)

        if result.get("error"):
            return f"COUNCIL ERROR: {result.get('answer', 'Unknown error')}"

        response = f"COUNCIL CONSENSUS:\n{result['answer']}"

        if return_stages and "stage1" in result:
            response += f"\n\n[Deliberation involved {len(result['stage1'])} models"
            response += f" with {len(result['stage2'])} peer reviews]"

        # Log council usage
        from .messaging_tools import send_message

        await send_message(
            to="all",
            subject=f"Council Consulted by {agent_id}",
            content=f"Question: {question}\n\nDecision: {result['answer'][:200]}...",
            from_agent=agent_id,
            message_type="direct",
            priority="NORMAL",
            tags="council,decision",
        )

        return response

    except ImportError:
        return "COUNCIL ERROR: Council bridge adapter not yet implemented. This feature requires Task D (Observability/Event Bus Service)."
    except Exception as e:
        return f"COUNCIL ERROR: Failed to get consensus: {e!s}\n(Ensure council backend is accessible and API key is set if needed)"


