# Remaining Gaps (Legacy vs New) - Grand Document

This document is the single append-only grand record of remaining gaps, decisions,
and readiness criteria. It should be updated as tasks complete or new gaps appear.

## 1) CI/CD and Release Pipeline
- ✅ Standard enforcement CI exists (`.github/workflows/enforcement.yml`)
- ✅ Release/publishing workflow exists (`.github/workflows/release.yml`) with blocking CVE checks
- ✅ Artifact publishing and release tagging workflow implemented

## 2) DB/Migrations Parity
- Legacy messaging/debate storage schemas are not represented in new core DB migrations.
- Migration strategy for legacy task/state data is undefined.
- Versioned schema ownership and rollback policy are unclear.

## 3) Security & Permissions
- Secret management and rotation practices are not implemented as first-class services.
- Sandbox policy enforcement is local-first but lacks audited permission profiles.
- Approval workflows exist but are not wired to external auth/identity.

## 4) Ops/Observability
- Event bus + health monitor services exist; backends/retention not standardized.
- Trace ID propagation exists; centralized collection/retention still undefined.
- Health checks exist; SLA targets not defined.

## 5) Test Strategy Coverage
- Unit/integration coverage is uneven across adapters and services.
- Golden tests exist but do not cover all critical workflows.
- E2E suite relies on local LLM assumptions; CI-safe profile exists but is not wired into CI.     

## 6) Dependency & Packaging
- Adapter dependencies are grouped as installable extras with pinned versions.
- CVE scan exists; license/supply-chain audit workflow still missing.

## 7) Docs as Source / Compliance
- Spec compliance workflow exists; must be adopted consistently across changes.
- No automatic doc generation/update policy from changes.
- Versioning and audit trail for specs/architecture docs needs definition.

## 8) CLI/Operator Tooling
- Legacy operator scripts are not fully mapped to new core workflows.
- New CLI UX is fragmented (multiple scripts with overlapping intent).
- Runbooks for common operations are missing or outdated.

## 9) Data Retention & Governance
- Retention and purge policies exist; enforcement beyond runs/artifacts is still minimal.
- Governance rules are defined but not enforced across all data stores.

## Next Action
- Use this list as input for enforcement, operations, and adapter lifecycle work.

---

## Discipline Controls (Prevent Legacy Drift)

1) **Adapter-First Enforcement**
- New capabilities must be integrated via adapters to open-source tools.
- Legacy code is read-only reference; no direct copy or port.

2) **Core Boundary Rules**
- Core includes only policy, gates, syscalls, contracts.
- Services/adapters live outside core; no cross-cutting logic in core.

3) **Protected Paths + Approvals**
- Changes to protected paths require explicit approval.
- Gate must fail closed when approval artifacts are missing.

4) **Policy-Gated Features**
- All optional subsystems behind policy toggles.
- Default profile must be warning-free and local-first.

5) **Deterministic Evidence**
- Verifier + gate reports are mandatory for success.
- Artifacts must be deterministic and stored per run.

6) **Dependency Discipline**
- Adapter dependencies are explicit extras with pinned versions.
- License/CVE checks required before enabling new adapters.

7) **Spec-First Compliance**
- No code changes without spec/plan linkage.
- Spec compliance score must be recorded and gated.

8) **CI & Review Guardrails**
- CI must run gates and critical tests.
- Codeowner review for core paths.

9) **Docs-as-Source**
- Changes to behavior require doc updates.
- Specs and architecture docs versioned and audited.

---

## Additional Gaps (Full-Spectrum Scan)

### Infra & Deployment
- No standardized deployment targets (local, server, container, k8s) documented.
- Missing operational runbooks for deploy/rollback/upgrade.
- No environment parity checks between dev/staging/prod.

### Identity, Auth, Access Control
- No unified auth/RBAC model for MCP or worker actions.
- Approval workflow not tied to identity verification.

### Secrets & Config Hygiene
- Secrets management/rotation not centralized.
- Config validation and schema enforcement are weak or absent.

### Data Governance & Retention
- No explicit retention and purge policy for runs/artifacts.
- Audit trails exist but lack governance-level retention/immutability policy.

### Observability & Telemetry
- No unified metrics/trace/log backend choice.
- No telemetry retention or alerting thresholds defined.

### Performance & Scalability
- No load/perf test suite or baseline SLOs.
- No request throttling/rate limiting for MCP tools.

### API Versioning & Compatibility
- MCP tool versioning and backward-compat policy not defined.
- Artifact schema migration policy not enforced in CI.

### Adapter Lifecycle
- Conformance tests exist; certification/compatibility matrix still missing.

### Sandbox & Isolation Hardening
- Sandbox profiles are not validated against known-good matrices.
- Worktree cleanup/garbage collection policy undefined.

### Docs Automation
- ✅ Doc graph generator exists (`scripts/build_doc_graph.py`) and runs in CI.
- Missing doc references still present; review `docs/reports/doc_graph.md`.
- No automated docs refresh or change detection pipeline.
- Missing standard doc templates for new adapters/tools.

