18 olarak# CODE STANDARDS

References:
- CONSTITUTION.md
- TESTING.md

## Python
- Python >= 3.11 (recommended 3.12)
- Type hints required for public functions/classes
- Async I/O uses anyio or asyncio consistently

## Formatting / Linting
- Ruff is the single source for formatting + linting
- Line length: 100
- Imports sorted by Ruff

## Typing
- mypy strict (incremental relax only by explicit decision)
- No untyped public APIs

## Tests
- pytest required for any behavior change
- tests layout:
  - tests/unit
  - tests/integration
  - tests/e2e (smoke)
  - tests/golden (stable behavior)
- Any gate logic change must include golden test coverage

## Logging
- Use structured JSONL logs for runs (events + logs)
- Do not print ad-hoc logs without journaling

## Git hygiene
- Keep commits small and evidence-backed
- Protected paths require approval

