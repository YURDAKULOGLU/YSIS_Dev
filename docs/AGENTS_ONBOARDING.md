# YBIS Agent Onboarding Protocol (Open Interface)

## Is this a Closed System? NO.
YBIS is designed as an **Open Agentic Platform** compliant with the **Model Context Protocol (MCP)**. Any CLI, IDE, or AI Agent that speaks MCP (or can edit Markdown) can participate.

---

## 📜 Constitutional Requirements (READ FIRST)

**BEFORE YOU CONNECT:** All agents (internal and external) must comply with [`docs/governance/YBIS_CONSTITUTION.md`](governance/YBIS_CONSTITUTION.md).

**Non-negotiable requirements:**
1. **Single execution spine:** `scripts/run_orchestrator.py` is the only runner
2. **MCP-first:** All task ops via `scripts/ybis.py` or MCP tools (no direct DB access)
3. **Artifacts required:** PLAN, RUNBOOK, RESULT, META, CHANGES for every completed task
4. **Local-first:** Local providers default, cloud is feature-flagged and opt-in

**Verification:** `python scripts/protocol_check.py --task-id <ID> --mode lite` must pass before task completion.

**Violations block task completion.** External agents that bypass these requirements will have their work rejected.

**See also:** [`docs/specs/GOVERNANCE_ACTION_PLAN.md`](../specs/GOVERNANCE_ACTION_PLAN.md)

---

## How to Connect (For External Agents)

### Method 1: The "Brain" Connection (Preferred)
*   **Protocol:** MCP (Model Context Protocol) over SSE.
*   **Endpoint:** `http://localhost:8000/sse` (when `ybis_server.py --brain-mode` is running).
*   **Capabilities:**
    -   `get_repo_tree()`: See the world.
    -   `get_next_task()`: Get work.
    -   `ask_user()`: Get permission.
    -   `get_suggested_workflow()`: Learn *how* to work.

### Method 2: MCP Task Ops (Async)
*   **Interface:** MCP tools over SSE.
*   **Tools:** `get_tasks`, `claim_task`, `update_task_status`
*   **Protocol:**
    1.  Query tasks via MCP.
    2.  Claim a task atomically.
    3.  Update status on completion.

### Method 3: The "CLI" Integration (Direct)
*   **Tool:** `scripts/run_orchestrator.py`
*   **Usage:** You can manually trigger the Orchestrator for specific tasks.
    ```bash
    python scripts/run_orchestrator.py --task-id TASK-ID
    ```

## Standard Workflows
Don't guess. Use the Registry:
-   `workflow-registry.yaml`: The "Constitution" of workflows.
-   **Rule:** If you are a new agent, read this file first to understand the company culture (processes).
