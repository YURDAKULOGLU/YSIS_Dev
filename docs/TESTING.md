# TESTING (Golden + Regression)

References:
- CONSTITUTION.md
- CODE_STANDARDS.md

## Baseline
- Unit tests: contracts, syscalls validation, gates decisions
- Integration tests: control-plane + workflow skeleton
- E2E smoke: docker sandbox run (minimal)

## Quick Commands
- Run unit tests: `python scripts/run_tests.py unit`
- Run integration tests: `python scripts/run_tests.py integration`
- Run e2e tests: `python scripts/run_tests.py e2e`

## Golden tests
Golden tests assert deterministic outcomes:
- given a known diff + policy => gate decision stable
- given known verifier outputs => routing decisions stable

Golden tests are required for:
- gates changes
- approval rules changes
- protected paths policy changes

## Regression strategy
- keep a small suite of "canonical tasks" that must always complete
- record expected artifacts and statuses

