---
id: TASK-New-8589
type: PLAN
status: DRAFT
target_files:
  - docs/specs/mission_tasks/bootstrap_phase2.md
  - docs/specs/mission_tasks/fix_core_tests.md
  - docs/specs/mission_tasks/fix_sentinel.md
  - docs/specs/mission_tasks/fix_governance.md
  - scripts/missions/run_bootstrap_phase2.py
  - scripts/missions/run_fix_core_tests.py
  - scripts/missions/run_fix_sentinel.py
  - scripts/missions/run_fix_governance.py
  - workspaces/active/TASK-New-8589/docs/PLAN.md
  - workspaces/active/TASK-New-8589/docs/RUNBOOK.md
  - workspaces/active/TASK-New-8589/artifacts/RESULT.md
  - workspaces/active/TASK-New-8589/META.json
  - workspaces/active/TASK-New-8589/CHANGES/changed_files.json
---
Goal: Convert mission scripts to task templates and deprecate direct execution.

Steps:
1. Create mission task templates for bootstrap/fix scripts.
2. Create tasks that reference those templates.
3. Deprecate mission scripts with pointers to tasks.
4. Record changes and verification status.
