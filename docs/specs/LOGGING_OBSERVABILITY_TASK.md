# LOGGING & OBSERVABILITY TASK

## Objective
Add comprehensive journal logging to ALL components. Every operation must be traceable.

## Current State
- **96 Python files** in `src/ybis/`
- **Only 12 files** have any logging
- **84 files** have ZERO observability

## Journal Event Pattern

```python
from ..syscalls.journal import append_event

append_event(
    ctx.run_path,           # or Path object
    "EVENT_TYPE",           # UPPERCASE_SNAKE_CASE
    {
        "key": "value",     # Relevant data
    },
    trace_id=ctx.trace_id,  # For correlation
)
```

---

## CRITICAL PRIORITY (Execute First)

### 1. `src/ybis/adapters/local_coder.py`
**Current:** 7 logger calls, 0 journal events
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `FILE_READ_FOR_EDIT` | Before LLM call | `{file, content_length, line_count}` |
| `LLM_REQUEST` | Before litellm.completion | `{model, file, prompt_length, input_content_length}` |
| `LLM_RESPONSE` | After LLM response | `{model, file, output_length, input_output_ratio, response_time_ms}` |
| `LLM_EMPTY_RESPONSE` | If response empty | `{model, file, input_length}` |
| `CONTENT_VALIDATION_FAIL` | If size_ratio < 0.5 | `{file, original_size, new_size, ratio}` |
| `FILE_SKIPPED_PROTECTED` | Protected file blocked | `{file, reason}` |
| `FILE_SKIPPED_NOT_FOUND` | File not in project | `{file, searched_paths}` |

**Implementation:**
```python
# Line ~160, after reading file
append_event(ctx.run_path, "FILE_READ_FOR_EDIT", {
    "file": str(file_path),
    "content_length": len(current_content),
    "line_count": current_content.count('\n') + 1,
    "exists": file_path.exists(),
}, trace_id=ctx.trace_id)

# Line ~233, before LLM call
import time
start_time = time.time()
append_event(ctx.run_path, "LLM_REQUEST", {
    "model": self.model,
    "file": file_path.name,
    "prompt_length": len(prompt),
    "input_content_length": len(current_content),
}, trace_id=ctx.trace_id)

# Line ~244, after LLM response
elapsed_ms = (time.time() - start_time) * 1000
append_event(ctx.run_path, "LLM_RESPONSE", {
    "model": self.model,
    "file": file_path.name,
    "output_length": len(new_content),
    "input_output_ratio": len(new_content) / len(current_content) if current_content else 0,
    "response_time_ms": round(elapsed_ms, 2),
}, trace_id=ctx.trace_id)

# If empty response
if not new_content or len(new_content.strip()) < 10:
    append_event(ctx.run_path, "LLM_EMPTY_RESPONSE", {
        "model": self.model,
        "file": file_path.name,
        "input_length": len(current_content),
    }, trace_id=ctx.trace_id)
```

---

### 2. `src/ybis/adapters/aider.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `AIDER_START` | Before aider call | `{files, objective, model}` |
| `AIDER_COMMAND` | Command constructed | `{command, cwd}` |
| `AIDER_OUTPUT` | After execution | `{exit_code, stdout_length, stderr_length, duration_ms}` |
| `AIDER_ERROR` | On failure | `{error, exit_code}` |
| `AIDER_FILES_CHANGED` | After completion | `{files_changed, diff_summary}` |

---

### 3. `src/ybis/orchestrator/planner.py`
**Current:** 0 logging (only print statements)
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `PLANNER_START` | Plan request | `{task_id, objective_length}` |
| `RAG_QUERY` | Vector store query | `{collection, query_length, results_count}` |
| `LLAMAINDEX_QUERY` | LlamaIndex query | `{query, results_count}` |
| `ERROR_KB_QUERY` | Error patterns query | `{patterns_count}` |
| `LLM_PLAN_REQUEST` | Before LLM | `{model, prompt_length}` |
| `LLM_PLAN_RESPONSE` | After LLM | `{files_count, steps_count, response_time_ms}` |
| `PLAN_VALIDATION` | After validation | `{original_files, validated_files, removed_count}` |
| `PLANNER_FALLBACK` | Heuristic used | `{reason}` |

---

### 4. `src/ybis/orchestrator/verifier.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `VERIFIER_START` | Verification begins | `{task_id, run_id, files_to_check}` |
| `LINT_START` | Ruff check starts | `{files}` |
| `LINT_RESULT` | Ruff completes | `{passed, errors_count, warnings_count, duration_ms}` |
| `TEST_START` | Pytest starts | `{test_path}` |
| `TEST_RESULT` | Pytest completes | `{passed, tests_run, failures, errors, duration_ms}` |
| `VERIFIER_COMPLETE` | All checks done | `{lint_passed, tests_passed, total_errors}` |

