# WORKFLOWS (LangGraph + Routing)

**References:**
- CONSTITUTION.md
- INTERFACES.md
- TESTING.md

**Workflow Specifications:**
- **Workflow Specs:** `configs/workflows/` (YAML files)
- **Workflow Schema:** `configs/workflows/schema.yaml`
- **Workflow Guide:** `docs/workflows/README.md`
- **Example:** `configs/workflows/ybis_native.yaml`

**Note:** Workflows should set executor selection via node config adapters or executor.

---

## Workflow System Overview

YBIS uses **data-driven workflows** defined in YAML files. Workflows specify execution graphs with nodes, connections, and requirements.

**Key Concepts:**
- **Workflow Spec:** YAML file defining nodes, connections, and requirements
- **Node:** Typed execution step (resolved via `NodeRegistry`)
- **Connection:** Edge between nodes (with optional conditional routing)
- **Artifact Enforcement:** Gate blocks if required artifacts are missing

**See:** [`docs/workflows/README.md`](workflows/README.md) for complete workflow specification guide.

---

## The Spec-First Protocol

**Philosophy:** "Think twice, code once."

We do not let agents "figure it out" in code. We define the **Spec** first, then the agent executes.

### The Roles

1. **The Architect** (What/Why)
   - Defines the problem, goals, and constraints.
   - Outputs: Requirements, structure, strategy.

2. **The Spec Writer** (How)
   - Converts requirements into technical specifications.
   - Outputs: Data models, API signatures, state charts, pseudo-code.

3. **The Executor** (Implementation)
   - Implements the spec exactly as defined.
   - **Constraint:** CANNOT deviate from the spec. If spec is wrong, halt and ask Architect.
   - Outputs: Code, tests, artifacts.

### The Workflow

1. Architect defines requirements.
2. Spec Writer creates technical spec.
3. Executor implements spec.
4. Verifier validates against spec.
5. Gate checks compliance.

**Forbidden:** "Cowboy Coding" (coding without a spec) is explicitly forbidden. All code must trace back to a spec.

---

## Canonical Workflows

Workflows are defined in `configs/workflows/` as YAML files.

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
9. **gate** → Check gates (verification + risk + artifacts)
10. **debate** → Council debate (if blocked)

**Required Artifacts (enforced by gate):**
- `plan.json`
- `executor_report.json`
- `verifier_report.json`
- `gate_report.json`
- `spec_structure_validation.json`
- `plan_validation.json`
- `implementation_validation.json`

### Future Workflows

- **speckit:** Spec-Kit-like workflow (planned)
- **bmad:** BMAD-like step-file workflow (planned)
- **evoagentx:** EvoAgentX-like workflow (planned)

**See:** `docs/workflows/README.md` for creating custom workflows.

## Shared skeleton
1) resolve_config (freeze policy snapshot)
2) init_run (create run folder + META.json)
3) acquire_context (optional)
4) plan
5) execute
6) apply_patch (syscall)
7) verify (ruff+pytest)
8) gates_and_risk (deterministic)
9) finalize (update DB)
10) approval step if required

## Deterministic Routing

Routing is defined in workflow specs with conditional functions:

- **verify fail + retries remaining** → repair loop
- **verify pass** → gates
- **gates PASS** → SUCCESS
- **gates REQUIRE_APPROVAL** → stop and request approval
- **gates BLOCK** → BLOCKED (or debate)

**Conditional Functions:**
- `should_continue_steps(state)` - Continue multi-step plan?
- `should_retry_route(state)` - Retry via repair or proceed?
- `should_debate(state)` - Route to debate or end?

**See:** `src/ybis/workflows/conditional_routing.py` for implementation.

---

## Gate Enforcement

The gate enforces workflow requirements:

1. **Verification Gate:** Checks verifier report (lint + tests)
2. **Risk Gate:** Checks patch size and protected paths
3. **Artifact Gate:** Checks for required workflow artifacts (Task D)

**Artifact Enforcement:**
- If workflow declares `requirements.artifacts`, gate checks for each artifact
- Missing artifacts → **BLOCK** decision
- All artifacts present → Continue with other gate checks

**See:** `src/ybis/orchestrator/graph.py:gate_node()` for implementation.