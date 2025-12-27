"""
YBIS MCP SERVER
Exposes YBIS Skills (Spec Writer, etc.) to the world via Model Context Protocol.
"""

import sys
import os
import asyncio
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add project root to path
sys.path.insert(0, os.getcwd())

from mcp.server.fastmcp import FastMCP
from src.agentic.skills.spec_writer import generate_spec, SpecWriterInput
from src.agentic.infrastructure.graph_db import GraphDB
from src.agentic.bridges.council_bridge import CouncilBridge

# Initialize Server
mcp = FastMCP("YBIS Factory Skills")

# Database path
DB_PATH = "Knowledge/LocalDB/tasks.db"

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

@mcp.tool()
def get_tasks(status: Optional[str] = None, assignee: Optional[str] = None) -> str:
    """
    Get tasks from YBIS task database.

    Args:
        status: Filter by status (BACKLOG, IN_PROGRESS, COMPLETED, FAILED). If None, returns all.
        assignee: Filter by assignee. If None, returns all.

    Returns:
        JSON string with list of tasks.
    """
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT id, goal, details, status, priority, assignee FROM tasks WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if assignee:
        query += " AND assignee = ?"
        params.append(assignee)

    query += " ORDER BY priority DESC, id"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    tasks = [dict(row) for row in rows]
    conn.close()

    return json.dumps({"tasks": tasks, "count": len(tasks)}, indent=2)

