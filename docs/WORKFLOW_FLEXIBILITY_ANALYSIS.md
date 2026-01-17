# Workflow Flexibility Analysis

> **Date:** 2026-01-12  
> **Question:** "Bizim yapı esnek workflowları destekler şekilde mi? Graph baya durağan?"

---

## Executive Summary

**Current State:** ⚠️ **HYBRID - Partially Flexible**

- ✅ **YAML-based workflow system** exists and is flexible
- ❌ **Legacy hardcoded graph** still present as fallback
- ⚠️ **Graph.py is static** (2,471 lines, hardcoded nodes/edges)

**Flexibility Score:** 60% (Good foundation, but legacy code limits flexibility)

---

## PART 1: What IS Flexible

### 1.1 YAML-Based Workflow Definitions

**Location:** `configs/workflows/*.yaml`

**Capabilities:**
- ✅ Define workflows in YAML (no code changes needed)
- ✅ Add/remove nodes dynamically
- ✅ Define connections (edges) between nodes
- ✅ Conditional routing (state-based, artifact-based, expression-based)
- ✅ Node configuration (per-node settings)
- ✅ Workflow inheritance (`extends` field)
- ✅ Parallel execution (multiple edges from same source)

**Example:**
```yaml
name: my_custom_workflow
nodes:
  - id: step1
    type: planner
    config:
      max_steps: 5
  - id: step2
    type: executor
connections:
  - from: START
    to: step1
  - from: step1
    to: step2
  - from: step2
    to: END
```

**Status:** ✅ **FULLY FLEXIBLE** - Can create new workflows by adding YAML files

---

### 1.2 Dynamic Node Registration

**Location:** `src/ybis/workflows/node_registry.py`

**Capabilities:**
- ✅ Register new node types at runtime
- ✅ Resolve node implementations by type string
- ✅ Node metadata (description, required modules)
- ✅ Decorator-based registration (`@register_node`)

**Example:**
```python
@register_node("my_custom_node", description="Custom node")
def my_custom_node(state: WorkflowState) -> WorkflowState:
    # Node implementation
    return state
```

**Status:** ✅ **FULLY FLEXIBLE** - Can add new node types without modifying core code

---

### 1.3 Dynamic Conditional Routing

**Location:** `src/ybis/workflows/dynamic_conditions.py`

**Capabilities:**
- ✅ Define conditions in YAML (no Python code needed)
- ✅ State-based conditions (`state_check`)
- ✅ Artifact-based conditions (`artifact_check`)
- ✅ Expression-based conditions (`expression`)
- ✅ Multiple operators (eq, ne, in, gt, lt, exists, etc.)

**Example:**
```yaml
connections:
  - from: verify
    to: repair
    condition:
      type: state_check
      field: retries
      operator: lt
      value: 3
      routes:
        true: repair
        false: gate
```

**Status:** ✅ **FULLY FLEXIBLE** - Can define complex routing logic in YAML

---

### 1.4 Workflow Inheritance

**Location:** `src/ybis/workflows/inheritance.py`

**Capabilities:**
- ✅ Extend base workflows
- ✅ Override nodes and connections
- ✅ Merge requirements (union)
- ✅ Merge node configs

**Example:**
```yaml
name: my_workflow
extends: ybis_native
nodes:
  - id: custom_step
    type: custom_node
    # Overrides or adds to base workflow
```

**Status:** ✅ **FULLY FLEXIBLE** - Can create workflow variants via inheritance

---

### 1.5 Parallel Execution

**Location:** `src/ybis/workflows/parallel_execution.py`

**Capabilities:**
- ✅ Automatic parallel execution (multiple edges from same source)
- ✅ Explicit parallel node groups
- ✅ State merging after parallel execution

**Example:**
```yaml
connections:
  - from: plan
    to: step1  # Runs in parallel
  - from: plan
    to: step2  # Runs in parallel
  - from: step1
    to: merge
  - from: step2
    to: merge
```

**Status:** ✅ **FULLY FLEXIBLE** - LangGraph handles parallel execution automatically

---

## PART 2: What IS NOT Flexible (Legacy Code)

### 2.1 Hardcoded Legacy Graph

**Location:** `src/ybis/orchestrator/graph.py:2334-2470`

