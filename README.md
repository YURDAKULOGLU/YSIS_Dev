# YBIS_Dev - Autonomous Software Factory (Tier 4.5)

> **Tier 4.5 Autonomous System: AI agents managing self-evolution through SQLite, Pydantic, and Git.**

---

## NEW AI Agent? Start Here

**Read this first:** [AI_START_HERE.md](./AI_START_HERE.md)
**Then read:** [SYSTEM_STATE.md](./SYSTEM_STATE.md) (Complete system architecture)

---

## Current Phase: Tier 4.5 "The Great Stabilization"

**Status:** ACTIVE - STABLE
**Goal:** Self-sustaining autonomous production with Git-based cleanup and SQLite persistence.

---

## Architecture: The Orchestration Engine

Protocol-based plugin architecture powered by LangGraph:

1.  **The Brain (OrchestratorGraph):** LangGraph state machine using Pydantic for validation.
2.  **The Executor (AiderEnhanced):** Advanced code generation with constitutional enforcement.
3.  **The Verifier (SentinelEnhanced):** High-security gates with AST analysis and isolated testing.
4.  **The Janitor (GitManager):** Automatic atomic commits for every successful task.
5.  **The Persistence (SQLite):** Thread-safe async task management via aiosqlite.

---

## Roadmap & Tiers

### Tier 4: The Sentinel (Completed)
- **Capability:** Automatic maintenance, Git-driven cleanup, and Pydantic validation.
- **Status:** Stable.

### Tier 5: Self-Architecture (NEXT)
- **Goal:** Agents designing and modifying the factory's own graph nodes.
- **Concept:** Architect agents using SDD (Spec-Driven Development) to mutate the system.

---

## Directory Structure

```
YBIS_Dev/
├── AI_START_HERE.md              # Agent onboarding
├── SYSTEM_STATE.md               # Complete system state
├── README.md                     # This file
│
├── src/agentic/core/
│   ├── graphs/                   # LangGraph workflows
│   ├── plugins/                  # Planner, Executor, Verifier, GitManager
│   ├── config.py                 # Path constants
│   ├── protocols.py              # Pydantic models & Interfaces
│   └── sdd_schema.py             # Spec-Driven Development schemas
│
├── src/agentic/infrastructure/
│   └── db.py                     # Async SQLite bridge
│
├── Knowledge/
│   ├── LocalDB/
│   │   ├── tasks.db              # SQLite Task Database (Source of Truth)
│   │   └── chroma_db/            # RAG vector database
│   └── API_References/           # Downloaded library documentation
│
├── .sandbox_worker/              # Production sandbox
└── tests/                        # Test suite
```

---
**Last Updated:** 2025-12-22
**System Version:** 4.5.0 (Tier 4 Stable)
**System Integrity:** 100%
