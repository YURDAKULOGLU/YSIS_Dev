---
id: TASK-New-6971
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T15:42:53.397782
target_files:
  - docs/AGENTS_ONBOARDING.md
---

# Task: TASK-DOC-006: Clarify Brain Path (Orchestrator vs Server Mode)

## Objective

Fix confusion in `AGENTS_ONBOARDING.md` about the canonical brain. The document currently presents `ybis_server.py --brain-mode` as the preferred connection method, which conflicts with the governance principle that `orchestrator_graph.py` is the canonical brain and `run_orchestrator.py` is the single execution spine.

## Approach

Replace the "Method 1: The Brain Connection" section (lines 28-36) with a clearer architecture description that:
1. Identifies `orchestrator_graph.py` as the canonical brain (single source of truth)
2. Identifies `run_orchestrator.py` as the execution spine (only runner)
3. Clarifies that `ybis_server.py --brain-mode` is OPTIONAL and for external integrations only
4. Notes that internal agents use orchestrator_graph directly
5. References the Governance Action Plan for authority

## Steps

1. Read current content of `docs/AGENTS_ONBOARDING.md` (DONE)
2. Update lines 28-36 to replace brain connection section
3. Update RUNBOOK.md with commands executed
4. Commit changes with constitutional reference
5. Create completion artifacts (RESULT.md, META.json, CHANGES/changed_files.json)
6. Verify with protocol_check.py
7. Complete task via ybis.py

## Risks & Mitigations

**Risk:** External agents currently using server mode might be confused by the change
**Mitigation:** Keep server mode documented as Method 1, but clarify it's optional and for external use only

**Risk:** Breaking existing integrations
**Mitigation:** This is documentation-only, no code changes. Server mode continues to work.

## Success Criteria

- [ ] Canonical brain path (`orchestrator_graph.py`) clearly identified
- [ ] Execution spine (`run_orchestrator.py`) clearly identified
- [ ] Server mode marked as optional for external integrations
- [ ] Internal agent workflow clarified
- [ ] Constitutional alignment verified (references Governance Action Plan)
- [ ] Changes committed with proper constitutional reference
- [ ] All required artifacts created (PLAN, RUNBOOK, RESULT, META, CHANGES)
- [ ] Protocol check passes

## Constitutional Alignment

This task enforces:
- **Governance Action Plan**: Single execution spine principle (orchestrator_graph.py → run_orchestrator.py)
- **YBIS Constitution §1**: Clarity on canonical brain architecture
