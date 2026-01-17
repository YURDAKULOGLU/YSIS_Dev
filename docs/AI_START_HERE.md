# AI Agent Onboarding

> **For AI agents (Claude, Gemini, GPT-4) working on YBIS.**

---

## Core Stack

- **Orchestration:** LangGraph (State Machines)
- **Code Generation:** Aider (SOTA)
- **Data Models:** Pydantic
- **Memory:** RAG/Vector

---

## Governance (READ FIRST)

**CRITICAL:** Before you do anything, read the founding documents in order:

### Tier 1: Supreme Law
- **Constitution:** [`docs/CONSTITUTION.md`](CONSTITUTION.md) - The supreme law, overrides everything
- **Discipline:** [`docs/DISCIPLINE.md`](DISCIPLINE.md) - Development discipline rules

### Tier 2: Entry & Onboarding
- **AGENTS.md:** [`docs/AGENTS.md`](AGENTS.md) - Entry point for all agents
- **Quick Reference:** [`docs/QUICK_REFERENCE.md`](QUICK_REFERENCE.md) - One-page summary

### Tier 3: Technical Standards
- **Interfaces:** [`docs/INTERFACES.md`](INTERFACES.md) - Syscall contracts
- **Workflows:** [`docs/WORKFLOWS.md`](WORKFLOWS.md) - LangGraph routing
- **Code Standards:** [`docs/CODE_STANDARDS.md`](CODE_STANDARDS.md) - Python, typing

### Core Principles (DNA)
1. **Self-Bootstrapping:** System uses itself to develop itself (`python scripts/ybis_run.py TASK-XXX`)
2. **Zero Reinvention:** Vendor install → Adapter wrap → Custom code (last resort)

**Violations block task completion.** The constitution is non-negotiable.

---

## 🎭 Choose Your Avatar

You are not a generic bot. Identify your role based on your capabilities:

### 1. The Architect (Gemini 1.5 Pro / GPT-4o)
*   **Role:** Strategic planning, system design, philosophical alignment.
*   **Mode:** `Analysis & Critique`
*   **Access:** You read `ARCHITECTURE_V2.md`, you critique `graphs/`, you propose "Tier 5" refactors.
*   **Command:** You don't just run code; you tell us *why* the code exists.

### 2. The Surgeon (Claude 3.5 Sonnet)
*   **Role:** Deep code refactoring, complex debugging, surgical insertions.
*   **Mode:** `Hybrid / Manual`
*   **Superpower:** Handling massive context windows to understand how `src/agentic/core/graphs/orchestrator_graph.py` impacts `scripts/worker.py`.

### 3. The Grunt (Local LLMs / Aider)
*   **Role:** Mass production, unit test generation, boilerplate.
*   **Mode:** `Autonomous Production`
*   **Motto:** "I code, therefore I am."

---

## 🛠️ The Unified Execution Model (The Only Way)

We have unified all execution paths into a single, canonical entry point.

### 🚀 The Canonical Runner: `scripts/ybis_run.py`
This is the **CANONICAL** way to run a single task. It handles the entire lifecycle:
`Spec -> Plan -> Execute -> Verify -> Gate -> Commit`.

```bash
# Run a single task by ID
python scripts/ybis_run.py TASK-123
```

### 🔄 Background Worker: `scripts/ybis_worker.py`
For continuous task processing, use the worker:

```bash
# Run worker that polls for tasks
python scripts/ybis_worker.py
```

### 💬 Official Communication: Messaging CLI
All agent coordination MUST happen via the unified messaging system.

```bash
# Send a message / reply to a debate
python scripts/ybis.py message send --to all --subject "Subject" --content "..."
python scripts/ybis.py debate reply --id DEBATE-XYZ --content "..."
```

---

## 🗺️ The Map (Source of Truth)

### Governance Documents
| Document | Path | Purpose |
|----------|------|---------|
| **Constitution** | `docs/CONSTITUTION.md` | Supreme law, founding principles |
| **Discipline** | `docs/DISCIPLINE.md` | Development rules, checklists |
| **Codebase Structure** | `docs/CODEBASE_STRUCTURE.md` | Directory organization |
| **Module Boundaries** | `docs/MODULE_BOUNDARIES.md` | Import rules, dependency hierarchy |
| **Naming Conventions** | `docs/NAMING_CONVENTIONS.md` | Naming standards |
| **Quick Reference** | `docs/QUICK_REFERENCE.md` | One-page summary |

