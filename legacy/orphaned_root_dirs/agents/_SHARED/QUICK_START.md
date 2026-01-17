# Quick Start (5 minutes)

## 1) Core Rules
- Do not edit `tasks.db` or JSON files directly.
- Use MCP tools via `scripts/ybis.py` or direct MCP calls.
- All messaging now through `scripts/ybis.py message` (MCP-based).

## 2) Task Flow (Tool-Based)
1. Claim task: `python scripts/ybis.py claim TASK-ID`
2. Work in `workspaces/active/<TASK_ID>/`.
3. Write `docs/PLAN.md`, `docs/RUNBOOK.md`, `artifacts/RESULT.md`.
4. Complete: `python scripts/ybis.py complete TASK-ID`

## 3) Messaging (MCP-Based)
- Send: `python scripts/ybis.py message send --to all --subject "Update" --content "..."`
- Read: `python scripts/ybis.py message read`
- Acknowledge: `python scripts/ybis.py message ack MSG-ID --action will_do`
- UI: Streamlit `src/dashboard/app.py` (Messaging tab)

## 4) Start Here
- `AI_START_HERE.md`
- `SYSTEM_STATE.md`
