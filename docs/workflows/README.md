# YBIS Workflow Specifications

**Purpose:** This directory contains workflow specifications that define execution graphs for YBIS tasks.

**Location:** `configs/workflows/`  
**Format:** YAML  
**Schema:** `configs/workflows/schema.yaml`

---

## Overview

YBIS uses **data-driven workflows** defined in YAML files. Workflows specify:
- **Nodes:** Typed execution steps (resolved via `NodeRegistry`)
- **Connections:** Edges between nodes (with optional conditional routing)
- **Requirements:** Modules, artifacts, and adapters needed by the workflow

The workflow engine (`WorkflowRunner`) loads these specs, resolves node implementations, and builds LangGraph `StateGraph` instances for execution.

---

## Workflow Spec Format

### Basic Structure

```yaml
name: my_workflow
version: 1
description: "Human-readable description"

nodes:
  - id: node1
    type: spec_generator
    description: "Optional node description"
  
  - id: node2
    type: planner
    config:  # Optional node-specific config
      max_steps: 10

connections:
  - from: START
    to: node1
  
  - from: node1
    to: node2
  
  - from: node2
    to: END

requirements:
  modules:
    - verifier
    - gate
  
  artifacts:
    - plan.json
    - verifier_report.json
    - gate_report.json
  
  adapters:
    - local_coder
```

### Required Fields

- **`name`:** Unique workflow identifier (lowercase, alphanumeric + underscores)
- **`version`:** Integer version number (for evolution/migration)
- **`nodes`:** Array of node definitions (at least one)
- **`connections`:** Array of edges between nodes

### Optional Fields

- **`description`:** Human-readable workflow description
- **`requirements`:** Workflow requirements (modules, artifacts, adapters)

---

## Node Types

Nodes are resolved via `NodeRegistry`. Available node types:

### Core Nodes

- **`spec_generator`:** Generates SPEC.md from task objective
- **`spec_validator`:** Validates spec structure and completeness
- **`planner`:** Generates plan.json from spec
- **`plan_validator`:** Validates plan against spec requirements
- **`executor`:** Executes plan using registered executor
- **`impl_validator`:** Validates implementation against spec
- **`verifier`:** Runs verifier (lint + tests)
- **`repair`:** Attempts to fix errors detected by verifier
- **`gate`:** Checks gates (verification + risk)
- **`debate`:** Conducts council debate when blocked

### Extended Nodes (Future)

- **`artifact_expander`:** Expands artifacts (e.g., spec → plan → tasks)
- **`rag_ingest`:** Ingests documents into RAG
- **`memory_read`:** Reads from memory/RAG
- **`memory_write`:** Writes to memory/RAG

**See:** `src/ybis/workflows/node_registry.py` for registered node types.

---

## Connections

### Simple Connections

```yaml
connections:
  - from: node1
    to: node2
```

### Conditional Routing

```yaml
connections:
  - from: verify
    to: repair
    condition: "should_retry_route"
  
  - from: verify
    to: gate
    condition: "should_retry_route"
```

**Conditional functions** are defined in `src/ybis/workflows/conditional_routing.py`:
- `should_continue_steps(state)` - Continue multi-step plan?
- `should_retry_route(state)` - Retry via repair or proceed?
- `should_debate(state)` - Route to debate or end?

---

## Requirements

### Modules

Modules are workflow-level dependencies (e.g., `verifier`, `gate`). These are checked for availability but don't block execution if missing (they're optional).

```yaml
requirements:
  modules:
    - verifier
    - gate
```

### Artifacts

**Artifacts are enforced by the gate.** If a workflow declares required artifacts, the gate will **BLOCK** if any are missing.

```yaml
requirements:
  artifacts:
    - plan.json
    - executor_report.json
    - verifier_report.json
    - gate_report.json
```

**Artifact paths:** All artifacts are expected in `workspaces/<task_id>/runs/<run_id>/artifacts/`

**Gate enforcement:** See `src/ybis/orchestrator/graph.py:gate_node()` for artifact checking logic.

### Adapters

Adapters are checked via policy (not enforced by gate). If an adapter is required but not available, the workflow may fail or use a fallback.

```yaml
requirements:
  adapters:
    - local_coder
    - e2b_sandbox
```

---

## Creating a New Workflow

### Step 1: Create YAML File

Create `configs/workflows/my_workflow.yaml`:

```yaml
name: my_workflow
version: 1
description: "My custom workflow"

nodes:
  - id: spec
    type: spec_generator
  
  - id: plan
    type: planner
  
  - id: execute
    type: executor
  
  - id: verify
    type: verifier
  
  - id: gate
    type: gate

connections:
  - from: START
    to: spec
  
  - from: spec
    to: plan
  
  - from: plan
    to: execute
  
  - from: execute
    to: verify
  
  - from: verify
    to: gate
  
  - from: gate
    to: END

requirements:
  artifacts:
    - plan.json
    - executor_report.json
    - verifier_report.json
    - gate_report.json
```

### Step 2: Register Nodes (if needed)

If you're using custom node types, register them in `src/ybis/workflows/bootstrap.py`:

