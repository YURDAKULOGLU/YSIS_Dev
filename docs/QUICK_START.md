# Quick Start Guide

> **Single Source of Truth:** [`docs/AGENTS.md`](AGENTS.md) - Refer to this file for canonical entry point.

---

## One-Command Setup

```bash
# Linux/Mac
./scripts/bootstrap.sh

# Windows (PowerShell)
.\scripts\bootstrap.ps1
```

This will:
- Create virtual environment
- Install dependencies
- Initialize database
- Create workspace directories

---

## Run Your First Task

```bash
# Run a single task
python scripts/ybis_run.py TASK-123

# Or run background worker
python scripts/ybis_worker.py
```

---

## Next Steps

1. Read [`docs/AGENTS.md`](AGENTS.md) - Entry point and authority order
2. Read [`docs/AI_START_HERE.md`](AI_START_HERE.md) - Detailed onboarding
3. Read [`docs/CONSTITUTION.md`](CONSTITUTION.md) - The supreme law

---

**Note:** For entry point information, always refer to [`docs/AGENTS.md`](AGENTS.md).

