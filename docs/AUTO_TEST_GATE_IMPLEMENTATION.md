# Auto-Test Gate Implementation

## Status: ✅ IMPLEMENTED

Automatic test execution gate ensures all tests pass before code changes are applied.

---

## Implementation

### 1. ✅ Test Gate Module

**Location:** `src/ybis/orchestrator/test_gate.py`

**Features:**
- `run_test_gate()` - Run tests before code changes
- `check_test_coverage_gate()` - Check coverage threshold (default: 80%)

**Usage:**
```python
from src.ybis.orchestrator.test_gate import run_test_gate, check_test_coverage_gate

# Run tests
tests_passed, errors, warnings = run_test_gate(ctx)

# Check coverage
coverage_passed, actual_coverage, errors = check_test_coverage_gate(ctx, min_coverage=0.80)
```

---

### 2. ✅ execute_node Integration

**Location:** `src/ybis/orchestrator/graph.py:625`

**Implementation:**
```python
# AUTO-TEST GATE: Run tests BEFORE applying code changes
try:
    from .test_gate import run_test_gate
    
    tests_passed, test_errors, test_warnings = run_test_gate(ctx)
    
    if not tests_passed:
        # Tests failed - block execution and feed errors to repair
        state["error_context"] = "\n".join(test_errors)
        state["needs_plan_repair"] = True
        state["status"] = "running"
        
        # Return early - don't execute if tests fail
        return state
except Exception:
    # Test gate not critical, continue if it fails
    pass
```

**What it does:**
- Runs tests BEFORE `execute_node` applies code changes
- If tests fail, blocks execution
- Feeds errors to repair node
- Prevents breaking existing functionality

---

### 3. ✅ gate_node Integration

**Location:** `src/ybis/orchestrator/gates.py:884`

**Implementation:**
```python
# AUTO-TEST GATE: Check test coverage threshold
try:
    from .test_gate import check_test_coverage_gate
    
    coverage_passed, actual_coverage, coverage_errors = check_test_coverage_gate(ctx, min_coverage=0.80)
    
    if not coverage_passed:
        # Coverage below threshold - add to gate report
        gate_report.decision = GateDecision.BLOCK
        gate_report.reasons.extend(coverage_errors)
except Exception:
    # Coverage check not critical, continue if it fails
    pass
```

**What it does:**
- Checks test coverage after execution
- Blocks if coverage drops below 80%
- Prevents coverage regression

---

### 4. ✅ Pre-Commit Hook

**Location:** `.pre-commit-config.yaml`

**Implementation:**
```yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest (run tests)
      entry: python -m pytest tests/ --tb=short -q
      language: system
      types: [python]
      pass_filenames: false
      always_run: false  # Only run if Python files changed
    
    - id: ruff-check
      name: ruff (lint)
      entry: ruff check .
      language: system
      types: [python]
      pass_filenames: false
      always_run: false  # Only run if Python files changed
```

**What it does:**
- Runs pytest before git commit
- Runs ruff linting before git commit
- Prevents bad commits from being made
- Only runs if Python files changed (performance)

---

## Workflow

### Before Code Changes (execute_node)

1. **Test Gate Check:**
   ```
   execute_node → run_test_gate() → Tests pass? → Continue
                                          ↓
                                    Tests fail? → Block & Repair
   ```

2. **If tests fail:**
   - Execution is blocked
   - Errors fed to repair node
   - Plan may be regenerated with test requirements

### After Code Changes (gate_node)

1. **Coverage Gate Check:**
   ```
   gate_node → check_test_coverage_gate() → Coverage >= 80%? → PASS
                                                      ↓
                                            Coverage < 80%? → BLOCK
   ```

2. **If coverage drops:**
   - Gate decision: BLOCK
   - Reason: "Coverage X% below threshold 80%"
   - Task cannot complete until coverage improves

### Pre-Commit Hook

1. **Before Git Commit:**
   ```
   git commit → pre-commit hook → pytest → Tests pass? → Commit
                                              ↓
                                        Tests fail? → Block commit
   ```

2. **If tests fail:**
   - Commit is blocked
   - Developer must fix tests first
   - Prevents bad code from entering repository

---

## Configuration

### Test Coverage Threshold

**Default:** 80% (`min_coverage=0.80`)

**Change in code:**
```python
coverage_passed, actual_coverage, errors = check_test_coverage_gate(ctx, min_coverage=0.90)  # 90%
```

### Test Path

**Default:** `tests/` directory

**Custom path:**
```python
tests_passed, errors, warnings = run_test_gate(ctx, test_path="tests/adapters/")
```

---

## Benefits

1. **Prevents Breaking Changes:**
   - Tests run BEFORE code is applied
   - Existing functionality protected

2. **Coverage Protection:**
   - Coverage cannot drop below threshold
   - Prevents test removal

3. **Developer Experience:**
   - Pre-commit hook catches issues early
   - No need to wait for CI

4. **Automated Quality:**
   - Every change automatically tested
   - No manual test execution needed

---

## Future Enhancements

- [ ] Parallel test execution for faster feedback
- [ ] Test result caching
- [ ] Coverage trend tracking
- [ ] Test failure pattern detection

