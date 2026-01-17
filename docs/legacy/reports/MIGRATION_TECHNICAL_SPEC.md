# MIGRATION TECHNICAL SPECIFICATION (L3 - ENGINEERING)

> **Purpose:** This document supplements the high-level `MIGRATION_ANALIZ_RAPORU.md` with low-level engineering details, focusing on data integrity, state refactoring, and concurrency safety.
> **Strategy:** HARD CUTOVER / COMPLETE REWORK. No hybrid state.

---

## 1. DATA MIGRATION STRATEGY (SQL)

**Problem:** Current `tasks` table mixes task definitions with execution status.
**Goal:** Split into `tasks` (definition) and `runs` (execution history).

### Schema Evolution

#### Old Schema
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    goal TEXT,
    details TEXT,
    status TEXT, -- Mix of backlog status and run status
    metadata TEXT -- JSON blob
);
```

#### New Schema (Target)
```sql
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    title TEXT,
    objective TEXT, -- mapped from 'goal'
    status TEXT, -- 'TODO', 'IN_PROGRESS', 'DONE', 'ARCHIVED'
    created_at TIMESTAMP,
    schema_version INTEGER DEFAULT 1
);

CREATE TABLE runs (
    run_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    status TEXT, -- 'PLANNING', 'EXECUTING', 'VERIFYING', 'SUCCESS', 'FAILED'
    run_path TEXT, -- 'workspaces/<task_id>/runs/<run_id>'
    artifact_summary TEXT, -- JSON summary of results
    created_at TIMESTAMP,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
);
```

### SQL Migration Logic (The Script)

We will treat current state as "Run 0" for active tasks.

```sql
BEGIN TRANSACTION;

-- 1. Create new tables
CREATE TABLE new_tasks (...);
CREATE TABLE runs (...);

-- 2. Migrate Tasks
INSERT INTO new_tasks (task_id, title, objective, status, schema_version)
SELECT 
    id, 
    'Imported Task ' || id, 
    goal, 
    CASE 
        WHEN status = 'COMPLETED' THEN 'DONE'
        WHEN status = 'FAILED' THEN 'TODO' -- Failed tasks go back to backlog
        ELSE 'TODO' -- Reset in-progress tasks to force clean run
    END,
    1
FROM tasks;

-- 3. Archive Old Runs (Optional - creates a historical run record for completed tasks)
INSERT INTO runs (run_id, task_id, status, run_path, created_at)
SELECT 
    id || '-legacy-01', -- deterministic run_id
    id,
    'SUCCESS',
    'workspaces/archive/' || id, -- point to old archive path
    datetime('now')
FROM tasks
WHERE status = 'COMPLETED';

COMMIT;
```

---

## 2. STATE DECOUPLING STRATEGY (COMPLETE REWORK)

**Directives:** No hybrid state. No RAM-based "God Object".
**Goal:** Nodes communicate strictly via Disk (Artifacts). RAM is only for Flow Control.

### The New Context Object
The old `TaskState` (holding plan, code, errors in RAM) is DELETED.
Replaced by a lightweight `RunContext` that only knows *where* things are.

```python
# src/ybis/contracts/context.py

class RunContext(BaseModel):
    """Immutable context passed between LangGraph nodes."""
    task_id: str
    run_id: str
    run_path: str  # e.g., "workspaces/TASK-1/runs/RUN-1"
    
    # Helpers to get paths (No data storage!)
    @property
    def plan_path(self) -> Path:
        return Path(self.run_path) / "artifacts/plan.json"
        
    @property
    def result_path(self) -> Path:
        return Path(self.run_path) / "artifacts/executor_report.json"
```

### Node Refactoring Pattern (Disk-in, Disk-out)

Every node in LangGraph must be rewritten to:
1. Load input artifacts from disk using `RunContext` paths.
2. Perform work.
3. Write output artifacts to disk.
4. Return simple status string (e.g., "verify_failed") for routing.

#### Example: Execution Node
**OLD (Bad):**
```python
def execute_node(state: TaskState):
    plan = state.plan  # RAM access
    result = executor.run(plan)
    state.code_result = result  # RAM mutation
    return state
```

**NEW (Good):**
```python
def execute_node(ctx: RunContext):
    # 1. READ from Disk
    plan_data = fs.read_json(ctx.plan_path)
    plan = Plan(**plan_data)
    
    # 2. EXECUTE
    result = executor.run(plan)
    
    # 3. WRITE to Disk
    fs.write_json(ctx.result_path, result.model_dump())
    
    # 4. RETURN Routing Signal only
    return {"status": "success" if result.success else "failed"}
```

---

## 3. CONCURRENCY & RACE CONDITIONS

**Problem:** Multiple workers (or async tasks) writing to `events.jsonl` or DB simultaneously.

### Solution A: Append-Only Journaling (Filesystem)
*   **OS Guarantee:** Appending to a file (`O_APPEND` mode) is generally atomic on POSIX/Windows for small writes (<4KB).
*   **Strategy:** Use a `JournalWriter` class that opens file in `a` mode for each event write, flushes, and closes. Do not keep file handles open across await points.

### Solution B: DB Locking (SQLite)
*   `aiosqlite` serializes writes by default (one writer).
*   **Risk:** "Check-then-Act" race conditions (e.g., Worker A checks lease, sees free. Worker B checks lease, sees free. Both claim.).
*   **Fix:** Use atomic SQL `UPDATE ... WHERE status='FREE'` and check `rowcount`.

```python
# Atomic Lease Claim
async def claim_task(worker_id):
    cursor = await db.execute("""
        UPDATE leases 
        SET worker_id = ?, expires_at = ? 
        WHERE task_id = ? AND (worker_id IS NULL OR expires_at < NOW())
    """, (worker_id, new_expiry, task_id))
    
    if cursor.rowcount == 0:
        raise LeaseError("Task already claimed")
```

---

## 4. ROLLBACK & RECOVERY

Since we are doing a "Hard Cutover" (complete rework), we need a safety net.

### Backup Procedure
Before running migration scripts:
1.  **Snapshot DB:** `cp tasks.db tasks.db.bak_v4`
2.  **Snapshot Workspaces:** `cp -r workspaces/ workspaces_backup/`

### Recovery Procedure
If V5 fails critically:
1.  Restore `tasks.db.bak_v4`.
2.  Revert code to `v4.5` tag (Git).
3.  V5 runs are isolated in `workspaces/<task>/runs/`, so they don't corrupt V4 workspaces. We can just ignore/delete the new run folders.

---

## 5. BRIDGE ADAPTER STRATEGY

**Goal:** Reuse existing logic in `src/agentic/bridges/` without tight coupling.

### Wrapper Pattern

Do not modify `src/agentic/bridges/crewai_bridge.py`. Instead, wrap it.

```python
# src/ybis/adapters/crewai_adapter.py (New)

from src.ybis.contracts.planner import PlannerProtocol
# Import the OLD bridge (legacy)
from src.agentic.bridges.crewai_bridge import CrewAIBridge as LegacyBridge

class CrewAIPlannerAdapter(PlannerProtocol):
    def __init__(self):
        self.legacy = LegacyBridge()

    async def plan(self, task: Task) -> Plan:
        # Map New Contract -> Old Contract
        legacy_result = await self.legacy.generate_plan(task.description)
        
        # Map Old Result -> New Contract
        return Plan(
            objective=legacy_result['goal'],
            steps=legacy_result['steps']
        )
```

This isolates the messy legacy code from the clean new core.
