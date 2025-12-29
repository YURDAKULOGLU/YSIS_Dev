---
id: TASK-New-4929
type: PLAN
status: DRAFT
target_files:
  - src/agentic/core/plugins/aider_executor_enhanced.py
  - workspaces/active/TASK-New-4929/docs/PLAN.md
  - workspaces/active/TASK-New-4929/docs/RUNBOOK.md
  - workspaces/active/TASK-New-4929/artifacts/RESULT.md
  - workspaces/active/TASK-New-4929/META.json
  - workspaces/active/TASK-New-4929/CHANGES/changed_files.json
---
Goal: Capture Aider stdout/stderr to artifacts/logs and add guardrails for unexpected file creation.

Steps:
1. Add log capture to Aider execution (direct + ACI).
2. Enforce non-empty plan files_to_modify or fail early.
3. Validate git status vs allowed file set; fail if unexpected files modified.
4. Document verification and limitations.
