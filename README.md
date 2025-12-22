# YBIS_Dev - Autonomous Software Factory

> **Tier 3 Autonomous System: AI agents that plan, code, test, and deploy software**

---

## 🚨 New AI Agent? Start Here

**👉 Read this first:** [AI_START_HERE.md](./AI_START_HERE.md)

**Then read:** [SYSTEM_STATE.md](./SYSTEM_STATE.md) (5 min - the complete system architecture)

---

## 🎯 Current Phase: Tier 3 Alpha

**Status:** 🚀 **FUNCTIONAL - Loop Closure in Progress**

**Goal:** Autonomous code generation, testing, and deployment with minimal human intervention.

---

## 🏗️ Architecture: The Orchestration Engine

Protocol-based plugin architecture with LangGraph orchestration:

1.  **🧠 The Brain (OrchestratorGraph):** LangGraph state machine managing `TaskState` flow (init → plan → execute → verify → done)
2.  **💪 The Executor (Aider):** Code generation using local LLMs (qwen2.5:32b) via Aider CLI
3.  **🛡️ The Verifier (Sentinel):** Quality control with pytest, AST analysis, coverage checks
4.  **📚 The Memory (RAG):** ChromaDB vector store with SentenceTransformers for semantic code search
5.  **🎯 The Sandbox:** Isolated execution environment (`.sandbox_hybrid/<TASK_ID>/`) before committing to main codebase

---

## 🗺️ Roadmap & Tiers

### ✅ Tier 1: The Sensor (Completed)
*   **Capability:** MCP Server exposing project structure to IDEs.
*   **Tech:** FastMCP, Python.

### ✅ Tier 2: The Loop (Completed & Deprecated)
*   **Capability:** Single-agent recursive coding loop.
*   **Status:** Replaced by Tier 3's multi-agent crews.

### 🚀 Tier 3: The Organization (CURRENT)
*   **Status:** Alpha - LangGraph integration complete, loop closure in progress
*   **Tech:** LangGraph + Aider + Sentinel + RAG (ChromaDB)
*   **Components:**
    *   `OrchestratorGraph`: State machine workflow
    *   `SimplePlanner`: Task decomposition (Ollama qwen2.5:14b)
    *   `AiderExecutor`: Code generation (Aider + qwen2.5:32b)
    *   `SentinelVerifier`: Quality gates (pytest, lint, coverage)
    *   `RAGMemory`: Semantic code search

### 🔮 Tier 4: The Sentinel (NEXT)
*   **Goal:** Autonomic maintenance.
*   **Concept:** A background agent that wakes up at night to refactor code, update dependencies, and fix "rot".
*   **Tech:** Scheduled CrewAI jobs + Semantic Grep.

---

## 🤖 Active Agents & Capabilities

| Agent | Role | Interface | Status |
| :--- | :--- | :--- | :--- |
| **OrchestratorGraph** | Workflow control | Python API | ✅ Active |
| **SimplePlanner** | Task decomposition | PlannerProtocol | ✅ Active |
| **AiderExecutor** | Code generation | ExecutorProtocol | ✅ Active |
| **SentinelVerifier** | Quality assurance | VerifierProtocol | ✅ Active |
| **External Agents** | Manual tasks | File-based queue | ✅ Active |

**External Agent Support:**
- Claude/GPT-4: Debugging, refactoring, integration
- Codex/Copilot: Implementation, tests
- Gemini: Architecture, design critique
- See: `10_META/Governance/agents.yaml` for capabilities

---

## 📜 Governance & Rules

All agents must follow these immutable principles:

1.  **Single Path Principle:** Never hardcode paths. Always use `src.agentic.core.config`
2.  **Verification Principle:** No code commits without passing Sentinel verification
3.  **Detachment Principle:** Long-running tasks use `auto_dispatcher.py` (async)

**Documents:**
- `SYSTEM_STATE.md` - System architecture & lessons learned
- `00_GENESIS/AGENT_CONTRACT.md` - Agent coordination rules
- `00_GENESIS/YBIS_CONSTITUTION.md` - Project vision & principles
- `10_META/Governance/agents.yaml` - Agent capability registry

---

## 🛠️ Quick Start

### For AI Agents
1. Read [AI_START_HERE.md](./AI_START_HERE.md)
2. Read [SYSTEM_STATE.md](./SYSTEM_STATE.md)
3. Check task queue: `cat Knowledge/LocalDB/tasks.json`
4. Or check file-based queue: `ls Knowledge/Tasks/backlog/`

### For Developers
```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Ensure Ollama is running
ollama pull qwen2.5:14b
ollama pull qwen2.5:32b

# 3. Start dashboard (optional)
python src/agentic/core/auto_dispatcher.py src/dashboard/app.py
# Visit: http://localhost:5000

# 4. Run a task through orchestrator
python run_tier3_step2.py  # or run_tier3_step3.py
```

---

## 📁 Directory Structure

```
YBIS_Dev/
├── AI_START_HERE.md              # ⭐ Agent onboarding
├── SYSTEM_STATE.md               # ⭐ Complete system state
├── README.md                     # This file
│
├── src/agentic/core/
│   ├── graphs/                   # LangGraph workflows
│   ├── plugins/                  # Planner, Executor, Verifier
│   ├── config.py                 # Path constants
│   └── protocols.py              # Plugin interfaces
│
├── Knowledge/
│   ├── LocalDB/
│   │   ├── tasks.json            # Task queue (operational memory)
│   │   └── chroma_db/            # RAG vector database
│   └── Tasks/                    # File-based task queue
│       ├── backlog/
│       ├── in_progress/
│       ├── done/
│       └── blocked/
│
├── .sandbox_hybrid/<TASK_ID>/    # Task execution sandbox
│   ├── PLAN.md
│   ├── RUNBOOK.md
│   ├── DECISIONS.json
│   ├── STATE_SNAPSHOT.json
│   └── RESULT.md
│
├── 00_GENESIS/                   # Constitution & vision
├── 10_META/                      # Governance & strategy
└── tests/                        # Test suite
```

---

**Last Updated:** 2025-12-20
**System Version:** 3.1 (Tier 3 Alpha)
**System Integrity:** 98%
**Next Milestone:** Loop Closure (Verifier → Executor retry)