# .YBIS_Dev Evolution Plan

> **Context:** This is the CLI-agent coordination layer for the Tier 3 Autonomous System (see: `../SYSTEM_STATE.md`).
> The core system has LangGraph orchestration, Aider execution, and RAG memory.
> This folder provides a **file-based, agent-agnostic interface** for multi-CLI-agent coordination.

---

## Current State (MVP)

✅ **What exists:**
- File-based task queue (`Meta/Active/Tasks/{backlog,in_progress,done,blocked}`)
- Artifact sandbox (`.sandbox_hybrid/<TASK_ID>/`)
- Agent capability registry (`Meta/Active/agents.yaml`)
- Contract (`CONTRACT.md`)
- MVP README

❌ **What's missing:**
- CLI implementation (`tools/ybis_dev_cli.py` - referenced but not written)
- Integration with core Tier 3 system (`src/agentic/core/orchestrator_graph.py`)
- Context management (agents have to explore from scratch every time)
- Decision checkpoints (no human-in-the-loop at critical points)
- Validation hooks (no automated quality gates)

---

## Evolution Phases

### Phase 1: CLI Foundation (Priority: P0)

**Goal:** Make `ybis-dev` command actually work.

**Deliverables:**
1. **Create:** `.YBIS_Dev/tools/ybis_dev_cli.py`
   - Commands: `next`, `claim`, `finish`, `verify`, `info`
   - Use `argparse` for CLI parsing
   - Read/write task files from `Meta/Active/Tasks/`
   - Simple file operations (move task files between folders)

2. **Create:** `.YBIS_Dev/tools/core/task_manager.py`
   - Functions: `list_backlog()`, `claim_task(task_id)`, `finish_task(task_id, status)`
   - JSON state tracking (who claimed what, when)

3. **Test:**
   ```bash
   ybis-dev info                    # Show system status
   ybis-dev next --agent claude     # Show next suitable task
   ybis-dev claim T-002             # Move to in_progress/
   ybis-dev finish T-002 --status done
   ```

**Acceptance:** A human or agent can claim/complete tasks using CLI only.

---

### Phase 2: Context Management (Priority: P0)

**Goal:** Stop wasting agent context on exploration. Pre-compute task context.

**Deliverables:**
1. **Create:** `.YBIS_Dev/tools/context_builder.py`
   - Function: `build_context(task_id) -> CONTEXT.json`
   - Analyzes task file, finds relevant code files (using grep/glob)
   - Finds related tests
   - Identifies dependencies (reads `package.json` or similar)
   - Stores minimal context snapshot

2. **CONTEXT.json Schema:**
   ```json
   {
     "task_id": "T-002",
     "files_to_read": ["packages/chat/src/MarkdownRenderer.tsx"],
     "test_files": ["packages/chat/__tests__/MarkdownRenderer.test.tsx"],
     "related_issues": ["T-001"],
     "dependencies": {"react": "18.2.0"},
     "keywords": ["Math.random", "React keys", "streaming"],
     "estimated_scope": "single-file-fix"
   }
   ```

3. **CLI Integration:**
   ```bash
   ybis-dev claim T-002            # Auto-generates CONTEXT.json
   ybis-dev context T-002          # Display context summary
   ```

**Acceptance:** Agent reads CONTEXT.json (50 lines) instead of exploring 200 files.

---

### Phase 3: Decision Checkpoints (Priority: P1)

**Goal:** Enable human decisions at critical junctions without blocking the entire flow.

**Deliverables:**
1. **Create:** `.YBIS_Dev/tools/checkpoint_manager.py`
   - Function: `register_checkpoint(task_id, question, options)`
   - Writes checkpoint to `.sandbox_hybrid/<TASK_ID>/CHECKPOINTS.yaml`
   - CLI command: `ybis-dev checkpoints T-002` (lists pending decisions)

2. **Task Template Update:**
   Add checkpoint markers to task files:
   ```markdown
   ## CHECKPOINT-1: Key generation strategy
   **Question:** How should we generate stable keys?
   **Options:**
     A) index-based (fast, collision risk)
     B) content-hash (stable, expensive)
     C) hybrid (index + substring)
   **Decision:** [PENDING]
   **Decided by:** [username]
   **Rationale:** [to be filled]
   ```

3. **CLI Commands:**
   ```bash
   ybis-dev checkpoints T-002                    # List pending decisions
   ybis-dev decide T-002 --checkpoint 1 --choice C --rationale "Best trade-off"
   ```

**Acceptance:** Agent pauses at checkpoints, human decides, agent continues.

---

### Phase 4: Tier 3 Integration (Priority: P1)

**Goal:** Connect `.YBIS_Dev` CLI with the core `OrchestratorGraph`.

**Why:** The core system has:
- LangGraph orchestration (`src/agentic/core/graphs/orchestrator_graph.py`)
- Aider executor (`src/agentic/core/plugins/aider_executor.py`)
- Sentinel verifier (`src/agentic/core/plugins/sentinel.py`)
- RAG memory (`src/agentic/core/plugins/rag_memory.py`)

**Current gap:** `.YBIS_Dev` is file-based. Core system is Python-based. No bridge.

