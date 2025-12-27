
# 🏗️ ARCHITECTURAL BLUEPRINT: Universal Agent Protocol (Phase 2 & 3)

**Author:** Gemini-CLI (The Architect)
**Status:** PROPOSAL / DRAFT
**Context:** Moving from File-based/MCP Baseline (Phase 1) to Real-time Coordination.

---

## 🛰️ PHASE 2: REDIS REAL-TIME LAYER (The Nervous System)

To prevent agents from stepping on each other's toes, we need a "Distributed Lock" and "Signal" system.

### 1. Channel Structure
-   `ybis:signals`: Ephemeral status updates (e.g., "Agent X is thinking...").
-   `ybis:locks`: Resource locking (e.g., "Agent Y is editing `src/core/main.py`").
-   `ybis:broadcast`: System-wide emergency or high-priority notifications.

### 2. Protocol: The "Pulse" Message
Every message in Redis must follow this strict schema:
```json
{
  "sender": "agent-id",
  "action": "LOCK | UNLOCK | SIGNAL | HEARTBEAT",
  "target": "file_path | task_id | null",
  "payload": {},
  "timestamp": "ISO8601"
}
```

---

## 🏛️ PHASE 3: AGENT REGISTRY & GATEWAY (The Governance)

### 1. The Registry (SQLite Based)
A new table in `tasks.db` called `agents`:
| Field | Type | Description |
|-------|------|-------------|
| id | TEXT (PK) | Unique agent ID (e.g., `claude-code`) |
| type | TEXT | `INTERNAL | EXTERNAL | CLI` |
| capabilities | JSON | List of MCP tools or skills |
| last_seen | TIMESTAMP | Heartbeat marker |
| status | TEXT | `IDLE | BUSY | OFFLINE` |

### 2. The REST Gateway (FastAPI)
For external tools (Cursor, Windsurf, etc.) that can't use MCP/Redis directly:
- `POST /v1/tasks/claim`: Atomic claim via API.
- `GET /v1/agents`: List active collaborators.
- `POST /v1/messages`: Bridge to internal messaging.

---

## 🚀 IMPLEMENTATION PRIORITY (Gemini's Verdict)

1.  **P0: The Registry Table.** We cannot coordinate if we don't know who is alive.
2.  **P1: Resource Locking.** Stop Aider and Claude from editing the same file simultaneously.
3.  **P2: REST Bridge.** Open the gates to non-CLI agents.

---

**Next Steps for Agents:**
- **Claude Code:** Review Phase 3 Gateway specs.
- **Codex:** Begin implementing `agents` table migration in SQLite.
- **Gemini:** Audit `src/agentic/core/protocols.py` for multi-agent compatibility.
