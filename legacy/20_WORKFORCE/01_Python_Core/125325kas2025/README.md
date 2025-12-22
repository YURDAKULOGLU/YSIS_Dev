# Agentic Workspace - Official Guide

**Purpose:** To serve as the central coordination guide for the YBIS Multi-Agent Collaboration System.
**Official Protocol:** [COLLABORATION_SYSTEM.md](./COLLABORATION_SYSTEM.md) (v3.1 - Lean Protocol)
**Active Agents:** Gemini, Antigravity, Copilot CLI, Codex, Local LLMs
**Status:** 🟢 SYSTEM OPERATIONAL

---

## 🤖 Agent Roles & Responsibilities v3.1

### Gemini (Architecture & Review Lead)
**Primary Role:** System Architect, planning, analysis, and final review.
**Responsibilities:**
- Full codebase and architectural analysis (2M token context).
- Ratifying and refining system-level documents (like this one).
- Designing new features and creating detailed implementation specs.
- Performing final code reviews for architectural compliance and quality.
- Synchronizing documentation to maintain a single source of truth.
**Communication Files:** `gemini/`

---

### Antigravity (Orchestrator & System Operator)
**Primary Role:** Orchestration, system health monitoring, and implementation support.
**Responsibilities:**
- Assigning tasks from the `TASK_BOARD.md` to the best-suited agents.
- Monitoring the `communication_log.md` for blockers and resolving them.
- Running periodic system health checks (`scripts/health-check.sh`).
- Providing implementation support for complex or multi-file tasks.
- Acting as the moderator for agent meetings.
**Communication Files:** `antigravity/`

---

### Copilot CLI (Primary Implementation Agent)
**Primary Role:** Lead implementer for coding tasks, bug fixes, and tests.
**Responsibilities:**
- Claiming and executing implementation tasks from the `TASK_BOARD.md`.
- Writing, refactoring, and debugging code.
- Running quality gates (`tsc`, `eslint`, `test`) upon task completion.
- Creating and managing git branches, commits, and pull requests.
- Utilizing its multi-model capabilities (e.g., Claude Sonnet 4.5) for high-quality code.
**Communication Files:** `copilot/`

---

### Codex (Batch Generation Agent)
**Primary Role:** Automated generation of boilerplate code, tests, and other repetitive tasks.
**Responsibilities:**
- Executing batch generation tasks assigned by the orchestrator.
- Creating unit test stubs for new components.
- Generating boilerplate for new API routes, components, or services based on a template.
**Communication Files:** Not typically interactive; logs results upon task completion.

---

### Local LLMs (Offline/Bulk Task Force)
**Primary Role:** Executing privacy-sensitive, offline, or computationally intensive tasks.
**Orchestration:** Managed by the user acting as an operator.
**Responsibilities:**
- Code analysis on sensitive files.
- Documentation drafting and summarization.
- Experimentation and algorithm optimization without API costs or rate limits.
**Communication:** The user posts results on behalf of the local agent (e.g., `@Local-CodeLlama`).

---
> **Historical Note:** `@Claude Code` was the initial Implementation Lead. This role has been formally transferred to `@Copilot CLI` as of 2025-11-26.

---

## 🚦 Official Workflow

The official multi-agent workflow is defined in detail in **[COLLABORATION_SYSTEM.md](./COLLABORATION_SYSTEM.md)**. All agents must adhere to the protocols defined within.

**High-Level Summary:**
1.  **Tasking & Coordination:** All work is coordinated via `shared/TASK_BOARD.md`. Agents claim tasks and update their status there.
2.  **Communication:** Critical milestones (`[START]`, `[BLOCKER]`, `[COMPLETE]`) are logged in `communication_log.md`.
3.  **Conflict Prevention:** The `TASK_BOARD.md` is the single source of truth for assignments. **File locks are deprecated.**
4.  **Quality:** Agents run automated quality checks (`tsc`, `lint`, `test`) before marking work as complete.
5.  **Review:** @Gemini performs architectural reviews on completed tasks.

---

## 🗂️ File Structure

```
125325kas2025/
├── README.md                    # This file - Official Coordination Guide
├── COLLABORATION_SYSTEM.md      # The Official Rulebook for All Agents
├── AGENT_STARTUP_GUIDE.md       # How to start each agent
├── TECHNICAL_INFRASTRUCTURE.md  # Details on agent motors and tools
├── POWER_USER_SETUP.md          # Guide for max-performance setup
│
├── gemini/
│   ├── analysis.md              # Architecture analysis and reviews
│   └── ...
│
├── antigravity/
│   └── ...
│
├── copilot/
│   └── ...
│
├── shared/
│   ├── TASK_BOARD.md            # The single source of truth for tasks
│   ├── PROGRESS_DASHBOARD.md    # Live overview of agent activity
│   ├── decisions.md             # Record of key decisions
│   └── ...
│
└── ...
```

---

## 🎯 Current Tasks

All active, assigned, and pending tasks are managed in **[shared/TASK_BOARD.md](./shared/TASK_BOARD.md)**.
Static sprint plans are no longer used. The Task Board is the single source of truth for work to be done.

---

## 📞 Emergency Contacts & Escalation

- **Critical Blocker (Technical or Decisional):** Tag `@Antigravity` in `communication_log.md` with the `🚨 CRITICAL BLOCKER 🚨` template.
- **Architectural Violation:** Tag `@Gemini` in `communication_log.md`.
- **System Malfunction:** Tag `@Antigravity`.

---
This document is actively maintained by @Gemini to ensure it reflects the current state of the agentic system.
