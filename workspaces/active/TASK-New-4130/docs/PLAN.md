---
id: TASK-New-4130
type: PLAN
status: COMPLETED
target_files: [src/agentic/core/llm/base.py, src/agentic/core/llm/providers/ollama.py, src/agentic/core/llm/providers/__init__.py, src/agentic/core/llm/provider_factory.py, src/agentic/core/llm/__init__.py, scripts/run_orchestrator.py, docs/specs/STABLE_VNEXT_ROADMAP.md]
---
# Provider Abstraction + Fallback Plan

## Goal
Introduce a manual provider abstraction with capability detection and fallback chain, while keeping LiteLLM optional.

## Scope
- Add BaseProvider protocol + ProviderCapabilities.
- Implement OllamaProvider (httpx).
- Add ProviderFactory to choose provider with fallback API -> CLI -> Ollama.
- Wire run_orchestrator to use ProviderFactory for planner choice.
- Keep LiteLLM provider optional and not default.

## Out of Scope
- Full API provider implementations beyond stubs.
- Langfuse integration (separate task).

## Steps
1) Define provider interfaces and capability model.
2) Implement OllamaProvider (local httpx) with capability flags.
3) Add ProviderFactory with fallback selection.
4) Update run_orchestrator to use ProviderFactory for planner choice.
5) Add minimal docs note in Stable vNext roadmap.

## Success Criteria
- Manual provider abstraction exists and compiles.
- OllamaProvider used by default.
- Fallback chain defined and selectable by flag.
- LiteLLM remains optional.

## Risks
- Provider selection mismatch with existing router.
- Planner expectations for structured output.

## Rollback
- Revert new provider layer and restore previous planner wiring.
