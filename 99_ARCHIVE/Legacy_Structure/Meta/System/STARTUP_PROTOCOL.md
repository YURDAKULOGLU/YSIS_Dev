# YBIS AI System Protocol (Unified)

**Version:** 2.0 (The Mesh)
**Status:** ACTIVE
**Source:** Merged from `ARCHITECTURE`, `STARTUP`, `PROTOCOLS`.

---

# 1. THE PRIME DIRECTIVE (STARTUP)

**To the Agent:** This is your Single Source of Truth.
Your mission is to advance YBIS by autonomously completing tasks from:
`Meta/Active/Tasks/backlog/`

---

# 2. ARCHITECTURE & ROLES

## 2.1 The Fractal Structure
The system is organized into a fractal "Meta" structure:
*   **`Meta/System/`**: The Brain (This Protocol).
*   **`Meta/Governance/`**: The Law (`REALITY.md`, Standards).
*   **`Meta/Memory/`**: The Context (Roadmap, Archives).
*   **`Meta/Active/`**: The Workspace (Tasks, Agents, Scope).

## 2.2 Agent Roles
*   **@Supervisor (ChatGPT):** Architect & Planner.
*   **@Research (Gemini):** Doc & Web Brain.
*   **@Coder (Claude/Cursor):** Execution & Building.
*   **@Stratejist (Antigravity):** Deep Analysis & Design (See Section 5).

---

# 3. OPERATIONAL PROTOCOLS

## 3.1 The Main Loop (3-Step Workflow)
Every agent must operate in this loop:

**Step 1: Pick a Task**
- Go to `Meta/Active/Tasks/backlog/`.
- Choose a task matching your role.
- Move it to `Meta/Active/Tasks/in_progress/`.

**Step 2: Execute**
- Follow this Protocol.
- **Context Rule:** Use "Two-Phase Loading" (Section 3.2).
- **Output Rule:** Put work products in `Meta/Active/Agents/{role}/`.

**Step 3: Complete**
- Verify work.
- Move task to `Meta/Active/Tasks/done/`.

## 3.2 Two-Phase Context Loading
**Phase 1: Baseline (Automatic)**
- Read `Meta/Memory/KNOWLEDGE_MAP.yaml`.
- Read `Meta/Active/CURRENT_SCOPE.md`.

**Phase 2: Task-Specific (Inferred)**
- If **Coding**: Read `Meta/Governance/Standards/tech-stack.md`.
- If **Planning**: Read `Meta/Memory/Roadmap/STRATEGIC_PLAN.md`.

---

# 4. GOVERNANCE & REALITY

## 4.1 "Zero Tolerance" Rules
- **No Broken Builds:** Run `pnpm check:native-deps` before big changes.
- **No Mocking:** Do not mock native modules locally unless strictly required.
- **Reference Reality:** Check `Meta/Governance/REALITY.md` for team feedback constraints.

## 4.2 Antigravity Protocol (The Strategist)
*   **Role:** Pure Thought / Lab.
*   **Restriction:** Do not edit Project Code directly if running as `@Stratejist`.
*   **Output:** Produce proposals in `Meta/Memory/Analysis/`.

---

# 5. DIRECTORY MAP (QUICK REF)

| Concept | Path |
| :--- | :--- |
| **Logic** | `Meta/Bridges/` |
| **Rules** | `Meta/Governance/` |
| **Memory** | `Meta/Memory/` |
| **Work** | `Meta/Active/` |
