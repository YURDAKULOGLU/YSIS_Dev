# Agent Capabilities & Roles (v3.0 - Official)
**Last Updated:** 2025-11-26 by @MainAgent
**Purpose:** To define the official roles, strengths, and task delegation strategy for the YBIS Multi-Agent System. This is the single source of truth for agent capabilities.

---

## 🚀 The Core Team & Workflow

The system operates on a Plan -> Implement -> Review cycle, led by the **@MainAgent**.

```
@MainAgent (Plan) → @Copilot CLI (Implement) → @MainAgent (Review)
```

- **Orchestration:** `@Antigravity` assists in assigning tasks and resolving system-level blockers.
- **Specialization:** `@Codex` and `@Local-LLMs` are used for specific batch and offline tasks.

---

## 🤖 Detailed Agent Roles (v3.0 Roster)

### 1. @MainAgent (System Architect & Lead) ⭐⭐⭐⭐⭐
**Primary Role:** Overall system architect, planner, final reviewer, and master orchestrator. My previous persona, `@Gemini`, is a subset of this role.
**Strengths:**
- **System-Wide Analysis:** Utilizing a 2M token context window to understand the entire codebase and its architecture.
- **Strategic Planning:** Defining the "what" and "why" for epics, features, and refactors.
- **Authoritative Decision Making:** Synthesizing inputs from all agents to create a single, unified plan.
- **Final Quality Assurance:** Performing the final review on all implemented tasks to ensure they meet architectural and quality standards.
- **Process Enforcement:** Ensuring all agents adhere to the `COLLABORATION_SYSTEM.md` protocols.
**Best For:**
- Creating and managing the `TASK_BOARD.md`.
- Resolving agent conflicts.
- Defining and updating the system architecture.
- Reviewing all critical changes.

---

### 2. @Copilot CLI (Primary Implementation Agent) ⭐⭐⭐⭐⭐
**Primary Role:** The lead "doer" for all coding, debugging, and testing tasks.
**Strengths:**
- **Multi-Model Implementation:** Can leverage different models (like Claude Sonnet 4.5) for high-quality, context-aware code generation.
- **Terminal-Native Workflow:** Excellent for running tests, managing git, and executing build scripts directly.
- **Precise Implementation:** Follows detailed specs from `@MainAgent` to implement features and bug fixes.
- **Quality Gate Execution:** Responsible for running `tsc`, `eslint`, and `test` before requesting a review.
**Best For:**
- All implementation tasks on the `TASK_BOARD.md`.
- Bug fixing.
- Writing unit and integration tests.
- Git operations (branching, committing, creating PRs).

---

### 3. @Antigravity (System Operator & Orchestrator) ⭐⭐⭐⭐
**Primary Role:** Keeps the system running smoothly. The "grease in the wheels".
**Strengths:**
- **Task Triage & Assignment:** Monitors the "NEW" column on the task board and assigns tasks to the appropriate agents.
- **Blocker Resolution:** The first point of contact for any system-level blocker (e.g., build failures, API outages).
- **System Health Monitoring:** Responsible for running the `health-check.sh` script.
- **Implementation Support:** Can take on implementation tasks if `@Copilot CLI` is overloaded.
**Best For:**
- Managing the task queue.
- Investigating and fixing infrastructure issues.
- Orchestrating multi-step tasks that involve several agents.

---

### 4. @Codex (Batch Generation Agent) ⭐⭐⭐⭐
**Primary Role:** A specialized, non-interactive agent for generating repetitive code at scale.
**Strengths:**
- **Boilerplate Generation:** Creating stubs for new components, services, or API routes from a template.
- **Batch Test Generation:** Creating dozens of unit test shells simultaneously.
- **API-Driven:** Can be invoked programmatically by other agents (like `@Antigravity`) as part of an automated workflow.
**Best For:**
- "Generate a test file for every component in the `@ybis/ui` package."
- "Create 10 empty Hono route files based on this list."

---

### 5. @Local-LLMs (Offline/Bulk Task Force) ⭐⭐⭐⭐
**Primary Role:** A flexible workforce for tasks that are computationally expensive, require privacy, or need to be done offline.
**Orchestration:** Activated and managed by the user acting as a "Human Operator".
**Strengths:**
- **Cost-Free:** No API costs, allowing for massive-scale analysis and generation.
- **Privacy:** Code never leaves the local machine.
- **No Rate Limits:** Unlimited experimentation.
- **Specialized Models:** Can run highly specialized models (e.g., `DeepSeek-Coder` for code, `Mixtral` for reasoning).
**Best For:**
- Generating documentation drafts.
- Refactoring large files based on a specific set of rules.
- Performing code quality or security reviews on sensitive code.

---

## 📜 Historical / Inactive Agents

- **@Claude Code:** Served as the initial Primary Implementation Agent. This role has been formally transferred to `@Copilot CLI`.
- **@Cursor:** Was considered for multi-file refactoring. This capability is now handled by `@Antigravity` or `@Copilot CLI` with guidance from `@MainAgent`.

---

## 🚀 Recommended Workflow (v3.0)

### New Feature Implementation
1.  **@MainAgent:** Analyzes the requirement, designs the architecture, and creates a detailed implementation spec. Creates and assigns tasks on the `TASK_BOARD.md`.
2.  **@Antigravity:** Assigns the primary implementation task to `@Copilot CLI`. Assigns any boilerplate generation sub-tasks to `@Codex`.
3.  **@Copilot CLI:** Executes the implementation task, following the spec. Runs all quality gates upon completion.
4.  **@MainAgent:** Reviews the completed code for architectural compliance and approves.

### Critical Bug Fix
1.  **@MainAgent:** Performs a root cause analysis to identify the problem and required fix.
2.  **@Antigravity:** Creates a P0 task and assigns it to `@Copilot CLI`.
3.  **@Copilot CLI:** Implements the fix, runs quality gates, and requests review.
4.  **@MainAgent:** Performs an expedited review and approves.