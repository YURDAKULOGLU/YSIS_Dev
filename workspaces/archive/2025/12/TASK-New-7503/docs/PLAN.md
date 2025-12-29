---
id: TASK-New-7503
type: PLAN
status: DRAFT
target_files:
  - workspaces/active/TASK-New-7503/docs/PLAN.md
  - workspaces/active/TASK-New-7503/docs/RUNBOOK.md
  - workspaces/active/TASK-New-7503/artifacts/RESULT.md
  - workspaces/active/TASK-New-7503/META.json
  - workspaces/active/TASK-New-7503/CHANGES/changed_files.json
---
Goal: Validate artifact enforcement (lite + full) by running protocol_check on completed tasks and documenting evidence.

Steps:
1. Create task artifacts (PLAN/RUNBOOK/RESULT/META/CHANGES).
2. Run protocol_check in lite mode on a completed task (archived) and capture output.
3. Run protocol_check in full mode on a completed task (archived) and capture output.
4. Run protocol_check for this task in lite mode.
5. Summarize results and lessons in RESULT.
