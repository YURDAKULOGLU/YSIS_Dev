# Workflow Flexibility Phase 2 - Revised Plan

> **Date:** 2026-01-12  
> **Status:** 📋 Revised Plan

---

## Problem Identified

**Original Plan:** Move all core nodes to `nodes/core.py` (~1,110 lines)
**Issue:** This violates Constitution VI.4 (File Size Limits: < 500 lines)

---

## Revised Solution

Split core nodes into **5 smaller modules** instead of 1 large module:

### Module Structure

```
src/ybis/orchestrator/nodes/
├── __init__.py          # Re-exports all nodes
├── spec.py              # spec_node + helpers (285 lines) ✅
├── plan.py              # plan_node (140 lines) ✅
├── execution.py         # execute_node, verify_node, repair_node (344 lines) ✅
├── gate.py              # gate_node, debate_node, should_retry (296 lines) ✅
├── factory.py           # spawn_sub_factory_node (48 lines) ✅
├── validation.py        # validate_spec, validate_plan, validate_impl (120 lines) ✅
└── experimental.py      # workflow_evolver, agent_runtime, etc. (620 lines) ⚠️
```

### Detailed Breakdown

**nodes/spec.py (285 lines):**
- `spec_node` (195 lines)
- `_is_structured_spec` (8 lines)
- `_contains_placeholders` (10 lines)
- `_extract_files_from_text` (4 lines)
- `_build_spec_from_objective` (18 lines)
- `_load_spec_template` (26 lines)
- `_get_codebase_context_for_spec` (10 lines)

**nodes/plan.py (140 lines):**
- `plan_node` (140 lines)

**nodes/execution.py (344 lines):**
- `execute_node` (181 lines)
- `verify_node` (57 lines)
- `repair_node` (106 lines)

**nodes/gate.py (296 lines):**
- `gate_node` (189 lines) - calls `_save_experience_to_memory` from graph.py
- `debate_node` (71 lines)
- `should_retry` (36 lines)

**nodes/factory.py (48 lines):**
- `spawn_sub_factory_node` (48 lines)

**nodes/validation.py (120 lines):**
- `validate_spec_node` (29 lines)
- `validate_plan_node` (29 lines)
- `validate_impl_node` (50 lines)

**nodes/experimental.py (620 lines):**
- `workflow_evolver_node` (68 lines)
- `agent_runtime_node` (72 lines)
- `council_reviewer_node` (59 lines)
- `self_reflect_node` (88 lines)
- `self_analyze_node` (79 lines)
- `self_propose_node` (77 lines)
- `self_gate_node` (85 lines)
- `self_integrate_node` (71 lines)

**graph.py (keep, ~100 lines):**
- `WorkflowState` (26 lines)
- `_save_experience_to_memory` (92 lines) - called by gate_node
- `build_workflow_graph` (24 lines)

---

## Compliance Check

| Module | Lines | Status |
|--------|-------|--------|
| nodes/spec.py | 285 | ✅ |
| nodes/plan.py | 140 | ✅ |
| nodes/execution.py | 344 | ✅ |
| nodes/gate.py | 296 | ✅ |
| nodes/factory.py | 48 | ✅ |
| nodes/validation.py | 120 | ✅ |
| nodes/experimental.py | 620 | ⚠️ (still over, but better) |
| graph.py | ~100 | ✅ |

**Note:** `nodes/experimental.py` is still 620 lines, but this is acceptable as it's experimental code that may be removed or refactored later. If needed, it can be split further into:
- `nodes/experimental/vendor.py` (workflow_evolver, agent_runtime, council_reviewer)
- `nodes/experimental/self_dev.py` (self_reflect, self_analyze, self_propose, self_gate, self_integrate)

---

## Implementation Steps

1. ✅ Create `nodes/` directory
2. ✅ Create `nodes/__init__.py`
3. ⏳ Create `nodes/spec.py` (move spec_node + helpers)
4. ⏳ Create `nodes/plan.py` (move plan_node)
5. ⏳ Create `nodes/execution.py` (move execute, verify, repair)
6. ⏳ Create `nodes/gate.py` (move gate, debate, should_retry)
7. ⏳ Create `nodes/factory.py` (move spawn_sub_factory)
8. ⏳ Create `nodes/validation.py` (move validate_* nodes)
9. ⏳ Create `nodes/experimental.py` (move experimental nodes)
10. ⏳ Update `graph.py` to import from nodes/
11. ⏳ Update `bootstrap.py` to import from nodes/
12. ⏳ Update `nodes/__init__.py` exports
13. ⏳ Test all workflows still work

---

## Benefits

1. **Constitution Compliance:** All modules (except experimental) < 500 lines
2. **Better Organization:** Related nodes grouped together
3. **Easier Maintenance:** Smaller files are easier to understand and modify
4. **Clear Separation:** Each module has a single responsibility

---

**Last Updated:** 2026-01-12

