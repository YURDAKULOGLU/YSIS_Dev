# SPEC: T-d5191e37

## Objective
ONLY edit configs/profiles/strict.yaml: set sandbox.type to "docker" under sandbox section. Do NOT modify any other files. Do NOT use sed/grep/find. Use only the editor tool. Do NOT run tests or lint; verifier will handle gates. If sandbox.type already present, update value. If missing, insert with correct indentation. Output only the edit.

## Requirements
- Implement the objective exactly as stated.
- Keep changes scoped to the identified files.

## Acceptance Criteria
- Required files are created or updated.
- Verifier passes under the active profile.

## Constraints
- Respect policy gates and protected paths.

## Files
- `configs/profiles/strict.yaml`
