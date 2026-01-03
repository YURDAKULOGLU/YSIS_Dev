---
id: TASK-New-6472
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T14:58:32.475722
target_files:
  - docs/governance/00_GENESIS/AGENT_CONTRACT.md
  - docs/MULTI_AGENT.md
  - docs/specs/SPEC_NEXT_EVOLUTION.md
---

# Task: TASK-DOC-005: Standardize Workspace Path References

## Objective

Fix conflicting workspace path references across documentation. Constitution specifies `workspaces/active/<TASK_ID>/` but several docs reference legacy `.sandbox*` paths creating confusion.

## Problem

**Current State:**
- `docs/governance/00_GENESIS/AGENT_CONTRACT.md`: References `.YBIS_Dev/.sandbox/**` and `.YBIS_Dev/.sandbox_hybrid/**`
- `docs/MULTI_AGENT.md`: References `.sandbox_worker`
- `docs/specs/SPEC_NEXT_EVOLUTION.md`: References `.sandbox_worker`

**Constitutional Requirement:**
- YBIS_CONSTITUTION.md §3: Workspace structure is `workspaces/active/<TASK_ID>/` with subdirectories: `docs/`, `artifacts/`, `tests/`

## Approach

Replace all legacy `.sandbox*` references with constitutional `workspaces/active/` path.

## Steps

1. Update `docs/governance/00_GENESIS/AGENT_CONTRACT.md`:
   - Lines 17, 24, 58, 65: Replace `.YBIS_Dev/.sandbox/**` references
   - Add subdirectory structure (docs/, artifacts/, tests/)
   - Reference constitution for workspace standards

2. Update `docs/MULTI_AGENT.md`:
   - Line 12: Replace `.sandbox_worker` reference
   - Clarify isolation boundaries
   - Add CHANGES tracking requirement

3. Update `docs/specs/SPEC_NEXT_EVOLUTION.md`:
   - Line 12: Same as MULTI_AGENT.md

4. Commit changes with proper constitutional reference

## Risks & Mitigations

**Risk:** LOW - Documentation-only changes
**Mitigation:** Simple git revert if confusion occurs

## Success Criteria

- [ ] All `.sandbox*` references removed from active docs
- [ ] All workspace refs use `workspaces/active/<TASK_ID>/`
- [ ] Subdirectory structure documented
- [ ] Constitution referenced
- [ ] Changes committed

**Constitutional Alignment:** §3 (Execution Protocol)
