# Feature Implementation Task
**Type:** Orchestration
**Required Agent:** Architect (Tier 3) -> Developer (Tier 2) -> QA
**Context:** Tier 3 Orchestration

## Objective
Implement a new feature from start to finish, based on a PRD or detailed requirement.

## Workflow Steps
1.  **Architectural Design (Architect):**
    *   Read PRD and Tech Stack docs.
    *   Create a mini-design doc (interfaces, DB schema changes).
    *   Break down into sub-tasks (JSON format).
2.  **Implementation Loop (Developer):**
    *   For each sub-task:
        *   Write Code (Sandbox).
        *   Write Unit Tests.
        *   Pass Lint/Type checks.
3.  **Integration (QA):**
    *   Verify all sub-tasks work together.
    *   Run integration tests.
4.  **Handoff:**
    *   Prepare PR description.

## Inputs
- `requirement_doc`: Path to PRD or issue description.
- `feature_name`: Name of the feature.

## Success Criteria
- [ ] Feature meets requirements.
- [ ] Code follows `YBIS_STANDARDS_CHEATSHEET.md`.
- [ ] Tests passed.
