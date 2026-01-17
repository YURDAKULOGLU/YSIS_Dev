# Self-Development Usage Guide

**Purpose:** Practical guide for using YBIS self-development system.
**Status:** Planning Phase
**Date:** 2026-01-09

---

## Quick Start

### 1. Start MCP Server (Optional but Recommended)

```bash
# Start MCP server in stdio mode (for CLI tools)
python scripts/ybis_mcp_server.py

# Or in SSE mode (for web clients)
python scripts/ybis_mcp_server.py --sse
```

**MCP Server provides:**
- `task_create` - Create self-development tasks
- `task_run` - Run workflows
- `task_status` - Check task status
- `approval_write` - Approve blocked tasks
- `artifact_read/write` - Access artifacts

### 2. Create Self-Development Task

**Via CLI (Direct):**
```bash
# Create task manually in DB
python -c "
from src.ybis.control_plane import ControlPlaneDB
import asyncio

async def create_task():
    db = ControlPlaneDB('platform_data/control_plane.db')
    await db.initialize()
    task = await db.create_task(
        title='Self-Development: Improve gate_node artifact enforcement',
        objective='Add artifact enforcement to gate_node to ensure required artifacts are checked',
        priority='HIGH'
    )
    print(f'Created task: {task.task_id}')

asyncio.run(create_task())
"
```

**Via MCP (Recommended):**
```python
# Using MCP client
from src.ybis.services.mcp_tools import task_tools

task = task_tools.task_create(
    title="Self-Development: Improve gate_node",
    objective="Add artifact enforcement to gate_node",
    priority="HIGH"
)
print(f"Created task: {task['task_id']}")
```

### 3. Run Self-Development Workflow

**Via CLI:**
```bash
# Run self-development workflow
python scripts/ybis_run.py TASK-123 --workflow self_develop
```

**Via MCP:**
```python
# Using MCP client
result = task_tools.task_run(
    task_id="TASK-123",
    workflow_name="self_develop"
)
print(f"Workflow started: {result}")
```

---

## How It Works

### 1. Git Worktree Isolation

**Every self-development run gets its own git worktree:**

```python
# src/ybis/data_plane/workspace.py
run_path = init_run_structure(
    task_id="TASK-123",
    run_id="R-abc123",
    use_git_worktree=True  # Creates isolated git worktree
)
```

**What happens:**
1. Creates git branch: `task-TASK-123-run-R-abc123`
2. Creates worktree at: `workspaces/TASK-123/runs/R-abc123/`
3. All changes happen in worktree, not main codebase
4. If successful → merge to main
5. If failed → discard worktree (safe rollback)

**Example:**
```bash
# Worktree created automatically
workspaces/
  TASK-123/
    runs/
      R-abc123/          # Git worktree (isolated)
        src/            # Code changes here
        artifacts/      # Artifacts
        journal/        # Journal events
```

### 2. Workflow Execution

**Self-Development Workflow Steps:**

```
1. reflect → Analyze system state
   - Reads recent runs from DB
   - Analyzes verifier/gate reports
   - Identifies improvement opportunities
   - Output: reflection_report.json

2. analyze → Prioritize improvements
   - Scores improvements by impact/risk
   - Checks dependencies
   - Prioritizes (P1, P2, P3)
   - Output: analysis_report.json

3. propose → Generate tasks
   - Converts improvements to tasks
   - Creates rollback plans
   - Registers tasks in DB
   - Output: proposal_report.json

4. spec → Generate SPEC.md
   - Creates specification for self-change
   - Uses existing spec_generator node
   - Output: spec.md

5. plan → Generate PLAN.json
   - Creates implementation plan
   - Uses existing planner node
   - Output: plan.json

6. execute → Apply changes
   - Executes plan in worktree
   - Uses existing executor node
   - Output: executor_report.json

7. verify → Test changes
   - Runs tests in worktree
   - Runs lint in worktree
   - Uses existing verifier node
   - Output: verifier_report.json

8. gate → Governance check
   - Stricter gate for self-changes
   - Checks for approval if core changes
   - Validates rollback plan
   - Output: gate_report.json

9. integrate → Merge changes
   - Creates rollback checkpoint
   - Merges worktree branch to main
   - Creates integration report
   - Output: integration_report.json
```

### 3. Docker Integration (Future)

**Docker sandbox for risky operations:**

```yaml
# configs/profiles/default.yaml
sandbox:
  enabled: true
  type: "docker"  # Future: Docker sandbox
  network: false
  allowlist:
    - "python"
    - "pytest"
```

**Self-development with Docker:**
- Risky operations (exec, file writes) run in Docker
- Worktree is mounted into container
- Changes stay isolated until verified
- Only merge if all tests pass

**Status:** Docker sandbox is "planned only" - not yet implemented.

### 4. MCP Server Integration

**MCP Server provides tools for self-development:**

