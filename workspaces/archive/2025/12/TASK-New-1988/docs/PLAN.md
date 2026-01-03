---
id: TASK-New-1988
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T17:15:00
target_files:
  - docs/governance/templates/SLIM_RESULT.md
  - docs/governance/templates/SLIM_META.json
---

# Task: Slim RESULT/META templates (TASK-GOV-SLIM-002)

## Objective
To reduce token burn by creating ultra-concise templates for RESULT and META artifacts. Target length for RESULT: 6-10 lines.

## Approach
Define new "Slim Mode" templates that focus only on:
1. What changed.
2. Why it changed.
3. Verification result.
4. Minimal metadata.

## Steps
1. Create `docs/governance/templates/SLIM_RESULT.md`.
2. Create `docs/governance/templates/SLIM_META.json`.
3. Propose using these as the default for Level 1/2 tasks.

## Acceptance Criteria
- [ ] Templates exist.
- [ ] RESULT template is < 10 lines.
- [ ] All mandatory artifacts produced.
