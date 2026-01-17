# Logging Gap Analysis

**Date:** 2026-01-10  
**Issue:** Process'in tamamı loglanmıyor

---

## Mevcut Durum

### ✅ Loglananlar:
1. **Syscalls:** `src/ybis/syscalls/journal.py`
   - File operations (read/write)
   - Command execution
   - Git operations
   - Journal: `workspaces/<task_id>/runs/<run_id>/journal/events.jsonl`

### ❌ Loglanmayanlar:

1. **Workflow Execution:**
   - Workflow başlangıç/bitiş
   - Workflow state transitions
   - Workflow hataları

2. **Node Execution:**
   - Node başlangıç/bitiş
   - Node input/output
   - Node execution time
   - Node hataları

3. **LLM Calls:**
   - LLM prompt/response
   - LLM model, tokens, cost
   - LLM latency
   - LLM errors

4. **State Changes:**
   - State transitions
   - State snapshots
   - State validation

5. **Performance Metrics:**
   - Node execution time
   - Total workflow time
   - Token usage
   - Cost tracking

6. **Errors/Exceptions:**
   - Exception details
   - Stack traces
   - Error context

---

## Mevcut Infrastructure

### 1. Observability Service
**Location:** `src/ybis/services/observability.py`

**Features:**
- `trace_generation()` - LLM call tracing
- `start_span()` - Distributed tracing
- Adapter pattern (Langfuse, OpenTelemetry)

**Problem:** ❌ **KULLANILMIYOR!**
- `graph.py`'de observability service çağrılmıyor
- LLM calls loglanmıyor
- Node execution loglanmıyor

### 2. Syscalls Journal
**Location:** `src/ybis/syscalls/journal.py`

**Features:**
- `append_event()` - Syscall events
- JSONL format
- Automatic trace_id extraction

**Problem:** ✅ Çalışıyor ama sadece syscalls için

---

## Çözüm: Comprehensive Logging

### 1. Workflow Execution Logging

**Eklemek:**
```python
# src/ybis/orchestrator/graph.py

def workflow_start_log(state: WorkflowState):
    """Log workflow start."""
    observability = get_observability_service()
    observability.trace_generation(
        name="workflow_start",
        model="ybis",
        input_data={"task_id": state["task_id"], "workflow": state["workflow_name"]},
        output_data=None,
        metadata={"run_id": state["run_id"], "trace_id": state.get("trace_id")}
    )
    
    # Also log to journal
    append_event(
        state["run_path"],
        "WORKFLOW_START",
        {"workflow": state["workflow_name"], "task_id": state["task_id"]},
        state.get("trace_id")
    )
```

### 2. Node Execution Logging

**Eklemek:**
```python
def node_execution_wrapper(node_func):
    """Wrapper to log node execution."""
    def wrapper(state: WorkflowState):
        node_name = node_func.__name__
        start_time = time.time()
        
        # Log node start
        append_event(
            state["run_path"],
            "NODE_START",
            {"node": node_name, "state": state},
            state.get("trace_id")
        )
        
        try:
            result = node_func(state)
            duration = time.time() - start_time
            
            # Log node success
            append_event(
                state["run_path"],
                "NODE_SUCCESS",
                {"node": node_name, "duration": duration},
                state.get("trace_id")
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            # Log node error
            append_event(
                state["run_path"],
                "NODE_ERROR",
                {"node": node_name, "error": str(e), "duration": duration},
                state.get("trace_id")
            )
            raise
    return wrapper
```

### 3. LLM Call Logging

**Eklemek:**
```python
# src/ybis/orchestrator/llm.py (or wherever LLM calls are made)

def llm_call_with_logging(prompt, model, **kwargs):
    """LLM call with observability logging."""
    observability = get_observability_service()
    
    start_time = time.time()
    try:
        response = litellm.completion(model=model, messages=prompt, **kwargs)
        duration = time.time() - start_time
        
        # Log to observability
        observability.trace_generation(
            name="llm_call",
            model=model,
            input_data={"prompt": prompt, "kwargs": kwargs},
            output_data={"response": response.choices[0].message.content},
            metadata={
                "tokens": response.usage.total_tokens,
                "cost": calculate_cost(model, response.usage),
                "duration": duration
            }
        )
        
        return response
    except Exception as e:
        # Log error
        observability.trace_generation(
            name="llm_error",
            model=model,
            input_data={"prompt": prompt},
            output_data=None,
            metadata={"error": str(e)}
        )
        raise
```

### 4. State Transition Logging

**Eklemek:**
```python
def log_state_transition(old_state: WorkflowState, new_state: WorkflowState):
    """Log state transition."""
    changes = {}
    for key in new_state:
        if key not in old_state or old_state[key] != new_state[key]:
            changes[key] = {"old": old_state.get(key), "new": new_state[key]}
    
    append_event(
        new_state["run_path"],
        "STATE_TRANSITION",
        {"changes": changes},
        new_state.get("trace_id")
    )
```

---

## Implementation Plan

### Phase 1: Basic Logging
1. ✅ Add workflow start/end logging
2. ✅ Add node execution logging wrapper
3. ✅ Add LLM call logging
4. ✅ Add state transition logging

### Phase 2: Observability Integration
1. ✅ Enable observability adapters in profiles
2. ✅ Integrate Langfuse/OpenTelemetry
3. ✅ Add distributed tracing

### Phase 3: Performance Metrics
1. ✅ Add execution time tracking
2. ✅ Add token/cost tracking
3. ✅ Add performance dashboards

---

## Files to Modify

1. `src/ybis/orchestrator/graph.py` - Add logging to all nodes
2. `src/ybis/orchestrator/llm.py` - Add LLM call logging (if exists)
3. `configs/profiles/default.yaml` - Enable observability adapters
4. `src/ybis/services/observability.py` - Ensure it's used

---

## Expected Output

After implementation, we should have:

1. **Journal Logs:** `workspaces/<task_id>/runs/<run_id>/journal/events.jsonl`
   - WORKFLOW_START
   - NODE_START
   - NODE_SUCCESS/NODE_ERROR
   - LLM_CALL
   - STATE_TRANSITION
   - WORKFLOW_END

2. **Observability Backend:** (if enabled)
   - Langfuse: LLM traces, costs, latency
   - OpenTelemetry: Distributed traces

3. **Performance Metrics:**
   - Node execution times
   - Total workflow time
   - Token usage
   - Cost per run

---

## Conclusion

**Problem:** Process'in tamamı loglanmıyor - sadece syscalls loglanıyor.

**Solution:** Comprehensive logging eklemek:
- Workflow execution logging
- Node execution logging
- LLM call logging
- State transition logging
- Performance metrics

**Status:** ⚠️ **TODO** - Implementation needed

