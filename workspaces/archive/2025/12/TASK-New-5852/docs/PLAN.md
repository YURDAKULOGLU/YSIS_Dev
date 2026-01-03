---
id: TASK-New-5852
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-28T19:30:00
target_files: ["scripts/enforce_architecture.py"]
---

# Task: Architecture Enforcement & Council Integration (TASK-ARC-001)

## Objective
To create an automated mechanism that enforces the "Single Entry Point" and "Single Brain" decisions reached in DEBATE-20251228174942. This ensures that the system does not drift back to deprecated modes.

## Approach
We will build a specialized linter/validator script (`scripts/enforce_architecture.py`) that scans the codebase for architectural violations.

## Steps
1.  **Create Validator Script:** Write `scripts/enforce_architecture.py`.
2.  **Define Rules:**
    *   **Rule 1 (The Ban):** Importing `src.agentic.graph.workflow` is FORBIDDEN. Must use `orchestrator_graph`.
    *   **Rule 2 (The Warning):** Usage of `run_next.py` or `run_production.py` triggers a DEPRECATION WARNING.
    *   **Rule 3 (The Mandate):** `run_orchestrator.py` must exist (eventually).
3.  **Integrate:** Add this script to `scripts/system_health_check.py` or run it manually.

## Risks & Mitigations
*   **Risk:** Valid legacy code might break.
*   **Mitigation:** The script will warn first, not delete. We will whitelist `legacy/` folder.

## Acceptance Criteria
- [ ] `scripts/enforce_architecture.py` exists and runs without errors.
- [ ] It detects imports of the old `workflow.py` in `src/`.
- [ ] It ignores `legacy/` and `_Archive/` directories.
- [ ] It reports "PASS" if the architecture is clean.
