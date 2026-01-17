---
id: ENTERPRISE_STABILIZATION
type: SPEC
status: DRAFT
---
# Enterprise Stabilization

## Objective
Provide safe stubs and templates for Testcontainers, Opik evaluation, and OpenTelemetry.

## Testcontainers
- Dependency: testcontainers (Python)
- Usage: run `TESTCONTAINERS_SMOKE=1 pytest tests/integration/test_testcontainers_smoke.py`
- Target: add Neo4j/Redis containers when CI is available

## Opik
- Dependency: opik SDK (optional)
- Integration plan: wrap evaluation calls behind a lightweight adapter
- Default: no-op when SDK missing

## OpenTelemetry
- Dependency: opentelemetry-sdk
- Helper: src/agentic/core/plugin_system/observability.py
- Default: Console exporter for local testing

## Next Steps
1) Add optional dependencies to requirements when approved.
2) Wire tracing into LLM provider layer.
3) Expand integration tests to use containers.
