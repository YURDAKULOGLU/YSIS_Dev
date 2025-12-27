# YBIS Tools & Systems Reference

Complete reference for all agents. Last updated: 2025-12-27

## MCP Server Tools (src/agentic/mcp_server.py)

### Task Management (5 tools)

**get_tasks(status, assignee)**
- List tasks from tasks.db
- Filter by status (BACKLOG, IN_PROGRESS, COMPLETED)
- Filter by assignee

**claim_task(task_id, agent_id)**
- Atomically claim a task
- Prevents race conditions
- Updates status to IN_PROGRESS

**update_task_status(task_id, status, final_status)**
- Update task status
- Valid: BACKLOG, IN_PROGRESS, COMPLETED, FAILED
- Optional final_status for completion notes

**create_spec_kit(project_name, description, tech_stack)**
- Generate technical specification
- Auto-creates Architecture, API, Schema docs

**hello_world()**
- Ping check
- Verify MCP server is online

### Messaging (3 tools)

**send_message(to, subject, content, from_agent, message_type, priority, reply_to, tags)**
- Send message via MCP
- to: agent ID or "all"
- priority: CRITICAL, HIGH, NORMAL, LOW
- message_type: direct, broadcast, debate, task_assignment
- Stored in SQLite messages table

**read_inbox(agent_id, status, limit)**
- Read messages for agent
- Filter by status (unread, read, archived)
- Returns JSON with message list

**ack_message(message_id, agent_id, action)**
- Acknowledge message
- action: noted, will_do, done, rejected
- Updates seen_by and metadata

### Agent Coordination (3 tools)

**register_agent(agent_id, name, agent_type, capabilities, allowed_tools)**
- Register new agent in system
- Creates entry in agents table
- Auto-creates agents/{agent_id}/ folder (future)

**get_agents(status)**
- List registered agents
- Filter by status (ACTIVE, IDLE, OFFLINE)
- Returns capabilities and last_heartbeat

**agent_heartbeat(agent_id)**
- Keep-alive signal
- Updates last_heartbeat timestamp
- Agents >10min without heartbeat marked IDLE

### Neo4j Dependency Analysis (3 tools)

**check_dependency_impact(file_path, max_depth)**
- CRITICAL: Check before modifying any file
- Shows what will break
- Returns affected files with distance
- Risk assessment (LOW/MEDIUM/HIGH)

**find_circular_dependencies()**
- Detect import cycles
- Returns list of circular chains
- Helps prevent architectural debt

**get_critical_files(limit)**
- Files with most dependents
- High-risk infrastructure files
- Changing these affects many files

## Database Systems

### SQLite (Knowledge/LocalDB/tasks.db)

**Tables:**
- tasks: id, goal, details, status, priority, assignee, final_status, metadata
- agents: id, name, type, capabilities, status, last_heartbeat, allowed_tools
- messages: id, from_agent, to_agent, type, subject, content, priority, tags, seen_by

**CLI Access:**
```bash
sqlite3 Knowledge/LocalDB/tasks.db "SELECT * FROM tasks WHERE status='BACKLOG'"
```

### Neo4j Graph (bolt://neo4j:7687)

**Nodes:**
- CodeFile (88 indexed)
- DocFile (52 indexed)
- Function (193)
- Class (78)

**Relationships:**
- IMPORTS (3)
- DEFINES (272)
- REFERENCES (doc->code links)

**Access:**
```python
from src.agentic.infrastructure.graph_db import GraphDB
with GraphDB() as db:
    impact = db.impact_analysis("src/config.py")
```

**Browser UI:** http://localhost:7474
**Credentials:** neo4j / ybis-graph-2025

### Redis (redis://redis:6379)

**Purpose:**
- Real-time messaging (future)
- Pub/sub channels (future)
- Cache (future)

**Status:** Infrastructure ready, not fully utilized yet

## Docker Services (docker-compose.yml)

**redis** - Port 6379
- Alpine image
- Healthcheck: redis-cli ping

**neo4j** - Ports 7474, 7687
- Community 5.15
- APOC + GDS plugins
- 2GB heap, 512M pagecache

**worker** - Background worker
- Python execution environment
- Access to Ollama (host.docker.internal:11434)

**dashboard** - Port 8501
- Streamlit dashboard
- Connected to all services

**viz** - Port 3000
- Standalone React app
- Vite + Sigma.js
- Graph visualization

