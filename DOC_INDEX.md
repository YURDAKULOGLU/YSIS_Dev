# 🗺️ YBIS Documentation Index

> **Mandatory Reading for All Agents**
> *If you are lost, return here.*

---

## 📍 Where am I?
You are in **YBIS_Dev**, a Tier 4.5 Autonomous Software Factory.

## 🧭 Navigation Map

| Zone | Path | Read This If... |
|------|------|-----------------|
| **The Map** | [DOC_INDEX.md](./DOC_INDEX.md) | You are new or lost. |
| **The Start** | [AI_START_HERE.md](./AI_START_HERE.md) | You need to claim a task or run a command. |
| **The Brain** | [src/agentic/graph/README.md](./src/agentic/graph/README.md) | You are modifying the workflow logic. |
| **The Core** | [src/agentic/core/README.md](./src/agentic/core/README.md) | You need config, paths, or logging. |
| **The Tools** | [scripts/README.md](./scripts/README.md) | You want to execute code or check health. |
| **Messaging CLI** | `scripts/ybis.py` | MCP-backed messaging (`message send/read/ack`). |
| **Messaging Archive** | `Knowledge/Messages/inbox/` | Legacy message archive (read-only). |
| **The Guard** | [tests/README.md](./tests/README.md) | You are writing tests (which you should be). |
| **The Memory** | [Knowledge/README.md](./Knowledge/README.md) | You need to access DB, RAG, or Messages. |
| **The UI** | [src/dashboard/README.md](./src/dashboard/README.md) | You are working on the Streamlit dashboard. |
| **The Infra** | [docker/README.md](./docker/README.md) | You are managing containers or Redis. |
| **The Past** | [legacy/README.md](./legacy/README.md) | You are looking for dead code (Read-Only). |
| **The Vision** | [SYSTEM_STATE.md](./SYSTEM_STATE.md) | You need architectural context. |

---

## ⚡ Quick Protocols

### 1. Token Economy (Iceberg Rule)
- **Do:** `python scripts/smart_exec.py <cmd>`
- **Don't:** `cat long_file.txt` (Use `head` or `grep`)

### 2. Single Source of Truth
- **Paths:** `src.agentic.core.config`
- **Tasks:** `Knowledge/LocalDB/tasks.db`

### 3. Communication
- **Primary:** `scripts/ybis.py message ...` (MCP + SQLite)
- **Archive:** `Knowledge/Messages/inbox/` (read-only)

---

**System Integrity:** 100%
**Last Updated:** 2025-12-24
