# Universal Agent Protocol - Migration Guide

**Version:** 1.0
**Date:** 2025-12-27
**Status:** PRODUCTION READY

---

## Overview

The YBIS system has been upgraded with the Universal Agent Protocol (UAP), enabling seamless multi-agent collaboration through standardized interfaces.

## What Changed

### New Infrastructure

1. **MCP Server** (`src/agentic/mcp_server.py`)
   - 8 standardized tools for agent operations
   - Direct task and agent management
   - MCP protocol compliance

2. **Agent Registry** (`agents` table in `tasks.db`)
   - Centralized agent discovery
   - Capability tracking
   - Health monitoring via heartbeat

3. **Enhanced Messaging** (`scripts/ybis.py message`)
   - MCP-backed CLI messaging
   - Supports send/read/ack
   - No manual JSON editing

4. **Redis Listener** (`scripts/listen.py`)
   - Real-time event processing
   - Multi-channel support: ybis-events, tasks, system

---

## Migration Steps

### For External CLI Agents (Claude Code, Gemini CLI, etc.)

#### Step 1: Register Your Agent

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from agentic.mcp_server import register_agent
import json

register_agent(
    agent_id='your-agent-id',
    name='Your Agent Name',
    agent_type='external_cli',
    capabilities=json.dumps(['capability1', 'capability2']),
    allowed_tools=json.dumps(['get_tasks', 'claim_task'])
)
"
```

#### Step 2: Use MCP Tools Instead of Direct DB Access

**OLD WAY (Deprecated):**
```python
import sqlite3
conn = sqlite3.connect('Knowledge/LocalDB/tasks.db')
# Manual SQL queries...
```

**NEW WAY (Recommended):**
```python
from agentic.mcp_server import get_tasks, claim_task, update_task_status
import json

# Get available tasks
tasks = json.loads(get_tasks(status='BACKLOG'))

# Claim a task
result = claim_task('TASK-001', 'your-agent-id')

# Update progress
update_task_status('TASK-001', 'COMPLETED', 'SUCCESS')
```

#### Step 3: Use ybis.py for Messaging

**OLD WAY (Deprecated):**
```python
# Manual JSON file creation in Knowledge/Messages/inbox/
```

**NEW WAY (Recommended):**
```bash
# Send message
python scripts/ybis.py message send --to broadcast \
    --subject "Task Complete" \
    --content "Finished TASK-001" \
    --from your-agent-id

# Read messages
python scripts/ybis.py message read --agent your-agent-id

# Acknowledge message
python scripts/ybis.py message ack --id MSG-XXX --agent your-agent-id --action noted
```

#### Step 4: Send Periodic Heartbeats

```python
from agentic.mcp_server import agent_heartbeat

# Call every 5-10 minutes
agent_heartbeat('your-agent-id')
```

---

### For Internal Agents (Codex, Aider, etc.)

#### Step 1: Update Task Claiming

Replace direct SQL with MCP tools:

```python
# Before
cursor.execute("UPDATE tasks SET status='IN_PROGRESS', assignee=? WHERE id=?", (agent_id, task_id))

# After
from agentic.mcp_server import claim_task
claim_task(task_id, agent_id)
```

#### Step 2: Use Messaging API

```bash
# Send status update
python scripts/ybis.py message send --to broadcast \
  --subject "Task Progress" \
  --content "Working on TASK-001" \
  --from your-agent-id

# Reply to debate
python scripts/ybis.py message send --to all \
  --type debate \
  --subject DEBATE-XXX \
  --content "My position..." \
  --from your-agent-id
```

---

## Available MCP Tools

### Task Management
- `get_tasks(status, assignee)` - Query tasks with filters
- `claim_task(task_id, agent_id)` - Atomic task claiming
- `update_task_status(task_id, status, final_status)` - Update progress

### Agent Registry
- `register_agent(agent_id, name, type, capabilities, allowed_tools)` - Register/update agent
- `get_agents(status)` - Discover other agents
- `agent_heartbeat(agent_id)` - Update health status

### Utilities
- `hello_world()` - Health check
- `create_spec_kit(project_name, description, tech_stack)` - Generate specs

### Messaging (MCP)
- `send_message(to, subject, content, from_agent, message_type, priority, reply_to, tags)`
- `read_inbox(agent_id, status, limit)`
- `ack_message(message_id, agent_id, action)`

## ybis.py Messaging (MCP)

Use the unified CLI instead of file-based tools:

```bash
# Send
python scripts/ybis.py message send --to broadcast \
  --subject "Update" \
  --content "Task finished." \
  --from your-agent-id

# Read
python scripts/ybis.py message read --agent your-agent-id

# Acknowledge
python scripts/ybis.py message ack --id MSG-XXX --agent your-agent-id --action noted
```
---

## Testing Your Migration

Run this test to verify your agent works with the new system:

```python
import sys
sys.path.insert(0, 'src')
from agentic.mcp_server import get_agents, agent_heartbeat
import json

# Test 1: Check if you're registered
agents = json.loads(get_agents())
your_agent = [a for a in agents['agents'] if a['id'] == 'your-agent-id']
assert len(your_agent) == 1, "Agent not registered!"

# Test 2: Send heartbeat
result = agent_heartbeat('your-agent-id')
assert 'SUCCESS' in result, "Heartbeat failed!"

print("Migration successful!")
```

---

## Breaking Changes

1. **File-based tasks are removed** - Use `tasks.db` only
2. **Manual JSON editing in Knowledge/Messages/ is PROHIBITED** - Use `scripts/ybis.py message`
3. **Direct SQLite writes for agents table require using MCP tools**

---

## Support

- **Questions:** Post in `DEBATE-20251227144126` (UAP debate)
- **Issues:** Send message to `broadcast` with type `question`
- **Documentation:** See `docs/MULTI_AGENT.md`

---

## Validation Checklist

- [ ] Agent registered in `agents` table
- [ ] Using MCP tools for task operations
- [ ] Using `scripts/ybis.py message` for messaging
- [ ] Sending periodic heartbeats
- [ ] No direct JSON file manipulation
- [ ] No legacy file-based task references

---

**Migration Deadline:** Immediate (system is production ready)
**Backward Compatibility:** Limited - old methods deprecated but functional for 1 week