**Start services:**
```bash
docker-compose up -d
docker-compose ps
```

## File-Based Systems

### Debates (Knowledge/Messages/debates/)
- JSON files: DEBATE-{timestamp}.json
- Structure: id, topic, initiator, proposal, messages[], status
- Start: `python scripts/ybis.py debate start --topic "..." --proposal "..." --agent your-id`
- Reply: `python scripts/ybis.py message send --type debate --subject DEBATE-XXX --content "..." --from your-id`

### Tasks (workspaces/active/)
- Each task gets: workspaces/active/TASK-ID/
- Contains: docs/PLAN.md, docs/RUNBOOK.md, artifacts/RESULT.md
- Frontmatter standard (YAML headers)

### Documentation (agents/, docs/)
- agents/ - Agent-specific onboarding
- docs/specs/ - System specifications
- docs/governance/ - Policies and principles

## CLI Tools

### scripts/ybis.py (Unified CLI)
```bash
# Task management
ybis.py list --status BACKLOG
ybis.py claim TASK-ID
ybis.py complete TASK-ID

# Messaging (NEW - MCP-based)
ybis.py message send --to all --subject "..." --content "..."
ybis.py message read
ybis.py message ack MSG-ID --action will_do

# Workspace
ybis.py workspace TASK-ID
```

### scripts/register_agent.py
```bash
python scripts/register_agent.py \
    --id agent-name \
    --name "Display Name" \
    --type cli \
    --capabilities "python,react,docker"
```

### scripts/ingest_graph.py
```bash
# Populate Neo4j graph
python scripts/ingest_graph.py

# Scans:
# - src/**/*.py (88 CodeFiles)
# - docs/**/*.md (52 DocFiles)
```

## Agent Capabilities Quick Reference

### Claude (Infrastructure Lead)
**Strong:** Python, Docker, Neo4j, MCP, SQLite, Backend
**Delegate:** Frontend→Codex, Strategy→Gemini

### Gemini (System Architect)
**Strong:** Architecture, Strategic Planning, Debate Facilitation, Analysis
**Delegate:** All Implementation→Claude/Codex

### Codex (Frontend Specialist)
**Strong:** React, TypeScript, Vite, Docs, Testing, Visualization
**Delegate:** Backend→Claude, Strategy→Gemini

## Common Workflows

### Before Modifying Code
```python
# ALWAYS check impact first
impact = check_dependency_impact("src/file.py")
if "HIGH RISK" in impact:
    # Start debate or get approval
```

### Claiming Work
```bash
# 1. List available
ybis.py list --status BACKLOG

# 2. Claim atomically
ybis.py claim TASK-ID

# 3. Work in workspace
cd workspaces/active/TASK-ID/

# 4. Complete
ybis.py complete TASK-ID
```

### Sending Messages
```bash
# Direct message
ybis.py message send --to gemini-cli \
    --subject "Question" \
    --content "Need architecture review"

# Broadcast
ybis.py message send --to all \
    --subject "Update" \
    --content "Task complete"

# Read inbox
ybis.py message read

# Acknowledge
ybis.py message ack MSG-123 --action will_do
```

### Starting Debates
```bash
python scripts/ybis.py debate start \
  --topic "Clear question" \
  --proposal "Context + Options A/B/C" \
  --agent your-agent-id
```

## Environment Variables

**Neo4j:**
- NEO4J_URI=bolt://neo4j:7687
- NEO4J_USER=neo4j
- NEO4J_PASSWORD=ybis-graph-2025

**Redis:**
- REDIS_HOST=redis

**Ollama:**
- OLLAMA_API_BASE=http://host.docker.internal:11434

## Troubleshooting

**MCP server down:**
- Check: src/agentic/mcp_server.py logs
- Restart: (no daemon mode yet - run manually)

**Neo4j offline:**
```bash
docker-compose up neo4j -d
docker logs ybis-neo4j
```

**Tasks.db locked:**
- SQLite doesn't support concurrent writes well
- Use MCP tools (they handle locking)
- Avoid direct SQL writes

**Message not delivered:**
- Check agent registry: get_agents()
- Verify recipient is ACTIVE
- Check messages table for status

---

**Last Updated:** 2025-12-27 by Claude Code
**Auto-generated:** No (manual for now)
**Future:** Auto-sync with actual MCP tools
