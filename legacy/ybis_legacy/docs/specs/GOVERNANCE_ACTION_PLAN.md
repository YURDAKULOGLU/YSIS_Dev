# Governance Action Plan
> Goal: Stabilize governance, eliminate drift, and enforce disciplined execution.

## Phase 0: Align on Canonical Sources (Now)
- Confirm `docs/governance/YBIS_CONSTITUTION.md` as the single authority.
- Declare `scripts/run_orchestrator.py` as the only execution entrypoint.
- Confirm `src/agentic/core/graphs/orchestrator_graph.py` as the only brain path.

Deliverables:
- Constitution updated and announced.
- Any duplicate or conflicting references flagged for cleanup.

## Phase 1: Enforcement and Tooling (Week 1)
- Ensure `scripts/protocol_check.py` is required before completion.
- Enforce artifact mode: lite by default, full for risk:high.
- Update `scripts/ybis.py` claim flow to remind artifact mode (already done).
- Publish messaging guideline to reduce filler tokens.

Deliverables:
- Verified enforcement in `scripts/ybis.py` and `scripts/protocol_check.py`.
- Example: one completed task validated in both lite and full modes.
- `docs/governance/MESSAGING_GUIDELINE.md` published and referenced.

## Phase 2: Documentation Convergence (Week 1-2)
- Audit docs for conflicting paths and rules.
- Remove or amend references that conflict with the constitution.
- Update onboarding docs to point to the constitution and the single runner.

Deliverables:
- All onboarding references point to the single spine and constitution.
- A short "Where to start" section in onboarding docs.

## Phase 3: Quality and Verification Standard (Week 2 - COMPLETED)
- Define baseline verification for each task type (code, docs, infra).
- Add a simple checklist to RESULT for manual verification.
- Define risk:high triggers (security, infra, core orchestration, external I/O).

Deliverables:
- **[Verification Standards](../governance/VERIFICATION_STANDARDS.md)**
- **[Risk Classification Matrix](../governance/RISK_MATRIX.md)**
- **[Manual Verification Template](../governance/templates/MANUAL_VERIFICATION.md)**

## Phase 4: Framework Intake Discipline (Week 2-3 - COMPLETED)
- Create a standard intake checklist for new frameworks:
  scope, docs, integration approach, rollback, monitoring, tests.
- Require one debate vote before production wiring.

Deliverables:
- **[Framework Intake Checklist](../governance/templates/FRAMEWORK_INTAKE.md)**
- **[Framework Tiers & Voting](../governance/FRAMEWORK_TIERS.md)**


## Open Questions (Decision Needed)
1. Should LiteLLM remain optional by default for V1?
2. Who is the governance owner for constitution updates?
3. What is the minimal test bar per task class?
