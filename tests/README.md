# 🛡️ The Guard (Testing Strategy)

> **Zone:** Verification & Quality Assurance
> **Access:** Mandatory for every Task

## Philosophy: "Test-First"
You cannot fix what you cannot measure.

## Structure

```
tests/
├── unit/           # Fast, isolated tests (pytest)
├── integration/    # Component interaction tests
└── e2e/            # Full system graph simulation
```

## How to Verify
Use the Sentinel's standard invocation:
```bash
python scripts/smart_exec.py "pytest tests/unit/"
```

## Rules
1. **New Feature?** -> Add `tests/unit/test_feature.py`.
2. **Bug Fix?** -> Add regression test.
3. **Mocking:** Use mocks for LLM calls (Aider) to save money/tokens.