```python
NodeRegistry.register(
    "my_custom_node",
    my_custom_node_function,
    description="My custom node",
)
```

### Step 3: Test Workflow

```python
from ybis.workflows import WorkflowRunner

runner = WorkflowRunner().load_workflow("my_workflow")
graph = runner.build_graph()

# Execute workflow
result = graph.invoke(initial_state)
```

---

## Example Workflows

### ybis_native

**File:** `configs/workflows/ybis_native.yaml`

The canonical YBIS workflow with spec-first validation and repair loop:

1. **spec** → Generate SPEC.md
2. **validate_spec** → Validate spec structure
3. **plan** → Generate plan.json
4. **validate_plan** → Validate plan against spec
5. **execute** → Execute plan
6. **validate_impl** → Validate implementation
7. **verify** → Run verifier (lint + tests)
8. **repair** → Fix errors (if needed)
9. **gate** → Check gates
10. **debate** → Council debate (if blocked)

**Required Artifacts:**
- `plan.json`
- `executor_report.json`
- `verifier_report.json`
- `gate_report.json`
- `spec_structure_validation.json`
- `plan_validation.json`
- `implementation_validation.json`

---

## Workflow Execution

### Loading a Workflow

```python
from ybis.workflows import WorkflowRegistry

# Load workflow spec
workflow_spec = WorkflowRegistry.load_workflow("ybis_native")

# Access workflow properties
print(workflow_spec.name)  # "ybis_native"
print(workflow_spec.nodes)  # List of node definitions
print(workflow_spec.requirements)  # Requirements dict
```

### Building a Graph

```python
from ybis.workflows import WorkflowRunner

# Build graph from workflow spec
runner = WorkflowRunner().load_workflow("ybis_native")
graph = runner.build_graph()

# Graph is a compiled LangGraph StateGraph
# Ready for execution
```

### Executing a Workflow

Workflows are executed via `build_workflow_graph()` in `src/ybis/orchestrator/graph.py`:

```python
from ybis.orchestrator.graph import build_workflow_graph

# Build graph (default: "ybis_native")
graph = build_workflow_graph("ybis_native")

# Execute with initial state
initial_state = {
    "task_id": "TASK-123",
    "run_id": "run-001",
    "task_objective": "Implement feature X",
    # ... other state fields
}

result = graph.invoke(initial_state)
```

---

## Validation

### Schema Validation

Workflow specs are validated against `configs/workflows/schema.yaml` when loaded.

**Validation checks:**
- Required fields present
- Node IDs are unique
- Connections reference valid nodes
- At least one gate node exists

### Runtime Validation

**Artifact Enforcement:**
- Gate checks for required artifacts
- Missing artifacts → BLOCK decision
- See `src/ybis/orchestrator/graph.py:gate_node()` for implementation

**Module Availability:**
- Modules are checked but don't block execution
- Missing modules may cause node failures

**Adapter Availability:**
- Adapters are checked via policy
- Missing adapters may cause fallback behavior

---

## Best Practices

### 1. Always Include a Gate Node

```yaml
nodes:
  - id: gate
    type: gate  # Required for workflow execution
```

### 2. Declare Required Artifacts

```yaml
requirements:
  artifacts:
    - plan.json
    - verifier_report.json
    - gate_report.json
```

This ensures gate enforcement and makes workflow requirements explicit.

### 3. Use Descriptive Node IDs

```yaml
nodes:
  - id: generate_spec  # Good: descriptive
    type: spec_generator
  
  - id: n1  # Bad: unclear
    type: spec_generator
```

### 4. Document Complex Workflows

Add comments in YAML for complex routing logic:

```yaml
connections:
  # Conditional: Retry via repair or proceed to gate
  - from: verify
    to: repair
    condition: "should_retry_route"
  
  - from: verify
    to: gate
    condition: "should_retry_route"
```

### 5. Version Your Workflows

```yaml
name: my_workflow
version: 1  # Increment when making breaking changes
```

---

## Migration Guide

### From Hardcoded to Workflow Spec

**Before (hardcoded):**
```python
def build_workflow_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("spec", spec_node)
    graph.add_node("plan", plan_node)
    # ... hardcoded nodes
    return graph.compile()
```

**After (workflow spec):**
```yaml
# configs/workflows/my_workflow.yaml
name: my_workflow
nodes:
  - id: spec
    type: spec_generator
  - id: plan
    type: planner
# ... workflow spec
```

```python
# Code
def build_workflow_graph(workflow_name="my_workflow"):
    runner = WorkflowRunner().load_workflow(workflow_name)
    return runner.build_graph()
```

---

## References

- **Schema:** `configs/workflows/schema.yaml`
- **Example:** `configs/workflows/ybis_native.yaml`
- **Registry:** `src/ybis/workflows/registry.py`
- **Runner:** `src/ybis/workflows/runner.py`
- **Node Registry:** `src/ybis/workflows/node_registry.py`
- **Bootstrap:** `src/ybis/workflows/bootstrap.py`
- **Conditional Routing:** `src/ybis/workflows/conditional_routing.py`
- **GRAND_ARCHITECTURE.md:** `docs/GRAND_ARCHITECTURE.md`

---

**Last Updated:** 2026-01-09

