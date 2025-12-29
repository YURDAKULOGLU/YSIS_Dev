---
id: TASK-New-3889
type: PLAN
status: DRAFT
target_files:
  - scripts/run_next.py
  - scripts/run_production.py
  - scripts/runners/orchestrator_main.py
  - scripts/run_graph.py
  - docs/specs/SCRIPT_REPLACEMENT_MATRIX.md
  - workspaces/active/TASK-New-3889/docs/PLAN.md
  - workspaces/active/TASK-New-3889/docs/RUNBOOK.md
  - workspaces/active/TASK-New-3889/artifacts/RESULT.md
  - workspaces/active/TASK-New-3889/META.json
  - workspaces/active/TASK-New-3889/CHANGES/changed_files.json
---
Goal: Deprecate legacy runner scripts and point to scripts/run_orchestrator.py.

Steps:
1. Review legacy runner scripts for direct-exec entrypoints.
2. Add deprecation banners + direct pointer to run_orchestrator.
3. Update script replacement matrix if needed.
4. Record changes and verification status.
