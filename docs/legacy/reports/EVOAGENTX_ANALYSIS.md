# EvoAgentX Analysis & Integration Plan

**Date:** 2026-01-10  
**Status:** Analysis Complete, Integration Pending

---

## EvoAgentX Overview

**EvoAgentX** is a self-evolving AI agent framework that:
- **Auto-constructs** multi-agent workflows from a single prompt
- **Evaluates** workflows using built-in evaluators
- **Optimizes** workflows using self-evolution algorithms (TextGrad, AFlow, MIPRO, SEW)
- **Supports** memory (short-term & long-term), HITL, and comprehensive tools

---

## Key Components

### 1. Workflow Generation
- **`WorkFlowGenerator`**: Generates multi-agent workflows from natural language goals
- **`WorkFlowGraph`**: Represents workflow structure (nodes, edges)
- **`WorkFlow`**: Executes workflows with agent manager

### 2. Optimizers (Self-Evolution)
- **`TextGradOptimizer`**: Gradient-based prompt optimization
- **`AFlowOptimizer`**: Automated workflow optimization
- **`MIPROOptimizer`**: Multi-iteration prompt optimization
- **`SEWOptimizer`**: Self-evolving workflow optimization

### 3. Evaluators
- **`WorkflowEvaluator`**: Evaluates workflow performance
- **`AFlowEvaluator`**: AFlow-specific evaluation

### 4. Tools
- Code interpreters (Python, Docker)
- Search tools (Google, Wikipedia, arXiv)
- Database tools (MongoDB, PostgreSQL, FAISS)
- Browser automation
- File I/O
- Image tools

---

## Current YBIS Integration Status

### ✅ Implemented
- Adapter skeleton (`src/ybis/adapters/evoagentx.py`)
- Workflow spec (`configs/workflows/evo_evolve.yaml`)
- Node implementation (`workflow_evolver_node` in `graph.py`)
- Registry registration

### ❌ Missing (Real Integration)
- Actual EvoAgentX API calls
- Workflow spec conversion (YBIS ↔ EvoAgentX)
- Optimizer integration
- Evaluator integration

---

## Integration Plan

### Phase 1: Basic Workflow Evolution

**Goal:** Use EvoAgentX to evolve YBIS workflow specs based on metrics.

**Steps:**
1. Convert YBIS workflow spec (YAML) to EvoAgentX format
2. Use EvoAgentX optimizer to evolve workflow
3. Convert evolved workflow back to YBIS format
4. Test with simple workflow

**Files to Modify:**
- `src/ybis/adapters/evoagentx.py` - Implement `evolve()` method
- Add conversion utilities (YBIS ↔ EvoAgentX)

### Phase 2: Workflow Scoring

**Goal:** Use EvoAgentX evaluator to score workflows.

**Steps:**
1. Extract metrics from YBIS artifacts
2. Use EvoAgentX evaluator to score workflow
3. Return normalized score (0.0-1.0)

**Files to Modify:**
- `src/ybis/adapters/evoagentx.py` - Implement `score()` method

### Phase 3: Full Integration

**Goal:** Full EvoAgentX capabilities in YBIS.

**Steps:**
1. Workflow generation from goals
2. Multi-optimizer support
3. Memory integration
4. Tool integration

---

## EvoAgentX API Usage

### Workflow Generation
```python
from evoagentx.workflow import WorkFlowGenerator, WorkFlowGraph, WorkFlow
from evoagentx.agents import AgentManager

goal = "Generate html code for the Tetris game"
workflow_graph = WorkFlowGenerator(llm=llm).generate_workflow(goal)
```

### Workflow Optimization
```python
from evoagentx.optimizers import TextGradOptimizer, AFlowOptimizer

optimizer = TextGradOptimizer(llm=llm)
evolved_workflow = optimizer.optimize(workflow_graph, metrics)
```

### Workflow Evaluation
```python
from evoagentx.evaluators import WorkflowEvaluator

evaluator = WorkflowEvaluator()
score = evaluator.evaluate(workflow_graph, artifacts)
```

---

## YBIS ↔ EvoAgentX Conversion

### YBIS Workflow Spec (YAML)
```yaml
name: ybis_native
nodes:
  - id: spec
    type: spec_generator
connections:
  - from: START
    to: spec
```

### EvoAgentX Workflow Graph
```python
WorkFlowGraph(
    nodes=[...],
    edges=[...],
    metadata={...}
)
```

**Conversion Strategy:**
- YBIS nodes → EvoAgentX agents
- YBIS connections → EvoAgentX edges
- YBIS artifacts → EvoAgentX evaluation metrics

---

## Next Steps

1. **Implement Basic Evolution:**
   - Convert YBIS workflow to EvoAgentX format
   - Apply optimizer
   - Convert back to YBIS format

2. **Test with Simple Workflow:**
   - Use `ybis_native` workflow
   - Run evolution
   - Verify evolved workflow

3. **Add Scoring:**
   - Use EvoAgentX evaluator
   - Score based on artifacts

4. **Full Integration:**
   - Workflow generation
   - Multi-optimizer support
   - Memory & tools

---

## References

- `vendors/EvoAgentX/README.md` - EvoAgentX documentation
- `src/ybis/adapters/evoagentx.py` - Current adapter
- `configs/workflows/evo_evolve.yaml` - Evolution workflow spec
- `docs/ADAPTER_INTEGRATION_PLAN.md` - Integration plan

