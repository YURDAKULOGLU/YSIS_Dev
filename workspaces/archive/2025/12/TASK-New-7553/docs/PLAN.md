---
id: TASK-New-7553
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-28T23:30:00
target_files:
  - src/agentic/core/observability/tracer.py
  - src/agentic/core/llm/litellm_provider.py
  - requirements.txt
---

# Task: Implement Langfuse Observability (TASK-New-7553)

## Objective
To provide full visibility into the AI system's execution by integrating **Langfuse**. This will allow us to trace LLM calls, costs, latency, and errors across the entire orchestration loop.

## Approach
We will implement a lightweight wrapper around the Langfuse SDK and inject it into the `UniversalLLMProvider`. We will use a "Singleton" pattern for the tracer to ensure efficient connection management.

## Steps
1.  **Install SDK:** Add `langfuse` to `requirements.txt`.
2.  **Create Tracer Module:** `src/agentic/core/observability/tracer.py`.
    - Handles initialization (API keys from env).
    - Provides decorators `@trace` for functions.
    - Provides direct `trace()` and `span()` methods.
3.  **Inject into LiteLLM:** Modify `src/agentic/core/llm/litellm_provider.py`.
    - Wrap `generate()` call with a Langfuse span.
    - Log input prompt, model parameters, and output response.
    - Log costs (if available).
4.  **Verify:** Create `scripts/test_tracing.py` to simulate a run and verify trace generation.

## Risks & Mitigations
*   **Risk:** Performance overhead.
*   **Mitigation:** Langfuse uses async background flushing. We will ensure it doesn't block the main thread.
*   **Risk:** Missing API Keys.
*   **Mitigation:** If keys are missing, the tracer will gracefully degrade (no-op) without crashing the app.

## Acceptance Criteria
- [ ] `langfuse` installed.
- [ ] `Tracer` class implemented with no-op fallback.
- [ ] `UniversalLLMProvider.generate` automatically creates traces.
- [ ] Test script confirms trace creation.
