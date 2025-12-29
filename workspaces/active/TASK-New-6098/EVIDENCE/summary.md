# Evidence

## Commands
- Get-Content -Raw src/agentic/core/plugin_system/observability.py
- Get-Content -Raw tests/integration/test_testcontainers_smoke.py
- Get-Content -Raw docs/specs/ENTERPRISE_STABILIZATION.md

## Notes
- Added OpenTelemetry helper with safe no-op when deps missing.
- Added Testcontainers smoke test template gated by TESTCONTAINERS_SMOKE.
- Added enterprise stabilization spec.
