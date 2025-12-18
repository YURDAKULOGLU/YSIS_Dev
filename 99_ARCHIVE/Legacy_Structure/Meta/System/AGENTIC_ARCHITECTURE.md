# YBIS Agentic Architecture (Spec-Driven)

**Philosophy:** "Think twice, code once."
We do not let Agents "figure it out" in code. We define the **Spec** first, then the Agent executes.

## 🏗️ The Roles

### 1. The Architect (User + Planner Agent)
- **Role:** Define the *WHAT* and *WHY*.
- **Output:** `STRUCTURE.md`, `RELEASE_SCHEDULE.md`, `STRATEGY.md`.
- **Tool:** `task_boundary`, `notify_user` (for approval).

### 2. The Spec Writer (Architecture Agent)
- **Role:** Define the *HOW* (Technical Spec).
- **Task:** Converts a Roadmap item (e.g., "Summarize Flow") into a pseudo-code spec.
- **Output:** `Meta/Specs/SPEC_001_SUMMARIZE_FLOW.md`.
- **Content:** Data Models, API Signatures, State Charts.

### 3. The Executor (Coding Agent)
- **Role:** Implement the Spec.
- **Constraint:** CANNOT deviate from the Spec. If Spec is wrong, halt and ask Architect.
- **Output:** Code, Tests.

## 🔄 The Workflow Loop

1.  **User Request:** "I want PDF Summaries."
2.  **Architect:** Adds "Summarize Flow" to `RELEASE_SCHEDULE.md` (v0.1.3).
3.  **Architect:** Creates `Meta/Specs/SPEC_00X_PDF_SUMMARY.md`.
    *   *Defines:* Input (PDF), Output (Text), Latency (<2s), UI (Chat Bubble).
4.  **Executor:** Reads Spec -> Writes Code -> Writes Test.
5.  **Review:** User verifies against Spec.

## 🤖 Why this works for YBIS?
- **Avoids "Spaghetti Code":** We solve the logic in English/Markdown before writing TypeScript.
- **Scalable:** Multiple agents can work on different Specs simultaneously.
- **Memory:** The `Specs/` folder becomes the true documentation of the system.
