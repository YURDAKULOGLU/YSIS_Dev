# Agent Instructions (Entry Point)

## Mission

**"We build the factory, not just the product."**

This is an Agentic Development Platform that uses itself to evolve itself.

---

## FOUNDING PRINCIPLES (DNA - Her Şeyden Önce)

Bu iki prensip YBIS'in temelidir. Diğer tüm kurallar bunlardan türer.

### 1. Self-Bootstrapping ("Dog Scales Dog")
```
Sistem kendini KENDI ARAÇLARIYLA geliştirmeli.
```
- **Task çalıştır:** `python scripts/ybis_run.py TASK-XXX` (bypass YASAK)
- **MCP kullan:** External agent'lar MCP üzerinden çalışmalı
- **Self-improve:** Yeni feature YBIS'in işini kolaylaştırmalı
- **Test:** Sistem kullanılarak otomatik test edilmeli

### 2. Zero Reinvention ("Vendor First")
```
Hazır varsa KODLAMA. Vendor install → Adapter wrap → Custom code (son çare)
```
- **Vendor araştır:** pip search, GitHub, PyPI
- **Adapter yaz:** `adapters/<name>.py` thin wrapper
- **Custom code:** SADECE core abstractions (Task, Run, Workflow, Syscalls)

**Hızlı Referans:** [`docs/QUICK_REFERENCE.md`](QUICK_REFERENCE.md)

---

## Platform Overview

This repo is an **Agentic Development Platform** (Python-first) with:
- LangGraph orchestration
- Multi-worker execution (leases)
- MCP server for external clients
- Evidence-first governance (reports + deterministic gates)
- Optional modules: dashboard, debate, safe self-evolution

## 🚀 Quick Start

**Canonical Entry Point:**
```bash
# Run a single task
python scripts/ybis_run.py TASK-123

# Run background worker
python scripts/ybis_worker.py
```

**See:** [`docs/AI_START_HERE.md`](docs/AI_START_HERE.md) for detailed onboarding.

## Authority Order (Read First)

### Tier 1: Supreme Law
1) docs/CONSTITUTION.md - The supreme law, overrides everything
2) docs/DISCIPLINE.md - Development discipline rules

### Tier 2: Entry & Onboarding
3) docs/AGENTS.md (this file - entry point)
4) docs/AI_START_HERE.md
5) docs/AGENT_READ_THIS_FIRST.md

### Tier 3: Technical Standards
6) docs/INTERFACES.md - Contracts, syscalls, MCP
7) docs/WORKFLOWS.md - LangGraph, routing
8) docs/CODE_STANDARDS.md - Python, typing, formatting
9) docs/SECURITY.md - Sandbox, permissions

### Tier 4: Governance Rules
10) docs/governance/COMMIT_STANDARDS.md - Git commit format
11) docs/governance/PR_STANDARDS.md - Pull request rules
12) docs/governance/CODE_REVIEW_CHECKLIST.md - Review process
13) docs/GOLDEN_TASKS.md - Regression suite

### Tier 5: Operations
14) docs/OPERATIONS.md - Day-to-day operations
15) docs/TESTING.md - Test strategy
16) docs/MIGRATIONS.md - Database migrations
17) docs/BOOTSTRAP_PLAN.md - Task order

## Non-Negotiables (Do not violate)

### Core Rules
- All writes/execs must go through **syscalls**.
- Each run is immutable: `workspaces/<task_id>/runs/<run_id>/`.
- "Done" means PASS in both `verifier_report.json` and `gate_report.json`.
- Changes to protected paths require approval (see Constitution + Security).
- Do not embed large third-party frameworks into core; integrate via adapters/MCP.

### Discipline Rules (from DISCIPLINE.md)
- **Pre-Implementation Checklist:** Complete before writing ANY code.
- **Single Responsibility:** One commit = one purpose.
- **Minimal Change:** Only change what's necessary.
- **Evidence Rule:** No journal event = didn't happen.
- **Error Handling:** No silent failures, no bare except.
- **Self-Review:** Apply CODE_REVIEW_CHECKLIST before submitting.

### Quality Gates
- Lint must pass (ruff)
- Type check must pass (mypy)
- Tests must pass (pytest)
- Golden tasks must pass (core subset)
- Journal events must exist for all operations

## How to start implementation
Follow docs/BOOTSTRAP_PLAN.md task order exactly. No skipping.

## If you are unsure
Stop and re-check docs/CONSTITUTION.md + docs/INTERFACES.md.

---

## 📚 Documentation Hierarchy

**This file (`docs/AGENTS.md`) is the single source of truth for:**
- Entry point: `scripts/ybis_run.py TASK-123`
- Quick start commands
- Authority order

**Other docs reference this file for entry point information.**

---

## 🤖 Claude Code Integration

Claude Code is a supported CLI agent for YBIS. See full capabilities:
- [`docs/CLAUDE_CODE_FEATURES.md`](docs/CLAUDE_CODE_FEATURES.md) - Complete feature reference
- MCP integration via `scripts/ybis_mcp_server.py`
- Configuration: `.claude/settings.json`