**Deliverables:**
1. **Create:** `.YBIS_Dev/tools/bridge/orchestrator_bridge.py`
   - Function: `run_task_via_graph(task_id)`
   - Reads task from `Meta/Active/Tasks/in_progress/T-XXX.md`
   - Converts to `TaskState` dict
   - Calls `orchestrator_graph.graph.invoke(state)`
   - Writes results back to `.sandbox_hybrid/<TASK_ID>/`

2. **CLI Command:**
   ```bash
   ybis-dev run T-002 --mode orchestrator    # Use Tier 3 graph
   ybis-dev run T-002 --mode manual          # Use CLI agent (current)
   ```

3. **Handoff Protocol:**
   - If task says `suggested_agents: ["codex"]` → manual mode
   - If task says `suggested_agents: ["orchestrator"]` → graph mode

**Acceptance:** Same task can be executed by:
- Manual agent (Cursor, Claude, Codex)
- Autonomous orchestrator (LangGraph → Aider → Sentinel)

---

### Phase 5: Validation Hooks (Priority: P2)

**Goal:** Automated quality gates before task completion.

**Deliverables:**
1. **Create:** `.YBIS_Dev/tools/hooks/pre_finish.py`
   - Checks:
     - All mandatory artifacts exist (`PLAN.md`, `RESULT.md`)
     - Tests pass (if code changes in `apps/`, `packages/`)
     - No TODOs left in code changes
     - CONTEXT.json matches actual files changed

2. **CLI Integration:**
   ```bash
   ybis-dev verify T-002               # Runs all hooks
   ybis-dev finish T-002 --skip-verify # Force finish (risky)
   ```

**Acceptance:** Task cannot move to `done/` if verification fails.

---

### Phase 6: Agent Learning Loop (Priority: P2)

**Goal:** Capture agent performance data for better task routing.

**Deliverables:**
1. **Create:** `.YBIS_Dev/Meta/Active/agent_history.json`
   ```json
   {
     "codex": {
       "tasks_completed": 5,
       "avg_time_seconds": 120,
       "failure_rate": 0.1,
       "preferred_task_types": ["bug-fix", "refactor"]
     }
   }
   ```

2. **Update:** `ybis-dev next --agent codex`
   - Use history to recommend tasks
   - "Codex is 90% successful on bug-fix tasks, here's T-005"

**Acceptance:** System learns which agents are good at what.

---

## Integration with Core System (SYSTEM_STATE.md)

### How .YBIS_Dev fits into Tier 3:

```
┌─────────────────────────────────────────┐
│ .YBIS_Dev (CLI Coordination Layer)     │
│  - Multi-agent task queue               │
│  - File-based handoffs                  │
│  - Context management                   │
│  - Decision checkpoints                 │
└─────────────┬───────────────────────────┘
              │
              ├──> Manual Agents (Cursor, Claude, Codex)
              │
              └──> Autonomous Mode
                   ↓
┌─────────────────────────────────────────┐
│ Core Tier 3 System (OrchestratorGraph) │
│  - LangGraph state machine              │
│  - Aider executor                       │
│  - Sentinel verifier                    │
│  - RAG memory (ChromaDB)                │
└─────────────────────────────────────────┘
```

**Key Principle:** `.YBIS_Dev` is the **interface**, not the **engine**.

---

## Critical Design Constraints

### 1. No Database in MVP (from CONTRACT.md)
- All coordination via files
- No SQLite, Redis, ChromaDB in `.YBIS_Dev`
- RAG memory stays in core system (`src/agentic/core/plugins/rag_memory.py`)

### 2. Agent Agnostic
- CLI must work for: Cursor, Claude, Codex, Gemini, Copilot, Antigravity
- No agent-specific hacks

### 3. Windows Path Safety (from SYSTEM_STATE.md)
- Use `pathlib.Path`
- Never hardcode `C:/Projeler`
- Relative paths from `.YBIS_Dev/` root

### 4. Async-Safe (from SYSTEM_STATE.md Rule 3)
- Long-running tasks via `auto_dispatcher.py`
- CLI must not block

---

## Next Immediate Actions

1. **Implement Phase 1 CLI** (Priority: P0)
   - File: `.YBIS_Dev/tools/ybis_dev_cli.py`
   - Commands: `next`, `claim`, `finish`, `verify`

2. **Test with Real Task** (Priority: P0)
   - Use existing `T-002_P0_Fix_Random_Keys_In_MarkdownRenderer.md`
   - Run full cycle: claim → execute → verify → finish

3. **Document Agent Onboarding** (Priority: P1)
   - File: `.YBIS_Dev/00_GENESIS/ONBOARDING.md`
   - Step-by-step for new agents

---

## Success Metrics

- [ ] CLI commands work without errors
- [ ] Agent can complete task without asking "where is X?"
- [ ] Human makes max 2-3 decisions per task (not 20)
- [ ] Task artifacts are consistent across agents
- [ ] Core Tier 3 system can be invoked via CLI

---

**Last Updated:** 2025-12-20
**Status:** Phase 0 (MVP structure exists, CLI not implemented)
