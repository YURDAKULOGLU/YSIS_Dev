# GRAND SYSTEM ANALYSIS REPORT (2025-12-22)
> **Status:** Active Analysis
> **Objective:** Comprehensive deep-dive into YBIS_Dev to identify all gaps, debts, and feature requirements.
> **Methodology:** Recursive Append (Layer by Layer Analysis)

---

## 1. ARCHITECTURAL CORE ANALYSIS
**Focus:** `src/agentic/core`, `scripts/`, `docs/` alignment.

### 1.1 The "Ghost Orchestrators" Issue
The codebase contains multiple, conflicting orchestrator implementations that are not documented or deprecated:
- **Active:** `src/agentic/core/graphs/orchestrator_graph.py` (The new LangGraph standard)
- **Zombie:** `src/agentic/core/orchestrator_v3.py` (Still heavily referenced, fully functional but theoretically legacy)
- **Dead:** `orchestrator_v2.py`, `orchestrator_hybrid.py`, `parallel_orchestrator.py` (Clutter)

**Verdict:** Immediate Cleanup Required. We must canonicalize `orchestrator_graph.py` and archive the rest.

### 1.2 Plugin System Reality Check
- **Good News:** A true modular `plugin_system` exists (`registry.py`, `loader.py`). It's not hardcoded.
- **Bad News:** The documentation (`ARCHITECTURE_V2.md`) treats plugins as static files, not a dynamic system.
- **Missing Roles:** The documentation claims "Architect" and "Product Owner" agents exist (Tier 3), but they are **Vaporware**. No specific plugin files exist for them; they are likely just prompt personas inside `SimplePlanner`.

### 1.3 Worker Alignment
- `scripts/run_next.py` -> Uses **OrchestratorGraph** (Correct)
- `scripts/worker.py` -> **Unknown/Suspect** (Needs verification, likely still on V3).

---

## 2. CAPABILITY & PLUGIN DEEP DIVE
**Focus:** `src/agentic/core/plugins/` content and logic.

### 2.1 Executor Schism
- **Active:** `AiderExecutor` (Standard). Functional but basic.
- **Hidden Gem:** `AiderExecutorEnhanced` (Exists but unused). This is vastly superior as it injects `CODE_STANDARDS`, `ARCHITECTURE_PRINCIPLES`, and enforces a "Test-First" workflow.
- **Verdict:** We must upgrade the Orchestrator to use `AiderExecutorEnhanced`.

### 2.2 The Gatekeeper (Sentinel)
- **Active:** `SentinelVerifier` (Basic path checking).
- **Hidden Gem:** `SentinelVerifierEnhanced` (AST analysis, Import checking, Emoji ban).
- **Verdict:** Immediate upgrade required to `SentinelVerifierEnhanced` to catch syntax errors earlier.

### 2.3 Task Board Fragility
- `TaskBoardManager` relies on a single `tasks.json` file without file locking.
- **Risk:** High concurrency risk if multiple workers run.
- **Mitigation:** We need a SQLite or file-lock based manager for Tier 4.

### 2.4 The Critical Disconnect (Worker)
- `scripts/run_next.py` -> Uses **LangGraph** (Modern).
- `scripts/worker.py` -> STILL Uses **OrchestratorV3** (Legacy).
- **Impact:** The main "always-on" worker is running the old, fragile brain.

---

## 3. DASHBOARD & UI ANALYSIS
**Focus:** `src/dashboard/app.py` and its capabilities.

### 3.1 The "Two Dashboards" Problem
- **Active:** `src/dashboard/app.py` (Streamlit). Functional, supports Mem0 and CrewAI.
- **Zombie:** `src/dashboard/src/dashboard/app.py` (Flask). A redundant nested file structure.
- **Verdict:** Delete the Flask zombie immediately to prevent confusion.

### 3.2 Feature Gaps (Streamlit)
- **Task Management:** Can *Add* tasks but cannot *Move* (Drag & Drop) or *Delete* them.
- **Hardcoding:** Critical paths (`Knowledge/LocalDB/tasks.json`) are hardcoded, ignoring `config.py`.

### 3.3 Research Lab (CrewAI)
- Surprisingly, the "Research Lab" tab is **fully functional**. It attempts to spin up real CrewAI agents using Ollama. This is a high-value asset we should protect.

---

## 4. TEST COVERAGE & QUALITY
**Focus:** `tests/` directory and code quality metrics.

### 4.1 The Illusion of Coverage
- **Unit Tests:** Exist (`test_orchestrator_graph.py`) but rely heavily on Mocks.
- **E2E Tests:** Non-existent for the new architecture. `legacy/old_tests/test_tier4_e2e.py` is archaic.
- **Organization:** Messy. `pluginTests.py` (CamelCase) vs `test_skills.py` (snake_case). Tests are scattered.

### 4.2 Quality Enforcement
- `config/code_quality_thresholds.json` exists but is a "Paper Tiger". No automated Git Hook or CI pipeline enforces it on commit.

---

## 5. STRATEGIC ROADMAP (Immediate Actions)

Based on this deep analysis, here is the required action plan to reach "Tier 4 Stability":

### Phase 1: Cleaning the House (Refactor)
- **[CRITICAL]** Delete `orchestrator_v3.py` and migration logic in `worker.py` to `OrchestratorGraph`.
- **[CRITICAL]** Delete the `src/dashboard/src` nesting zombie.
- **[HIGH]** Standardize `src/agentic/core/plugins` (Remove unused files, promote 'Enhanced' versions).

### Phase 2: Solidifying Foundations (Infrastructure)
- **[HIGH]** Implement File-Locking or SQLite for `TaskBoardManager` (Fix concurrency).
- **[MED]** Centralize configuration (Remove hardcoded paths in Dashboard).

### Phase 3: Expansion (Features)
- **[MED]** Enable "Drag & Drop" and "Delete" in Dashboard.
- **[LOW]** Formalize the "Architect" and "Product Owner" roles in the Graph structure.

---
> *End of Analysis - Ready for Task Assignment*