---

### 5. `src/ybis/orchestrator/self_improve.py`
**Current:** 41 logger calls, but missing journal events for LLM
**Add Events:**

| Event | When | Payload |
|-------|------|---------|
| `SELF_IMPROVE_REFLECT_START` | Reflect begins | `{task_id}` |
| `SELF_IMPROVE_REFLECT_COMPLETE` | Reflect done | `{issues_count, opportunities_count}` |
| `SELF_IMPROVE_PLAN_START` | Plan begins | `{objective}` |
| `SELF_IMPROVE_PLAN_COMPLETE` | Plan done | `{files_count, steps_count}` |
| `SELF_IMPROVE_IMPLEMENT_START` | Implement begins | `{files}` |
| `SELF_IMPROVE_IMPLEMENT_COMPLETE` | Implement done | `{files_changed}` |
| `SELF_IMPROVE_REPAIR_START` | Repair begins | `{attempt, max_retries}` |
| `SELF_IMPROVE_REPAIR_COMPLETE` | Repair done | `{actions_taken}` |

---

### 6. `src/ybis/orchestrator/graph.py`
**Current:** 14 events, but missing node-level detail
**Add Events:**

| Event | When | Payload |
|-------|------|---------|
| `NODE_ENTER` | Each node starts | `{node_name, state_keys}` |
| `NODE_EXIT` | Each node ends | `{node_name, status, duration_ms}` |
| `NODE_ERROR` | Node fails | `{node_name, error, traceback_summary}` |
| `ROUTING_DECISION` | Conditional routing | `{from_node, to_node, condition}` |

---

## HIGH PRIORITY

### 7. `src/ybis/services/reflection_engine.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `REFLECTION_START` | Reflect begins | `{}` |
| `REFLECTION_HEALTH_CHECK` | Health assessed | `{score, status}` |
| `REFLECTION_METRICS_COLLECTED` | Metrics done | `{total_runs, success_rate, failure_rate}` |
| `REFLECTION_PATTERNS_ANALYZED` | Patterns done | `{patterns_count, top_error_type}` |
| `REFLECTION_COMPLETE` | All done | `{issues_count, opportunities_count}` |

---

### 8. `src/ybis/services/error_knowledge_base.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `ERROR_KB_RECORD` | Error recorded | `{error_type, task_id, step}` |
| `ERROR_KB_PATTERN_DETECTED` | Pattern found | `{error_type, occurrences}` |
| `ERROR_KB_QUERY` | Query executed | `{query_type, results_count}` |

---

### 9. `src/ybis/services/health_monitor.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `HEALTH_CHECK_START` | Check begins | `{check_name}` |
| `HEALTH_CHECK_RESULT` | Check done | `{check_name, status, message}` |
| `HEALTH_ALL_COMPLETE` | All done | `{healthy_count, total_count, overall_status}` |

---

### 10. `src/ybis/services/lesson_engine.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `LESSON_RECORD` | Lesson saved | `{lesson_type, source}` |
| `LESSON_QUERY` | Lessons queried | `{query, results_count}` |
| `LESSON_APPLY` | Lesson applied | `{lesson_id, target}` |

---

### 11. `src/ybis/data_plane/vector_store.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `VECTOR_STORE_INIT` | Store initialized | `{provider, persist_dir}` |
| `VECTOR_STORE_ADD` | Documents added | `{collection, doc_count}` |
| `VECTOR_STORE_QUERY` | Query executed | `{collection, query_length, results_count, duration_ms}` |
| `VECTOR_STORE_ERROR` | Operation failed | `{operation, error}` |

---

### 12. `src/ybis/control_plane/db.py`
**Current:** 0 logging
**Required Events:**

| Event | When | Payload |
|-------|------|---------|
| `DB_TASK_CREATE` | Task created | `{task_id, title}` |
| `DB_TASK_UPDATE` | Task updated | `{task_id, status}` |
| `DB_RUN_CREATE` | Run created | `{run_id, task_id}` |
| `DB_RUN_UPDATE` | Run updated | `{run_id, status}` |
| `DB_QUERY` | Query executed | `{query_type, results_count}` |

---

## MEDIUM PRIORITY

### 13. `src/ybis/adapters/` (All remaining)

