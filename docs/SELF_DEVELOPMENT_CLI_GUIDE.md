# Self-Development CLI Guide

**Purpose:** Quick reference for using YBIS self-development via CLI.
**Status:** Ready to Use
**Date:** 2026-01-09

---

## Quick Commands

### 1. Run Self-Development Workflow

```bash
# Create task and run self-development workflow
python scripts/ybis_run.py TASK-123 --workflow self_develop
```

### 2. Start MCP Server

```bash
# Stdio mode (for CLI tools)
python scripts/ybis_mcp_server.py

# SSE mode (for web clients)
python scripts/ybis_mcp_server.py --sse
```

### 3. Check Task Status

```bash
# Via Python
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

---

## Complete Workflow Example

### Step 1: Create Self-Development Task

```bash
# Option A: Via Python
python -c "
import asyncio
from src.ybis.control_plane import ControlPlaneDB

async def main():
    db = ControlPlaneDB('platform_data/control_plane.db')
    await db.initialize()
    task = await db.create_task(
        title='Self-Dev: Improve gate_node',
        objective='Add artifact enforcement to gate_node',
        priority='HIGH'
    )
    print(f'Task created: {task.task_id}')

asyncio.run(main())
"

# Option B: Via MCP (if MCP server running)
# Use MCP client to call task_create()
```

### Step 2: Run Self-Development Workflow

```bash
# Run with self-development workflow
python scripts/ybis_run.py TASK-123 --workflow self_develop
```

**What happens:**
1. ✅ Git worktree created automatically (`workspaces/TASK-123/runs/R-abc123/`)
2. ✅ Workflow executes: reflect → analyze → propose → spec → plan → execute → verify → gate → integrate
3. ✅ All changes happen in worktree (isolated)
4. ✅ Artifacts saved to `workspaces/TASK-123/runs/R-abc123/artifacts/`
5. ✅ If successful → merge to main
6. ✅ If failed → worktree discarded (safe rollback)

### Step 3: Check Results

```bash
# List artifacts
ls workspaces/TASK-123/runs/*/artifacts/

# Read gate report
cat workspaces/TASK-123/runs/*/artifacts/gate_report.json

# Read reflection report
cat workspaces/TASK-123/runs/*/artifacts/reflection_report.json
```

---

## Worktree Management

### Automatic Worktree

**Every run gets isolated worktree:**
- Branch: `task-TASK-123-run-R-abc123`
- Path: `workspaces/TASK-123/runs/R-abc123/`
- All changes isolated from main codebase

### Manual Cleanup

```bash
# Cleanup worktree if needed
python -c "
from pathlib import Path
from src.ybis.data_plane.git_workspace import cleanup_git_worktree

cleanup_git_worktree(
    worktree_path=Path('workspaces/TASK-123/runs/R-abc123'),
    force=True
)
"
```

---

## MCP Server Usage

### Start MCP Server

```bash
# Terminal 1: Start server
python scripts/ybis_mcp_server.py

# Terminal 2: Use MCP client or external agent
# MCP tools available:
# - task_create(title, objective, priority)
# - task_run(task_id, workflow_name="self_develop")
# - task_status(task_id)
# - approval_write(task_id, run_id, approver, reason)
```

### External Agent Example

```python
# External agent (Claude, GPT-4, etc.) can:
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

## Docker Integration

### Current Status

**Docker sandbox:** ⚠️ **Planned Only** (not yet implemented)

**Available sandbox types:**
- `e2b` - E2B cloud sandbox (✅ Available)
- `local` - Local subprocess (✅ Available)
- `docker` - Docker container (⚠️ Planned only)

### When Docker is Available

```yaml
# configs/profiles/default.yaml
sandbox:
  enabled: true
  type: "docker"  # Future: Docker sandbox
  network: false
```

**Self-development with Docker:**
- Worktree mounted into Docker container
- All execution in container (isolated)
- Changes stay isolated until verified
- Only merge if tests pass

---

## Approval Workflow

### When Approval is Required

**Core changes require approval:**
- Changes to `src/ybis/contracts/`
- Changes to `src/ybis/syscalls/`
- Changes to `src/ybis/control_plane/`
- Changes to `src/ybis/orchestrator/gates.py`

### How to Approve

**Via CLI:**
```bash
# Create approval artifact
echo '{"approver": "user", "reason": "Changes look good"}' > \
  workspaces/TASK-123/runs/R-abc123/artifacts/approval.json

# Or via MCP
python -c "
from src.ybis.services.mcp_tools import task_tools
task_tools.approval_write(
    task_id='TASK-123',
    run_id='R-abc123',
    approver='user',
    reason='Changes look good'
)
"
```

---

## Available Workflows

### List of Workflows

```bash
# Default workflow (spec → plan → execute → verify → gate)
python scripts/ybis_run.py TASK-123 --workflow ybis_native

# Self-development workflow (reflect → analyze → propose → spec → plan → execute → verify → gate → integrate)
python scripts/ybis_run.py TASK-123 --workflow self_develop

# EvoAgentX workflow evolution
python scripts/ybis_run.py TASK-123 --workflow evo_evolve

# Reactive agents workflow
python scripts/ybis_run.py TASK-123 --workflow reactive_agent

# Council review workflow
python scripts/ybis_run.py TASK-123 --workflow council_review

# Self-improve workflow (vendor-based)
python scripts/ybis_run.py TASK-123 --workflow self_improve
```

---

## Troubleshooting

### Worktree Creation Fails

**If git worktree creation fails:**
- Falls back to regular directory
- Check git repository status: `git status`
- Ensure GitPython is installed: `pip install GitPython`

### Approval Required

**If task is blocked:**
```bash
# Check gate report
cat workspaces/TASK-123/runs/*/artifacts/gate_report.json

# Create approval
echo '{"approver": "user", "reason": "Approved"}' > \
  workspaces/TASK-123/runs/*/artifacts/approval.json

# Re-run workflow
python scripts/ybis_run.py TASK-123 --workflow self_develop
```

### Rollback Needed

**If changes need to be rolled back:**
```bash
# Check rollback plan
cat workspaces/TASK-123/runs/*/artifacts/rollback_plan.json

# Cleanup worktree
python -c "
from pathlib import Path
from src.ybis.data_plane.git_workspace import cleanup_git_worktree
cleanup_git_worktree(Path('workspaces/TASK-123/runs/R-abc123'), force=True)
"
```

---

## Summary

**Self-development workflow:**
1. ✅ **Git worktree** - Automatic isolation per run
2. ✅ **CLI support** - `--workflow self_develop` parameter
3. ✅ **MCP server** - External agents can trigger self-development
4. ⚠️ **Docker** - Planned only (use `e2b` or `local` for now)

**Quick start:**
```bash
# 1. Create task
python -c "..." # (create task code above)

# 2. Run self-development
python scripts/ybis_run.py TASK-123 --workflow self_develop

# 3. Check results
ls workspaces/TASK-123/runs/*/artifacts/
```

---

## References

- `docs/SELF_DEVELOPMENT_PLAN.md` - Detailed plan
- `docs/SELF_DEVELOPMENT_USAGE.md` - Full usage guide
- `scripts/ybis_run.py` - CLI runner (updated with --workflow support)
- `scripts/ybis_mcp_server.py` - MCP server
- `src/ybis/data_plane/git_workspace.py` - Worktree management

