# Governance (Approvals + Review)

References:
- CONSTITUTION.md
- SECURITY.md
- WORKFLOWS.md
- INTERFACES.md

## 1) Purpose
Governance exists to prevent:
- unsafe self-modification
- drift in core contracts
- silent regressions in gates/sandbox
- "it worked once" non-reproducible changes

## 2) Roles (minimal)
### Maintainer (you)
- can approve protected/high-risk changes
- can change policy profiles
- owns releases/stable snapshots

### Worker (automation)
- executes tasks under policy
- cannot self-approve protected changes

### Reviewer (optional future)
- second human reviewer for high-risk changes

## 3) Approval Triggers (must approve)
Approval required if any is true:
- protected paths touched (see SECURITY.md)
- risk_score >= threshold
- patch size exceeds threshold
- migrations changed
- syscall or gate logic changed
- sandbox profile changes
- policy profile changes

## 4) Approval Artifact
Approvals must be explicit and recorded:
- stored under run folder (or via approvals syscall)
- referenced by gate_report.json
- includes: run_id, decision, reason, timestamp, approver identity

Decisions:
- APPROVE
- REJECT
- REQUEST_CHANGES

## 5) Debate Output
Debate is advisory only:
- debate_report.json can inform decisions
- it cannot override gate logic

## 6) Change Control Rules
- Any change to contracts/syscalls/gates requires:
  - golden tests updated or added
  - evidence reports updated if schema changes
  - migrations updated if needed

## 7) Stable Snapshot Definition
A "stable snapshot" is valid only if:
- passes full test suite (unit/integration/golden)
- security audit checklist passes
- migration docs updated (if needed)
- policy profiles validated

## 8) Exceptions
If an exception is needed:
- must be documented in approval artifact
- must include explicit risk statement
- must include a follow-up task to remove exception

