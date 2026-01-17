# Workflow System Enhancements

## Status: ✅ IMPLEMENTED

Enhanced workflow system with Node Config Injection and Dynamic Conditional Routing.

---

## ✅ 1. Node Config Injection - IMPLEMENTED

### Problem
Node'lar YAML'dan config alamıyordu. Her node hardcoded parametrelerle çalışıyordu.

### Solution
Node'lar artık YAML'dan config alabiliyor.

### Implementation

**Location:** `src/ybis/workflows/node_config.py`

**Features:**
- `inject_node_config()` - Config'i node function'a inject eder
- `get_node_config()` - State'den config değeri okur

**Usage in YAML:**
```yaml
nodes:
  - id: spec
    type: spec_generator
    config:
      model: "ollama/llama3.2:3b"
      temperature: 0.7
      max_tokens: 2000
```

**Usage in Node:**
```python
def spec_node(state: WorkflowState) -> WorkflowState:
    from ..workflows.node_config import get_node_config
    
    # Get config from YAML
    model = get_node_config(state, "spec", "model", default="ollama/llama3.2:3b")
    temperature = get_node_config(state, "spec", "temperature", default=0.7)
    
    # Use config
    ...
```

**Integration:**
- `WorkflowRunner.build_graph()` - Config'i node'a inject ediyor
- Config state'de saklanıyor, downstream node'lar erişebiliyor

---

## ✅ 2. Dynamic Conditional Routing - IMPLEMENTED

### Problem
Condition'lar sadece 3 sabit fonksiyonla sınırlıydı:
- `should_continue_steps`
- `should_retry_route`
- `should_debate`

Yeni condition'lar eklemek için kod değişikliği gerekiyordu.

### Solution
Condition'lar artık YAML'dan dinamik olarak tanımlanabiliyor.

### Implementation

**Location:** `src/ybis/workflows/dynamic_conditions.py`

**Condition Types:**

#### 1. State Check
```yaml
connections:
  - from: verify
    to: repair
    condition:
      type: state_check
      field: status
      operator: eq
      value: "failed"
      routes:
        true: repair
        false: gate
```

**Operators:**
- `eq` - Equal
- `ne` - Not equal
- `in` - In list
- `not_in` - Not in list
- `gt`, `gte`, `lt`, `lte` - Comparisons
- `exists`, `not_exists` - Existence checks

#### 2. Artifact Check
```yaml
connections:
  - from: plan
    to: execute
    condition:
      type: artifact_check
      artifact: plan.json
      check: exists
      routes:
        true: execute
        false: plan
```

**Check Types:**
- `exists` - Artifact exists
- `not_exists` - Artifact doesn't exist
- `has_content` - Artifact exists and has content

#### 3. Expression (Advanced)
```yaml
connections:
  - from: gate
    to: debate
    condition:
      type: expression
      expression: "state.get('risk_score', 0) > 50"
      routes:
        true: debate
        false: END
```

**Integration:**
- `WorkflowRunner.build_graph()` - YAML condition'ları parse ediyor
- `create_condition_function()` - Condition function oluşturuyor
- Legacy function name'ler hala destekleniyor (backward compatible)

---

## ✅ 3. Parallel Nodes - IMPLEMENTED

**Status:** ✅ Fully implemented

**How it works:**
LangGraph automatically executes nodes in parallel when multiple edges are added from the same source. No special syntax needed!

**Usage:**
```yaml
connections:
  # PARALLEL EXECUTION: Both test1 and test2 start after plan
  - from: plan
    to: test1
  
  - from: plan
    to: test2
  
  # Synchronization: Both must complete before verify
  - from: test1
    to: verify
  
  - from: test2
    to: verify
```

**What happens:**
1. `plan` completes
2. `test1` and `test2` start **simultaneously** (parallel)
3. `verify` waits for **both** to complete (synchronization)

**Implementation:**
- `src/ybis/workflows/parallel_execution.py` - Utilities for parallel execution
- `WorkflowRunner.build_graph()` - Automatically handles parallel edges
- LangGraph's StateGraph handles parallel execution natively

**Example:** `configs/workflows/example_parallel.yaml`

---

## ✅ 4. Workflow Inheritance - IMPLEMENTED

**Status:** ✅ Fully implemented

**Features:**
- `extends` keyword for workflow inheritance
- Node override (same ID overrides base)
- Connection override (same from/to overrides base)
- Requirements merge (union of base + child)

**Usage:**
```yaml
name: advanced_workflow
extends: ybis_native

nodes:
  # Override existing node with custom config
  - id: spec
    type: spec_generator
    config:
      model: "ollama/qwen2.5-coder:32b"
      temperature: 0.3
  
  # Add new node
  - id: pre_validate
    type: spec_validator
    description: "Pre-validation step"

connections:
  # Override: Add pre-validation before spec
  - from: START
    to: pre_validate
  
  - from: pre_validate
    to: spec
  
  # All other connections from base workflow are preserved
```

**Merge Strategy:**
- **Nodes:** Child nodes with same ID override base nodes, new nodes are added
- **Connections:** Child connections with same (from, to) override base, new connections are added
- **Requirements:** Union of base and child (no duplicates)
- **Config:** Child config merges with base config (child overrides base values)

**Implementation:**
- `src/ybis/workflows/inheritance.py` - Inheritance resolution
- `WorkflowRegistry.load_workflow()` - Automatically resolves inheritance
- `resolve_workflow_inheritance()` - Merges base and child specs

**Example:** `configs/workflows/example_inheritance.yaml`

---

## Usage Examples

### Example 1: Node Config

```yaml
nodes:
  - id: spec
    type: spec_generator
    config:
      model: "ollama/qwen2.5-coder:32b"
      temperature: 0.3
      max_retries: 3
```

### Example 2: Dynamic Condition

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

### Example 3: Artifact Condition

```yaml
connections:
  - from: plan
    to: execute
    condition:
      type: artifact_check
      artifact: plan.json
      check: has_content
      routes:
        true: execute
        false: plan
```

---

## Benefits

1. **Flexibility:**
   - Node'lar YAML'dan config alabiliyor
   - Condition'lar YAML'dan tanımlanabiliyor
   - Kod değişikliği olmadan workflow özelleştirilebiliyor

2. **Backward Compatibility:**
   - Legacy function name'ler hala çalışıyor
   - Mevcut workflow'lar etkilenmiyor

3. **Extensibility:**
   - Yeni condition type'ları kolayca eklenebiliyor
   - Node config sistemi genişletilebiliyor

---

## Future Enhancements

- [ ] Parallel node execution
- [ ] Workflow inheritance
- [ ] Condition composition (AND/OR)
- [ ] Config validation schema
- [ ] Config inheritance from base workflow

