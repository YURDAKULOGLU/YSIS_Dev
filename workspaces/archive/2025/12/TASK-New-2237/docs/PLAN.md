---
id: TASK-New-2237
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T16:35:00
target_files:
  - docs/governance/P0_PROTOCOL.md
  - scripts/ybis.py (Ref check)
---

# Task: Manual Verification for P0 Tasks (TASK-GOV-QUALITY-002)

## Objective
To ensure that any task marked as CRITICAL or P0 cannot be closed by an agent alone. It requires an explicit "Architect/User Acknowledgment" in the message system.

## Approach
Draft the `P0_PROTOCOL.md` and define the required interaction in the `ybis.py` messaging system.

## Steps
1.  Draft `docs/governance/P0_PROTOCOL.md`.
2.  Define the "Review-Acknowledge-Complete" flow.
3.  Add a reminder to `ybis.py` (optional, via documentation update).

## Acceptance Criteria
- [ ] P0 Protocol exists.
- [ ] Mandates evidence review by a human/architect.
- [ ] Mandatory artifacts produced.
