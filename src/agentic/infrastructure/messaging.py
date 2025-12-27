"""
Agent-to-Agent Messaging System
Simple file-based messaging for multi-agent coordination.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from src.agentic.core.protocols import InterAgentMessage
except Exception:
    InterAgentMessage = None

class AgentMessaging:
    """File-based messaging between Claude and Gemini."""

    def __init__(self, agent_id: str = "claude"):
        self.agent_id = agent_id
        self.base_path = Path("Knowledge/Messages")
        self.inbox = self.base_path / "inbox"
        self.outbox = self.base_path / "outbox"
        self.debates = self.base_path / "debates"

        self.allow_legacy_writes = os.getenv("YBIS_ALLOW_LEGACY_MESSAGING", "0") == "1"

        # Ensure directories exist
        for path in [self.inbox, self.outbox, self.debates]:
            path.mkdir(parents=True, exist_ok=True)

    def send_message(
        self,
        to: str,
        subject: str,
        content: str,
        msg_type: str = "message",
        reply_to: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Send a message to another agent."""
        if not self.allow_legacy_writes:
            raise RuntimeError("Legacy file-based messaging is disabled. Use MCP tools via scripts/ybis.py message.")
        msg_id = f"MSG-{self.agent_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        message = {
            "id": msg_id,
            "from": self.agent_id,
            "to": to,
            "type": msg_type,
            "subject": subject,
            "content": content,
            "reply_to": reply_to,
            "timestamp": datetime.now().isoformat(),
            "status": "unread",
            "metadata": metadata or {},
            "seen_by": []
        }

        message = self._validate_message(message)

        # Write to outbox
        outbox_file = self.outbox / f"{msg_id}.json"
        with open(outbox_file, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2)

        # Also write to recipient's inbox
        inbox_file = self.inbox / f"{msg_id}.json"
        with open(inbox_file, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2)

        return msg_id

    def get_unread_messages(self) -> List[Dict[str, Any]]:
        """Get all unread messages from inbox."""
        messages = []
        for msg_file in self.inbox.glob("*.json"):
            with open(msg_file, 'r', encoding='utf-8') as f:
                msg = json.load(f)
                try:
                    msg = self._validate_message(msg)
                except ValueError:
                    continue
                seen_by = msg.get("seen_by", [])
                if msg.get("status") == "unread" and self.agent_id not in seen_by and msg.get("to") in [self.agent_id, "broadcast"]:
                    messages.append(msg)

        # Sort by timestamp
        messages.sort(key=lambda x: x["timestamp"])
        return messages

    def mark_as_read(self, msg_id: str):
        """Mark a message as read for this agent."""
        self.ack_message(msg_id, self.agent_id)

    def ack_message(self, msg_id: str, agent_id: str) -> bool:
        """Acknowledge a message as read and record seen_by."""
        msg_file = self.inbox / f"{msg_id}.json"
        if msg_file.exists():
            with open(msg_file, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            try:
                msg = self._validate_message(msg)
            except ValueError:
                return False
            seen_by = msg.get("seen_by", [])
            if agent_id not in seen_by:
                seen_by.append(agent_id)
            msg["seen_by"] = seen_by
            msg["status"] = "read"
            with open(msg_file, 'w', encoding='utf-8') as f:
                json.dump(msg, f, indent=2)
            return True
        return False

    def start_debate(self, topic: str, proposal: str) -> str:
        """Start a new debate."""
        if not self.allow_legacy_writes:
            raise RuntimeError("Legacy debate writes are disabled. Use MCP tools via scripts/ybis.py debate.")
        debate_id = f"DEBATE-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        debate = {
            "id": debate_id,
            "topic": topic,
            "initiator": self.agent_id,
            "proposal": proposal,
            "messages": [],
            "status": "open",
            "started_at": datetime.now().isoformat()
        }

        debate_file = self.debates / f"{debate_id}.json"
        with open(debate_file, 'w', encoding='utf-8') as f:
            json.dump(debate, f, indent=2)

        # Notify other agent
        self.send_message(
            to="broadcast",
            subject=f"New Debate: {topic}",
            content=f"Debate started: {debate_id}\nProposal: {proposal}",
            msg_type="debate"
        )

        return debate_id

    def reply_to_debate(self, debate_id: str, content: str) -> bool:
        """Reply to an existing debate."""
        if not self.allow_legacy_writes:
            raise RuntimeError("Legacy debate writes are disabled. Use MCP tools via scripts/ybis.py debate reply.")
        debate_file = self.debates / f"{debate_id}.json"
        
        if not debate_file.exists():
            return False

        with open(debate_file, 'r', encoding='utf-8') as f:
            debate = json.load(f)

        new_message = {
            "from": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "content": content
        }

        debate["messages"].append(new_message)

        with open(debate_file, 'w', encoding='utf-8') as f:
            json.dump(debate, f, indent=2)

        # Notify participants via broadcast
        self.send_message(
            to="broadcast",
            subject=f"Reply to Debate: {debate.get('topic', debate_id)}",
            content=f"New reply from {self.agent_id} in debate {debate_id}.",
            msg_type="debate_reply"
        )
        
        return True

    def _validate_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        if "metadata" not in message:
            message["metadata"] = {}
        if "seen_by" not in message:
            message["seen_by"] = []
        if "status" not in message:
            message["status"] = "unread"
        if "reply_to" not in message:
            message["reply_to"] = None
        if isinstance(message.get("timestamp"), datetime):
            message["timestamp"] = message["timestamp"].isoformat()
        if "from" in message and "from_agent" not in message:
            message["from_agent"] = message["from"]
        if "type" in message and "message_type" not in message:
            message["message_type"] = message["type"]
        if InterAgentMessage is None:
            return message
        model = InterAgentMessage(**message)
        data = model.dict(by_alias=True)
        if isinstance(data.get("timestamp"), datetime):
            data["timestamp"] = data["timestamp"].isoformat()
        if "message_type" in data and "type" not in data:
            data["type"] = data["message_type"]
        return data


if __name__ == "__main__":
    # Test messaging (NO EMOJIS - Windows cp1254 compatibility)
    claude = AgentMessaging("claude")

    # Send test message
    msg_id = claude.send_message(
        to="gemini",
        subject="Test Message",
        content="Hello Gemini! Can you hear me?",
        msg_type="question"
    )

    print(f"[OK] Message sent: {msg_id}")

    # Check unread
    unread = claude.get_unread_messages()
    print(f"[INFO] Unread messages: {len(unread)}")
