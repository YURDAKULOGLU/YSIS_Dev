# System External Gaps (Outside-In Assessment)

**Date:** 2026-01-09  
**Scope:** Outside-in view of YBIS maturity and missing capabilities.

## Executive Snapshot

This assessment focuses on what a new contributor, integrator, or evaluator sees
first: entry points, operational clarity, and proof of reliability. The gaps
below represent blockers to adoption and confidence rather than internal
implementation details.

## High-Impact Gaps

1. **Canonical entry point is unclear**
   - Multiple run scripts exist and documentation does not converge on one
     authoritative runner.
   - Impact: onboarding friction, inconsistent usage, and conflicting guidance.

2. **Workflow definition layer is missing**
   - The system has a single graph, but no first-class "workflow spec" registry
     for varying task types.
   - Impact: can't express new process styles without editing core code.

3. **Verification quality is not production-grade**
   - E2E and golden tasks exist, but there is no standard suite that proves
     real-world feature work passes (smoke/regression/negative cases).
   - Impact: external trust is limited; regressions will slip.

4. **RAG pipeline is not closed-loop**
   - Scraping and ingest exist, but there is no continuous update + validation
     + retrieval policy with observable quality signals.
   - Impact: memory drifts, low recall precision, unpredictable outputs.

5. **Observability is not demonstrably complete**
   - Dashboard is not wired to real data; status/health visibility is weak.
   - Impact: external operators cannot confirm system health or diagnose issues.

## Medium-Impact Gaps

6. **Documentation drift controls are weak**
   - Too many docs with overlapping rules; "single source of truth" is not
     enforced.
   - Impact: stale instructions and conflicting guidance.

7. **Adapter lifecycle governance is incomplete**
   - Registry exists, but deprecation, compatibility, and version pinning
     policies are not enforced consistently.
   - Impact: adapter sprawl and breaking changes over time.

8. **One-command bootstrap is missing**
   - A clean, deterministic "install and run" path is not clearly documented.
   - Impact: trials fail early; reproducibility is poor.

## Lower-Impact Gaps (Still Visible)

9. **Security boundaries are not enforced end-to-end**
   - Threat model exists but runtime enforcement is not consistently visible.
   - Impact: external reviewers question safety guarantees.

10. **Dogfooding example is not production-ready**
   - A real internal product built by the system itself (e.g., dashboard) is
     incomplete.
   - Impact: no flagship proof that the factory builds itself.

## Recommended Next Steps (Outside-In)

1. **Canonical Runner + Entry Doc**
   - Decide the single runner script and name it in `README.md`.
   - Add a short "Quickstart" section with one command path.
   - Remove or clearly mark legacy runners in docs.

2. **Workflow Registry (Adapter-First)**
   - Define a workflow schema (JSON/YAML) for nodes, edges, and artifacts.
   - Add `WorkflowRegistry` and `WorkflowRunner` (no changes to core graph).
   - Ship at least two workflows: `ybis_native`, `speckit_flow`.

3. **Verification Suite (Smoke + Regression)**
   - Create a smoke suite that runs in <5 minutes and blocks on failures.
   - Add a regression suite with golden tasks for core flows.
   - Gate on pass rate, not just report generation.

4. **RAG Closed Loop**
   - Standardize doc ingestion paths for `Frameworks` and `Vendors`.
   - Add validation reports (missing docs, duplicates, stale versions).
   - Define a retrieval policy (collection name, top-k, required sources).

5. **Dogfood Product**
   - Finish the internal dashboard using real artifacts and DB.
   - Add a minimal UI smoke test and data checks.
   - Make it the default example in docs.
