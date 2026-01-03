# 🛠️ The Toolbox (Scripts)

> **Zone:** Execution & Maintenance
> **Access:** All Agents

## ⚡ Primary Tools (Use These)

| Script | Command | Purpose |
|--------|---------|---------|
| **The Button** | `python scripts/run_next.py` | Claims the next task from DB and runs it. (Atomic) |
| **Smart Exec** | `python scripts/smart_exec.py <cmd>` | Runs shell commands quietly (saves tokens). |
| **Listener** | *(Coming Soon)* | Listens to Redis for real-time triggers. |

## 🏥 Diagnostics

| Script | Command | Purpose |
|--------|---------|---------|
| **Doctor** | `python scripts/system_health_check.py` | Checks imports and paths. |
| **Runner** | `python scripts/run_production.py` | *Legacy loop*, prefer `run_next.py`. |

## Rules
- **Output:** Always use `smart_exec.py` for long commands (`npm install`, `pip install`).
- **Async:** Do not modify these scripts unless you are in "Maintenance Mode".