@mcp.tool()
def claim_task(task_id: str, agent_id: str) -> str:
    """
    Claim a task atomically from BACKLOG.

    Args:
        task_id: Task ID to claim
        agent_id: Agent claiming the task

    Returns:
        Success/failure message
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if task exists and is available
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

        if not row:
            return f"ERROR: Task {task_id} not found"

        if row[0] != "BACKLOG":
            return f"ERROR: Task {task_id} is already {row[0]}"

        # Atomic claim
        cursor.execute("""
            UPDATE tasks
            SET status = 'IN_PROGRESS', assignee = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'BACKLOG'
        """, (agent_id, task_id))

        conn.commit()

        if cursor.rowcount == 0:
            return f"ERROR: Task {task_id} was claimed by another agent"

        return f"SUCCESS: Task {task_id} claimed by {agent_id}"

    finally:
        conn.close()

@mcp.tool()
def claim_next_task(agent_id: str) -> str:
    """
    Claim the next available BACKLOG task (atomic).

    Args:
        agent_id: Agent claiming the task

    Returns:
        JSON string with claimed task or message when empty.
    """
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute("""
            SELECT id, goal, details, status, priority, assignee
            FROM tasks
            WHERE status = 'BACKLOG'
            ORDER BY
                CASE priority
                    WHEN 'HIGH' THEN 1
                    WHEN 'MEDIUM' THEN 2
                    ELSE 3
                END,
                id
            LIMIT 1
        """)
        row = cursor.fetchone()

        if not row:
            conn.rollback()
            return json.dumps({"task": None, "message": "No BACKLOG tasks available"}, indent=2)

        task_id = row["id"]
        cursor.execute("""
            UPDATE tasks
            SET status = 'IN_PROGRESS', assignee = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'BACKLOG'
        """, (agent_id, task_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return json.dumps({"task": None, "message": "Task was claimed by another agent"}, indent=2)

        conn.commit()

        task = dict(row)
        task["status"] = "IN_PROGRESS"
        task["assignee"] = agent_id
        return json.dumps({"task": task}, indent=2)

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return json.dumps({"error": str(e)}, indent=2)
    finally:
        conn.close()

@mcp.tool()
def update_task_status(task_id: str, status: str, final_status: Optional[str] = None) -> str:
    """
    Update task status.

    Args:
        task_id: Task ID
        status: New status (BACKLOG, IN_PROGRESS, COMPLETED, FAILED)
        final_status: Optional final status for completed/failed tasks

    Returns:
        Success/failure message
    """
    valid_statuses = ["BACKLOG", "IN_PROGRESS", "COMPLETED", "FAILED"]

    if status not in valid_statuses:
        return f"ERROR: Invalid status '{status}'. Must be one of {valid_statuses}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if final_status:
            cursor.execute("""
                UPDATE tasks
                SET status = ?, final_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, final_status, task_id))
        else:
            cursor.execute("""
                UPDATE tasks
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, task_id))

        conn.commit()

        if cursor.rowcount == 0:
            return f"ERROR: Task {task_id} not found"

        return f"SUCCESS: Task {task_id} updated to {status}"

    finally:
        conn.close()

@mcp.tool()
def register_agent(agent_id: str, name: str, agent_type: str, capabilities: Optional[str] = None, allowed_tools: Optional[str] = None) -> str:
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
    import json

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if agent already exists
        cursor.execute("SELECT id FROM agents WHERE id = ?", (agent_id,))
        existing = cursor.fetchone()

        if existing:
            # Update existing agent
            cursor.execute("""
                UPDATE agents
                SET name = ?, type = ?, capabilities = ?, allowed_tools = ?,
                    last_heartbeat = CURRENT_TIMESTAMP, status = 'ACTIVE'
                WHERE id = ?
            """, (name, agent_type, capabilities, allowed_tools, agent_id))
            msg = f"Agent {agent_id} updated"
        else:
            # Insert new agent
            cursor.execute("""
                INSERT INTO agents (id, name, type, capabilities, allowed_tools, status)
                VALUES (?, ?, ?, ?, ?, 'ACTIVE')
            """, (agent_id, name, agent_type, capabilities, allowed_tools))
            msg = f"Agent {agent_id} registered"

        conn.commit()
        return f"SUCCESS: {msg}"

    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def get_agents(status: Optional[str] = None) -> str:
    """
    Get registered agents.

    Args:
        status: Filter by status (ACTIVE, IDLE, OFFLINE). If None, returns all.

    Returns:
        JSON string with list of agents
    """
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if status:
        cursor.execute("SELECT * FROM agents WHERE status = ? ORDER BY last_heartbeat DESC", (status,))
    else:
        cursor.execute("SELECT * FROM agents ORDER BY last_heartbeat DESC")

    rows = cursor.fetchall()
    agents = [dict(row) for row in rows]
    conn.close()

    return json.dumps({"agents": agents, "count": len(agents)}, indent=2)

@mcp.tool()
def agent_heartbeat(agent_id: str) -> str:
    """
    Update agent heartbeat timestamp.

    Args:
        agent_id: Agent identifier

    Returns:
        Success/failure message
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE agents
            SET last_heartbeat = CURRENT_TIMESTAMP, status = 'ACTIVE'
            WHERE id = ?
        """, (agent_id,))

        conn.commit()

        if cursor.rowcount == 0:
            return f"ERROR: Agent {agent_id} not found. Please register first."

        return f"SUCCESS: Heartbeat updated for {agent_id}"

    finally:
        conn.close()

@mcp.tool()
def check_dependency_impact(file_path: str, max_depth: int = 3) -> str:
    """
    Check what breaks if you modify this file.

    Args:
        file_path: Path to file to analyze (e.g., 'src/config.py')
        max_depth: Maximum dependency depth to analyze (default: 3)

    Returns:
        Impact analysis report with affected files
    """
    try:
        # Check if Neo4j is available
        try:
            from neo4j.exceptions import ServiceUnavailable
        except ImportError:
            return "[ERROR] Neo4j driver not installed. Run: pip install neo4j\n\nThis tool requires Neo4j for dependency tracking."

        with GraphDB() as db:
            # Get impact
            affected = db.impact_analysis(file_path, max_depth)

            if not affected:
                return f"[SAFE] No dependencies found on {file_path}\n\nThis file can be modified with minimal risk."

            # Build report
            report = f"[WARNING] {len(affected)} files will be affected if you modify {file_path}:\n\n"

            # Group by distance
            by_distance = {}
            for item in affected:
                dist = item['distance']
                if dist not in by_distance:
                    by_distance[dist] = []
                by_distance[dist].append(item)

            for dist in sorted(by_distance.keys()):
                report += f"\nDistance {dist} (direct dependents):\n"
                for item in by_distance[dist][:10]:  # Limit to 10 per distance
                    report += f"  - {item['path']} ({item['type']})\n"

                if len(by_distance[dist]) > 10:
                    report += f"  ... and {len(by_distance[dist]) - 10} more\n"

            # Risk assessment
            if len(affected) > 20:
                report += "\n[HIGH RISK] This is a critical file with many dependents!"
            elif len(affected) > 10:
                report += "\n[MEDIUM RISK] Careful - multiple files depend on this."
            else:
                report += "\n[LOW RISK] Limited impact - proceed with caution."

            return report

    except Exception as e:
        error_msg = str(e)
        if "ServiceUnavailable" in str(type(e)) or "Failed to establish connection" in error_msg:
            return "[ERROR] Neo4j is not running or unreachable.\n\nStart Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
        return f"[ERROR] Failed to analyze dependencies: {error_msg}\n\nMake sure Neo4j is running and graph has been populated:\n  python scripts/ingest_graph.py"

@mcp.tool()
def find_circular_dependencies() -> str:
    """
    Find circular dependency chains in the codebase.

    Returns:
        List of circular dependency cycles
    """
    try:
        # Check if Neo4j is available
        try:
            from neo4j.exceptions import ServiceUnavailable
        except ImportError:
            return "[ERROR] Neo4j driver not installed. Run: pip install neo4j\n\nThis tool requires Neo4j for dependency tracking."

        with GraphDB() as db:
            cycles = db.find_circular_dependencies()

            if not cycles:
                return "[OK] No circular dependencies found!"

            report = f"[WARNING] Found {len(cycles)} circular dependency chains:\n\n"

            for i, cycle in enumerate(cycles[:10], 1):  # Limit to 10
                report += f"{i}. Cycle length {len(cycle)}:\n"
                for file in cycle:
                    report += f"   -> {file}\n"
                report += "\n"

            if len(cycles) > 10:
                report += f"... and {len(cycles) - 10} more cycles\n"

            report += "\n[ACTION] Break these cycles to improve code maintainability."

            return report

    except Exception as e:
        error_msg = str(e)
        if "ServiceUnavailable" in str(type(e)) or "Failed to establish connection" in error_msg:
            return "[ERROR] Neo4j is not running or unreachable.\n\nStart Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
        return f"[ERROR] {error_msg}"

@mcp.tool()
def get_critical_files(limit: int = 10) -> str:
    """
    Get files with the most dependents (high-risk files).

    Args:
        limit: Maximum number of files to return (default: 10)

    Returns:
        List of critical files ranked by number of dependents
    """
    try:
        # Check if Neo4j is available
        try:
            from neo4j.exceptions import ServiceUnavailable
        except ImportError:
            return "[ERROR] Neo4j driver not installed. Run: pip install neo4j\n\nThis tool requires Neo4j for dependency tracking."

        with GraphDB() as db:
            critical = db.get_critical_nodes(min_dependents=3, limit=limit)

            if not critical:
                return "[INFO] No critical nodes found (all files have < 3 dependents)"

            report = f"[CRITICAL FILES] Top {len(critical)} files with most dependents:\n\n"

            for i, node in enumerate(critical, 1):
                report += f"{i}. {node['path']}\n"
                report += f"   Type: {node['type']}\n"
                report += f"   Dependents: {node['dependents']}\n"
                report += f"   [RISK] Changing this affects {node['dependents']} other files!\n\n"

            report += "[WARNING] These files are infrastructure - changes here have wide impact."

            return report

    except Exception as e:
        error_msg = str(e)
        if "ServiceUnavailable" in str(type(e)) or "Failed to establish connection" in error_msg:
            return "[ERROR] Neo4j is not running or unreachable.\n\nStart Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
        return f"[ERROR] {error_msg}"

# --- MESSAGING TOOLS ---

def _debate_archive_dir() -> str:
    base = os.path.join("Knowledge", "Messages", "debates")
    os.makedirs(base, exist_ok=True)
    return base

def _write_debate(debate_id: str, topic: str, initiator: str, proposal: str) -> None:
    payload = {
        "id": debate_id,
        "topic": topic,
        "initiator": initiator,
        "proposal": proposal,
        "messages": [],
        "status": "open",
        "started_at": datetime.now().isoformat()
    }
    path = os.path.join(_debate_archive_dir(), f"{debate_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def _append_debate_message(debate_id: str, agent_id: str, content: str) -> bool:
    path = os.path.join(_debate_archive_dir(), f"{debate_id}.json")
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        debate = json.load(f)
    debate["messages"].append(
        {
            "from": agent_id,
            "timestamp": datetime.now().isoformat(),
            "content": content
        }
    )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(debate, f, indent=2)
    return True

@mcp.tool()
def send_message(to: str, subject: str, content: str, from_agent: str = "mcp-client",
                 message_type: str = "direct", priority: str = "NORMAL",
                 reply_to: Optional[str] = None, tags: Optional[str] = None) -> str:
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
    import json
    from datetime import datetime

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Generate message ID
        msg_id = f"MSG-{from_agent}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Parse tags
        tags_list = [t.strip() for t in tags.split(",")] if tags else []

        # Insert into messages table
        cursor.execute("""
            INSERT INTO messages
            (id, from_agent, to_agent, type, subject, content, reply_to, priority, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            msg_id,
            from_agent,
            to,
            message_type,
            subject,
            content,
            reply_to,
            priority,
            json.dumps(tags_list),
            json.dumps({})
        ))

        conn.commit()

        return f"SUCCESS: Message sent. ID: {msg_id}"

    except Exception as e:
        return f"ERROR: Failed to send message: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def start_debate(topic: str, proposal: str, agent_id: str = "mcp-client") -> str:
    """
    Start a debate: archive in Knowledge/Messages/debates and broadcast via MCP.
    """
    import json
    from datetime import datetime

    debate_id = f"DEBATE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        _write_debate(debate_id, topic, agent_id, proposal)
        send_message(
            to="all",
            subject=debate_id,
            content=f"Debate started: {debate_id}\nTopic: {topic}\n\n{proposal}",
            from_agent=agent_id,
            message_type="debate",
            priority="HIGH",
            reply_to=None,
            tags="debate"
        )
        return f"SUCCESS: Debate started. ID: {debate_id}"
    except Exception as e:
        return f"ERROR: Failed to start debate: {str(e)}"

