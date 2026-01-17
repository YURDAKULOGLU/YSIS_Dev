# SPEC: T-534ee341

## Objective
Update docs/WORKFLOWS.md to note that executor selection is workflow-driven via node config (node.config.adapter or executor) and that workflows should explicitly set it. Keep it concise and add the note near the workflow specs section.

## Requirements
- Implement the objective exactly as stated.
- Keep changes scoped to the identified files.

## Acceptance Criteria
- Required files are created or updated.
- Verifier passes under the active profile.

## Constraints
- Respect policy gates and protected paths.

## Files
- `docs/WORKFLOWS.md`
