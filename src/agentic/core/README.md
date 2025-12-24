# 🧠 Core Architecture

> **Zone:** System Logic & Configuration
> **Access:** Critical / Read-Heavy

## Key Components

| File | Purpose |
|------|---------|
| `config.py` | **The Source of Truth** for paths. Never hardcode paths; import from here. |
| `protocols.py` | **The Law.** Pydantic models defining data structures (`TaskState`, `Plan`). |
| `logger.py` | **The Voice.** Loguru-based smart logging (Console=Clean, File=Verbose). |
| `smart_logger.py`| *Legacy wrapper*, prefer `logger.py`. |

## Rules
1. **Importing:** Always import `PROJECT_ROOT` from `config.py`.
2. **Logging:** Use `from src.agentic.core.logger import log`.
3. **Typing:** All data passing between agents MUST use `protocols.py` models.
