"""
Agent Management MCP Tools.

Tools for agent registration and heartbeat tracking.
"""

import json
import logging

from ...constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


async def register_agent(
    agent_id: str,
    name: str,
    agent_type: str,
    capabilities: str | None = None,
    allowed_tools: str | None = None,
) -> str:
    """
    Register an agent in the YBIS system.

    Args:
        agent_id: Unique agent identifier (e.g., 'claude-code', 'gemini-cli')
        name: Human-readable agent name
        agent_type: Type of agent ('cli', 'internal', 'external', 'mcp_client')
        capabilities: JSON string of agent capabilities (optional)
        allowed_tools: JSON string of allowed tools for this agent (optional)

    Returns:
        Success/failure message
    """
    try:
        import aiosqlite

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"

        # Check if agent already exists
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT id FROM agents WHERE id = ?", (agent_id,)) as cursor:
                existing = await cursor.fetchone()

            if existing:
                # Update existing agent
                await db.execute(
                    """
                    UPDATE agents
                    SET name = ?, type = ?, capabilities = ?, allowed_tools = ?,
                        last_heartbeat = CURRENT_TIMESTAMP, status = 'ACTIVE'
                    WHERE id = ?
                    """,
                    (name, agent_type, capabilities, allowed_tools, agent_id),
                )
                await db.commit()
                msg = f"Agent {agent_id} updated"
            else:
                # Insert new agent
                await db.execute(
                    """
                    INSERT INTO agents (id, name, type, capabilities, allowed_tools, status)
                    VALUES (?, ?, ?, ?, ?, 'ACTIVE')
                    """,
                    (agent_id, name, agent_type, capabilities, allowed_tools),
                )
                await db.commit()
                msg = f"Agent {agent_id} registered"

        return f"SUCCESS: {msg}"
    except Exception as e:
        return f"ERROR: {e!s}"


async def get_agents(status: str | None = None) -> str:
    """
    Get registered agents.

    Args:
        status: Filter by status (ACTIVE, IDLE, OFFLINE). If None, returns all.

    Returns:
        JSON string with list of agents
    """
    try:
        import aiosqlite

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"

        async with aiosqlite.connect(db_path) as db:
            if status:
                async with db.execute(
                    "SELECT * FROM agents WHERE status = ? ORDER BY last_heartbeat DESC", (status,)
                ) as cursor:
                    rows = await cursor.fetchall()
            else:
                async with db.execute("SELECT * FROM agents ORDER BY last_heartbeat DESC") as cursor:
                    rows = await cursor.fetchall()

        agents = []
        for row in rows:
            agent = {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "capabilities": row[3],
                "allowed_tools": row[4],
                "status": row[5],
                "last_heartbeat": row[6],
            }
            agents.append(agent)

        return json.dumps({"agents": agents, "count": len(agents)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


async def agent_heartbeat(agent_id: str) -> str:
    """
    Update agent heartbeat timestamp.

    Args:
        agent_id: Agent identifier

    Returns:
        Success/failure message
    """
    try:
        import aiosqlite

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"

        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute(
                """
                UPDATE agents
                SET last_heartbeat = CURRENT_TIMESTAMP, status = 'ACTIVE'
                WHERE id = ?
                """,
                (agent_id,),
            )
            await db.commit()

            if cursor.rowcount == 0:
                return f"ERROR: Agent {agent_id} not found. Please register first."

        return f"SUCCESS: Heartbeat updated for {agent_id}"
    except Exception as e:
        return f"ERROR: {e!s}"

