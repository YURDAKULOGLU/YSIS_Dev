---
id: TASK-New-4759
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T17:10:11.521193
target_files:
  - scripts/protocol_check.py
  - docs/governance/YBIS_CONSTITUTION.md
---

# Task: TASK-GOV-SLIM-001: Introduce artifact tiers (Tier0/1/2)

## Objective

Implement constitutional artifact tier system to reduce token waste while maintaining auditability. Current system forces all tasks to produce 5 artifacts (~1500 tokens). New tier system scales artifacts to task risk level.

## Approach

Define 3 tiers based on task risk/scope:
- **Tier 0 (doc-only):** RUNBOOK.md only (commands + commit)
- **Tier 1 (low-risk):** + RESULT.md (5-line summary)
- **Tier 2 (high-risk):** Current LITE (all 5 files)

Auto-detect tier from git diff stats: <10 lines = Tier 0, <50 lines = Tier 1, ≥50 = Tier 2

## Steps

1. Update `scripts/protocol_check.py`:
   - Add REQUIRED_TIER0, REQUIRED_TIER1 constants
   - Add --tier parameter (0, 1, 2, auto)
   - Add auto-detection logic using git diff --stat
2. Update `docs/governance/YBIS_CONSTITUTION.md`:
   - Document tier definitions in §4 (Artifacts)
   - Specify auto-detection rules
   - Update completion requirements
3. Create RUNBOOK.md, RESULT.md, META.json, CHANGES/
4. Commit with tier system implementation
5. Test tier detection on sample tasks

## Risks & Mitigations

**Risk:** Auto-detection might mis-classify tasks
**Mitigation:** Allow manual override with --tier flag

**Risk:** Breaking existing tasks expecting full artifacts
**Mitigation:** Default to Tier 2 if auto-detection fails

**Risk:** Reduced artifacts = reduced auditability
**Mitigation:** Git history + RUNBOOK always present. Tier 0 still has commit hash for full audit trail.

## Success Criteria

- [ ] protocol_check.py supports --tier 0/1/2/auto
- [ ] Auto-detection logic based on git diff --stat
- [ ] Constitution §4 updated with tier definitions
- [ ] Sample test: doc-only task passes with --tier 0
- [ ] Backward compatible: existing tasks still pass with --tier 2
- [ ] Changes committed and verified

## Token Impact

**Current:** 1500 tokens/task (5 artifacts)
**Tier 0:** 150 tokens (RUNBOOK only)
**Tier 1:** 300 tokens (+ minimal RESULT)
**Expected:** 75% of tasks → Tier 0/1 = **80% token reduction**
