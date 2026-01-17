# YBIS QUICK REFERENCE CARD

> Agent'lar için tek sayfa özet. Detaylar ilgili dokümanlarda.

---

## DNA (Asla Unutma)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SELF-BOOTSTRAPPING: Sistem kendini kendi araçlarıyla       │
│     geliştirmeli. YBIS orchestrator'ı kullan.                  │
│                                                                 │
│  2. ZERO REINVENTION: Hazır varsa KODLAMA.                     │
│     Vendor install → Adapter wrap → (son çare) Custom code     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Canonical Entry Points

```bash
# Task çalıştır (TEK DOĞRU YOL)
python scripts/ybis_run.py TASK-123

# Background worker
python scripts/ybis_worker.py

# MCP server
python scripts/ybis_mcp_server.py

# CLI
python scripts/ybis.py <command>
```

---

## Directory Cheat Sheet

| Ne ekliyorsun? | Nereye? |
|----------------|---------|
| External tool integration | `src/ybis/adapters/` |
| Workflow orchestration | `src/ybis/orchestrator/` |
| Internal service | `src/ybis/services/` |
| Guarded operation | `src/ybis/syscalls/` |
| Data model | `src/ybis/contracts/` |
| Workflow definition | `configs/workflows/` |
| Test | `tests/unit/` veya `tests/integration/` |
| Documentation | `docs/` |

---

## Pre-Code Checklist (Kısa)

```
□ Vendor araştırdım mı? (pip search, GitHub)
□ Mevcut kodu okudum mu? (READ before WRITE)
□ Plan oluşturuldu mu?
□ Journal events ekledim mi?
□ Test yazdım mı?
```

---

## Naming Quick Reference

| Tip | Format | Örnek |
|-----|--------|-------|
| File | `snake_case.py` | `local_coder.py` |
| Class | `PascalCase` | `TaskManager` |
| Function | `snake_case` | `create_task()` |
| Constant | `UPPER_SNAKE` | `MAX_RETRIES` |
| Event | `UPPER_SNAKE` | `TASK_CREATED` |
| Config key | `snake_case` | `default_enabled` |

---

## Import Rules

```
Layer 0: constants, contracts     ← Herkes import edebilir
Layer 1: syscalls, data_plane     ← Sadece üst layer'lar
Layer 2: services, adapters       ← Sadece üst layer'lar
Layer 3: orchestrator, workflows  ← Sadece cli/entry
Layer 4: cli, mcp_server          ← Entry points

KURAL: Aşağı import YASAK. Yukarı OK.
```

---

## Commit Format

```
<type>(<scope>): <subject>

Types: feat, fix, refactor, docs, test, chore
Scope: planner, executor, adapters, etc.

Örnek: feat(planner): add RAG context injection
```

---

## Must-Have Artifacts

```
artifacts/
├── plan.json              # Execution plan
├── executor_report.json   # What was done
├── verifier_report.json   # Lint + test results
└── gate_report.json       # Final decision
```

---

## Journal Events (Her İşte Zorunlu)

```python
from ..syscalls.journal import append_event

append_event(ctx.run_path, "EVENT_NAME", {
    "key": "value",
}, trace_id=ctx.trace_id)
```

---

## Error Handling

```python
# DOĞRU
try:
    result = await operation()
except SpecificError as e:
    append_event(..., "ERROR", {"error": str(e)})
    raise

# YANLIŞ
try:
    result = await operation()
except:  # Bare except YASAK
    pass  # Silent fail YASAK
```

---

## Size Limits

| Ne | Max |
|----|-----|
| Module | 500 satır |
| Class | 300 satır |
| Function | 50 satır |
| PR | 400 satır (ideal) |

---

## Forbidden

```
❌ Direct file write (syscall kullan)
❌ Bypass orchestrator
❌ Silent errors
❌ Missing journal events
❌ Custom code when vendor exists
❌ Import from lower to higher layer
❌ Protected path without approval
❌ Secrets in code/logs
```

---

## When in Doubt

1. **CONSTITUTION.md** oku (Section 0 - Founding Principles)
2. **DISCIPLINE.md** oku (Pre-Implementation Checklist)
3. **INTERFACES.md** oku (Syscall contracts)
4. Hala emin değilsen → **SOR**

---

## Key Documents

| Doküman | Ne için? |
|---------|----------|
| CONSTITUTION.md | Supreme law, founding principles |
| DISCIPLINE.md | Development rules, checklists |
| CODEBASE_STRUCTURE.md | Directory organization |
| MODULE_BOUNDARIES.md | Import rules |
| NAMING_CONVENTIONS.md | Naming standards |
| INTERFACES.md | Syscall contracts |
| GOLDEN_TASKS.md | Regression tests |
