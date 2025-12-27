
# STABILIZATION PROTOCOL: "DB-Driven Execution" (v3.0)

**Philosophy:** SQLite is the Brain (`tasks.db`), Filesystem is the Workbench (`workspaces/`).

## 1. THE GOLDEN RULE
**The Database (`tasks.db`) is the SINGLE SOURCE OF TRUTH.**
- Do not trust file names.
- Do not trust folder presence.
- Trust only the row in SQLite.

## 2. EXECUTION FLOW

### A. CLAIM (DB Operation)
When an agent picks a task:
1.  **UPDATE DB:** Set `status='IN_PROGRESS'`, `assignee='<AGENT_ID>'`.
2.  **INIT WORKSPACE:** Create `workspaces/active/<TASK_ID>/`.
3.  **LINK:** Update DB `metadata` column with `{"workspace": "workspaces/active/<TASK_ID>"}`.

### B. EXECUTE (Filesystem Operation)
Work exclusively within `workspaces/active/<TASK_ID>/`.
-   Write `docs/PLAN.md` (Strategy)
-   Write `docs/RUNBOOK.md` (Log)
-   Generate `artifacts/` (Outputs)

### C. FINISH (Hybrid Operation)
1.  **VERIFY:** Ensure code passes tests.
2.  **FINALIZE:** Write `artifacts/RESULT.md`.
3.  **UPDATE DB:** Set `status='DONE'`, `final_status='SUCCESS'`.
4.  **ARCHIVE:** Move folder to `workspaces/archive/YYYY/MM/<TASK_ID>/` and update DB `metadata` with new path.

## 3. ASSIGNMENTS

### CODEX (The Auditor)
- **Role:** Ensure no "Ghost Tasks" exist (folders without DB rows, or DB rows without folders).

### CLAUDE (The Builder)
- **Role:** Update `scripts/ybis.py` (Unified CLI) to handle the DB-Filesystem bridging automatically.

### GEMINI (The Architect)
- **Role:** Validate the protocol with `TASK-New-218-FINAL` (Self-Propagation).

---
**Authorized by:** The Architect
