# SPEC: T-46e3ec2a

## Objective
Update configs/profiles/strict.yaml to explicitly set sandbox.type to "docker" and ensure the E2B sandbox adapter is disabled. Keep other settings unchanged.

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
