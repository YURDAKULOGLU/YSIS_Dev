# Master Gap List (System-Wide)

**Purpose:** Consolidated view of remaining system needs and missing capabilities.
**Scope:** Workflow, quality, RAG, adapters, ops, observability, docs governance.

---

## 1) Workflow-Defined System

- Workflow-first usage is not fully enforced (legacy graph fallback still used).
- YAML workflows exist but core usage is not fully switched to them everywhere.

## 2) Quality Gates & Tests

- Smoke/regression suites for real-world tasks are missing.
- Dashboard and dogfooding tests are incomplete.
- Gate relies on limited verifier signals in some profiles.

## 3) RAG Closed Loop

- Scrape + ingest exists, but no freshness/drift validation.
- Retrieval policy not standardized (collections, top-k, scope).
- Vendor doc updates not automatically re-ingested.

## 4) Adapter Lifecycle

- Deprecation/migration/version pinning policy not enforced.
- Adapter conformance tests cover basics but not lifecycle behaviors.

## 5) Bootstrap & Ops

- One-command bootstrap exists but lacks post-install validation.
- No single “health check” command for runtime sanity.

## 6) Observability

- Dashboard is not fully wired to real data.
- Telemetry pipelines (Langfuse/OTel) are optional but not turnkey.

## 7) Documentation Governance

- Doc graph lint not enforced as a gate.
- Single source of truth exists but drift control is not automated.

## 8) Workflow Evolvability

- EvoAgentX/aiwaves/self-improve adapters are planned, not implemented.
- No automated evaluation loop for workflow evolution.

---

## Summary

Core architecture direction is set; remaining gaps are operational and
workflow/evolution execution. These should be prioritized before feature
expansion to avoid systemic drift.

---

## Executor Task List

### Task A: Enforce Workflow-First
- Remove legacy fallback usage from primary run paths.
- Ensure all executions load YAML workflow specs.
- Add validation that workflow_name is always present.

### Task B: Real-World Quality Gates
- Add smoke test suite (fast, blocking).
- Add regression suite with golden tasks.
- Make gate fail if smoke suite fails.

### Task C: RAG Closed Loop
- Add freshness/drift validation for docs.
- Standardize retrieval policy (collection, top-k, scope).
- Add scheduled re-ingest workflow.

### Task D: Adapter Lifecycle Policy
- Add deprecation/version policy doc and enforcement.
- Extend conformance tests with lifecycle checks.

### Task E: Bootstrap Health Check
- Add `scripts/health_check.py` or equivalent.
- Run after bootstrap to validate DB + adapters + workflow specs.

### Task F: Observability Wiring
- Wire dashboard to real artifacts and DB data.
- Add minimal UI smoke test.

### Task G: Doc Governance Gate
- Add doc graph lint to gate/CI.
- Fail if missing references or broken links.

### Task H: Workflow Evolution
- Implement EvoAgentX/aiwaves/self-improve adapters.
- Add evaluation loop workflow spec.
