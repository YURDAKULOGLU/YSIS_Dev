# Agent System Improvements

**Created:** 2025-11-26
**Author:** Antigravity

## Observations
The current system is robust for task execution but lacks a dedicated space for high-level discussion and "soft" coordination (the "Meeting Room" concept).

## Proposed Improvements

### 1. Formalize "Meeting Room" Protocols
- **Current:** `communication_log.md` is a linear log of actions.
- **Proposal:** Introduce a specific tag or section in `communication_log.md` for discussions (e.g., `### [MEETING] Topic`).
- **Benefit:** Separates execution logs from strategic discussions.
- **Status:** ƒo Implemented via `shared/MEETING_ROOM.md` with template + tagging guidance.

### 2. Agent "Presence" Indicators
- **Current:** Status is manual in `DAILY_STANDUP.md`.
- **Proposal:** Add a "Current Focus" line to `ACTIVE_AGENTS.md` or a lightweight `presence.md` file for real-time status (e.g., "Thinking", "Coding", "Idle").
- **Status:** ƒo Implemented via `shared/presence.md` (editable board).

### 3. Decision Records
- **Current:** Decisions are scattered in logs.
- **Proposal:** Enforce usage of `shared/decisions.md` for all architectural decisions made in the "Meeting Room".

### 4. Antigravity's Role
- **Current:** Orchestrator.
- **Proposal:** Explicitly define Antigravity as the "Meeting Moderator" who summarizes discussions and ensures decisions are recorded.

---

## New Lightweight Practices (Codex)
- Use `shared/presence.md` to show live focus/availability; update when switching tasks.
- Use `shared/MEETING_ROOM.md` template for discussions in `communication_log.md` and propagate decisions to `shared/decisions.md`.
- Keep execution logs short; move actionable items to `shared/TASK_BOARD.md` and agent `status.md` files.
