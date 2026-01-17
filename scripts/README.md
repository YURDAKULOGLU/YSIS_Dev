# [TOOLS]️ The Toolbox (Scripts)

> **Zone:** Execution & Maintenance
> **Access:** All Agents

## ⚡ Primary Tools (Use These)

| Script | Command | Purpose |
|--------|---------|---------|
| **YBIS Runner** | `python scripts/ybis_run.py <task_id>` | Runs a single task workflow. |
| **Worker** | `python scripts/ybis_worker.py` | Background worker that polls for tasks. |
| **Smart Exec** | `python scripts/smart_exec.py <cmd>` | Runs shell commands quietly (saves tokens). |
| **Listener** | *(Coming Soon)* | Listens to Redis for real-time triggers. |

## 🏥 Diagnostics

| Script | Command | Purpose |
|--------|---------|---------|
| **Doctor** | `python scripts/system_health_check.py` | Checks imports and paths. |
| **Pulse** | `python scripts/ybis_pulse.py` | System health check and status. |

## Rules
- **Output:** Always use `smart_exec.py` for long commands (`npm install`, `pip install`).
- **Async:** Do not modify these scripts unless you are in "Maintenance Mode".