```python
# Available MCP tools for self-development
tools = [
    "task_create",      # Create self-development tasks
    "task_run",         # Run self-development workflow
    "task_status",      # Check task status
    "approval_write",   # Approve blocked tasks
    "artifact_read",    # Read artifacts
    "artifact_write",   # Write artifacts
    "debate_start",     # Start council debate
    "memory_search",    # Search knowledge base
]
```

**Example: External agent using MCP:**
```python
# External agent (Claude, GPT-4, etc.) can:
1. task_create() → Create self-development task
2. task_run() → Start self-development workflow
3. task_status() → Monitor progress
4. approval_write() → Approve if blocked
5. artifact_read() → Read results
```

---

## CLI Usage Examples

### Example 1: Manual Self-Development Task

```bash
# 1. Create task
python -c "
import asyncio
from src.ybis.control_plane import ControlPlaneDB

async def main():
    db = ControlPlaneDB('platform_data/control_plane.db')
    await db.initialize()
    task = await db.create_task(
        title='Self-Dev: Fix gate_node artifact check',
        objective='Add missing artifact enforcement to gate_node',
        priority='HIGH'
    )
    print(f'Task created: {task.task_id}')

asyncio.run(main())
"

# 2. Run self-development workflow
python scripts/ybis_run.py TASK-123 --workflow self_develop

# 3. Check status
python -c "
import asyncio
from src.ybis.control_plane import ControlPlaneDB

async def main():
    db = ControlPlaneDB('platform_data/control_plane.db')
    await db.initialize()
    task = await db.get_task('TASK-123')
    print(f'Status: {task.status}')

asyncio.run(main())
"
```

### Example 2: Using MCP Server

```bash
# Terminal 1: Start MCP server
python scripts/ybis_mcp_server.py

# Terminal 2: Use MCP client (or external agent)
# MCP client can call:
# - task_create(title, objective, priority)
# - task_run(task_id, workflow_name="self_develop")
# - task_status(task_id)
# - approval_write(task_id, run_id, approver, reason)
```

### Example 3: Automated Self-Development

```bash
# Run self-development workflow automatically
python scripts/ybis_run.py TASK-123 --workflow self_develop

# Workflow will:
# 1. Reflect on system state
# 2. Identify improvements
# 3. Propose tasks
# 4. Execute improvements
# 5. Verify changes
# 6. Gate check (may require approval)
# 7. Integrate if passed
```

---

## Worktree Management

### Automatic Worktree Creation

**Every run gets isolated worktree:**

```python
# src/ybis/data_plane/workspace.py
run_path = init_run_structure(
    task_id="TASK-123",
    run_id="R-abc123",
    use_git_worktree=True  # Automatic worktree creation
)
```

**Worktree structure:**
```
workspaces/
  TASK-123/
    runs/
      R-abc123/              # Git worktree
        src/                 # Code (isolated)
        artifacts/           # Artifacts
          reflection_report.json
          analysis_report.json
          proposal_report.json
          spec.md
          plan.json
          executor_report.json
          verifier_report.json
          gate_report.json
          rollback_plan.json
        journal/             # Journal events
```

### Manual Worktree Cleanup

```python
# Cleanup worktree after run
from src.ybis.data_plane.git_workspace import cleanup_git_worktree

cleanup_git_worktree(
    worktree_path=Path("workspaces/TASK-123/runs/R-abc123"),
    force=True  # Force cleanup if needed
)
```

---

## Docker Integration (Future)

### Docker Sandbox for Self-Development

**When Docker sandbox is implemented:**

```yaml
# configs/profiles/default.yaml
sandbox:
  enabled: true
  type: "docker"  # Future: Docker sandbox
  network: false
  allowlist:
    - "python"
    - "pytest"
    - "ruff"
```

**Self-development with Docker:**
1. Worktree is mounted into Docker container
2. All execution happens in container
3. Changes stay isolated
4. Only merge if tests pass

**Status:** Docker sandbox is "planned only" - use `e2b` or `local` for now.

---

## MCP Server Usage

### Starting MCP Server

```bash
# Stdio mode (for CLI tools)
python scripts/ybis_mcp_server.py

# SSE mode (for web clients)
python scripts/ybis_mcp_server.py --sse
```

### Available MCP Tools

**Task Management:**
- `task_create(title, objective, priority)` - Create task
- `task_run(task_id, workflow_name)` - Run workflow
- `task_status(task_id)` - Get status
- `get_tasks(status)` - List tasks

**Artifact Management:**
- `artifact_read(task_id, run_id, artifact_name)` - Read artifact
- `artifact_write(task_id, run_id, artifact_name, content)` - Write artifact
- `approval_write(task_id, run_id, approver, reason)` - Approve task

**Debate & Memory:**
- `start_debate(topic, context)` - Start council debate
- `search_memory(query)` - Search knowledge base

