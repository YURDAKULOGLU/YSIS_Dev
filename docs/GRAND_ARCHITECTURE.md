# YBIS Grand Architecture (Execution Spec)

**Purpose:** Comprehensive architecture spec for the next-gen YBIS structure.
This document is the execution blueprint for the executor agent.
**Status:** Draft - refine and enforce.

---

## 1) Vision Summary

YBIS is an agentic development platform that builds and evolves itself. The
design must enable:

- Minimal core with strict boundaries.
- Workflow-defined behavior (data-driven graphs).
- Adapter-first integrations.
- Evidence-first gates (deterministic decisions).
- Immutable runs with traceable artifacts.

---

## 2) Definitions

**Core**: Minimal stable engine that does not vary per workflow.
**Workflow**: Data-defined execution graph (nodes + connections).
**Node**: Typed step resolved via registry.
**Adapter**: External integration resolved via policy.
**Artifact**: Immutable output from a run.
**Gate**: Deterministic decision point (PASS/BLOCK/REQUIRE_APPROVAL).
**Run**: Immutable execution instance (task_id/run_id).

---

## 3) Core Boundary (What Is "Core")

Core is the smallest stable engine that does not change per workflow.

**Core MUST include:**
- Workflow engine runner (LangGraph runtime wrapper).
- Policy loader and gate enforcement.
- Syscalls (all IO/exec passes through syscalls).
- RunContext + immutable run structure.
- Registry for workflows and adapters.

**Core MUST NOT include:**
- Domain-specific workflows (spec/plan/tasks/implement).
- UI or dashboard logic.
- RAG, memory, or storage integrations.
- External frameworks or heavy libraries.

**Core Output:**
- Gate decision (PASS/BLOCK/REQUIRE_APPROVAL).
- Minimal artifacts required by policy.

---

## 4) Workflow-Defined System

Behavior is defined by workflow specs. The engine only executes them.

**Workflow Spec** (YAML, canonical):
- Nodes: typed steps with inputs/outputs.
- Connections: edges between nodes.
- Required modules (optional hooks).
- Artifact expectations (optional).

**Example:**
```yaml
name: ybis_native
version: 1
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
  - from: spec
    to: plan
  - from: plan
    to: execute
  - from: execute
    to: verify
  - from: verify
    to: gate
requirements:
  modules:
    - verifier
    - gate
  artifacts:
    - plan.json
    - executor_report.json
    - verifier_report.json
    - gate_report.json
```

**Rules:**
- Gate node is mandatory.
- Nodes resolve via registry (type -> implementation).
- Workflows live in `configs/workflows/`.

---

## 5) Node and Adapter Model

**Node Types (examples):**
- spec_generator
- planner
- tasks_generator
- executor
- verifier
- gate
- debate
- artifact_expander
- rag_ingest

**Adapter Registry:**
- Adapter types: llm, vector_store, graph_store, sandbox, executor, event_bus.
- Adapter selection is policy-driven.
- Default behavior is opt-in (disabled unless enabled).

---

## 6) Artifacts: Optional by Workflow

Artifacts are not mandatory globally. They are required per workflow, enforced
by policy and workflow spec.

**Artifact classes:**
- plan.json
- spec.md
- tasks.md
- executor_report.json
- verifier_report.json
- gate_report.json
- validation reports

**Rule:** If workflow declares an artifact, it must exist or gate blocks.

---

## 7) Evidence-First Gates

Gate logic is deterministic and policy-driven.

**Gate inputs:**
- Verifier report (lint/test/coverage).
- Workflow-declared artifacts.
- Spec compliance (optional per workflow).
- Risk gate (patch size + protected paths).

**Decisions:**
- PASS: all required checks pass.
- BLOCK: required artifact missing or failures.
- REQUIRE_APPROVAL: policy or risk demands review.

---

## 8) RAG and Memory (Not Core)

RAG is an optional module:

- Docs ingestion -> `platform_data/knowledge/`.
- Vector store adapter enabled by policy.
- Retrieval policy defines top-k and source scope.

**RAG integration is workflow-based** (not global).

---

## 9) Documentation Taxonomy (Canonical)

**Core docs (authoritative):**
- docs/AGENTS.md (entry point)
- docs/CONSTITUTION.md
- docs/INTERFACES.md
- docs/WORKFLOWS.md
- docs/SECURITY.md

**Workflow docs:**
- docs/workflows/

**Adapter docs:**
- docs/adapters/

**Operational docs:**
- docs/OPERATIONS.md
- docs/TESTING.md

**Legacy:**
- legacy/ (isolated; no forward references)

---

## 10) Deliverables (Spec)

**Core deliverables:**
- `configs/workflows/schema.yaml` (workflow schema)
- `src/ybis/workflows/registry.py` (WorkflowRegistry)
- `src/ybis/workflows/runner.py` (WorkflowRunner)
- `configs/workflows/ybis_native.yaml` (native workflow spec)

**Supporting deliverables:**
- `docs/workflows/README.md` (workflow spec guide)
- `docs/WORKFLOWS.md` updated to reference workflow spec

---

## 11) Migration Plan (Current -> Workflow Spec)

**Phase 1: Define Spec Format**
- Create workflow schema and validator.
- Build `WorkflowRegistry`.

**Phase 2: Wrap Existing Graph**
- Create `configs/workflows/ybis_native.yaml`.
- Map current LangGraph nodes to registry nodes.

**Phase 3: Add Optional Workflows**
- SpecKit-like workflow.
- BMAD-like step-file workflow.

---

## 12) Execution Tasks (For Executor)

### Task A: Workflow Spec System
- Add workflow schema + validation.
- Add `WorkflowRegistry` with load/resolve functions.
- Add `WorkflowRunner` to execute workflows.

### Task B: Node Registry
- Register node types for existing graph steps.
- Ensure node adapter interface is stable.

### Task C: ybis_native Workflow
- Serialize existing graph into workflow YAML.
- Verify it runs without core change.

### Task D: Workflow Artifact Enforcement
- If workflow declares artifacts, block on missing.
- Add to gate logic.

### Task E: Docs and Taxonomy
- Add `docs/workflows/README.md`.
- Update `docs/WORKFLOWS.md` to reference workflow spec.

---

## 13) Acceptance Criteria

- Workflow spec can express existing graph.
- Runner can execute `ybis_native` workflow.
- Gate blocks on missing declared artifacts.
- Core stays minimal; no new heavy dependencies.
- Docs point to workflow spec as source of truth.

---

## 14) Non-Negotiables

- All writes/execs via syscalls.
- Runs are immutable.
- Gate + verifier must pass for "done".
- Protected paths require approval.
- No large third-party frameworks inside core.
