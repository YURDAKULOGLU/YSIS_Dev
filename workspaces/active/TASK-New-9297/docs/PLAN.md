---
id: TASK-New-9297
type: PLAN
status: COMPLETED
target_files: [scripts/run_orchestrator.py, scripts/run_next.py, scripts/run_production.py, README.md, AI_START_HERE.md, docs/AGENTS_ONBOARDING.md, docs/EXTERNAL_AGENTS_PIPELINE.md, docs/PROMPTS_WORKFLOWS.md, workflow-registry.yaml]
---
# Orchestrator Spine Plan

## Goal
Create a single MCP-first orchestration spine (claim -> plan -> execute -> verify -> artifacts -> update) and eliminate drift between entrypoints and docs.

## Scope
- Add scripts/run_orchestrator.py as the single entrypoint.
- Convert scripts/run_next.py and scripts/run_production.py into thin wrappers.
- Choose a single Brain path and align README/AI_START_HERE/AGENTS_ONBOARDING to it.
- Enforce CoreConfig-only paths and remove hardcoded .YBIS_Dev references in onboarding docs.
- Add missing governance docs and workflow registry.
- Document MCP 2025-11-25 async ops and planner enhancements as follow-up hooks.

## Out of Scope
- New product features (dashboard/UI).
- Legacy/archive refactors beyond doc references.

## Steps
1) Inspect orchestrator/graph entrypoints and pick the canonical Brain path.
2) Implement scripts/run_orchestrator.py with MCP-first flow.
3) Update run_next/run_production to delegate and mark deprecated.
4) Align docs (README, AI_START_HERE, AGENTS_ONBOARDING) to the canonical Brain and entrypoint.
5) Add missing docs: EXTERNAL_AGENTS_PIPELINE, PROMPTS_WORKFLOWS, workflow-registry.yaml.
6) Add MCP upgrade hooks and planner enhancements (documented in code comments/config hooks).
7) Verify by static checks and ensuring artifact outputs exist for this task.

## Success Criteria
- scripts/run_orchestrator.py exists and is the only recommended entrypoint.
- run_next/run_production are thin wrappers to run_orchestrator.
- README/AI_START_HERE/AGENTS_ONBOARDING reference the same Brain path.
- .YBIS_Dev hardcodes removed from onboarding docs touched in this task.
- Missing docs and workflow-registry.yaml exist.
- Artifacts created for this task under workspaces/active/TASK-New-9297/.

## Risks
- MCP SDK upgrade may break integrations.
- Brain path choice may conflict with legacy references.
- Async ops may introduce race conditions.

## Rollback
- Revert to previous entrypoints and MCP SDK if integration fails.
- Restore prior docs from git diff.
