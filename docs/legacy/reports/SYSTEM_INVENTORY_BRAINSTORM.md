# System Inventory Brainstorm

**Purpose:** List everything the project currently contains (capabilities, modules, vendors, workflows, docs, tooling).
**Status:** Brainstorm - raw inventory before cleanup and prioritization.

---

## 1) Core Runtime
- LangGraph-based workflow engine
- Workflow registry + runner
- Policy + gate enforcement
- Syscalls (IO/exec boundary)
- RunContext + immutable run structure

## 2) Orchestrator Nodes
- spec / validate_spec
- plan / validate_plan
- execute / validate_impl
- verify / repair
- gate / debate
- **Vendor Nodes (Phase 2 Complete):**
  - workflow_evolver (EvoAgentX)
  - agent_runtime (reactive-agents)
  - council_reviewer (llm-council)
  - self_improve_reflect / plan / implement / test / integrate (Self-Improve-Swarms)

## 3) Workflow Specs
- configs/workflows/schema.yaml
- configs/workflows/ybis_native.yaml (canonical native workflow)
- **Vendor Workflows (Phase 1 Complete):**
  - configs/workflows/evo_evolve.yaml (EvoAgentX workflow evolution)
  - configs/workflows/reactive_agent.yaml (reactive-agents agent runtime)
  - configs/workflows/council_review.yaml (llm-council multi-model review)
  - configs/workflows/self_improve.yaml (Self-Improve-Swarms self-improvement loop)

## 4) Adapters (Core Types)
- executor (local_coder, aider)
- sandbox (e2b_sandbox, local)
- vector_store (chroma, qdrant)
- graph_store (neo4j)
- event_bus (redis)
- llm (llamaindex_adapter)
- observability (langfuse, opentelemetry)

## 5) Vendor Adapters (Phase 1-3 Complete ✅)
**Status:** Contracts, skeletons, nodes, and graceful fallback implementations complete.
**Vendor API Integration:** Pending (TODO comments ready for real vendor integration)

- **workflow_evolution:** evoagentx (EvoAgentX - workflow evolution & optimization)
- **agent_runtime:** reactive_agents (reactive-agents - tool-using agent execution)
- **council_review:** llm_council (llm-council - multi-model review & ranking)
- **agent_learning:** aiwaves_agents (aiwaves-agents - symbolic learning & pipeline optimization)
- **self_improve_loop:** self_improve_swarms (Self-Improve-Swarms - reflection-based self-improvement)

**Implementation Status:**
- ✅ Contract interfaces (Protocol definitions)
- ✅ Adapter skeletons with graceful fallback
- ✅ Workflow node implementations
- ✅ Method implementations (graceful fallback pattern)
- ✅ Catalog registration
- ✅ Policy toggles (default disabled, opt-in)
- ✅ Test coverage (conformance, validation, smoke, integration)

## 6) Evidence & Gates
- verifier_report.json
- gate_report.json
- spec_validation.json
- dependency_impact.json
- code_quality_metrics.json

## 7) Data Plane
- platform_data/control_plane.db
- platform_data/knowledge/Frameworks
- platform_data/knowledge/Vendors
- workspaces/<task>/runs/<run>

## 8) Tools & Scripts
- scripts/ybis_run.py
- scripts/ybis_worker.py
- scripts/e2e_test_runner.py
- scripts/auto_scrape_package_docs.py
- scripts/ingest_docs_to_rag.py
- scripts/validate_sandbox_profiles.py
- scripts/lint_core_boundary.py

## 9) Docs (Canonical)
- docs/AGENTS.md
- docs/CONSTITUTION.md
- docs/AI_START_HERE.md
- docs/WORKFLOWS.md
- docs/INTERFACES.md
- docs/SECURITY.md
- docs/OPERATIONS.md
- docs/TESTING.md

## 10) Vendors
- autogen, metagpt, langchain, llamaindex
- opendevin, OpenHands, open-interpreter
- EvoAgentX, BMAD, spec-kit, n8n
- langfuse, opentelemetry, promptfoo, trulens
- chroma, qdrant, e2b
- (see vendors/ for full list)

## 11) Gaps (High Level)
- Workflow-first enforcement
- Real-world smoke/regression suites
- RAG closed loop + freshness checks
- Adapter lifecycle policy enforcement
- Observability wiring
- **Vendor API Integration:** Vendor adapters have graceful fallback but need real vendor API integration (Phase 3 TODO comments ready)

---

**Next:** Convert this brainstorm into a structured inventory with ownership, status, and priority.

---

## Append Notes (Unstructured Additions)

Local-first execution remains default, but hard tasks can escalate to external
APIs or headless agents:

- **Local-managed by default:** runs use local models/tools; no external access.
- **Escalation for hard tasks:** policy can allow cloud models for specific steps
  (e.g., complex planning or verification).
