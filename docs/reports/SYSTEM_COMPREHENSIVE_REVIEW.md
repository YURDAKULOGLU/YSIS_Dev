---
id: SYSTEM_COMPREHENSIVE_REVIEW
type: REPORT
status: DRAFT
---
# Comprehensive System Review (YBIS)

## Executive Summary
YBIS has strong unique capabilities (multi-LLM council, Neo4j dependency graph,
memory, self-modification). However, the system currently suffers from drift
between docs, entrypoints, and brain paths; inconsistent artifact discipline;
and unclear provider/feature gating. The fastest path to a stable, scalable
platform is a strict onboarding protocol, a single execution spine, and hard
gates for artifacts and policy. This report provides an objective review,
risks, and a disciplined action plan.

---

## What YBIS Gets Right (Strengths)
1) Multi-LLM Council
   - Differentiator: consensus-based decisions with multiple model viewpoints.
   - Useful for architecture/design and risk assessment.

2) Neo4j Dependency Graph
   - Impact analysis is rare in agentic systems.
   - Enables risk-aware planning and regression avoidance.

3) Local-first + Cloud fallback vision
   - Strategic: retains autonomy while enabling higher quality on demand.

4) Artifact discipline (conceptually strong)
   - PLAN/RUNBOOK/EVIDENCE/CHANGES/META standard is correct in principle.

5) MCP-first direction
   - Good foundation for tooling consistency and agent interoperability.

---

## What Is Broken (Weaknesses)
1) Drift between docs and execution
   - Multiple entrypoints and brain paths described across docs.
   - Onboarding guidance is inconsistent.

2) Incomplete artifact enforcement
   - Tasks marked complete without required artifacts.
   - Completion gate not enforced everywhere.

3) Provider/feature gating unclear
   - LiteLLM exists but not consistently wired.
   - Optimization Trinity depends on provider features without explicit gating.

4) Parallel orchestration graphs
   - Legacy workflow and core orchestrator co-exist.
   - Split-brain risk and maintenance overhead.

5) Governance gaps
   - Missing or outdated documents referenced by policies.
   - Framework onboarding lacks strict enforcement.

---

## Critical Risks
1) Operational inconsistency
   - Agents choose wrong entrypoint or docs, leading to drift.

2) Silent failure in artifacts
   - Missing evidence undermines auditability and reproducibility.

3) Provider regressions
   - Non-gated feature use can break or degrade tasks.

4) Security/Policy erosion
   - Lack of enforced policy gates invites misuse or leakage.

---

## Root Causes
1) No single source of truth for execution
2) No hard gate for completion artifacts
3) Framework adoption without standardized intake + contracts

---

## Recommended Standard (Non-Negotiable)
### A) Single Execution Spine
- One entrypoint: scripts/run_orchestrator.py
- One brain path: src/agentic/core/graphs/orchestrator_graph.py
- All docs must reference these.

### B) Artifact Hard Gate
- Completion must fail if artifacts are missing.
- Protocol check script must be mandatory.

### C) Framework Onboarding Protocol
Every new framework must include:
1) Intake docs: docs/frameworks/<name>/README snapshot + intake summary
2) Adapter + Contract + Contract Tests
3) Policy requirements (tool allowlist, file allowlist, network)
4) Rollback plan
5) Pilot tasks with metrics

### D) Provider Abstraction with Feature Flags
- Default: manual provider (Ollama) for stability.
- LiteLLM optional via feature flag.
- Feature detection required for caching/structured outputs/thinking.

---

## Objective Evaluation of Suggested Frameworks
### Tier 1 (Critical)
1) Langfuse (Observability)
   - Pros: tracing, cost, prompt versioning, self-hosted
   - Cons: overhead, data masking needed
   - Verdict: adopt with a generic tracer interface + toggle

2) LiteLLM (Provider abstraction)
   - Pros: multi-provider, caching, structured outputs, fallback
   - Cons: external dependency, potential black-box perception
   - Verdict: keep as optional; default to manual provider

3) Aider Git Intelligence
   - Pros: improves diff awareness and commit hygiene
   - Cons: can change workflow semantics
   - Verdict: integrate via adapter and enforce policy gates

### Tier 2 (High Value)
4) SWE-agent ACI
   - Pros: constrained execution, safer interaction
   - Cons: integration effort
   - Verdict: phase after observability + provider stability

5) Playwright
   - Pros: docs scraping, E2E testing
   - Cons: dependency overhead
   - Verdict: add minimal templates now, expand later

### Tier 3 (Nice to Have)
6) MetaGPT Roles
   - Pros: role-based voting
   - Cons: adds complexity
   - Verdict: do after governance is stable

7) Opik / OpenTelemetry / Testcontainers
   - Pros: enterprise readiness
   - Cons: heavy
   - Verdict: final stabilization phase

---

## Current Status Snapshot (Known)
- Orchestrator spine now present.
- Protocol check script added.
- Completion gating added in ybis.py.
- Several tasks completed without artifacts (process enforcement now fixed).
- LiteLLM exists in code but is not default.

---

## Action Plan (Disciplined Path)
### Phase 0 (Now)
- Lock single entrypoint + single brain path
- Gate completion on artifacts (already enforced)
- Require protocol_check at claim and completion

### Phase 1 (Next)
- Langfuse: implement GenericTracer + toggle + masking
- Provider abstraction: manual provider + optional LiteLLM flag

### Phase 2
- Optimization Trinity (Claude only)
- Planner wiring to provider capabilities

### Phase 3
- SWE-agent ACI
- Playwright expansion

### Phase 4
- Code graph ingestion (tree-sitter -> Neo4j)
- Spec-first (SDD) workflow

### Phase 5
- Testcontainers, Opik, OpenTelemetry full rollout

---

## Acceptance Criteria (Stable vNext)
- Single entrypoint and brain path across docs
- MCP-first flow for tasks and messaging
- Observability enabled (sampling ok)
- Provider abstraction and fallback in place
- Artifact enforcement strict
- Golden tasks core subset passing

---

## Open Questions (Need Team Input)
1) Should LiteLLM be default or optional by flag?
2) Which metrics define "go/no-go" for provider rollout?
3) Which tasks are permitted to use external CLI providers?
4) How do we store provider secrets (env, vault, config)?

---

## Requests to Other Agents
- Gemini: confirm Langfuse integration scope and timeline.
- Claude: confirm Optimization Trinity gating plan.
- All: verify frameworks must pass intake protocol before adoption.

---

## Notes
- This report is based on repository inspection and internal debates.
- External research not executed in this report.
