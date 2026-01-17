# Protocols

## Task Protocol
- Source of truth: `Knowledge/LocalDB/tasks.db`.
- Workspace: `workspaces/active/<TASK_ID>/`.
- Required artifacts: `docs/PLAN.md`, `docs/RUNBOOK.md`, `artifacts/RESULT.md`.
- PLAN/RESULT must include YAML frontmatter.

## Messaging Protocol
- Use `scripts/ybis.py message` for send/read/ack.
- Avoid manual JSON edits in `Knowledge/Messages/`.

## MCP Tools (Core)
- `get_tasks(status, assignee)`
- `claim_task(task_id, agent_id)`
- `update_task_status(task_id, status, final_status)`
