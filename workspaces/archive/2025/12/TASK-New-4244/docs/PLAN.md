---
id: TASK-New-4244
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T15:50:34.279796
target_files:
  - docs/governance/00_GENESIS/AGENT_CONTRACT.md
  - docs/MULTI_AGENT.md
  - docs/specs/SPEC_NEXT_EVOLUTION.md
---

# Task: TASK-DOC-007: Standardize Verification Tool References

## Objective

Eliminate confusion caused by multiple verification tool references (`protocol_check.py`, `ybis-dev verify`, `Sentinel`) across documentation. Standardize to the canonical tool `scripts/protocol_check.py` as specified in YBIS_CONSTITUTION.md §4.

## Approach

Replace all references to deprecated verification tools with the constitutional standard:
1. In AGENT_CONTRACT.md: Replace 3 instances of `ybis-dev verify` (lines 51, 76, 104)
2. In MULTI_AGENT.md: Replace 2 instances of "Sentinel" (lines 18, 28)
3. In SPEC_NEXT_EVOLUTION.md: Replace 2 instances of "Sentinel" (lines 18, 28)

All replacements will:
- Point to `python scripts/protocol_check.py --task-id <TASK_ID> --mode lite`
- Explain lite vs full modes
- Reference constitution §4

## Steps

1. Read all target files to confirm line numbers (DONE)
2. Update AGENT_CONTRACT.md (3 changes)
   - Line 51: Replace ybis-dev verify in example acceptance criteria
   - Line 76: Replace ybis-dev verify in base verification section
   - Line 104: Replace ybis-dev verify in mandatory checklist
3. Update MULTI_AGENT.md (2 changes)
   - Line 18: Replace "Sentinel" with protocol_check.py
   - Line 28: Replace "Sentinel Verification" with protocol_check.py
4. Update SPEC_NEXT_EVOLUTION.md (2 changes)
   - Same pattern as MULTI_AGENT.md
5. Commit changes with constitutional reference
6. Create completion artifacts
7. Verify with protocol_check.py
8. Complete task

## Risks & Mitigations

**Risk:** Teams/agents might still use deprecated tools (ybis-dev verify, Sentinel)
**Mitigation:** This is documentation-only. Actual tool enforcement happens at completion time via protocol_check.py

**Risk:** Breaking instructions for external agents
**Mitigation:** protocol_check.py is already the enforced tool, we're just updating docs to match reality

## Success Criteria

- [ ] All ybis-dev verify references replaced (3 in AGENT_CONTRACT.md)
- [ ] All Sentinel references replaced (2 in MULTI_AGENT.md, 2 in SPEC_NEXT_EVOLUTION.md)
- [ ] protocol_check.py established as canonical tool
- [ ] Lite vs full modes explained
- [ ] Constitution §4 referenced
- [ ] Changes committed
- [ ] All artifacts created
- [ ] Protocol check passes

## Constitutional Alignment

This task enforces YBIS_CONSTITUTION.md §4 (Artifacts & Verification):
- Establishes protocol_check.py as the single canonical verification tool
- Eliminates conflicting tool references
- Aligns all docs with constitutional standard
