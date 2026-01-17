"""
Messaging MCP Tools.

Tools for inter-agent messaging and communication.
"""

import json
import logging
from datetime import datetime

from ...constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


async def send_message(
    to: str,
    subject: str,
    content: str,
    from_agent: str = "mcp-client",
    message_type: str = "direct",
    priority: str = "NORMAL",
    reply_to: str | None = None,
    tags: str | None = None,
) -> str:
    """
    Send a message to another agent via the unified messaging system.

    Args:
        to: Recipient agent ID or 'all' for broadcast
        subject: Message subject
        content: Message content (supports markdown)
        from_agent: Sender agent ID (default: mcp-client)
        message_type: Type of message (direct, broadcast, debate, task_assignment)
        priority: Message priority (CRITICAL, HIGH, NORMAL, LOW)
        reply_to: Message ID being replied to (optional)
        tags: Comma-separated tags (optional)

    Returns:
        Success message with message ID
    """
    try:
        import aiosqlite

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        msg_id = f"MSG-{from_agent}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Parse tags
        tags_list = [t.strip() for t in tags.split(",")] if tags else []

        # Insert into messages table
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                """
                INSERT INTO messages
                (id, from_agent, to_agent, type, subject, content, reply_to, tags, metadata, seen_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    msg_id,
                    from_agent,
                    to,
                    message_type,
                    subject,
                    content,
                    reply_to,
                    json.dumps(tags_list),
                    json.dumps({}),
                    json.dumps([]),
                ),
            )
            await db.commit()

        return f"SUCCESS: Message sent. ID: {msg_id}"
    except Exception as e:
        return f"ERROR: Failed to send message: {e!s}"


async def read_inbox(agent_id: str, status: str | None = None, limit: int = 50) -> str:
    """
    Read messages from inbox for a specific agent.

    Args:
        agent_id: Agent ID to read messages for
        status: Filter by status (unread, read, archived). If None, returns all.
        limit: Maximum number of messages to return (default: 50)

    Returns:
        JSON string with list of messages
    """
    try:
        import aiosqlite

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"

        # Build query
        query = """
            SELECT id, from_agent, subject, content, type, priority,
                   timestamp, status, reply_to, tags
            FROM messages
            WHERE (to_agent = ? OR to_agent = 'all')
        """
        params = [agent_id]

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        async with aiosqlite.connect(db_path) as db, db.execute(query, params) as cursor:
            rows = await cursor.fetchall()

        messages = []
        for row in rows:
            msg = {
                "id": row[0],
                "from_agent": row[1],
                "subject": row[2],
                "content": row[3],
                "type": row[4],
                "priority": row[5],
                "timestamp": row[6],
                "status": row[7],
                "reply_to": row[8],
                "tags": json.loads(row[9]) if row[9] else [],
            }
            messages.append(msg)

        return json.dumps(
            {
                "agent_id": agent_id,
                "messages": messages,
                "count": len(messages),
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


async def ack_message(message_id: str, agent_id: str, action: str = "noted") -> str:
    """
    Acknowledge a message (mark as read and add acknowledgment).

    Args:
        message_id: Message ID to acknowledge
        agent_id: Agent acknowledging the message
        action: Acknowledgment action (noted, will_do, done, rejected)

    Returns:
        Success/failure message
    """
    try:
        import aiosqlite

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"

        # Get current message
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT seen_by, metadata FROM messages WHERE id = ?", (message_id,)) as cursor:
                row = await cursor.fetchone()

            if not row:
                return f"ERROR: Message {message_id} not found"

            # Update seen_by list
            seen_by = json.loads(row[0]) if row[0] else []
            if agent_id not in seen_by:
                seen_by.append(agent_id)

            # Update metadata with ack
            metadata = json.loads(row[1]) if row[1] else {}
            if "ack_by" not in metadata:
                metadata["ack_by"] = {}
            metadata["ack_by"][agent_id] = action

            # Update message
            await db.execute(
                """
                UPDATE messages
                SET status = 'read',
                    seen_by = ?,
                    metadata = ?
                WHERE id = ?
                """,
                (json.dumps(seen_by), json.dumps(metadata), message_id),
            )
            await db.commit()

        return f"SUCCESS: Message {message_id} acknowledged by {agent_id} ({action})"
    except Exception as e:
        return f"ERROR: {e!s}"

