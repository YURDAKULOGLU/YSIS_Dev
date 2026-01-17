# 🧠 The Knowledge Base

> **Zone:** Long-term Memory & Data
> **Access:** Read/Write (via Standard Bridges)

## Sectors

| Sector | Path | Description |
|--------|------|-------------|
| **LocalDB** | `LocalDB/tasks.db` | **SQLite.** The operational state (Tasks, Status). |
| **RAG** | `LocalDB/chroma_db/` | **Vector Store.** Embeddings for semantic search. |
| **Messages** | `Messages/` | **Communication.** Inbox/Outbox and Debates. |
| **Archives** | `...` | Old run logs and artifacts. |

## Rules
- **Direct Access:** ⚠️ AVOID direct file I/O on DB files. Use `src.agentic.infrastructure.db`.
- **Backups:** Git ignores big DBs, ensure you use the export scripts.