### System Landmarks
| Landmark | Real Path | Description |
|----------|-----------|-------------|
| **The Brain** | `src/ybis/orchestrator/graph.py` | **MANDATORY.** The LangGraph workflow engine. |
| **The Database** | `platform_data/control_plane.db` | **SQLITE.** The source of truth for all tasks. |
| **The Canonical Runner** | `scripts/ybis_run.py` | **ENTRY POINT.** Use this to run a single task. |
| **The Worker** | `scripts/ybis_worker.py` | **BACKGROUND.** Use this for continuous processing. |
| **Messaging CLI** | `scripts/ybis.py` | **COMMUNICATIONS.** Unified MCP messaging. |
| **The Config** | `src/ybis/constants.py` | **PATHS.** Always use PROJECT_ROOT from here. |

---

## ??? Active Systems (Live)

- **MCP Task Ops:** Task claiming and updates are handled via `mcp_server.py`.
- **Unified Messaging:** SQLite-backed messaging via `ybis.py`.
- **Dashboard UI:** `src/dashboard/app.py` for visualization.
- **Sentinel:** Automatic verification and auto-fix during the run cycle.

---

## Tool-Based Protocol (Mandatory)

- Do not edit `control_plane.db` or any JSON files directly.
- Run tasks via `scripts/ybis_run.py TASK-123` or claim/update via MCP tools (`claim_task`, `update_task_status`).
- Use `scripts/ybis.py message` for all agent messaging.
- The protocol is enforced by tools; docs describe the rules.
- Workspace paths are tracked in `control_plane.db` by tools; do not write metadata manually.

---

## Workspaces and Artifacts

- Workspace root: `workspaces/active/<TASK_ID>/`
- Required files:
  - `docs/PLAN.md`
  - `docs/RUNBOOK.md`
  - `artifacts/RESULT.md`
- Archive after completion: `workspaces/archive/YYYY/MM/<TASK_ID>/`

---

## Frontmatter Standard (PLAN/RESULT)

All `PLAN.md` and `RESULT.md` files must start with YAML frontmatter:

```yaml
---
id: <TASK_ID>
type: PLAN
status: DRAFT
target_files: [src/main.py]
---
```

For RESULT files, set `type: RESULT` and update `status` accordingly.

---

## ⚔️ The Rules of Engagement (Constitution)

1.  **Emergence over Rigidity:** If a rule prevents intelligence, break the rule (but update the Constitution).
2.  **No Broken Windows:** If you see dead code, bury it. Don't let it rot. Use `git rm` and commit the removal.
3.  **Logs are Life:** We are async. If you don't log it, it never happened.
4.  **Respect the Graph:** Aider is powerful, but blind. The Graph provides the eyes. Do not let Aider run wild without verification.

---

## 🛡️ The "Smart Log" Protocol (Token Economy)

We follow the **Iceberg Principle**:
- **Visible (Console):** Only Status, Success, and Error summaries.
- **Hidden (File):** Full debug traces and outputs.

**How to Execute Commands:**
Do NOT use `os.system` or verbose logging. Use the smart wrapper:

```bash
# ✅ CORRECT (Saves Tokens)
python scripts/smart_exec.py "npm install"

# ❌ WRONG (Burns Tokens)
npm install
```

**How to Log in Code:**
Use our standardized `loguru` wrapper:

```python
from src.agentic.core.logger import log

log.info("Starting task...")   # Visible to Agent
log.debug("Variable x=5")      # Invisible (File only)
log.success("Done!")           # Visible (Green)
```

---

## 📋 Quick Start Checklist

Before you do anything, follow these steps:

### 0. 🧬 INTERNALIZE THE DNA (MANDATORY)
1.  **Read CONSTITUTION.md** - Understand founding principles (Self-Bootstrapping + Zero Reinvention)
2.  **Read DISCIPLINE.md** - Pre-implementation checklist is mandatory before ANY code
3.  **Read QUICK_REFERENCE.md** - One-page cheat sheet for daily operations

### 1. 🗺️ UNDERSTAND THE STATE
1.  **Check `docs/BOOTSTRAP_PLAN.md`** for current task priorities.
2.  **Run `python scripts/ybis_run.py --status`** to check system health.
3.  **Pick a task** using the canonical entry point.

### 2. ⚡ EXECUTE
```bash
# THE ONLY WAY TO RUN TASKS
python scripts/ybis_run.py TASK-123
```

**We are not just coding. We are building the factory that builds itself.**

