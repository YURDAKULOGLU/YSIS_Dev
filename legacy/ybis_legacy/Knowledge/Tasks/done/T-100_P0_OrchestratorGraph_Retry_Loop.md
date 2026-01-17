# T-100 (P0) Implement Retry Loop in OrchestratorGraph

**Suggested agents:** orchestrator (autonomous)
**Priority:** P0 (Critical - Next Milestone)
**Mode:** autonomous

**Scope:**
- `src/agentic/core/graphs/orchestrator_graph.py`
- `src/agentic/core/protocols.py` (if state schema update needed)
- `tests/test_orchestrator_graph.py` (new file)

---

## Problem

Current implementation has linear flow:
```
planner → executor → verifier → END
```

If verifier fails, the task just ends. No retry mechanism.

**From SYSTEM_STATE.md §5:**
> "Loop Closure (Retry): NEXT IMMEDIATE GOAL. Connect Verifier --fail--> Executor"

---

## Strategic Decisions (Pre-determined)

### Retry Policy
- **Max retries:** 3
- **Retry trigger conditions:**
  - `verification.tests_passed == False`
  - OR `verification.lint_passed == False`
- **Exit to FAILED state when:**
  - `retry_count >= max_retries`

### State Schema Updates
Add to `TaskState` (protocols.py):
```python
retry_count: int  # Already exists
error_history: List[str]  # NEW - track all failure reasons
failed_at: Optional[datetime]  # NEW - timestamp of final failure
```

### Graph Changes
Replace:
```python
builder.add_edge("verifier", END)
```

With conditional edge:
```python
builder.add_conditional_edges(
    "verifier",
    should_retry_or_end,
    {
        "retry": "executor",
        "done": END,
        "failed": "failed_node"  # New terminal node
    }
)
```

Add new node:
```python
builder.add_node("failed_node", _failed_node)
```

---

## Implementation Plan (For Aider)

### Step 1: Update protocols.py
Add new fields to TaskState:
- `error_history: List[str]`
- `failed_at: Optional[datetime]`

### Step 2: Add routing function
In `orchestrator_graph.py`:
```python
def should_retry_or_end(state: TaskState) -> Literal["retry", "done", "failed"]:
    verification = state["verification"]

    # Success case
    if verification.tests_passed and verification.lint_passed:
        return "done"

    # Retry budget exhausted
    if state["retry_count"] >= state["max_retries"]:
        return "failed"

    # Retry available
    return "retry"
```

### Step 3: Add failed_node
```python
async def _failed_node(self, state: TaskState) -> Dict[str, Any]:
    print(f"[Graph] Task FAILED after {state['retry_count']} retries")
    return {
        "phase": "failed",
        "failed_at": datetime.now()
    }
```

### Step 4: Update verifier_node
Append errors to error_history:
```python
async def _verifier_node(self, state: TaskState) -> Dict[str, Any]:
    verification = await self.verifier.verify(...)

    error_msg = None
    if not verification.tests_passed or not verification.lint_passed:
        error_msg = f"Retry {state['retry_count']}: {', '.join(verification.errors)}"

    return {
        "verification": verification,
        "phase": "verify",
        "retry_count": state["retry_count"] + 1,
        "error_history": state.get("error_history", []) + ([error_msg] if error_msg else [])
    }
```

### Step 5: Update graph builder
Replace linear edge with conditional:
```python
builder.add_node("failed", self._failed_node)

builder.add_conditional_edges(
    "verifier",
    should_retry_or_end,
    {
        "retry": "executor",
        "done": END,
        "failed": "failed"
    }
)
```

---

## Tests Required (For Sentinel)

Create `tests/test_orchestrator_graph.py`:

### Test 1: Success on first try
- Verifier passes → END state
- retry_count = 1

### Test 2: Retry once then succeed
- First verify fails → retry → second verify passes
- retry_count = 2
- error_history has 1 entry

### Test 3: Exhaust retries
- Verify fails 3 times
- Final state = "failed"
- retry_count = 3
- error_history has 3 entries
- failed_at is set

### Test 4: Partial failure (lint pass, tests fail)
- Should still trigger retry

---

## Acceptance Criteria

- [ ] Conditional edge added to graph
- [ ] failed_node exists and sets failed_at
- [ ] error_history accumulates failure reasons
- [ ] Tests prove retry works (3 test cases minimum)
- [ ] No infinite loops (max_retries enforced)
- [ ] State includes all new fields

---

## Execution Mode

**Use OrchestratorGraph itself to implement this!**

```bash
# Create task in tasks.json
# Invoke orchestrator
# Let Aider write the code
# Let Sentinel verify
# Dogfooding = we test the system by using it
```

---

**Created by:** Claude (Strategic Architect)
**Assigned to:** OrchestratorGraph (via auto_dispatcher)
**Est. Complexity:** Medium (single file changes, clear requirements)
