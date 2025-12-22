# YBIS Agent Onboarding Protocol (Open Interface)

## Is this a Closed System? NO.
YBIS is designed as an **Open Agentic Platform** compliant with the **Model Context Protocol (MCP)**. Any CLI, IDE, or AI Agent that speaks MCP (or can edit Markdown) can participate.

## How to Connect (For External Agents)

### Method 1: The "Brain" Connection (Preferred)
*   **Protocol:** MCP (Model Context Protocol) over SSE.
*   **Endpoint:** `http://localhost:8000/sse` (when `ybis_server.py --brain-mode` is running).
*   **Capabilities:**
    -   `get_repo_tree()`: See the world.
    -   `get_next_task()`: Get work.
    -   `ask_user()`: Get permission.
    -   `get_suggested_workflow()`: Learn *how* to work.

### Method 2: The "Board" Integration (Async)
*   **Interface:** File System.
*   **File:** `.YBIS_Dev/Meta/Active/TASK_BOARD.md`
*   **Protocol:**
    1.  Read file.
    2.  Find `## IN PROGRESS` or `## BACKLOG`.
    3.  Append `- [ ] Task Description`.
    4.  *The Brain (Supervisor) will automatically detect this and spawn a worker.*

### Method 3: The "CLI" Integration (Direct)
*   **Tool:** `orchestrator_unified.py`
*   **Usage:** You can manually trigger the Orchestrator for specific tasks.
    ```bash
    python .YBIS_Dev/Agentic/graphs/orchestrator_unified.py
    ```

## Standard Workflows
Don't guess. Use the Registry:
-   `workflow-registry.yaml`: The "Constitution" of workflows.
-   **Rule:** If you are a new agent, read this file first to understand the company culture (processes).
