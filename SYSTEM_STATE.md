# YBIS SYSTEM STATE & CONSTITUTION (Tier 4 Stabilized)

> **Status:** ACTIVE - STABLE
> **Current Version:** v4.0.0 "LangGraph-Pydantic Unified"
> **Last Update:** 2025-12-22

---

## 1. THE SUPREME LAW (The Constitution)

All agents working in YBIS MUST adhere to these rules. Failure results in automatic Task Rejection.

1.  **PATH INTEGRITY:** NEVER hardcode paths. ALWAYS use `src.agentic.core.config`.
2.  **TEST-FIRST:** New logic MUST have a corresponding unit test in `tests/unit/`.
3.  **CLEAN WORKSPACE:** Only modify `src/` and `tests/`. Do NOT touch `legacy/` or `_Archive/`.
4.  **STATE VALIDATION:** All internal data transfer MUST use Pydantic `BaseModel` from `protocols.py`.
5.  **OTONOM COMMIT:** Successful tasks are committed by `GitManager`. Do not auto-commit via Aider.

---

## 2. ARCHITECTURAL BLUEPRINT

The system is built on "The Giants":

-   **The Brain (LangGraph):** Manages the state machine and node transitions.
-   **The Skeleton (Pydantic):** Ensures type safety and validation between all nodes.
-   **The Worker (Aider):** Elite pair-programmer that executes the actual code changes.
-   **The Guard (Sentinel):** Strict verifier using AST analysis, Ruff, and Pytest.
-   **The Janitor (GitManager):** Keeps the repo clean by auto-committing successful tasks.

---

## 3. AGENT ONBOARDING PIPELINE (Step-by-Step)

If you are a newly joined agent, follow this sequence to become context-aware:

1.  **Read `SYSTEM_STATE.md` (This file):** Understand the current law and architecture.
2.  **Read `AI_START_HERE.md`:** Learn how to invoke tools and run tasks.
3.  **Check `Knowledge/LocalDB/tasks.json`:** See the current backlog and recent successes.
4.  **Check `src/agentic/core/protocols.py`:** Understand the data structures you will handle.
5.  **Audit `docs/governance/YBIS_CONSTITUTION.md`:** Deep-dive into the factory's mission.

---

## 4. CURRENT SYSTEM HEALTH

-   **Tier Level:** 4 (Autonomous Software Factory)
-   **Stability:** High (Pydantic models validated)
-   **Cleanliness:** High (GitManager active)
-   **RAG Awareness:** Active (Memory storage via Mem0)

---

## 5. KNOWN ISSUES & LESSONS LEARNED

-   **Emoji Ban:** Always use clean ASCII for code. Comments can be in Turkish but avoid symbols.
-   **Partial Updates:** LangGraph nodes return updates, not the whole state. Use `TaskState.model_validate` carefully.
-   **Git Status:** Aider sometimes reports too many files. We now filter for `src/` and `tests/`.

---
*End of System State*