- **Headless agent runners:** support invoking Claude Code, Codex, Gemini CLI in
  headless mode as adapters (agent_runtime).  

Inline skills and commands:
- Skills map to **inline command equivalents** (skills -> tools -> syscalls).
- Skill invocation should be traceable in artifacts (inputs, outputs, decisions).

Dashboard:
- Must read `platform_data/control_plane.db` and latest run artifacts.
- Should display: run status, gate decisions, verifier errors, adapter health,
  workflow name, artifact completeness.
- Example: “Run R-1234 failed: Missing required artifacts: plan.json”.

Context graph:
- Build a **context graph** from docs + code + runs.
- Nodes: files, symbols, workflows, adapters, runs.
- Edges: references, dependencies, execution, ownership.
- Example query: “Which workflows touch adapter `evoagentx`?” → graph traversal.

Examples (Concrete):
- **Hard task escalation:** If plan validation score < 0.6, allow one external
  model call to refine spec; record in artifact `escalation_log.json`.
- **Headless runner:** `codex --project . --run "speckit.plan"` -> adapter
  captures output, stores under `artifacts/agent_runtime/`.
- **Inline skill call:** `/skill:debate` -> maps to `debate` node + artifact
  `debate_report.json`.

Additional planned components:
- Local-managed secrets store (per-workspace) for API keys.
- Workflow-level toggles: `allow_cloud`, `allow_headless_agents`,
  `require_context_graph`.

Self-development (Organism Model):
- Define a **self-develop loop** explicitly (reflect -> plan -> implement -> test -> integrate).
- Prefer **external proven frameworks** when flexibility is needed; if not, implement a **YBIS-native** version.
- Treat self-development as a **first-class workflow** with its own task + artifact schema.
- Use existing types (workflow, task, adapter, policy, artifact) to **generate new entities**:
  - Create a new agent profile from tasks + policies.
  - Create a new skill from repeated tool usage patterns.
- Require evidence for self-changes (spec + plan + tests + gate).

Wisdom Additions:
- "Self-improvement without governance is drift."
- "Every evolution needs a rollback path."

Atomic System Model (Industry Alignment):
- **Bounded contexts**: Each subsystem (workflow, adapter, policy, memory, ops)
  is isolated with clear contracts.
- **Immutable execution units**: The atomic unit is the workflow run, not just a
  task. Every run produces artifacts and decisions.
- **Contract-first interfaces**: Components interact only via schemas and
  defined artifacts.
- **Event-sourcing mindset**: All changes are traceable and replayable through
  artifacts.

Gaps I might be missing (call out explicitly):
- **Stable release train**: No clear versioned milestones, which breaks the
  original goal of iterating stable releases to improve other projects.
- **Roadmap discipline**: “Add everything” without version gates leads to drift.

Wisdom Additions (Stability):
- "Without a stable release train, every feature is a moving target."
- "Roadmaps are not plans; they are commitments to stop adding."

MCP External Usage (Headless CLIs):
- **Create task** via MCP: `task_create(title, objective, priority)`
- **Run workflow** via MCP: `task_run(task_id, workflow_name)`
- **Check status** via MCP: `task_status(task_id)`

Gate enforcement for external callers:
- External MCP runs still execute full workflow and gates.
- Gate decisions are written to `artifacts/gate_report.json`.
- If blocked, caller must write approval via `approval_write`.

Additional Gaps and Ideas (Comprehensive):
- **Release train + changelog discipline**: each version has fixed scope,
  freeze, and rollback plan.
- **Workflow versioning**: semver for workflow specs + migration notes.
- **Capability matrix**: adapter/agent/feature compatibility per profile/env.
- **Secrets governance**: local secrets store + redaction + audit trail.
- **Retention policy**: TTL + hold/release for artifacts and logs.
- **Failure taxonomy**: standardized verifier/gate error classes.
- **Sandbox policy**: clear local vs cloud escalation rules + approvals.
- **Benchmark suite**: release scorecard for quality/performance.
- **Compatibility policy**: Python/OS/adapter support matrix.
- **Traceability**: spec -> tasks -> artifacts -> gate chain.

Workflow Flexibility (Idealized):
- Workflows are **not forced to be task-based**. They can run:
  - research-only flows
  - report generation
  - audit/verification flows
  - self-evaluation loops
- Workflows can **invoke other workflows** as subflows.
- Workflow specs should support `call_workflow` nodes.
- Workflows must declare whether they require tasks or are taskless.

Sandbox and Git Discipline (Idealized):
- **Sandbox is mandatory** for risky steps (exec, external tools).
- **Git usage stabilized**:
  - Explicit commit policy per workflow (when/if to commit).
  - Artifacts capture commit hashes and diffs.
  - No hidden git operations; all via syscalls.
- Commit strategy is workflow-configurable (e.g., commit per phase, commit at end).
