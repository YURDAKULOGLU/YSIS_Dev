# YBIS ARCHITECTURE V4.5 (LangGraph + Pydantic + SQLite)

> **Philosophy:** Reliability through strict validation and protocol-based orchestration.

---

## 1. THE CORE STACK

- **Orchestration:** LangGraph (State machine management).
- **Data Integrity:** Pydantic (Strong type validation for all states).
- **Storage:** SQLite (Async task persistence via aiosqlite).
- **Execution:** Aider (Specialized local coding agent).
- **Cleanup:** GitManager (Automated repo maintenance).

---

## 2. THE WORKFLOW

The factory follows a strict state-machine flow:

1.  **PLAN:** A task is promoted from the SQLite backlog. A planner (32B model) generates a structured `Plan` object.
2.  **EXECUTE:** The executor (Aider) modifies code in the `src/` and `tests/` directories based on the `Plan`.
3.  **VERIFY:** The sentinel analyzes the modified files using AST, Ruff, and isolated Pytest runs.
4.  **COMMIT:** On success, GitManager performs an atomic commit with the task ID.
5.  **CHAIN:** Any `proposed_tasks` created during the session are automatically added to the SQLite database.

---

## 3. STATE MANAGEMENT (TaskState)

We use a single Pydantic model (`TaskState`) defined in `src/agentic/core/protocols.py`. 
- Every node receives a `TaskState` object.
- Every node returns a `dict` update.
- LangGraph ensures all updates are merged and validated.

---

## 4. PERSISTENCE LAYER (SQLite)

The system has moved away from file-based task storage.
- **DB Path:** `Knowledge/LocalDB/tasks.db`
- **Bridge:** `src/agentic/infrastructure/db.py`
- **Capability:** Supports concurrent access from multiple workers and the Dashboard.

---

## 5. SELF-IMPROVEMENT (Tier 5 Readiness)

The system is now capable of "Spec-Driven Development" (SDD).
- Agents can create new specifications (Blueprints) under `docs/specs/`.
- The system can convert these specifications into new tasks via `proposed_tasks`.

---
*Architectural Blueprint - Established 2025-12-22*
