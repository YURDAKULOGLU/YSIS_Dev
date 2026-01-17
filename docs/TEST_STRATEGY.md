# TEST STRATEGY: Preventing Common Errors

**Objective:** Define comprehensive test coverage to prevent the errors we encountered during E2E testing.

---

## Errors Encountered & Prevention Strategy

### 1. Missing Import Errors (PROJECT_ROOT, etc.)

**Error:** `NameError: name 'PROJECT_ROOT' is not defined`

**Root Cause:** Missing imports in graph nodes.

**Prevention Tests:**
- ✅ **Import validation test** - Verify all nodes import required constants
- ✅ **Static analysis** - Use `ruff check` to catch undefined names
- ✅ **Type checking** - Use `mypy` to catch missing imports

**Test File:** `tests/test_imports.py`

---

### 2. Async/Await Pattern Violations

**Error:** `RuntimeError: asyncio.run() cannot be called from a running event loop`

**Root Cause:** Using `asyncio.run()` inside LangGraph nodes (which already run in an event loop).

**Prevention Tests:**
- ✅ **Async pattern test** - Verify no `asyncio.run()` calls in graph nodes
- ✅ **Static analysis** - Grep for `asyncio.run(` in orchestrator code
- ✅ **Integration test** - Run workflow in async context and verify no errors

**Test File:** `tests/test_async_patterns.py`

---

### 3. Missing Required Fields in RunContext

**Error:** `ValidationError: Field required [type=missing, input_value={...}, input_type=dict]`

**Root Cause:** `RunContext` requires `trace_id` but it wasn't passed in all creation sites.

**Prevention Tests:**
- ✅ **RunContext validation test** - Verify all RunContext creations include required fields
- ✅ **Type checking** - Use Pydantic strict mode to catch missing fields
- ✅ **Coverage test** - Ensure all RunContext creation sites are tested

**Test File:** `tests/test_runcontext_validation.py`

---

### 4. WorkflowState TypedDict Mismatch

**Error:** `KeyError` or type mismatches when accessing state fields.

**Root Cause:** `WorkflowState` TypedDict didn't include all fields used in nodes.

**Prevention Tests:**
- ✅ **WorkflowState schema test** - Verify TypedDict matches all node usage
- ✅ **Type checking** - Use mypy to validate state access
- ✅ **Coverage test** - Ensure all state fields are defined

**Test File:** `tests/test_workflow_state_schema.py`

---

### 5. LangGraph Edge Conflicts

**Error:** `InvalidUpdateError: Can receive only one value per step`

**Root Cause:** Multiple edges from the same node (direct edge + conditional edge).

**Prevention Tests:**
- ✅ **Graph compilation test** - Verify graph compiles without conflicts
- ✅ **Edge validation test** - Check for duplicate edges from same node
- ✅ **Routing test** - Verify all conditional edges have valid targets

**Test File:** `tests/test_graph_structure.py`

---

### 6. Database Constraint Violations

**Error:** `UNIQUE constraint failed: runs.run_id`

**Root Cause:** Attempting to INSERT a run that already exists (should use UPDATE).

**Prevention Tests:**
- ✅ **Database operation test** - Verify INSERT vs UPDATE logic
- ✅ **Idempotency test** - Ensure operations can be retried safely
- ✅ **Constraint test** - Verify UNIQUE constraints are respected

**Test File:** `tests/test_db_operations.py`

---

## Test Categories

### A. Unit Tests (Fast, Isolated)

**Purpose:** Test individual components in isolation.

**Files:**
- `tests/test_imports.py` - Import validation
- `tests/test_runcontext_validation.py` - RunContext creation
- `tests/test_workflow_state_schema.py` - State schema validation
- `tests/test_async_patterns.py` - Async pattern compliance

**Run:** `pytest tests/test_*.py -v`

---

### B. Integration Tests (Medium Speed, Component Interaction)

**Purpose:** Test component interactions.

**Files:**
- `tests/test_graph_structure.py` - Graph compilation and structure
- `tests/test_db_operations.py` - Database operations
- `tests/test_orchestrator_graph.py` - Full workflow execution (mocked)

**Run:** `pytest tests/test_*integration*.py -v`

---

### C. Smoke Tests (Fast E2E)

**Purpose:** Quick validation that system works end-to-end.

**Files:**
- `tests/test_smoke.py` - Minimal workflow execution
- `scripts/e2e_test_runner.py` - Full E2E scenarios

**Run:** `pytest tests/test_smoke.py -v`

---

## Pre-Commit Hooks

**Location:** `.pre-commit-config.yaml`

**Checks:**
1. **Ruff linting** - Catch undefined names, unused imports
2. **Mypy type checking** - Catch type errors
3. **Import validation** - Verify all imports are valid
4. **Async pattern check** - Grep for `asyncio.run(`

---

## CI/CD Pipeline Tests

**Order of Execution:**
1. **Lint** (Ruff) - 30 seconds
2. **Type Check** (Mypy) - 1 minute
3. **Unit Tests** - 2 minutes
4. **Integration Tests** - 5 minutes
5. **Smoke Tests** - 3 minutes

**Total:** ~11 minutes

---

## Test Implementation Priority

### Phase 1: Critical (Prevent Current Errors)
1. ✅ `test_imports.py` - Import validation
2. ✅ `test_async_patterns.py` - Async pattern check
3. ✅ `test_runcontext_validation.py` - RunContext validation
4. ✅ `test_graph_structure.py` - Graph compilation

### Phase 2: Important (Prevent Future Errors)
5. ✅ `test_workflow_state_schema.py` - State schema
6. ✅ `test_db_operations.py` - Database operations
7. ✅ `test_smoke.py` - Quick E2E validation

### Phase 3: Nice to Have (Comprehensive Coverage)
8. Integration test improvements
9. Performance tests
10. Stress tests

---

## Test Execution Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific category
pytest tests/test_imports.py tests/test_async_patterns.py -v

# Run with coverage
pytest tests/ --cov=src/ybis --cov-report=html

# Run pre-commit hooks manually
pre-commit run --all-files
```

---

## Success Criteria

**A test suite is successful if:**
- ✅ All unit tests pass (< 5 minutes)
- ✅ All integration tests pass (< 10 minutes)
- ✅ Smoke test completes successfully
- ✅ No linting errors
- ✅ No type errors
- ✅ Coverage > 80% for critical paths

---

## Maintenance

**When to update tests:**
- After fixing a bug (add regression test)
- When adding new features (add feature test)
- When refactoring (update affected tests)
- Monthly review (remove obsolete tests)

