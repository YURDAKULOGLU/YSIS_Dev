# EvoAgentX Quick Start for YBIS

**Date:** 2026-01-10

---

## EvoAgentX Nedir?

**EvoAgentX** = Self-evolving AI agent framework

### Özellikler:
1. **Workflow Auto-Construction**: Tek prompt'tan multi-agent workflow oluşturur
2. **Built-in Evaluation**: Otomatik değerlendirme
3. **Self-Evolution**: Workflow'ları optimize eder (TextGrad, AFlow, MIPRO, SEW)
4. **Memory**: Kısa ve uzun vadeli hafıza
5. **HITL**: Human-in-the-loop desteği
6. **Tools**: 30+ built-in tool (code, search, database, browser, image)

---

## YBIS'te Ne İşe Yarar?

### Mevcut Durum:
- ✅ Adapter skeleton var (`src/ybis/adapters/evoagentx.py`)
- ✅ Workflow spec var (`configs/workflows/evo_evolve.yaml`)
- ❌ **Gerçek entegrasyon yok** (placeholder kod)

### Yapılacaklar:

#### 1. Workflow Evolution
```python
# YBIS workflow spec'i al
ybis_workflow = load_workflow("ybis_native")

# EvoAgentX'e çevir
evo_workflow = convert_to_evoagentx(ybis_workflow)

# Optimize et
optimizer = TextGradOptimizer(llm=llm)
evolved = optimizer.optimize(evo_workflow, metrics)

# YBIS'e geri çevir
ybis_evolved = convert_to_ybis(evolved)
```

#### 2. Workflow Scoring
```python
# Artifact'ları al
artifacts = {
    "verifier_report": {...},
    "gate_report": {...}
}

# EvoAgentX evaluator ile score
evaluator = WorkflowEvaluator(llm=llm)
score = evaluator.evaluate(workflow, artifacts)
```

#### 3. Workflow Generation
```python
# Goal'dan workflow oluştur
goal = "Improve YBIS spec quality"
generator = WorkFlowGenerator(llm=llm)
workflow = generator.generate_workflow(goal)
```

---

## EvoAgentX API Örnekleri

### Workflow Generation
```python
from evoagentx.workflow import WorkFlowGenerator, WorkFlowGraph, WorkFlow
from evoagentx.agents import AgentManager

goal = "Generate html code for the Tetris game"
workflow_graph = WorkFlowGenerator(llm=llm).generate_workflow(goal)

agent_manager = AgentManager()
agent_manager.add_agents_from_workflow(workflow_graph, llm_config=llm_config)

workflow = WorkFlow(graph=workflow_graph, agent_manager=agent_manager, llm=llm)
output = workflow.execute()
```

### Workflow Optimization
```python
from evoagentx.optimizers import TextGradOptimizer, AFlowOptimizer

optimizer = TextGradOptimizer(llm=llm, graph=workflow_graph)
optimizer.optimize(dataset=benchmark)
```

### Workflow Evaluation
```python
from evoagentx.evaluators import Evaluator

evaluator = Evaluator(llm=llm)
results = evaluator.evaluate(graph=workflow_graph, benchmark=benchmark)
```

---

## YBIS ↔ EvoAgentX Conversion

### YBIS Format (YAML)
```yaml
name: ybis_native
nodes:
  - id: spec
    type: spec_generator
connections:
  - from: START
    to: spec
```

### EvoAgentX Format (Python)
```python
WorkFlowGraph(
    nodes=[WorkFlowNode(...)],
    edges=[WorkFlowEdge(...)],
    goal="..."
)
```

**Conversion Strategy:**
- YBIS `nodes` → EvoAgentX `WorkFlowNode`
- YBIS `connections` → EvoAgentX `WorkFlowEdge`
- YBIS `artifacts` → EvoAgentX evaluation metrics

---

## Next Steps

1. **Implement Basic Evolution** (Phase 1)
   - Convert YBIS → EvoAgentX
   - Apply optimizer
   - Convert EvoAgentX → YBIS

2. **Add Scoring** (Phase 2)
   - Use EvoAgentX evaluator
   - Score based on artifacts

3. **Full Integration** (Phase 3)
   - Workflow generation
   - Multi-optimizer support
   - Memory & tools

---

## Test Plan

1. **Test Workflow Evolution:**
   ```bash
   python scripts/ybis_run.py T-TEST --workflow evo_evolve
   ```

2. **Verify Evolution:**
   - Check `workflow_evolution.json`
   - Compare original vs evolved workflow
   - Run evolved workflow

3. **Test Scoring:**
   - Run workflow
   - Check `workflow_evolution.json` for score
   - Verify score is 0.0-1.0

---

## References

- `vendors/EvoAgentX/README.md` - Full documentation
- `docs/reports/EVOAGENTX_ANALYSIS.md` - Detailed analysis
- `src/ybis/adapters/evoagentx.py` - Current adapter
- `configs/workflows/evo_evolve.yaml` - Evolution workflow

