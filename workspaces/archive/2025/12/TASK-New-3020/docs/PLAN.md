---
id: TASK-New-3020
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T15:50:00
target_files:
  - docs/governance/RISK_MATRIX.md
---

# Task: Codify risk:high triggers (TASK-GOV-RISK-001)

## Objective
To define exactly what constitutes a "High Risk" task. High Risk tasks mandate a multi-LLM Council Vote and "Full Artifact Mode" (including evidence/summary.md).

## Approach
Create a `RISK_MATRIX.md` that categorizes actions into Levels (Low, Med, High).

## Steps
1.  Draft `docs/governance/RISK_MATRIX.md`.
2.  Define "Triggers" (e.g., shell execution, file system writes).
3.  Propose Constitutional update.

## Acceptance Criteria
- [ ] Risk Matrix document exists.
- [ ] High Risk triggers are clearly defined (Shell, Network, Secrets).
- [ ] All mandatory artifacts produced.