### Example: External Agent Using MCP

```python
# External agent (Claude, GPT-4, etc.) can use MCP:

# 1. Create self-development task
task = mcp_client.call_tool("task_create", {
    "title": "Self-Dev: Improve gate_node",
    "objective": "Add artifact enforcement",
    "priority": "HIGH"
})

# 2. Run workflow
result = mcp_client.call_tool("task_run", {
    "task_id": task["task_id"],
    "workflow_name": "self_develop"
})

# 3. Monitor status
status = mcp_client.call_tool("task_status", {
    "task_id": task["task_id"]
})

# 4. Approve if blocked
if status["status"] == "blocked":
    mcp_client.call_tool("approval_write", {
        "task_id": task["task_id"],
        "run_id": status["latest_run"]["run_id"],
        "approver": "external_agent",
        "reason": "Changes look good"
    })
```

---

## Approval Workflow

### When Approval is Required

**Core changes require approval:**
- Changes to `src/ybis/contracts/`
- Changes to `src/ybis/syscalls/`
- Changes to `src/ybis/control_plane/`
- Changes to `src/ybis/orchestrator/gates.py`

**How to approve:**

**Via CLI:**
```bash
# Create approval artifact
echo '{"approver": "user", "reason": "Changes look good"}' > \
  workspaces/TASK-123/runs/R-abc123/artifacts/approval.json
```

**Via MCP:**
```python
task_tools.approval_write(
    task_id="TASK-123",
    run_id="R-abc123",
    approver="user",
    reason="Changes look good"
)
```

**Via File:**
```json
// workspaces/TASK-123/runs/R-abc123/artifacts/approval.json
{
  "approver": "user",
  "reason": "Changes look good",
  "timestamp": "2026-01-09T12:00:00Z"
}
```

---

## Rollback Mechanism

### Automatic Rollback

**If gate blocks or tests fail:**
1. Worktree is automatically discarded
2. Main codebase remains unchanged
3. Rollback plan is available in artifacts

**Manual rollback:**
```bash
# If needed, manually cleanup worktree
python -c "
from pathlib import Path
from src.ybis.data_plane.git_workspace import cleanup_git_worktree

cleanup_git_worktree(
    worktree_path=Path('workspaces/TASK-123/runs/R-abc123'),
    force=True
)
"
```

### Rollback Plan

**Every self-change includes rollback plan:**

```json
// artifacts/rollback_plan.json
{
  "git_checkpoint": "tag:before-self-dev-TASK-123",
  "manual_steps": [
    "Revert changes to src/ybis/orchestrator/graph.py",
    "Restore previous gate_node implementation"
  ],
  "automated": true
}
```

---

## Complete Example

### Full Self-Development Cycle

```bash
# 1. Start MCP server (optional)
python scripts/ybis_mcp_server.py &

# 2. Create self-development task
python scripts/ybis_run.py --create-task \
  --title "Self-Dev: Improve gate_node" \
  --objective "Add artifact enforcement" \
  --priority HIGH

# Output: Task TASK-123 created

# 3. Run self-development workflow
python scripts/ybis_run.py TASK-123 --workflow self_develop

# Workflow execution:
# - reflect → Identifies improvement
# - analyze → Prioritizes (P1)
# - propose → Creates task
# - spec → Generates SPEC.md
# - plan → Generates PLAN.json
# - execute → Applies changes in worktree
# - verify → Tests pass
# - gate → Checks governance (may require approval)
# - integrate → Merges to main

# 4. Check results
ls workspaces/TASK-123/runs/*/artifacts/
# reflection_report.json
# analysis_report.json
# proposal_report.json
# spec.md
# plan.json
# executor_report.json
# verifier_report.json
# gate_report.json
# rollback_plan.json
```

---

## Troubleshooting

### Worktree Creation Fails

**If git worktree creation fails:**
- Falls back to regular directory
- Check git repository status
- Ensure GitPython is installed: `pip install GitPython`

### Approval Required

**If task is blocked:**
- Check `gate_report.json` for reasons
- Create `approval.json` artifact
- Or use MCP `approval_write` tool

### Rollback Needed

**If changes need to be rolled back:**
- Check `rollback_plan.json` for instructions
- Use git checkpoint if available
- Or manually revert changes

---

## Next Steps

1. **Implement self-development workflow:** `configs/workflows/self_develop.yaml`
2. **Implement nodes:** Start with `self_reflect` node
3. **Test with simple improvement:** Fix a small issue
4. **Add Docker support:** When Docker sandbox is ready

---

## References

- `docs/SELF_DEVELOPMENT_PLAN.md` - Detailed plan
- `scripts/ybis_run.py` - CLI runner
- `scripts/ybis_mcp_server.py` - MCP server
- `src/ybis/data_plane/git_workspace.py` - Worktree management
- `src/ybis/services/mcp_tools/` - MCP tools