### Incident Response
- No incident workflow (severity, escalation, postmortem templates).

---

## Enforcement Follow-Ups (Post-Implementation Gaps)

### Adapter Policy Coverage
- ✅ Policy profiles declare adapters explicitly (`default.yaml`, `e2e.yaml` have `adapters` section)
- ✅ Defaults are explicit per environment (opt-in model: `enabled: false` by default)
- ✅ Canonical adapter list exists (`configs/adapters.yaml`); doc references still needed

- ✅ Registry and bootstrap exist (`src/ybis/services/adapter_bootstrap.py`)
- ✅ Adapters are registered (executors, sandboxes, vector stores, graph stores, event bus)
- ⚠️ Ensure required adapters are registered per workflow (validation needed)
- ⚠️ Add automated validation for required adapter sets (CI check needed)

### Spec Validation Artifacts
- ✅ `spec_validation.json` is generated via `generate_spec_validation_artifact()` (Task B complete)
- ⚠️ Ensure semantic validation reliability and CI stability (ongoing)

### Core Boundary Violations (Code Fixes Needed)
- Core modules with direct adapter/service imports must be refactored to use registry/DI.
- Lint now detects these violations; remediation tasks are pending.

### ~~CI Adapter Tests Are Non-Blocking (Action Required)~~ ✅ **FIXED**
- ✅ Adapter conformance tests are now blocking in `.github/workflows/enforcement.yml`
- ✅ `continue-on-error: false` ensures failures fail CI
- ✅ Regressions are now visible and block CI

---

## Self-Improving Factory: Readiness Criteria & Timeline Signals

### What “Self-Improving Factory” Means Here
- The system can create its own tasks, execute changes, verify evidence, and gate itself without manual babysitting.
- Evolution is policy-driven, adapter-first, and produces auditable artifacts by default.

### Minimum Readiness Criteria (Must Be True)
1) **Enforcement Automation**
   - Core boundary lint + CI gates are mandatory and blocking.
   - Spec compliance is validated (not stubbed) and enforced in gates.

2) **Adapter-First Infrastructure**
   - Adapter registry is populated and policy-driven (opt-in with explicit enablement).
   - Core is free of direct adapter/service imports.

3) **Evidence-First Loop**
   - Verifier + gate pass required for “done”.
   - Artifact generation is deterministic and covers spec compliance + security.

4) **Operational Safety**
   - Sandbox isolation validated against known-good profiles.
   - Worktree cleanup/GC policy defined and enforced.

5) **CI & Review Discipline**
   - Protected paths require approval + codeowner review.
   - CI enforces gates and core boundary lint on every merge.

### When We’re “In the Zone”
- Spec validation produces `spec_validation.json` consistently.
- Adapter registry non-empty with defined defaults per profile.
- MCP server runs with full tool surface behind policy gating.
- E2E golden suite passes under CI-safe profile.
- Zero core boundary lint violations.

### Current Blockers (As of Now)
- ⚠️ Adapter catalog + conformance tests exist but are not enforced as blocking in CI.
- ⚠️ CI-safe E2E profile missing (e2e.yaml exists but may need refinement).
- ⚠️ Core boundary violations still present in code (lint detects, refactoring pending - see `docs/CORE_BOUNDARY_REFACTOR_PLAN.md`).

### Expected Transition Point
- The system enters “self-improving factory” mode after:
  - Spec validation is implemented end-to-end,
  - Adapter registry is live and policy-driven,
  - CI/gates are strictly enforced,
  - Golden E2E passes in CI profile.

---

## Adapter Ecosystem (Target State + Gaps)

### Target State
- A catalog of adapters with clear ownership, maturity, and policy defaults.
- Adapters are installed and enabled via policy (opt-in).
- Each adapter declares its dependencies, health checks, and tests.
- Core never imports adapters directly; all access via registry.

### Current Gaps
- ✅ Adapter catalog exists (`configs/adapters.yaml`) but needs doc references.
- ✅ Registry exists and adapters are registered via `bootstrap_adapters()` (opt-in via policy).
- ⚠️ Adapter conformance tests exist but are not enforced as blocking in CI.
- ✅ Policy profiles have explicit adapter enablement list (`default.yaml`, `e2e.yaml`).
- ⚠️ No adapter lifecycle policy (deprecation, version pinning, CVE response).

### Required Artifacts (Adapter Discipline)
1) `configs/adapters.yaml` (catalog: name, type, owner, maturity, deps)
2) `tests/adapters/` (conformance tests per adapter type)
3) `docs/adapters/` (per-adapter usage + policy examples)
4) Policy profiles with explicit adapter enablement (opt-in)

### Evolving System Implications
- Adapter catalog becomes the source of truth for integration scope.
- Policy defines which adapters can run per environment.
- CI validates adapter conformance before enabling.

---

## Grand Task List (Remaining Gaps)

**Rules:** Adapter-first. No legacy code copy. Core stays minimal. Policy-gated.