| File | Events Needed |
|------|---------------|
| `llamaindex_adapter.py` | `LLAMAINDEX_INIT`, `LLAMAINDEX_INDEX`, `LLAMAINDEX_QUERY` |
| `vector_store_chroma.py` | `CHROMA_INIT`, `CHROMA_ADD`, `CHROMA_QUERY` |
| `vector_store_qdrant.py` | `QDRANT_INIT`, `QDRANT_ADD`, `QDRANT_QUERY` |
| `graph_store_neo4j.py` | `NEO4J_CONNECT`, `NEO4J_QUERY`, `NEO4J_UPDATE` |
| `llm_council.py` | `COUNCIL_DEBATE_START`, `COUNCIL_VOTE`, `COUNCIL_DECISION` |
| `evoagentx.py` | `EVOAGENT_INIT`, `EVOAGENT_RUN`, `EVOAGENT_RESULT` |
| `self_improve_swarms.py` | `SWARM_INIT`, `SWARM_TASK`, `SWARM_COMPLETE` |
| `registry.py` | `ADAPTER_REGISTER`, `ADAPTER_GET`, `ADAPTER_NOT_FOUND` |

---

### 14. `src/ybis/workflows/` (All)

| File | Events Needed |
|------|---------------|
| `runner.py` | `WORKFLOW_LOAD`, `WORKFLOW_VALIDATE`, `WORKFLOW_EXECUTE` |
| `registry.py` | `WORKFLOW_REGISTER`, `WORKFLOW_GET` |
| `parallel_execution.py` | `PARALLEL_START`, `PARALLEL_TASK_COMPLETE`, `PARALLEL_ALL_DONE` |
| `bootstrap.py` | `BOOTSTRAP_START`, `BOOTSTRAP_STEP`, `BOOTSTRAP_COMPLETE` |
| `node_registry.py` | `NODE_REGISTER`, `NODE_RESOLVE` |

---

### 15. `src/ybis/services/mcp_tools/` (All)

| File | Events Needed |
|------|---------------|
| `task_tools.py` | `MCP_TASK_CREATE`, `MCP_TASK_LIST`, `MCP_TASK_UPDATE` |
| `memory_tools.py` | `MCP_MEMORY_STORE`, `MCP_MEMORY_QUERY` |
| `dependency_tools.py` | `MCP_DEP_CHECK`, `MCP_DEP_IMPACT` |
| `artifact_tools.py` | `MCP_ARTIFACT_CREATE`, `MCP_ARTIFACT_READ` |
| `debate_tools.py` | `MCP_DEBATE_START`, `MCP_DEBATE_RESPOND` |

---

## Implementation Guidelines

### 1. Import Pattern
```python
# At top of file
from ..syscalls.journal import append_event
```

### 2. Context Handling
```python
# If RunContext available
append_event(ctx.run_path, "EVENT", {...}, trace_id=ctx.trace_id)

# If no context (service layer)
from ..constants import PROJECT_ROOT
append_event(PROJECT_ROOT / "platform_data", "EVENT", {...})
```

### 3. Error Handling
```python
try:
    # operation
    append_event(..., "OPERATION_SUCCESS", {...})
except Exception as e:
    append_event(..., "OPERATION_ERROR", {"error": str(e)})
    raise
```

### 4. Timing Pattern
```python
import time
start = time.time()
# operation
duration_ms = (time.time() - start) * 1000
append_event(..., "OPERATION_COMPLETE", {"duration_ms": round(duration_ms, 2)})
```

---

## Verification Checklist

After implementation, verify with:

```bash
# Count journal events per file
grep -r "append_event" src/ybis --include="*.py" -c | sort -t: -k2 -n -r

# Run a test workflow and check journal
python scripts/ybis_run.py TEST-LOGGING --workflow default
cat workspaces/TEST-LOGGING/runs/*/journal/events.jsonl | jq '.event_type' | sort | uniq -c
```

Expected minimum events per workflow run:
- `WORKFLOW_START`: 1
- `NODE_ENTER`: 5+ (per node)
- `NODE_EXIT`: 5+
- `LLM_REQUEST`: 1+ (if LLM used)
- `LLM_RESPONSE`: 1+
- `FILE_WRITE`: 3+ (artifacts)
- `WORKFLOW_COMPLETE`: 1

---

## Priority Order

1. **local_coder.py** - Most critical, LLM black box
2. **planner.py** - Plan generation visibility
3. **verifier.py** - Test results tracking
4. **reflection_engine.py** - Self-improvement visibility
5. **error_knowledge_base.py** - Error tracking
6. **vector_store.py** - RAG visibility
7. **aider.py** - External tool tracking
8. **All remaining files**

---

## Success Criteria

- [ ] Every LLM call has REQUEST/RESPONSE events
- [ ] Every file read/write has events
- [ ] Every external tool call has START/COMPLETE events
- [ ] Every node has ENTER/EXIT events
- [ ] Every error has ERROR event with details
- [ ] Running `grep -r "append_event" src/ybis -l | wc -l` returns 50+
