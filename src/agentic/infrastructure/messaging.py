"""
Agent-to-Agent Messaging System
Simple file-based messaging for multi-agent coordination.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

class AgentMessaging:
    """File-based messaging between Claude and Gemini."""

    def __init__(self, agent_id: str = "claude"):
        self.agent_id = agent_id
        self.base_path = Path("Knowledge/Messages")
        self.inbox = self.base_path / "inbox"
        self.outbox = self.base_path / "outbox"
        self.debates = self.base_path / "debates"

        # Ensure directories exist
        for path in [self.inbox, self.outbox, self.debates]:
            path.mkdir(parents=True, exist_ok=True)

    def send_message(
        self,
        to: str,
        subject: str,
        content: str,
        msg_type: str = "message",
        reply_to: Optional[str] = None
    ) -> str:
        """Send a message to another agent."""
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
            "status": "unread"
        }

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
                if msg.get("status") == "unread" and msg.get("to") in [self.agent_id, "broadcast"]:
                    messages.append(msg)

        # Sort by timestamp
        messages.sort(key=lambda x: x["timestamp"])
        return messages

    def mark_as_read(self, msg_id: str):
        """Mark a message as read."""
        msg_file = self.inbox / f"{msg_id}.json"
        if msg_file.exists():
            with open(msg_file, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            msg["status"] = "read"
            with open(msg_file, 'w', encoding='utf-8') as f:
                json.dump(msg, f, indent=2)

    def start_debate(self, topic: str, proposal: str) -> str:
        """Start a new debate."""
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


if __name__ == "__main__":
    # Test messaging
    claude = AgentMessaging("claude")

    # Send test message
    msg_id = claude.send_message(
        to="gemini",
        subject="Test Message",
        content="Hello Gemini! Can you hear me?",
        msg_type="question"
    )

    print(f"Message sent: {msg_id}")

    # Check unread
    unread = claude.get_unread_messages()
    print(f"Unread messages: {len(unread)}")
