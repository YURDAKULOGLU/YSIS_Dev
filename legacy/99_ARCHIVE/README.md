# YBIS-OS (Agentic Operating System)

> **Human-AI Collaborative Development Platform**
> *Formerly YBIS Mobile App*

[![Status](https://img.shields.io/badge/Status-Operational-green.svg)]()
[![Kernel](https://img.shields.io/badge/Kernel-LangGraph-blue.svg)]()
[![Brain](https://img.shields.io/badge/Memory-Local_RAG-orange.svg)]()
[![Muscle](https://img.shields.io/badge/Runtime-Ollama_%2B_MCP-red.svg)]()

---

## 🚀 What is YBIS-OS?

YBIS-OS is not just an application; it is an **Agentic Operating System** designed to build, maintain, and evolve software autonomously. It unifies human intent with AI execution through a strict governance protocol.

It powers the development of the **YBIS Mobile App** (a personal assistant), but the OS itself is the true product.

### Core Architecture
1.  **The Kernel (Orchestrator):** Python-based LangGraph state machine that manages workflows.
2.  **The Brain (Memory):** Local RAG (ChromaDB) for semantic knowledge + Task Board for active state.
3.  **The Muscle (Runners):** Hybrid execution engine using local LLMs (Ollama) and cloud models (Anthropic) via MCP.
4.  **The Law (Governance):** A strict "Constitution" enforced by Pydantic validators (No `any`, No `console.log`).

---

## 🛠️ Developer Guide (How to Use)

### 1. The "Magic" Command
To start the autonomous development loop:

```bash
# Windows
.YBIS_Dev\Agentic\.venv\Scripts\python .YBIS_Dev\Agentic\Core\orchestrator.py

# Mac/Linux
source .YBIS_Dev/Agentic/.venv/bin/activate
python .YBIS_Dev/Agentic/Core/orchestrator.py
```

This command will:
1.  Read the top task from `.YBIS_Dev/Meta/Active/TASK_BOARD.md`.
2.  Analyze it with the **Architect Agent**.
3.  Implement it with the **Developer Agent**.
4.  Verify it against the Constitution.

### 2. Manual Control (MCP)
You can connect your favorite AI IDE (Cursor, Claude Desktop) to YBIS-OS via the Model Context Protocol (MCP).

*   **Config:** See `.YBIS_Dev/Agentic/MCP/README_MCP_CLIENTS.md`
*   **Capabilities:** Ask Claude/Cursor to "Search YBIS Memory" or "Pick next task".

---

## 📂 System Structure

```
.YBIS_Dev/               # The OS Root
├── Agentic/             # The Engine
│   ├── Core/            # LangGraph Orchestrator
│   ├── Agents/          # PydanticAI Personas (Architect, Dev)
│   ├── Tools/           # Capabilities (RAG, TaskManager)
│   └── Local/           # Ollama/Cloud Router
├── Meta/                # The Governance Layer
│   ├── Governance/      # Constitution.md
│   └── Active/          # TASK_BOARD.md (The Input)
└── Workflows/           # YAML Definitions (The Logic)
```

---

## 📱 The "Payload" (YBIS Mobile App)

While YBIS-OS builds it, the product is a React Native (Expo) app located in `apps/mobile`.

- **Stack:** React Native, Tamagui, Supabase, Hono.
- **Run:** `pnpm run mobile`

---

## 📜 License

Private Repository. All Rights Reserved.