### Task 1: Adapter Catalog & Registry Population
**Status:** ✅ **COMPLETED**
**Objective:** Make adapter ecosystem explicit and enforceable.
**Deliverables:**
- ✅ `configs/adapters.yaml` catalog (name, type, owner, maturity, deps) - **8 adapters cataloged**
- ✅ `src/ybis/services/adapter_catalog.py` - Catalog loader and validator
- ✅ Register adapters from catalog in `bootstrap_adapters()` (catalog-first, fallback to hardcoded)
- ✅ Policy profiles have explicit adapter enablement (`default.yaml`, `e2e.yaml`)

### Task 2: Adapter Conformance Tests
**Status:** ✅ **COMPLETED**
**Objective:** Prevent unstable adapters from entering production.
**Deliverables:**
- ✅ `tests/adapters/` conformance tests per adapter type
  - ✅ `test_adapter_protocol.py` - Protocol conformance tests
  - ✅ `test_executor_adapters.py` - Executor adapter tests
  - ✅ `test_vector_store_adapters.py` - Vector store adapter tests
  - ✅ `test_graph_store_adapters.py` - Graph store adapter tests
  - ✅ `test_sandbox_adapters.py` - Sandbox adapter tests
  - ✅ `test_event_bus_adapters.py` - Event bus adapter tests
- ✅ CI job to run adapter tests before enabling (`.github/workflows/enforcement.yml` - blocking)

### Task 3: Adapter Lifecycle Policy
**Status:** ✅ **COMPLETED**
**Objective:** Control deprecation, version pinning, and CVE response.
**Deliverables:**
- ✅ `docs/adapters/LIFECYCLE_POLICY.md` - Complete lifecycle policy document
- ✅ Dependency pinning strategy in `pyproject.toml` (optional-dependencies per adapter)
- ✅ `scripts/check_adapter_cves.py` - CVE scanning script
- ✅ Catalog validation for deprecated adapters and CVE status

### Task 4: CI/Release Enforcement
**Status:** ✅ **COMPLETED**
**Objective:** Ensure enforcement is mandatory across environments.
**Deliverables:**
- ✅ CI gates for core boundary lint, adapter registry checks, and spec validation (`.github/workflows/enforcement.yml`)
- ✅ `.github/CODEOWNERS` - Protected path codeowner rules
- ✅ `.github/workflows/release.yml` - Release workflow with enforcement checks
- ✅ Adapter catalog validation in CI
- ✅ Adapter conformance tests in CI
- ✅ CVE checking in release workflow

### Task 5: Spec Validation Artifact Generator
**Status:** ✅ **COMPLETED** (Task B)
**Objective:** Produce `spec_validation.json` so gates can enforce spec compliance.
**Deliverables:**
- ✅ Spec validation nodes (`validate_spec_node`, `validate_plan_node`, `validate_impl_node`)
- ✅ `spec_validation.json` artifact per run (via `generate_spec_validation_artifact()`)
- ✅ Full spec parsing, plan validation, implementation validation, LLM semantic validation

### Task 6: Adapter Docs & Examples
**Status:** ✅ **COMPLETED**
**Objective:** Make adapters usable without tribal knowledge.
**Deliverables:**
- ✅ `docs/adapters/README.md` - Adapter documentation index
- ✅ `docs/adapters/local_coder.md` - Local Coder usage guide
- ✅ `docs/adapters/e2b_sandbox.md` - E2B Sandbox usage guide
- ✅ `docs/adapters/neo4j_graph.md` - Neo4j Graph usage guide
- ✅ Integration guide in `docs/ADAPTER_REGISTRY_GUIDE.md`

### Task 7: Observability Backends (Adapter)
**Status:** ✅ **COMPLETED**
**Objective:** Provide standard metrics/logs/tracing via adapters.
**Deliverables:**
- ✅ `src/ybis/services/observability.py` - Unified observability service
- ✅ `src/ybis/adapters/observability_langfuse.py` - Langfuse adapter
- ✅ `src/ybis/adapters/observability_opentelemetry.py` - OpenTelemetry adapter
- ✅ Adapters registered in catalog and bootstrap
- ✅ Policy-driven enablement

### Task 8: Sandbox Profile Validation
**Status:** ✅ **COMPLETED**
**Objective:** Guarantee safety across local/sandbox profiles.
**Deliverables:**
- ✅ `docs/governance/SANDBOX_PROFILE_MATRIX.md` - Known-good profile matrix with safety guarantees
- ✅ `scripts/validate_sandbox_profiles.py` - Automated validation script
- ✅ CI integration in `.github/workflows/enforcement.yml`

### Task 9: Data Retention & Governance
**Status:** ✅ **COMPLETED**
**Objective:** Define retention policies for runs/artifacts and enforce them.
**Deliverables:**
- ✅ `docs/governance/DATA_RETENTION_POLICY.md` - Complete retention policy document
- ✅ `scripts/enforce_retention_policy.py` - Retention enforcement script
- ✅ CI check for policy drift in `.github/workflows/enforcement.yml`
