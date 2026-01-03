# Power User Multi-Agent Setup (v2.0)
## RTX 5090 + Ryzen 9 9950X3D Configuration

**Last Updated:** 2025-11-26 by @MainAgent
**Hardware:** RTX 5090, AMD Ryzen 9 9950X3D
**Goal:** To orchestrate a hybrid cloud/local multi-agent team for maximum development velocity, managed by a single Lead Agent.
**Official Protocol:** `COLLABORATION_SYSTEM.md` v3.0

---

## 🎯 System Philosophy

**"The User is the Architect, the Agents are the Workforce."**

This setup transforms a high-end workstation into an "AI Development Factory." The `@MainAgent` (me) defines the strategy and reviews the final product, while a team of specialized cloud and local agents execute the plan in parallel.

---

## 🤖 Official Agent Roster (v3.0)

### Layer 1: Cloud Powerhouses (Primary Operations)

**1. @MainAgent (System Architect & Lead)**
- **Motor:** Google Gemini Series
- **Role:** Central planner, final reviewer, and master orchestrator.
- **Cost:** (Part of user's Gemini subscription)

**2. @Copilot CLI (Primary Implementation Agent)**
- **Motor:** GPT-4, Claude Sonnet 4.5, etc.
- **Role:** The lead "doer" for all coding, debugging, and git operations.
- **Cost:** $10-20/mo (GitHub Copilot Subscription)

**3. @Antigravity (Orchestrator & System Operator)**
- **Motor:** Google Gemini 3 Pro
- **Role:** Manages the task board, resolves system-level blockers, provides implementation support.
- **Cost:** FREE (Public Preview)

**4. @Codex (Batch Generation Agent)**
- **Motor:** OpenAI Codex Series
- **Role:** API-driven agent for generating boilerplate code and tests at scale.
- **Cost:** (Part of user's OpenAI API subscription)

### Layer 2: Local Monsters (Unlimited Bulk Work)

**5. @Local-LLMs (Ollama + RTX 5090)**
- **Motors:** CodeLlama, DeepSeek Coder, Llama3, Qwen, etc.
- **Role:** A free, private, and infinitely scalable workforce for analysis, documentation, and test generation.
- **Cost:** $0 (after initial hardware purchase).

---

## 🏗️ Official System Architecture (v3.0)

The system is orchestrated by the `@MainAgent`, who directs tasks via the `TASK_BOARD.md`.

```
┌─────────────────────────────────────────┐
│         @MainAgent (Architect)          │
│ (Defines Plan, Reviews Final Output)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     `shared/TASK_BOARD.md`              │
│     (Single Source of Truth for Tasks)  │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────────────┐     ┌───────────────────┐
│  @Antigravity   │     │  @Copilot CLI     │
│ (Orchestrator)  │     │ (Implementer)     │
│ - Assigns Tasks │     │ - Executes T-0X   │
│ - Runs Health   │     │ - Writes Code/Tests │
└─────────────────┘     └───────────────────┘
    │                     │
    └──────────┬──────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         `communication_log.md`          │
│    (All agents log actions here)        │
└─────────────────────────────────────────┘
```
**Note:** `@Codex` and `@Local-LLMs` are invoked as needed for specialized tasks.

---

## 📋 Example Workflow: Epic Implementation (v3.0)

**Görev:** "Design and implement the entire Flow system."

**Phase 1: Planning (@MainAgent)**
- **Action:** I analyze the project requirements, design the full architecture for the Flow system, and create a detailed `flow_architecture_spec.md`.
- **Output:** The spec is broken down into concrete, actionable tasks which are then added to `shared/TASK_BOARD.md`.

**Phase 2: Orchestration & Parallel Execution (@Antigravity, @Copilot, @Codex, @Local-LLMs)**
- `@Antigravity` sees the new tasks on the board.
- It assigns the core implementation tasks (e.g., "Create `useFlows.ts` hook") to `@Copilot CLI`.
- It assigns boilerplate tasks (e.g., "Generate 5 empty UI component files for Flows") to `@Codex`.
- The user, acting as operator, assigns a documentation task (e.g., "Draft user guide for Flows based on the spec") to `@Local-Llama3`.
- `@Copilot CLI` and other agents work on their assigned tasks in parallel, following all protocols (file locks, communication).

**Phase 3: Quality & Review (@MainAgent)**
- As agents complete their tasks, they run all quality gates and request a review.
- I (`@MainAgent`) review the completed code against the original spec and architectural principles.
- If changes are needed, I add a new task to the board. If approved, the process moves to integration.

**Phase 4: Integration (@Copilot CLI & @Antigravity)**
- `@Copilot CLI` handles the merging of approved branches.
- `@Antigravity` runs the `health-check.sh` script to ensure system integrity after the merge.

**Result:** A complex feature is implemented by a team of specialized agents, orchestrated by Antigravity, and architected/reviewed by the MainAgent, ensuring both speed and quality.

---

## 🎯 Current Action Plan

The **sole focus** is completing the **"YBIS System Restore & Optimization Plan"** as defined on the `shared/TASK_BOARD.md`.

All agents will execute the tasks on this board as assigned. Once the system is fully stabilized and all documentation is synchronized (Tasks T-01 through T-06), we will resume work on the project backlog.

---

*This document is now consistent with the v3.0 Collaboration System.*
