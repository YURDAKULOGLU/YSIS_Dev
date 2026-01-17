# MCP Tools Reference

**Version:** 1.0  
**Date:** 2026-01-08  
**Server:** `src/ybis/services/mcp_server.py`

This document provides a comprehensive reference for all MCP (Model Context Protocol) tools available in the YBIS platform.

---

## Table of Contents

1. [Task Management Tools](#task-management-tools)
2. [Artifact Management Tools](#artifact-management-tools)
3. [Messaging Tools](#messaging-tools)
4. [Debate Tools](#debate-tools)
5. [Dependency Analysis Tools](#dependency-analysis-tools)
6. [Memory Tools](#memory-tools)
7. [Agent Management Tools](#agent-management-tools)

---

## Task Management Tools

Tools for creating, managing, and tracking tasks.

### `task_create`

Create a new task in the system.

**Parameters:**
- `title` (string, required): Task title
- `objective` (string, required): Task objective/description
- `priority` (string, optional): Task priority. Options: `LOW`, `MEDIUM`, `HIGH`. Default: `MEDIUM`

**Returns:**
JSON string with task information:
```json
{
  "task_id": "T-abc12345",
  "title": "Task Title",
  "objective": "Task objective",
  "status": "pending",
  "priority": "MEDIUM"
}
```

**Example:**
```python
task_create(
    title="Implement user authentication",
    objective="Add login and registration functionality",
    priority="HIGH"
)
```

---

### `task_status`

Get task status and latest run information.

**Parameters:**
- `task_id` (string, required): Task identifier

**Returns:**
JSON string with task and run status:
```json
{
  "task_id": "T-abc12345",
  "title": "Task Title",
  "objective": "Task objective",
  "status": "running",
  "priority": "HIGH",
  "latest_run": {
    "run_id": "RUN-xyz67890",
    "status": "completed",
    "risk_level": "low"
  }
}
```

**Example:**
```python
task_status("T-abc12345")
```

---

### `get_tasks`

Get list of tasks with optional filtering.

**Parameters:**
- `status` (string, optional): Filter by status (`pending`, `running`, `completed`, `failed`). If not provided, returns all tasks.
- `limit` (integer, optional): Maximum number of tasks to return. Default: 50
- `offset` (integer, optional): Offset for pagination. Default: 0

**Returns:**
JSON string with list of tasks:
```json
{
  "tasks": [
    {
      "task_id": "T-abc12345",
      "title": "Task Title",
      "status": "running",
      "priority": "HIGH"
    }
  ],
  "count": 1
}
```

**Example:**
```python
get_tasks(status="running", limit=10)
```

---

### `claim_task`

Claim a task for execution (atomic operation).

**Parameters:**
- `task_id` (string, required): Task identifier
- `worker_id` (string, required): Worker/agent identifier claiming the task

**Returns:**
Success message with task and run information, or error message if task is already claimed.

**Example:**
```python
claim_task(task_id="T-abc12345", worker_id="worker-1")
```

---

### `claim_next_task`

Atomically claim the next available task.

**Parameters:**
- `worker_id` (string, required): Worker/agent identifier claiming the task
- `priority` (string, optional): Preferred priority (`LOW`, `MEDIUM`, `HIGH`). Default: `MEDIUM`

**Returns:**
Task information if available, or message indicating no tasks available.

**Example:**
```python
claim_next_task(worker_id="worker-1", priority="HIGH")
```

---

### `update_task_status`

Update task status.

**Parameters:**
- `task_id` (string, required): Task identifier
- `status` (string, required): New status (`pending`, `running`, `completed`, `failed`, `blocked`)
- `metadata` (string, optional): JSON string with additional metadata

**Returns:**
Success/failure message.

**Example:**
```python
update_task_status(
    task_id="T-abc12345",
    status="completed",
    metadata='{"notes": "Task completed successfully"}'
)
```

---

## Artifact Management Tools

Tools for reading and writing artifacts from runs.

### `artifact_read`

Read an artifact from a run.

**Parameters:**
- `task_id` (string, required): Task identifier
- `run_id` (string, required): Run identifier
- `artifact_name` (string, required): Artifact name (e.g., `plan.json`, `verifier_report.json`, `gate_report.json`)

**Returns:**
JSON string with artifact content:
```json
{
  "content": { /* parsed JSON if applicable */ },
  "raw": "/* raw content */"
}
```

**Example:**
```python
artifact_read(
    task_id="T-abc12345",
    run_id="RUN-xyz67890",
    artifact_name="plan.json"
)
```

---

### `artifact_write`

Write an artifact to a run's artifacts directory.

**Parameters:**
- `run_id` (string, required): Run identifier
- `name` (string, required): Artifact name (e.g., `executor_report.json`)
- `content` (string, required): Artifact content (string, can be JSON)

**Returns:**
JSON string with write confirmation:
```json
{
  "run_id": "RUN-xyz67890",
  "artifact_name": "executor_report.json",
  "artifact_path": "/path/to/artifact",
  "status": "written"
}
```

**Example:**
```python
artifact_write(
    run_id="RUN-xyz67890",
    name="executor_report.json",
    content='{"success": true, "files_changed": ["src/main.py"]}'
)
```

---

### `approval_write`

Write an approval record for a blocked run.

**Parameters:**
- `task_id` (string, required): Task identifier
- `run_id` (string, required): Run identifier
- `approver` (string, required): Approver identifier
- `reason` (string, required): Approval reason

**Returns:**
JSON string with approval confirmation:
```json
{
  "task_id": "T-abc12345",
  "run_id": "RUN-xyz67890",
  "approver": "admin",
  "status": "approved"
}
```

**Example:**
```python
approval_write(
    task_id="T-abc12345",
    run_id="RUN-xyz67890",
    approver="admin",
    reason="Changes are safe and necessary"
)
```

---

## Messaging Tools

Tools for inter-agent messaging and communication.

### `send_message`

Send a message to another agent via the unified messaging system.

**Parameters:**
- `to` (string, required): Recipient agent ID or `all` for broadcast
- `subject` (string, required): Message subject
- `content` (string, required): Message content (supports markdown)
- `from_agent` (string, optional): Sender agent ID. Default: `mcp-client`
- `message_type` (string, optional): Type of message. Options: `direct`, `broadcast`, `debate`, `task_assignment`. Default: `direct`
- `priority` (string, optional): Message priority. Options: `CRITICAL`, `HIGH`, `NORMAL`, `LOW`. Default: `NORMAL`
- `reply_to` (string, optional): Message ID being replied to
- `tags` (string, optional): Comma-separated tags

**Returns:**
Success message with message ID:
```
SUCCESS: Message sent. ID: MSG-mcp-client-20260108120000
```

**Example:**
```python
send_message(
    to="agent-1",
    subject="Task completed",
    content="Task T-abc12345 has been completed successfully.",
    from_agent="worker-1",
    priority="HIGH",
    tags="task,notification"
)
```

---

### `read_inbox`

Read messages from inbox for a specific agent.

**Parameters:**
- `agent_id` (string, required): Agent ID to read messages for
- `status` (string, optional): Filter by status (`unread`, `read`, `archived`). If `None`, returns all.
- `limit` (integer, optional): Maximum number of messages to return. Default: 50

**Returns:**
JSON string with list of messages:
```json
{
  "agent_id": "agent-1",
  "messages": [
    {
      "id": "MSG-123",
      "from_agent": "worker-1",
      "subject": "Task completed",
      "content": "Task completed...",
      "type": "direct",
      "priority": "HIGH",
      "timestamp": "2026-01-08T12:00:00",
      "status": "unread",
      "reply_to": null,
      "tags": ["task", "notification"]
    }
  ],
  "count": 1
}
```

**Example:**
```python
read_inbox(agent_id="agent-1", status="unread", limit=10)
```

---

### `ack_message`

Acknowledge a message (mark as read and add acknowledgment).

**Parameters:**
- `message_id` (string, required): Message ID to acknowledge
- `agent_id` (string, required): Agent acknowledging the message
- `action` (string, optional): Acknowledgment action. Options: `noted`, `will_do`, `done`, `rejected`. Default: `noted`

**Returns:**
Success/failure message:
```
SUCCESS: Message MSG-123 acknowledged by agent-1 (noted)
```

**Example:**
```python
ack_message(
    message_id="MSG-123",
    agent_id="agent-1",
    action="will_do"
)
```

---

## Debate Tools

Tools for debate system integration and council consultation.

### `start_debate`

Start a debate: archive in `platform_data/knowledge/Messages/debates` and broadcast via MCP.

**Parameters:**
- `topic` (string, required): Debate topic
- `proposal` (string, required): Initial proposal
- `agent_id` (string, optional): ID of agent starting the debate. Default: `mcp-client`

**Returns:**
Success message with debate ID:
```
SUCCESS: Debate started. ID: DEBATE-20260108120000
```

**Example:**
```python
start_debate(
    topic="Memory System Selection",
    proposal="Should we use Cognee or MemGPT for memory?",
    agent_id="architect"
)
```

---

### `reply_to_debate`

Reply to a debate: append to archive and notify via MCP.

**Parameters:**
- `debate_id` (string, required): Debate ID to reply to
- `content` (string, required): Reply content
- `agent_id` (string, optional): ID of agent replying. Default: `mcp-client`

**Returns:**
Success/failure message:
```
SUCCESS: Reply posted to DEBATE-20260108120000
```

**Example:**
```python
reply_to_debate(
    debate_id="DEBATE-20260108120000",
    content="I recommend Cognee because it integrates with Neo4j.",
    agent_id="engineer"
)
```

---

### `ask_council`

Ask the LLM Council for consensus decision on important questions.

Uses 3-stage deliberation:
- Stage 1: Multiple LLMs provide individual responses
- Stage 2: Anonymous peer review and ranking
- Stage 3: Chairman synthesizes final consensus

**Parameters:**
- `question` (string, required): The question to deliberate on
- `agent_id` (string, optional): ID of agent asking (for logging). Default: `mcp-client`
- `use_local` (boolean, optional): Use local Ollama models (`True`) or OpenRouter (`False`). Default: `False`
- `return_stages` (boolean, optional): Return full deliberation details (`True`) or just answer (`False`). Default: `False`

**Returns:**
Consensus answer from the council, or error message:
```
COUNCIL CONSENSUS:
[Consensus answer from the council]

[Deliberation involved 3 models with 2 peer reviews]  # if return_stages=True
```

**Example:**
```python
ask_council(
    question="Should we use Cognee or MemGPT for memory?",
    agent_id="architect",
    use_local=True,
    return_stages=False
)
```

**Note:** Requires `CouncilBridgeAdapter` to be implemented (Task D).

---

## Dependency Analysis Tools

Tools for code dependency analysis using graph database.

### `check_dependency_impact`

Check what breaks if you modify this file.

**Parameters:**
- `file_path` (string, required): Path to file to analyze (e.g., `src/config.py`)
- `max_depth` (integer, optional): Maximum dependency depth to analyze. Default: 3

**Returns:**
Impact analysis report with affected files:
```
[WARNING] 5 files will be affected if you modify src/config.py:

Distance 1 (direct dependents):
  - src/main.py (CodeFile)
  - src/utils.py (CodeFile)

Distance 2:
  - src/api.py (CodeFile)

[HIGH RISK] This is a critical file with many dependents!
```

**Example:**
```python
check_dependency_impact(
    file_path="src/config.py",
    max_depth=3
)
```

**Note:** Requires Neo4j graph adapter to be enabled in policy (`adapters.neo4j_graph.enabled: true`).

---

### `find_circular_dependencies`

Find circular dependency chains in the codebase.

**Parameters:**
None

**Returns:**
List of circular dependency cycles:
```
[WARNING] Found 2 circular dependency chains:

1. Cycle length 3:
   -> src/module_a.py
   -> src/module_b.py
   -> src/module_c.py
   -> src/module_a.py

[ACTION] Break these cycles to improve code maintainability.
```

**Example:**
```python
find_circular_dependencies()
```

**Note:** Requires Neo4j graph adapter to be enabled.

---

### `get_critical_files`

Get files with the most dependents (high-risk files).

**Parameters:**
- `limit` (integer, optional): Maximum number of files to return. Default: 10

**Returns:**
List of critical files ranked by number of dependents:
```
[CRITICAL FILES] Top 5 files with most dependents:

1. src/config.py
   Type: CodeFile
   Dependents: 15
   [RISK] Changing this affects 15 other files!

[WARNING] These files are infrastructure - changes here have wide impact.
```

**Example:**
```python
get_critical_files(limit=10)
```

**Note:** Requires Neo4j graph adapter to be enabled.

---

## Memory Tools

Tools for memory system integration using vector/graph adapters.

### `add_to_memory`

Add information to the system's persistent memory.

This stores data in a graph+vector hybrid database for later retrieval. Use this to remember important information, decisions, or learnings.

**Parameters:**
- `data` (string, required): The information to store (text)
- `agent_id` (string, optional): ID of agent adding the memory. Default: `mcp-client`
- `metadata` (string, optional): JSON string with metadata

**Returns:**
Success message or error:
```
SUCCESS: Memory added and indexed. 150 characters stored.
```

**Example:**
```python
add_to_memory(
    data="We decided to use Cognee for memory because it integrates with Neo4j",
    agent_id="architect",
    metadata='{"category": "decision", "importance": "high"}'
)
```

**Note:** Requires memory store adapter to be implemented (Task E).

---

### `search_memory`

Search the system's persistent memory for relevant information.

Uses hybrid graph+vector search to find related memories.

**Parameters:**
- `query` (string, required): Search query (question or keywords)
- `agent_id` (string, optional): ID of agent searching. Default: `mcp-client`
- `limit` (integer, optional): Maximum number of results. Default: 5

**Returns:**
Search results or error:
```
MEMORY SEARCH RESULTS (3 found):

1. We decided to use Cognee for memory because it integrates with Neo4j...

2. Previous decision: Use ChromaDB for vector storage...

3. Architecture decision: Neo4j for graph dependencies...
```

**Example:**
```python
search_memory(
    query="What did we decide about memory systems?",
    agent_id="planner",
    limit=5
)
```

**Note:** Requires memory store adapter to be implemented (Task E).

---

## Agent Management Tools

Tools for agent registration and heartbeat tracking.

### `register_agent`

Register an agent in the YBIS system.

**Parameters:**
- `agent_id` (string, required): Unique agent identifier (e.g., `claude-code`, `gemini-cli`)
- `name` (string, required): Human-readable agent name
- `agent_type` (string, required): Type of agent. Options: `cli`, `internal`, `external`, `mcp_client`
- `capabilities` (string, optional): JSON string of agent capabilities
- `allowed_tools` (string, optional): JSON string of allowed tools for this agent

**Returns:**
Success/failure message:
```
SUCCESS: Agent claude-code registered
```

**Example:**
```python
register_agent(
    agent_id="claude-code",
    name="Claude Code Assistant",
    agent_type="mcp_client",
    capabilities='["coding", "planning", "debugging"]',
    allowed_tools='["task_create", "artifact_read", "send_message"]'
)
```

---

### `get_agents`

Get registered agents.

**Parameters:**
- `status` (string, optional): Filter by status (`ACTIVE`, `IDLE`, `OFFLINE`). If `None`, returns all.

**Returns:**
JSON string with list of agents:
```json
{
  "agents": [
    {
      "id": "claude-code",
      "name": "Claude Code Assistant",
      "type": "mcp_client",
      "capabilities": "[\"coding\", \"planning\"]",
      "allowed_tools": "[\"task_create\", \"artifact_read\"]",
      "status": "ACTIVE",
      "last_heartbeat": "2026-01-08T12:00:00"
    }
  ],
  "count": 1
}
```

**Example:**
```python
get_agents(status="ACTIVE")
```

---

### `agent_heartbeat`

Update agent heartbeat timestamp.

**Parameters:**
- `agent_id` (string, required): Agent identifier

**Returns:**
Success/failure message:
```
SUCCESS: Heartbeat updated for claude-code
```

**Example:**
```python
agent_heartbeat("claude-code")
```

---

## Tool Categories Summary

| Category | Tools | Count |
|----------|-------|-------|
| Task Management | `task_create`, `task_status`, `get_tasks`, `claim_task`, `claim_next_task`, `update_task_status` | 6 |
| Artifact Management | `artifact_read`, `artifact_write`, `approval_write` | 3 |
| Messaging | `send_message`, `read_inbox`, `ack_message` | 3 |
| Debate | `start_debate`, `reply_to_debate`, `ask_council` | 3 |
| Dependency Analysis | `check_dependency_impact`, `find_circular_dependencies`, `get_critical_files` | 3 |
| Memory | `add_to_memory`, `search_memory` | 2 |
| Agent Management | `register_agent`, `get_agents`, `agent_heartbeat` | 3 |

**Total:** 23 tools

---

## Notes

1. **Adapter Requirements:** Some tools require specific adapters to be enabled in policy:
   - Dependency tools require `adapters.neo4j_graph.enabled: true`
   - Memory tools require memory store adapter (Task E)
   - Council tools require `CouncilBridgeAdapter` (Task D)

2. **Error Handling:** All tools return error messages in a consistent format when operations fail.

3. **JSON Responses:** Most tools return JSON strings for structured data. Parse with `json.loads()` in client code.

4. **Async Operations:** Some tools use async database operations internally but expose synchronous interfaces for MCP compatibility.

5. **Policy Gating:** Tool availability may be restricted by policy configuration. Check policy settings if tools are unavailable.

---

## See Also

- [MCP Server Implementation](../../src/ybis/services/mcp_server.py)
- [Adapter Registry Guide](../ADAPTER_REGISTRY_GUIDE.md)
- [Policy Configuration](../../configs/profiles/default.yaml)



