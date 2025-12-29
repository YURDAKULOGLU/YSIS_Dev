---
id: TASK-New-9297
type: RUNBOOK
status: COMPLETED
---
# Orchestrator Spine Runbook

## Purpose
Provide a single MCP-first entrypoint and align docs and governance to stop drift.

## Preconditions
- Repo root set as current working directory.
- MCP tools available via src/agentic/mcp_server.py.

## Execution Steps
1) Add scripts/run_orchestrator.py (single entrypoint).
2) Update scripts/run_next.py and scripts/run_production.py to delegate.
3) Align docs to canonical Brain path and entrypoint.
4) Add missing governance docs and workflow registry.

## Verification
- Static scan: ensure docs refer to one brain path and one entrypoint.
- Ensure .YBIS_Dev hardcode removed from onboarding docs.
- Ensure required artifacts exist in workspace.

## Rollback
- Restore previous entrypoint files from git diff.
- Revert docs changes.
