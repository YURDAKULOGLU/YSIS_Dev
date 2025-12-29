---
id: TASK-New-9297
type: RESULT
status: SUCCESS
completed_at: 2025-12-28
---
# Task Result: Orchestrator Spine

## Summary
- Added a single MCP-first orchestrator entrypoint and converted legacy runners to wrappers.
- Aligned key docs to the canonical Brain path and entrypoint.
- Added missing governance docs and workflow registry.

## Changes Made
- scripts/run_orchestrator.py added
- scripts/run_next.py and scripts/run_production.py wrapped
- README.md, AI_START_HERE.md, docs/AGENTS_ONBOARDING.md updated
- docs/EXTERNAL_AGENTS_PIPELINE.md, docs/PROMPTS_WORKFLOWS.md, workflow-registry.yaml added

## Files Modified
See workspaces/active/TASK-New-9297/CHANGES/changed_files.json

## Tests Run
- Not run (doc and orchestration wiring only)

## Verification
- Manual review of entrypoint wiring and doc alignment

## Notes
- MCP 2025-11-25 async ops documented as follow-up in docs/PROMPTS_WORKFLOWS.md