**Problem:**
- ❌ **2,471 lines** of hardcoded graph construction
- ❌ Nodes are hardcoded (`spec_node`, `plan_node`, etc.)
- ❌ Edges are hardcoded (`workflow.add_edge(...)`)
- ❌ Conditional routing functions are hardcoded (`should_continue_steps`, `should_retry_route`, etc.)
- ❌ **Fallback mechanism** - If YAML workflow fails, falls back to legacy

**Code:**
```python
def _build_legacy_workflow_graph() -> StateGraph:
    workflow = StateGraph(WorkflowState)
    
    # Hardcoded nodes
    workflow.add_node("spec", spec_node)
    workflow.add_node("plan", plan_node)
    # ... 20+ more hardcoded nodes
    
    # Hardcoded edges
    workflow.add_edge(START, "spec")
    workflow.add_edge("spec", "plan")
    # ... 30+ more hardcoded edges
    
    # Hardcoded conditional routing
    workflow.add_conditional_edges(
        "verify",
        should_retry_route,  # Hardcoded function
        {"repair": "repair", "gate": "gate"}
    )
```

**Impact:**
- 🔴 **Cannot modify legacy workflow without code changes**
- 🔴 **Legacy graph is completely static**
- 🔴 **Fallback prevents YAML workflow errors from being visible**

**Status:** ❌ **NOT FLEXIBLE** - Requires code changes to modify

---

### 2.2 Hardcoded Conditional Routing Functions

**Location:** `src/ybis/orchestrator/graph.py:2354-2456`

**Problem:**
- ❌ Functions like `should_continue_steps`, `should_retry_route`, `repair_route`, `should_debate` are hardcoded
- ❌ Logic is embedded in Python code, not configurable
- ❌ Cannot change routing logic without code changes

**Example:**
```python
def should_continue_steps(state: WorkflowState) -> str:
    # Hardcoded logic
    if executor_path.exists():
        return "continue"
    return "done"
```

**Impact:**
- 🔴 **Routing logic is not data-driven**
- 🔴 **Cannot customize routing without code changes**

**Status:** ❌ **NOT FLEXIBLE** - Requires code changes to modify

---

### 2.3 Graph.py Size and Complexity

**Location:** `src/ybis/orchestrator/graph.py` (2,471 lines)

**Problem:**
- ❌ **5x over Constitution limit** (500 lines max)
- ❌ Contains both legacy and new systems
- ❌ Hard to maintain and extend
- ❌ Violates Single Responsibility Principle

**Impact:**
- 🔴 **Hard to understand and modify**
- 🔴 **High risk of breaking changes**
- 🔴 **Difficult to test**

**Status:** ❌ **NOT FLEXIBLE** - Architecture violation

---

## PART 3: Current Workflow Loading Flow

### 3.1 How Workflows Are Loaded

```python
def build_workflow_graph(workflow_name: str = "ybis_native") -> StateGraph:
    # 1. Try to load from YAML
    try:
        runner = WorkflowRunner().load_workflow(workflow_name)
        return runner.build_graph()  # ✅ Flexible YAML-based
    except (FileNotFoundError, ValueError) as e:
        # 2. Fallback to legacy hardcoded graph
        return _build_legacy_workflow_graph()  # ❌ Static hardcoded
```

**Issues:**
1. ⚠️ **Silent fallback** - Errors are hidden by fallback
2. ⚠️ **Legacy is default** - If YAML fails, uses hardcoded graph
3. ⚠️ **No validation** - Doesn't validate YAML before falling back

---

## PART 4: Comparison with Modern Solutions

### 4.1 Prefect (2026 SOTA)

**Prefect Approach:**
- ✅ **Python-based workflows** (not YAML)
- ✅ **Dynamic workflow creation** at runtime
- ✅ **No hardcoded graphs**
- ✅ **Completely flexible** - workflows are Python code

**Example:**
```python
@flow
def my_workflow():
    result1 = task1()
    result2 = task2()
    return merge(result1, result2)
```

**YBIS vs Prefect:**
- YBIS: YAML-based (good) but has legacy hardcoded fallback (bad)
- Prefect: Python-based (more flexible, but requires code)

---

### 4.2 LangGraph (Current Foundation)

**LangGraph Approach:**
- ✅ **Dynamic graph construction** via Python API
- ✅ **No hardcoded graphs** (graphs are built programmatically)
- ✅ **Completely flexible** - graphs are Python code

