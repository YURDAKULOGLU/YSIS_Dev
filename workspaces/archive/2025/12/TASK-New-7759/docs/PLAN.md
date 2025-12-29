---
id: TASK-New-7759
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T17:25:00
target_files:
  - docs/governance/TAGGING_STANDARD.md
  - docs/governance/templates/SLIM_META.json
---

# Task: Constitution tags in META.json (TASK-GOV-SLIM-004)

## Objective
To stop agents from writing verbose compliance sentences in every file. We will replace these with short "Constitution Tags" in the metadata.

## Approach
Define a mapping of Constitution Sections to Tags (e.g., Article 1 -> `§1`). Update the metadata template to include a `constitution_tags` field.

## Steps
1.  Draft `docs/governance/TAGGING_STANDARD.md`.
2.  Define the tag mapping.
3.  Update `docs/governance/templates/SLIM_META.json` to include the tags field.

## Acceptance Criteria
- [ ] Tagging standard document exists.
- [ ] Tags are short (e.g., `§1`, `§2`).
- [ ] Mandatory artifacts produced.