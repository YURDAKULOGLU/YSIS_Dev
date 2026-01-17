# SPEC: T-61aec807

## Objective
Normalize executor_report files_changed to project-relative paths so spec validation correctly detects overlap. Update spec validation to handle worktree/absolute paths when comparing spec files to modified files. Keep changes scoped to executor and spec validation logic.

## Requirements
- Implement the objective exactly as stated.
- Keep changes scoped to the identified files.

## Acceptance Criteria
- Required files are created or updated.
- Verifier passes under the active profile.

## Constraints
- Respect policy gates and protected paths.

## Files
- `TBD`