**YBIS vs LangGraph:**
- YBIS: Uses LangGraph but wraps it in hardcoded legacy graph
- LangGraph: Pure dynamic construction (what YBIS should be)

---

## PART 5: Recommendations

### 5.1 Immediate Actions (High Priority)

1. **Remove Legacy Fallback**
   - ❌ Remove `_build_legacy_workflow_graph()`
   - ✅ Make YAML workflows mandatory
   - ✅ Fail fast if YAML workflow is invalid

2. **Split graph.py**
   - ❌ Current: 2,471 lines (5x limit)
   - ✅ Split into:
     - `graph.py` - WorkflowState, RunContext (200 lines)
     - `nodes/` - Individual node implementations (50-200 lines each)
     - `runner.py` - Already exists, keep it
     - `legacy.py` - Move legacy code here, mark as deprecated

3. **Convert Legacy to YAML**
   - ✅ Convert `_build_legacy_workflow_graph()` to `configs/workflows/ybis_native.yaml`
   - ✅ Already exists! Just remove legacy code

---

### 5.2 Medium-Term Improvements

4. **Python Workflow Support**
   - ✅ Add support for Python-based workflows (like Prefect)
   - ✅ Allow workflows to be defined in Python files
   - ✅ Keep YAML support for simple workflows

5. **Runtime Workflow Creation**
   - ✅ Allow workflows to be created at runtime (via API)
   - ✅ Store workflows in database, not just files
   - ✅ Support workflow versioning and migration

6. **Workflow Composition**
   - ✅ Allow workflows to call other workflows (sub-workflows)
   - ✅ Support workflow templates with parameters
   - ✅ Dynamic workflow generation based on task type

---

### 5.3 Long-Term Vision

7. **Self-Evolving Workflows**
   - ✅ Use EvoAgentX to evolve workflows automatically
   - ✅ Learn optimal workflow structures from past runs
   - ✅ Generate workflows based on task characteristics

8. **Hybrid Orchestration**
   - ✅ Use Prefect for production scheduling/observability
   - ✅ Use LangGraph for agentic workflow logic
   - ✅ Best of both worlds

---

## PART 6: Flexibility Scorecard

| Feature | Current State | Target State | Gap |
|---------|--------------|--------------|-----|
| **YAML Workflows** | ✅ Fully Flexible | ✅ Fully Flexible | ✅ None |
| **Node Registration** | ✅ Fully Flexible | ✅ Fully Flexible | ✅ None |
| **Dynamic Conditions** | ✅ Fully Flexible | ✅ Fully Flexible | ✅ None |
| **Workflow Inheritance** | ✅ Fully Flexible | ✅ Fully Flexible | ✅ None |
| **Parallel Execution** | ✅ Fully Flexible | ✅ Fully Flexible | ✅ None |
| **Legacy Graph** | ❌ Hardcoded | ✅ Removed | 🔴 **CRITICAL** |
| **Graph.py Size** | ❌ 2,471 lines | ✅ < 500 lines | 🔴 **CRITICAL** |
| **Python Workflows** | ❌ Not Supported | ✅ Supported | 🟡 Medium |
| **Runtime Creation** | ❌ File-based only | ✅ API + Database | 🟡 Medium |
| **Workflow Composition** | ❌ Not Supported | ✅ Supported | 🟡 Medium |

**Overall Flexibility:** 60% → **Target: 90%**

---

## PART 7: Answer to User's Question

> "Bizim yapı esnek workflowları destekler şekilde mi? Graph baya durağan?"

**Answer:**

✅ **YES, the structure SUPPORTS flexible workflows** (YAML-based system is fully flexible)

❌ **BUT, graph.py is STATIC** (2,471 lines of hardcoded legacy code)

**The Problem:**
- YAML workflow system is excellent and flexible
- But `graph.py` contains a hardcoded legacy graph as fallback
- Legacy graph is completely static (cannot be modified without code changes)
- Legacy graph violates Constitution (5x file size limit)

**The Solution:**
1. Remove legacy fallback (make YAML mandatory)
2. Split `graph.py` into smaller modules
3. Convert legacy graph to YAML (already done: `ybis_native.yaml`)
4. Add Python workflow support (like Prefect)

**Current State:** Hybrid (60% flexible)  
**Target State:** Fully Flexible (90%+)

---

**Conclusion:** The foundation is good (YAML-based system), but legacy code limits flexibility. Removing legacy and splitting `graph.py` will make the system fully flexible.

