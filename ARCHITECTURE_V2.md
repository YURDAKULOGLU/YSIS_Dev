# YBIS_Dev Architecture V2 (The Single Source of Truth)

> **Status:** Active & Enforced
> **Version:** 2.0.0
> **Date:** 2025-12-20

## 1. Core Philosophy: The Factory
YBIS_Dev is not just a project; it is an **Autonomous Software Factory**. It uses a recursive bootstrap protocol to build itself.
- **Framework 1 (The Kernel):** The Python core enabling agent operations (`src/agentic`).
- **Framework 2 (The Builder):** The agents (Planner, Executor, Verifier) that write code.
- **Framework 3 (The Product):** The features built by the agents (Dashboard, Missions, etc.).

## 2. Directory Structure (Standardized)

All agents MUST adhere to this structure. No exceptions.

```
YBIS_Dev/
├── src/                    # THE KERNEL (Python Source Code)
│   ├── agentic/            # Core Agent Framework
│   │   ├── core/           # Orchestrator, Graphs, Plugins
│   │   ├── config.py       # PATH CONSTANTS (Import from here!)
│   │   └── protocols.py    # Interfaces (Planner, Executor, Verifier)
│   ├── dashboard/          # Web UI
│   └── utils/              # Shared Utilities
│
├── scripts/                # ENTRY POINTS (CLI & Maintenance)
│   ├── bootstrap/          # System setup scripts
│   ├── missions/           # Mission runners (e.g., run_weather.py)
│   └── utils/              # Helper scripts
│
├── docs/                   # KNOWLEDGE BASE (Static)
│   ├── governance/         # Rules, Principles, Roles
│   └── architecture/       # System Design
│
├── knowledge/              # MEMORY (Dynamic/Operational)
│   ├── local_db/           # ChromaDB, Tasks.json
│   └── tasks/              # File-based task queues
│
├── tests/                  # VERIFICATION
│   ├── unit/
│   └── integration/
│
├── legacy/                 # ARCHIVE (Do not touch unless migrating)
│   └── workforce/          # Old agent teams (CrewAI, AutoGen)
│
└── .sandbox/               # EXECUTION ZONES
    ├── hybrid/             # Active task execution
    └── docker/             # Containerized execution (Future)
```

## 3. The Prime Directives (For Agents)

1.  **Path Hygiene:** NEVER hardcode paths. ALWAYS import `PROJECT_ROOT` from `src.agentic.core.config`.
2.  **Entry Points:** Do NOT clutter the root. Create scripts in `scripts/`.
3.  **Verification:** No code is "Done" until `Sentinel` says it is verified.
4.  **Legacy Isolation:** Ignore `legacy/` unless explicitly instructed to perform archaeology.

## 4. Key Components (The Engine)

| Component | Path | Responsibility |
|-----------|------|----------------|
| **Orchestrator** | `src/agentic/core/graphs/orchestrator_graph.py` | State Machine Logic (LangGraph) |
| **Executor** | `src/agentic/core/plugins/aider_executor.py` | Coding (via Aider CLI) |
| **Verifier** | `src/agentic/core/plugins/sentinel.py` | Quality Control (Pytest/Lint) |
| **Memory** | `src/agentic/core/plugins/rag_memory.py` | Context Retrieval (ChromaDB) |

## 5. Bootstrap Protocol Status

- **Phase 0:** Kernel Stabilization (Current Step)
- **Phase 1:** Memory Integration (RAG)
- **Phase 2:** Docker Sandbox
- **Phase 3:** Open SWE Integration

---
**End of Specification.**
