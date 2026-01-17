---
id: STABLE_VNEXT_CHECKLIST
type: CHECKLIST
status: DRAFT
---
# Stable vNext Milestone Checklist

## Milestone A: Spine Stable
- [ ] Single entrypoint (scripts/run_orchestrator.py)
- [ ] Wrapper runners only
- [ ] Canonical brain path referenced everywhere
- [ ] Workflow registry is source of truth
- [ ] Onboarding docs aligned

## Milestone B: Observability + Provider Backbone
- [ ] GenericTracer interface
- [ ] Langfuse adapter with toggle + masking
- [ ] Provider abstraction with capability detection
- [ ] Fallback chain API -> CLI -> Ollama

## Milestone C: Trinity Activated
- [ ] Structured outputs enabled for supported providers
- [ ] Prompt caching enabled where available
- [ ] Extended thinking enabled where available
- [ ] Metrics collected (cost/latency/parse errors)

## Milestone D: Execution Discipline
- [ ] ACI allowlist enforced
- [ ] Playwright automation for docs/E2E
- [ ] scripts/automation/run_playwright_scrape.py available

## Milestone E: Intelligence + Memory
- [ ] Code graph ingestion (tree-sitter -> Neo4j)
- [ ] Spec Kit (SDD) pipeline

## Milestone F: Enterprise Stabilization
- [ ] Testcontainers for Neo4j/Redis
- [ ] Opik evaluation framework
- [ ] OpenTelemetry integrated

## Release Gate: Stable vNext
- [ ] MCP-first workflow enforced
- [ ] Artifacts mandatory (PLAN/RUNBOOK/EVIDENCE/CHANGES/META)
- [ ] Golden tasks core subset pass
