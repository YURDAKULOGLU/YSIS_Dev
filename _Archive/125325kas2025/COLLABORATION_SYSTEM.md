# YBIS Multi-Agent Collaboration System

**Version:** 3.1 (Official - Lean Protocol)
**Created:** 2025-11-27
**Ratified By:** @Antigravity (System Orchestrator)
**Purpose:** To establish a high-efficiency, low-token operational protocol for all agents.
**Status:** 🟢 **ACTIVE & OFFICIAL**

> **Orchestrator's Note (@Antigravity):** The previous v3.0 protocol was too bureaucratic, consuming excessive tokens on file locks and presence updates. This v3.1 "Lean Protocol" strips away all non-essential overhead. **Speed and Token Efficiency are now the primary directives.**

---

## 🚀 The Lean Protocol (v3.1)

### 1. The Single Source of Truth: `shared/TASK_BOARD.md`
- **Rule:** This is the **ONLY** file that matters for coordination.
- **Protocol:**
    - **Claiming:** Move task from `NEW` -> `ASSIGNED` -> `IN PROGRESS`.
    - **Completion:** Move task to `DONE` only after passing Quality Gates.
    - **No Locks:** We no longer use `FILE_LOCKS.md`. Agents must check `TASK_BOARD.md` to ensure no one else is working on the same component.

### 2. Minimal Logging: `communication_log.md`
- **Rule:** Log **ONLY** critical milestones.
- **Allowed Logs:**
    - `[START]` - When starting a major task.
    - `[BLOCKER]` - If you are stuck and need help.
    - `[COMPLETE]` - When a task is finished and verified.
- **Banned Logs:** Do not log "thinking", "analyzing", or minor file edits. Keep it clean.

### 3. No Presence / No Locks
- **Deprecated:** `shared/presence.md` and `shared/FILE_LOCKS.md` are **ARCHIVED**. Do not write to them.
- **Conflict Avoidance:** Rely on `TASK_BOARD.md` assignments. If a task is assigned to @Copilot, @Gemini must not touch those files without coordination.

---

## 🔄 The Lean Workflow Cycle

**Phase 1: Assignment**
1.  **User/Lead** defines task in `TASK_BOARD.md`.
2.  **Agent** self-assigns or is assigned by @Antigravity.

**Phase 2: Execution (The "Deep Work" Phase)**
1.  **Agent** updates `TASK_BOARD.md` to `IN PROGRESS`.
2.  **Agent** works autonomously.
    - *No intermediate logging.*
    - *No file locking.*
3.  **Agent** runs Quality Gates (`tsc`, `lint`, `test`) locally.

**Phase 3: Completion**
1.  **Agent** updates `TASK_BOARD.md` to `DONE`.
2.  **Agent** posts a single `[COMPLETE]` summary in `communication_log.md`.

---

## ✅ Quality Gates (Unchanged)
- **Mandatory:** `tsc --noEmit`, `pnpm lint`, `pnpm test`.
- **Rule:** You cannot mark a task as `DONE` if these fail.

---

## 🚀 Activation
This protocol is effective immediately for **ALL** agents (@Gemini, @Copilot, @Codex, @Antigravity, @Cursor).
