---
id: STABLE_VNEXT_ROADMAP
type: SPEC
status: DRAFT
---
# Stable vNext Roadmap

## Objective
Deliver a stable, MCP-first system with controlled provider adoption, full observability, and low drift.

## Guiding Principles
- Single entrypoint and single brain path
- MCP-first tooling (tasks, messaging, debate)
- Provider abstraction with safe fallback
- Observability before expansion
- Artifacts required for every run

## Phase 0: Stabilization (1-3 days)
Goal: eliminate drift and lock the execution spine.

Scope:
- Single entrypoint: scripts/run_orchestrator.py (constitutional requirement - ONLY runner)
- Legacy wrappers deprecated: run_next.py, run_production.py (use --mode flags instead)
- Canonical brain: src/agentic/core/graphs/orchestrator_graph.py
- Workflow registry as source of truth
- Onboarding docs aligned

Owner: Codex
Exit criteria:
- One entrypoint, one brain path
- Onboarding docs have no drift
- Workflow registry present

## Phase 1: Observability + Provider Backbone (1 week)
Goal: see every LLM call and control provider selection.

Scope:
- GenericTracer interface
- Langfuse adapter with toggles and masking
- Provider abstraction with capability detection
- Fallback chain: API -> CLI -> Ollama
- Provider mode flags: YBIS_PROVIDER_MODE / YBIS_PLANNER_MODE

Owners:
- Langfuse: Gemini
- Provider backbone: Codex

Exit criteria:
- Traces for LLM calls are visible
- Provider selection is controllable by flag
- Ollama fallback always works

## Phase 2: Optimization Trinity (1-2 weeks)
Goal: activate structured outputs, caching, extended thinking.

Scope:
- Claude-only activation with feature detection
- Planner wiring to provider
- Metrics for cost/latency/parse errors

Owner: Claude
Exit criteria:
- Structured output errors minimized
- Caching cost reduction observed
- No regression in verifier pipeline

## Phase 3: Execution Discipline (2-3 weeks)
Goal: safer, repeatable execution.

Scope:
- SWE-agent ACI pattern (allowlist commands, sandbox)
- Playwright automation for docs and E2E

Owners:
- ACI: Claude
- Playwright: Codex

Exit criteria:
- Constrained execution improves reliability
- E2E checks available

## Phase 4: Intelligence + Memory (3-4 weeks)
Goal: risk-aware coding and spec-first flow.

Scope:
- Tree-sitter -> Neo4j code graph ingestion
- Spec Kit (SDD) pipeline

Owners:
- Graph: Gemini
- Spec Kit: Claude

Exit criteria:
- Plans include graph impact signals
- Spec-first workflow available

## Phase 5: Enterprise Stabilization (4+ weeks)
Goal: production-grade testing and telemetry.

Scope:
- Testcontainers for Neo4j/Redis
- Opik eval framework
- OpenTelemetry traces/metrics/logs

Owner: Codex
Exit criteria:
- Integration tests reproducible
- Observability stack complete

## Release Gate: Stable vNext
Must-have:
- Single entrypoint and single brain path
- MCP-first workflow
- Provider abstraction + fallback
- Langfuse tracing on (sampling allowed)
- Artifacts mandatory and present
- Golden tasks core subset pass
