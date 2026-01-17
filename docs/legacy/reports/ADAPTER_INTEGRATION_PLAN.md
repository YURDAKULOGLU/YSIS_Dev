# Adapter Integration Plan (Vendor Targets)

**Purpose:** Define how selected vendor systems map to YBIS adapters and
workflows without bloating core.
**Scope:** EvoAgentX, reactive-agents, llm-council, aiwaves-agents,
Self-Improve-Swarms.

---

## 1) Target Selection (Why These)

- **EvoAgentX**: Workflow evolution + evaluators/optimizers.
- **reactive-agents**: Tool-using agent builder + MCP support.
- **llm-council**: Multi-model review and ranking.
- **aiwaves-agents**: Symbolic learning + agent pipeline optimization.
- **Self-Improve-Swarms**: Reflection -> plan -> implement -> test -> integrate loop.

---

## 2) Adapter Types to Add

Each vendor maps to a new adapter type, not core:

1) **workflow_evolution** (EvoAgentX)
2) **agent_runtime** (reactive-agents)
3) **council_review** (llm-council)
4) **agent_learning** (aiwaves-agents)
5) **self_improve_loop** (Self-Improve-Swarms)

---

## 3) Required Interfaces (Contracts)

Create new contract interfaces in `src/ybis/contracts/`:

### 3.1 workflow_evolution
- `evolve(workflow_spec: dict, metrics: dict) -> dict`
- `score(workflow_spec: dict, artifacts: dict) -> float`

### 3.2 agent_runtime
- `run(task: str, tools: list[str], context: dict) -> dict`
- `supports_tools() -> bool`

### 3.3 council_review
- `review(prompt: str, candidates: list[str]) -> dict`

### 3.4 agent_learning
- `learn(trajectory: dict) -> dict`
- `update_pipeline(pipeline: dict, gradients: dict) -> dict`

### 3.5 self_improve_loop
- `reflect(state: dict) -> dict`
- `plan(reflection: dict) -> dict`
- `implement(plan: dict) -> dict`
- `test(implementation: dict) -> dict`
- `integrate(result: dict) -> dict`

---

## 4) Adapter Implementations (Per Vendor)

### 4.1 EvoAgentX Adapter
**Location:** `src/ybis/adapters/evoagentx.py`
- Read workflow spec from YAML.
- Call EvoAgentX optimization/evaluation APIs.
- Return updated workflow spec + score.

### 4.2 reactive-agents Adapter
**Location:** `src/ybis/adapters/reactive_agents.py`
- Map YBIS tool registry to reactive-agents tool decorator inputs.
- Execute run with LLM provider configuration.

### 4.3 llm-council Adapter
**Location:** `src/ybis/adapters/llm_council.py`
- Provide multi-model review function.
- Output ranking + consensus summary.

### 4.4 aiwaves-agents Adapter
**Location:** `src/ybis/adapters/aiwaves_agents.py`
- Provide learning and pipeline update hooks.
- Optional integration: store gradients as artifacts.

### 4.5 Self-Improve-Swarms Adapter
**Location:** `src/ybis/adapters/self_improve_swarms.py`
- Provide loop phases as callable methods.
- Integrate with YBIS gate decisions.

---

## 5) Workflow Integration

Create new workflow specs that call adapters:

1) `configs/workflows/evo_evolve.yaml`
   - Nodes: plan -> execute -> verify -> evolve -> gate

2) `configs/workflows/reactive_agent.yaml`
   - Nodes: spec -> plan -> agent_runtime -> verify -> gate

3) `configs/workflows/council_review.yaml`
   - Nodes: execute -> council_review -> gate

4) `configs/workflows/self_improve.yaml`
   - Nodes: reflect -> plan -> implement -> test -> integrate -> gate

---

## 6) Policy Gates

Add policy toggles for each adapter:

- `adapters.evoagentx.enabled`
- `adapters.reactive_agents.enabled`
- `adapters.llm_council.enabled`
- `adapters.aiwaves_agents.enabled`
- `adapters.self_improve_swarms.enabled`

---

## 7) Executor Task List

### Task 1: Contracts
- Add contract interfaces under `src/ybis/contracts/` for:
  - workflow_evolution
  - agent_runtime
  - council_review
  - agent_learning
  - self_improve_loop
- Ensure each interface includes method stubs listed in Section 3.

### Task 2: Adapter Skeletons
- Create adapter files in `src/ybis/adapters/`:
  - `evoagentx.py`
  - `reactive_agents.py`
  - `llm_council.py`
  - `aiwaves_agents.py`
  - `self_improve_swarms.py`
- Implement minimal adapter classes with method stubs and clear errors for unimplemented calls.
- Register each adapter in the adapter registry and catalog (if used).

### Task 3: Workflow Specs
- Add workflow specs under `configs/workflows/`:
  - `evo_evolve.yaml`
  - `reactive_agent.yaml`
  - `council_review.yaml`
  - `self_improve.yaml`
- Each spec must include a gate node and declared artifacts.

### Task 4: Policy Toggles
- Extend policy profiles to include adapter toggles listed in Section 6.
- Default to disabled (opt-in).

### Task 5: Minimal Smoke Tests
- Add lightweight tests to confirm:
  - Adapter registry registration
  - Workflow spec loads and validates
  - Gate blocks missing declared artifacts