@mcp.tool()
def ask_council(
    question: str,
    agent_id: str = "mcp-client",
    use_local: bool = False,
    return_stages: bool = False
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
        # Initialize council bridge
        bridge = CouncilBridge(use_local=use_local)

        # Get consensus
        result = bridge.ask_council(question, return_stages=return_stages)

        # Format response
        if result.get("error"):
            return f"COUNCIL ERROR: {result.get('answer', 'Unknown error')}"

        response = f"COUNCIL CONSENSUS:\n{result['answer']}"

        # Add stage details if requested
        if return_stages and 'stage1' in result:
            response += f"\n\n[Deliberation involved {len(result['stage1'])} models"
            response += f" with {len(result['stage2'])} peer reviews]"

        # Log council usage
        send_message(
            to="all",
            subject=f"Council Consulted by {agent_id}",
            content=f"Question: {question}\n\nDecision: {result['answer'][:200]}...",
            from_agent=agent_id,
            message_type="direct",
            priority="NORMAL",
            tags="council,decision"
        )

        return response

    except Exception as e:
        return f"COUNCIL ERROR: Failed to get consensus: {str(e)}\n(Ensure council backend is accessible and API key is set if needed)"

@mcp.tool()
def reply_to_debate(debate_id: str, content: str, agent_id: str = "mcp-client") -> str:
    """
    Reply to a debate: append to archive and notify via MCP.
    """
    try:
        if not _append_debate_message(debate_id, agent_id, content):
            return f"ERROR: Debate {debate_id} not found"
        send_message(
            to="all",
            subject=debate_id,
            content=f"Reply from {agent_id}:\n\n{content}",
            from_agent=agent_id,
            message_type="debate",
            priority="NORMAL",
            reply_to=None,
            tags="debate"
        )
        return f"SUCCESS: Reply posted to {debate_id}"
    except Exception as e:
        return f"ERROR: Failed to reply to debate: {str(e)}"

@mcp.tool()
def read_inbox(agent_id: str, status: Optional[str] = None, limit: int = 50) -> str:
    """
    Read messages from inbox for a specific agent.

    Args:
        agent_id: Agent ID to read messages for
        status: Filter by status (unread, read, archived). If None, returns all.
        limit: Maximum number of messages to return (default: 50)

    Returns:
        JSON string with list of messages
    """
    import json

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
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

        cursor.execute(query, params)
        rows = cursor.fetchall()

        messages = []
        for row in rows:
            msg = dict(row)
            # Parse JSON fields
            if msg.get('tags'):
                try:
                    msg['tags'] = json.loads(msg['tags'])
                except:
                    msg['tags'] = []
            messages.append(msg)

        return json.dumps({
            "agent_id": agent_id,
            "messages": messages,
            "count": len(messages)
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conn.close()

@mcp.tool()
def ack_message(message_id: str, agent_id: str, action: str = "noted") -> str:
    """
    Acknowledge a message (mark as read and add acknowledgment).

    Args:
        message_id: Message ID to acknowledge
        agent_id: Agent acknowledging the message
        action: Acknowledgment action (noted, will_do, done, rejected)

    Returns:
        Success/failure message
    """
    import json

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get current message
        cursor.execute("SELECT seen_by, metadata FROM messages WHERE id = ?", (message_id,))
        row = cursor.fetchone()

        if not row:
            return f"ERROR: Message {message_id} not found"

        # Update seen_by list
        seen_by = json.loads(row[0]) if row[0] else []
        if agent_id not in seen_by:
            seen_by.append(agent_id)

        # Update metadata with ack
        metadata = json.loads(row[1]) if row[1] else {}
        if 'ack_by' not in metadata:
            metadata['ack_by'] = {}
        metadata['ack_by'][agent_id] = action

        # Update message
        cursor.execute("""
            UPDATE messages
            SET status = 'read',
                seen_by = ?,
                metadata = ?
            WHERE id = ?
        """, (json.dumps(seen_by), json.dumps(metadata), message_id))

        conn.commit()

        return f"SUCCESS: Message {message_id} acknowledged by {agent_id} ({action})"

    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        conn.close()

# --- MEMORY TOOLS (Cognee Integration) ---

@mcp.tool()
def add_to_memory(
    data: str,
    agent_id: str = "mcp-client",
    metadata: Optional[str] = None
) -> str:
    """
    Add information to the system's persistent memory (Cognee).

    This stores data in a graph+vector hybrid database for later retrieval.
    Use this to remember important information, decisions, or learnings.

    Args:
        data: The information to store (text)
        agent_id: ID of agent adding the memory
        metadata: Optional JSON string with metadata

    Returns:
        Success message or error

    Example:
        add_to_memory("We decided to use Cognee for memory because it integrates with Neo4j")
    """
    try:
        import cognee
        import asyncio
        import os

        # Configure Cognee for Neo4j
        os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
        os.environ['GRAPH_DATABASE_URL'] = 'bolt://localhost:7687'
        os.environ['GRAPH_DATABASE_USERNAME'] = 'neo4j'
        os.environ['GRAPH_DATABASE_PASSWORD'] = 'ybis-graph-2025'
        os.environ['ENABLE_BACKEND_ACCESS_CONTROL'] = 'false'

        # Add to memory (async)
        async def add_async():
            await cognee.add(data)
            await cognee.cognify()

        asyncio.run(add_async())

        # Log memory addition
        send_message(
            to="all",
            subject=f"Memory Added by {agent_id}",
            content=f"Added to system memory:\n\n{data[:200]}...",
            from_agent=agent_id,
            message_type="direct",
            priority="LOW",
            tags="memory,learning"
        )

        return f"SUCCESS: Memory added and indexed. {len(data)} characters stored."

    except Exception as e:
        return f"MEMORY ERROR: Failed to add memory: {str(e)}\n(Ensure Cognee is configured and Neo4j is accessible)"

@mcp.tool()
def search_memory(
    query: str,
    agent_id: str = "mcp-client",
    limit: int = 5
) -> str:
    """
    Search the system's persistent memory for relevant information.

    Uses hybrid graph+vector search to find related memories.

    Args:
        query: Search query (question or keywords)
        agent_id: ID of agent searching
        limit: Maximum number of results

    Returns:
        Search results or error

    Example:
        search_memory("What did we decide about memory systems?")
    """
    try:
        import cognee
        import asyncio
        import os

        # Configure Cognee
        os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
        os.environ['GRAPH_DATABASE_URL'] = 'bolt://localhost:7687'
        os.environ['GRAPH_DATABASE_USERNAME'] = 'neo4j'
        os.environ['GRAPH_DATABASE_PASSWORD'] = 'ybis-graph-2025'
        os.environ['ENABLE_BACKEND_ACCESS_CONTROL'] = 'false'

        # Search memory (async)
        async def search_async():
            return await cognee.search(query, limit=limit)

        results = asyncio.run(search_async())

        if not results or len(results) == 0:
            return f"MEMORY: No results found for: {query}"

        # Format results
        response = f"MEMORY SEARCH RESULTS ({len(results)} found):\n\n"
        for i, result in enumerate(results, 1):
            # Handle different result formats
            if isinstance(result, dict):
                content = result.get('content', result.get('text', str(result)))
            elif isinstance(result, str):
                content = result
            else:
                content = str(result)

            response += f"{i}. {content[:300]}\n\n"

        return response

    except Exception as e:
        return f"MEMORY ERROR: Failed to search memory: {str(e)}\n(Ensure Cognee is configured and has data)"

# --- ENTRY POINT ---
if __name__ == "__main__":
    print("🚀 YBIS MCP Server Starting...")
    mcp.run()
