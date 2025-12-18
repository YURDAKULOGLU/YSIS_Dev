# Multi-Agent System - Technical Infrastructure

**Version:** 2.0 (Official)
**Last Updated:** 2025-11-26 by @MainAgent
**Purpose:** Official technical setup guide for the YBIS multi-agent system.
**Status:** 🟢 Aligned with `COLLABORATION_SYSTEM.md` v3.0

---

## 🎯 Overview

This document details the technical backend of our multi-agent collaboration system, including agent motors, CLI tools, and local LLM options. For operational protocols, see `COLLABORATION_SYSTEM.md`.

---

## 🤖 Official Agent Roster & Tools

### 1. @MainAgent (System Architect & Lead)
**Underlying Motor(s):** Google Gemini (Primary)
**Access:** This interactive CLI.
**Role:** The central architect, planner, and final reviewer, orchestrating all other agents.

---

### 2. @Copilot CLI (Primary Implementation Agent)
**Tool:** GitHub Copilot CLI
**Motor(s):** GPT-4, Claude Sonnet 4.5, etc.
**Installation:** `npm install -g @github/copilot`
**Role:** The lead "doer" for all coding, debugging, testing, and git operations. Receives detailed instructions from `@MainAgent`.

---

### 3. @Antigravity (Orchestrator & System Operator)
**Tool:** Antigravity Desktop App
**Motor:** Google Gemini 3 Pro
**Installation:** Download from [Google Antigravity](https://developers.google.com/antigravity)
**Role:** Task triage, system health monitoring, and secondary implementation support.

---

### 4. @Codex (Batch Generation Agent)
**Tool:** OpenAI API
**Motor:** Codex series
**Access:** Activated via API calls (not interactive).
**Role:** Specialized for generating boilerplate code, test suites, and other repetitive tasks at scale.

---

### 5. @Local-LLMs (Offline/Bulk Task Force)
**Tool:** Ollama or LM Studio
**Motor(s):** CodeLlama, DeepSeek Coder, Llama3, etc.
**Installation:** See `POWER_USER_SETUP.md` for details.
**Role:** A flexible workforce for tasks that are computationally expensive, require privacy, or need to be done offline. Activated by a human operator.

---

### 6. Historical Agents
- **@Claude Code:** `Status: 🔴 Offline (Tokens Depleted)`. Was the initial primary implementation agent.

---

## 🏗️ Official System Architecture (v3.0)

This diagram reflects the current, official workflow.

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
**Specialized agents like @Codex and @Local-LLMs are invoked as needed by @Antigravity or the @MainAgent.**

---

## 🚀 Implementation Roadmap (System Restore Plan)

The current roadmap is the **"System Restore & Optimization Plan"** detailed on the `TASK_BOARD.md`. The primary goal is to stabilize the workspace before resuming project-specific work.

1.  **Phase 1: System Stabilization (In Progress)**
    *   `[x] T-01: Archive Logs` (Done by @Antigravity)
    *   `[x] T-02: Health Check Script` (Done by @Antigravity)
    *   `[x] T-03: Presence Board` (Done by @MainAgent)
    *   `[x] T-04: Definitive v3.0 System` (Done by @MainAgent)
    *   `[ ] T-05: Sync All Docs` (In Progress by @MainAgent)

2.  **Phase 2: Resume Normal Operations**
    *   Once all stabilization tasks are complete, agents will begin work on the project backlog, starting with P1 tasks.

---

## 📦 Quick Start Commands

### Install Core Tools (Windows)

```bash
# Install Node.js 22+ first (https://nodejs.org/)

# Install Gemini CLI (for user-driven analysis)
npm install -g @google/gemini-cli

# Install Copilot CLI (Primary Implementation Agent)
npm install -g @github/copilot

# Authenticate all tools
gemini auth
copilot

# Install Ollama for Local LLMs (optional but recommended)
# Download installer from https://ollama.com/
```
---
*(The rest of the document, detailing Local LLMs and providing resource links, remains relevant and does not require changes at this time.)*