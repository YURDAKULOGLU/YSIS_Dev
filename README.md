# YBIS Development Core (.YBIS_Dev)

> **Meta-development system that builds YBIS**

---

## 🎯 Current Phase: Tier 3 (The Hybrid Engine)

**Status:** 🚀 **ACTIVE & EVOLVING**

**Goal:** Build an autonomous software organization where specialized AI agents (CrewAI) are orchestrated by a central brain (LangGraph) to plan, code, and maintain the YBIS project with minimal human intervention.

---

## 🏗️ Architecture: The Hybrid Engine

We have moved beyond simple scripts to a sophisticated **Hybrid Architecture**:

1.  **🧠 The Brain (LangGraph):** Manages state, decisions, and workflows. It knows *what* to do next and handles errors.
2.  **💪 The Muscles (CrewAI):** Specialized teams of agents (Architects, Developers, QA) that execute tasks. They use **Local LLMs** (Llama 3.2, DeepSeek) to do the heavy lifting for free.
3.  **📚 The Memory (RAG + Protocols):** A tiered context loading system (`AI_AGENT_PROTOCOLS.md`) ensures agents know the project's Constitution and technical standards.
4.  **🛡️ The Playground (Shadow Workspace):** A sandboxed environment where code is written and verified before touching the real codebase.

---

## 🗺️ Roadmap & Tiers

### ✅ Tier 1: The Sensor (Completed)
*   **Capability:** MCP Server exposing project structure to IDEs.
*   **Tech:** FastMCP, Python.

### ✅ Tier 2: The Loop (Completed & Deprecated)
*   **Capability:** Single-agent recursive coding loop.
*   **Status:** Replaced by Tier 3's multi-agent crews.

### 🚀 Tier 3: The Hybrid Engine (CURRENT)
*   **Goal:** Orchestrate multiple agents to implement full features from PRD.
*   **Tech:** LangGraph + CrewAI + Local LLMs.
*   **Key Agents:**
    *   `PlanningCrew`: Product Owner + Architect (Analyzes & Plans).
    *   `DevCrew`: Senior Dev + QA (Codes & Verifies).

### 🔮 Tier 4: The Sentinel (NEXT)
*   **Goal:** Autonomic maintenance.
*   **Concept:** A background agent that wakes up at night to refactor code, update dependencies, and fix "rot".
*   **Tech:** Scheduled CrewAI jobs + Semantic Grep.

---

## 🤖 Active Agents & Crews

| Agent/Crew | Role | Powered By | Status |
| :--- | :--- | :--- | :--- |
| **Orchestrator** | Traffic Control | LangGraph | ✅ Active |
| **PlanningCrew** | Requirement Analysis | CrewAI (Llama 3.2) | ✅ Active |
| **DevCrew** | Code Implementation | CrewAI (Llama 3.2) | ⚠️ Implementation |
| **Architect** | System Design | DeepSeek R1 | ✅ Active |
| **Gemini (You)** | Strategic Architect | Google 1.5 Pro | 👑 God Mode |

---

## 📜 Governance (The 3 Constitutions)

All agents must strictly adhere to the 3 Constitutions found in `Meta/Governance/`:
1.  **Project Constitution:** The "Why" and "What" of YBIS.
2.  **Universal Standards:** Code quality, SOLID principles, Testing.
3.  **Development Governance:** Rules of engagement for AI agents.

---

## 🛠️ Quick Start

```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Ensure Local LLM is Ready (Ollama)
ollama pull llama3.2:latest

# 3. Run the Master Orchestrator
python run_system_update.py
```

---

**Last Updated:** 2025-12-15
**System Version:** 3.0 (Hybrid)
**Next Milestone:** Activate `The Sentinel` (Tier 4)