# INTERFACES (Contracts + Syscalls + MCP)

References:
- CONSTITUTION.md
- WORKFLOWS.md
- SECURITY.md

## 1) Contracts (minimum)
### Task
task_id, title, objective, status, priority, schema_version, timestamps, workspace_path

### Run
run_id, task_id, workflow, status, risk_level, run_path, timestamps, schema_version

### Evidence reports
All artifacts/*.json must include:
schema_version, task_id, run_id, timestamps, status, metrics, warnings/errors.

Required artifacts baseline for any write-capable workflow:
- patch.diff (if changes)
- executor_report.json
- patch_apply_report.json
- verifier_report.json
- gate_report.json
- journal/events.jsonl
Spec files are stored in `docs/specs/<task_id>_SPEC.md` (not run artifacts).

## 2) Syscalls (single enforcement point)
Filesystem:
- fs.read
- fs.write_file
- fs.apply_patch

Execution:
- exec.run (sandboxed, allowlisted, network policy)

Git:
- git.status, git.diff, git.commit(allowed_files)

DB:
- task.*, run.*, lease.*, worker.*

Governance:
- approvals.write
- migrate.check/apply

## 3) MCP tools (remote facade)

The MCP server (`src/ybis/services/mcp_server.py`) exposes 7+ tools for external clients (FastMCP-based, with a local MCPServer wrapper for scripts):

### Task Management
- **`task_create(title, objective, priority)`**: Create a new task
  - Returns: `{task_id, title, objective, status, priority}`
- **`task_status(task_id)`**: Get task and latest run information
  - Returns: `{task_id, title, objective, status, priority}`
- **`task_claim(worker_id)`**: Claim a pending task for a worker
  - Returns: `{task_id, title, objective, run_id, run_path, status: "claimed"}` or `{task: null}` if none available
  - **Note:** This atomically claims a task via lease mechanism. Only one worker can claim a task at a time.
- **`task_complete(task_id, run_id, status, result_summary, worker_id)`**: Mark task as complete and release lease
  - Returns: `{task_id, run_id, status, result_summary, lease_released: true}`

### Artifact Management
- **`artifact_read(task_id, run_id, artifact_name)`**: Read artifact from a run
  - Returns: `{content: {...}, raw: "..."}` or `{error: "..."}`
  - Common artifacts: `plan.json`, `verifier_report.json`, `gate_report.json`, `executor_report.json`
- **`artifact_write(run_id, name, content)`**: Write artifact to a run's artifacts directory
  - Returns: `{run_id, artifact_name, artifact_path, status: "written"}`
  - **Note:** This is used by external workers to write execution results.

### Approval Management
- **`approval_write(task_id, run_id, approver, reason)`**: Write approval for blocked run
  - Returns: `{task_id, run_id, approver, status: "approved"}`
  - Creates `approval.json` artifact that allows the run to resume.

### Example: External Worker Flow
```python
# 1. Claim a task
result = await mcp.task_claim(worker_id="my-worker")
if result["task"]:
    task_id = result["task_id"]
    run_id = result["run_id"]
    
    # 2. Execute work (external logic)
    # ... do work ...
    
    # 3. Write artifacts
    await mcp.artifact_write(run_id, "executor_report.json", json.dumps(report))
    
    # 4. Complete task
    await mcp.task_complete(task_id, run_id, "completed", "Work done", "my-worker")
```

---

## 4) Planner Protocol (Spec-First)

**Input:** `Task` object with `title` and `objective`

**Output:** `Plan` object with:
- `objective`: Clear description of what to do
- `files`: List of file paths to modify
- `instructions`: Step-by-step instructions
- `steps`: Multi-step plan (optional)
- `referenced_context`: Relevant codebase context from RAG

**Process:**
1. Planner queries vector store (RAG) for relevant context
2. Planner uses Code Graph for impact analysis ("Changing X affects Y, Z")
3. Planner uses LlamaIndex for legacy code context (if available)
4. LLM generates structured JSON plan
5. Plan includes impact warnings from dependency analysis

**Spec-First Protocol:**
- **Architect** (What/Why): Defines requirements
- **Spec Writer** (How): Creates technical spec (implicit in plan)
- **Executor** (Implementation): Implements plan exactly

**Forbidden:** "Cowboy Coding" - All code must trace back to a plan/spec.

---

## 5) Worker Protocol (Lease/Heartbeat Cycle)

**Purpose:** Multi-worker coordination with atomic task claiming.

### Lease Mechanism
- Tasks are claimed via atomic database operations
- Only one worker can hold a lease for a task at a time
- Leases have TTL (default: 300 seconds)
- Workers must send heartbeats to renew leases

### Worker Lifecycle
1. **Startup:** Worker initializes DB connection, generates unique `worker_id`
2. **Poll Loop:** Worker polls for pending tasks every `poll_interval` seconds
3. **Claim:** Worker attempts to claim a task via `claim_task(task_id, worker_id, duration_sec)`
4. **Heartbeat:** Background thread sends heartbeats every `heartbeat_interval` seconds
5. **Execute:** Worker executes workflow (plan → execute → verify → gate)
6. **Complete:** Worker updates task status and releases lease

### Heartbeat Protocol
- Heartbeat updates lease expiration time
- If heartbeat fails, lease expires and task becomes available again
- Prevents "zombie" workers from holding tasks indefinitely

### Example Worker Implementation
```python
worker = YBISWorker(worker_id="worker-1", poll_interval=5, heartbeat_interval=60)
await worker.start()  # Runs until stopped
```

**Key Methods:**
- `start()`: Start worker loop and heartbeat thread
- `stop()`: Gracefully stop worker
- `_poll_and_execute()`: Main polling loop (internal)
- `_heartbeat_loop()`: Background heartbeat thread (internal)

