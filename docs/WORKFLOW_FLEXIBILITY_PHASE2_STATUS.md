# Workflow Flexibility Phase 2 - Status Report

> **Date:** 2026-01-12  
> **Status:** ⏳ In Progress

---

## Executive Summary

Phase 2 of workflow flexibility improvements is in progress. The goal is to split `graph.py` (2,326 lines) into smaller modules (< 500 lines each) to comply with Constitution VI.4.

**Current Progress:**
- ✅ Phase 1 Complete: Legacy fallback removed
- ⏳ Phase 2 In Progress: graph.py split
- ⏳ Phase 3 Pending: Python workflow support

---

## PART 1: Completed Work (Phase 1)

1. ✅ **Removed legacy fallback** from `build_workflow_graph()`
2. ✅ **Removed `_build_legacy_workflow_graph()`** function (140 lines)
3. ✅ **Made YAML workflows mandatory** (no fallback)

**Result:** graph.py reduced from 2,471 to 2,326 lines (-145 lines)

---

## PART 2: Current Work (Phase 2)

### 2.1 Infrastructure Created

1. ✅ **Created `nodes/` directory**
2. ✅ **Created `nodes/__init__.py`** with exports
3. ⏳ **Removing duplicate self-improve nodes** from graph.py

### 2.2 Node Organization Plan

**Target Structure:**
```
src/ybis/orchestrator/
├── graph.py              # WorkflowState, build_workflow_graph, _save_experience_to_memory (~200 lines)
├── nodes/
│   ├── __init__.py       # Node exports
│   ├── core.py           # spec, plan, execute, verify, repair, gate, debate (~800 lines)
│   ├── validation.py     # validate_spec, validate_plan, validate_impl (~200 lines)
│   └── experimental.py   # workflow_evolver, agent_runtime, council_reviewer, self_reflect, etc. (~500 lines)
└── self_improve.py       # Already exists, keep it
```

### 2.3 Node Functions to Move

**Core Nodes (→ nodes/core.py):**
- `spawn_sub_factory_node` (54-101)
- `spec_node` (105-299) + helpers (302-388)
- `plan_node` (392-531)
- `execute_node` (647-827)
- `verify_node` (831-887)
- `should_retry` (890-925)
- `repair_node` (929-1034)
- `gate_node` (1038-1226)
- `debate_node` (1229-1299)

**Validation Nodes (→ nodes/validation.py):**
- `validate_spec_node` (534-562)
- `validate_plan_node` (565-593)
- `validate_impl_node` (596-645)

**Experimental Nodes (→ nodes/experimental.py):**
- `workflow_evolver_node` (1307-1374)
- `agent_runtime_node` (1377-1448)
- `council_reviewer_node` (1450-1508)
- `self_reflect_node` (1798-1885)
- `self_analyze_node` (1888-1966)
- `self_propose_node` (1969-2045)
- `self_gate_node` (2048-2131)
- `self_integrate_node` (2134-2204)

**Keep in graph.py:**
- `WorkflowState` (26-51)
- `build_workflow_graph` (2301-2324)
- `_save_experience_to_memory` (2207-2298)

**Remove (duplicates):**
- `self_improve_reflect_node` (1511-1563) - duplicate, use self_improve.py
- `self_improve_plan_node` (1566-1620) - duplicate, use self_improve.py
- `self_improve_implement_node` (1623-1677) - duplicate, use self_improve.py
- `self_improve_test_node` (1680-1734) - duplicate, use self_improve.py
- `self_improve_integrate_node` (1737-1791) - duplicate, use self_improve.py

---

## PART 3: Next Steps

### 3.1 Immediate Actions

1. **Remove duplicate self-improve nodes** from graph.py
2. **Create nodes/core.py** and move core nodes
3. **Create nodes/validation.py** and move validation nodes
4. **Create nodes/experimental.py** and move experimental nodes
5. **Update graph.py** to import from nodes/
6. **Update bootstrap.py** to import from nodes/
7. **Update __init__.py** exports

### 3.2 Testing

After splitting:
- Test all workflows still work
- Test node registration still works
- Test imports are correct
- Run linting and type checking

---

## PART 4: Estimated Impact

**Before:**
- graph.py: 2,326 lines (4.6x over limit)

**After:**
- graph.py: ~200 lines ✅
- nodes/core.py: ~800 lines ⚠️ (still over, but better organized)
- nodes/validation.py: ~200 lines ✅
- nodes/experimental.py: ~500 lines ⚠️ (still over, but better organized)

**Compliance:**
- graph.py: ✅ Compliant (< 500 lines)
- nodes/core.py: ⚠️ Still over (but can be split further if needed)
- nodes/experimental.py: ⚠️ Still over (but can be split further if needed)

**Flexibility:**
- Current: 70%
- Target: 90%+
- After Phase 2: 85%+

---

## Conclusion

Phase 2 is a large refactoring that requires careful extraction of node functions. The work is in progress and will significantly improve code organization and Constitution compliance.

**Last Updated:** 2026-01-12

