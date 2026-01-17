# Local Integrations Summary

> **Constitution V3.0 Compliant** - All quality gates implemented locally

**Date:** 2026-01-12  
**Status:** ✅ Complete

---

## Overview

All local development quality gates have been implemented according to Constitution V3.0 and supporting standards. These tools enforce code quality, type safety, module boundaries, and git discipline **before** code reaches the repository.

---

## Implemented Integrations

### 1. Pre-commit Hooks (`.pre-commit-config.yaml`)

**Quality Gates:**
- ✅ **Ruff** - Linting and formatting (Constitution V.1)
- ✅ **Mypy** - Type checking (Constitution IV.4)
- ✅ **Import-linter** - Module boundary enforcement (Constitution III.5)
- ✅ **Emoji check** - No emojis in code (Constitution VI.2)
- ✅ **Commit message validation** - Git discipline (Constitution X.1)
- ✅ **Standard hooks** - Merge conflicts, private keys, JSON/YAML validation

**Installation:**
```bash
pip install -e ".[dev]"
pre-commit install
```

**Usage:**
```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

---

### 2. Custom Scripts

**`scripts/check_emoji.py`**
- Checks for emoji and problematic unicode characters
- Prevents Windows terminal crashes (CP1254 encoding issues)
- Constitution VI.2 compliant

**`scripts/validate_commit_msg.py`**
- Validates commit message format: `<type>(<scope>): <subject>`
- Enforces COMMIT_STANDARDS.md rules
- Constitution X.1 compliant

---

### 3. Import-linter Configuration (`pyproject.toml`)

**Module Boundary Contracts:**
- ✅ Syscalls cannot import from orchestrator
- ✅ Adapters cannot import from orchestrator
- ✅ Data plane cannot import from orchestrator
- ✅ Control plane cannot import from orchestrator
- ✅ Services cannot import from orchestrator
- ✅ Constants and contracts can be imported by anyone

**See:** `docs/MODULE_BOUNDARIES.md` for full rules

---

### 4. DevContainer (`.devcontainer/devcontainer.json`)

**Features:**
- Python 3.11 pre-installed
- Docker-in-Docker support
- VS Code extensions pre-installed
- Auto-runs `pip install -e ".[dev]"` on creation
- Port forwarding for Dashboard (8501), Neo4j (7474), Viz (3000)

**Usage:**
- Open in VS Code
- VS Code will prompt: "Reopen in Container"
- Or: `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

---

### 5. GitHub Actions CI/CD (`.github/workflows/ci.yml`)

**Jobs:**
- ✅ **Lint** - Ruff check and format
- ✅ **Type Check** - Mypy strict mode
- ✅ **Import Lint** - Module boundary checks
- ✅ **Test** - Unit tests with coverage
- ✅ **Security** - Bandit and pip-audit

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

---

### 6. VS Code Configuration

**Settings (`.vscode/settings.json`):**
- Auto-format on save (Ruff)
- Auto-organize imports
- Ruff linting enabled
- Mypy type checking enabled
- File exclusions (legacy, vendors, workspaces)

**Extensions (`.vscode/extensions.json`):**
- Python, Pylance, Ruff, Mypy
- Black formatter, YAML, JSON, Docker
- GitHub Copilot (optional)

**Tasks (`.vscode/tasks.json`):**
- Lint (ruff)
- Format (ruff)
- Type Check (mypy)
- Import Lint
- Run Tests
- Run All Tests
- Pre-commit (all files)

**Launch (`.vscode/launch.json`):**
- Python: Current File
- Python: YBIS CLI
- Python: Run Task
- Python: Pytest Current File
- Python: Pytest All

---

## Constitution V3.0 Compliance Matrix

| Constitution Rule | Tool | Enforcement | Status |
|-------------------|------|-------------|--------|
| IV.4 Type Safety | Mypy | Pre-commit + CI | ✅ |
| III.5 Layer Discipline | Import-linter | Pre-commit + CI | ✅ |
| V.1 Test Pyramid | Pytest | Pre-commit + CI | ✅ |
| VI.2 Naming | Emoji check | Pre-commit | ✅ |
| X.1 Git Discipline | Commit validator | Pre-commit | ✅ |
| IV.2 Minimal Change | Ruff | Pre-commit + CI | ✅ |
| IV.3 Explicit Over Implicit | Ruff | Pre-commit + CI | ✅ |

---

## Quick Start Guide

### First Time Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd YBIS_Dev

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks
pre-commit install

# 5. Verify setup
pre-commit run --all-files
```

### Daily Development

**Before committing:**
```bash
# Hooks run automatically, but you can test:
pre-commit run --all-files
```

**VS Code:**
- Format on save is automatic
- Linting shows inline
- Type errors highlighted
- Tasks available via `Ctrl+Shift+P` → "Tasks: Run Task"

---

## Troubleshooting

### Pre-commit Hooks Not Running

```bash
# Reinstall
pre-commit uninstall
pre-commit install

# Test manually
pre-commit run --all-files
```

### Mypy Errors

```bash
# Check specific file
mypy src/ybis/orchestrator/planner.py

# See pyproject.toml for configuration
```

### Import-linter Errors

```bash
# Check specific contract
lint-imports --contract "Syscalls cannot import from orchestrator"

# See MODULE_BOUNDARIES.md for rules
```

### Ruff Format Conflicts

```bash
# Auto-fix
ruff format .

# Check only
ruff format --check .
```

---

## Files Created/Modified

### Created:
- ✅ `scripts/check_emoji.py`
- ✅ `scripts/validate_commit_msg.py`
- ✅ `.devcontainer/devcontainer.json`
- ✅ `.github/workflows/ci.yml`
- ✅ `.vscode/settings.json`
- ✅ `.vscode/extensions.json`
- ✅ `.vscode/tasks.json`
- ✅ `.vscode/launch.json`
- ✅ `README_LOCAL_SETUP.md`
- ✅ `docs/LOCAL_INTEGRATIONS_SUMMARY.md` (this file)

### Modified:
- ✅ `.pre-commit-config.yaml` (updated with new hooks)
- ✅ `pyproject.toml` (added import-linter config)

---

## Next Steps

1. **Install dependencies:** `pip install -e ".[dev]"`
2. **Install hooks:** `pre-commit install`
3. **Test:** `pre-commit run --all-files`
4. **Start coding:** Follow `docs/DISCIPLINE.md` checklist

---

## References

- **Constitution:** `docs/CONSTITUTION.md`
- **Discipline:** `docs/DISCIPLINE.md`
- **Module Boundaries:** `docs/MODULE_BOUNDARIES.md`
- **Naming Conventions:** `docs/NAMING_CONVENTIONS.md`
- **Commit Standards:** `docs/governance/COMMIT_STANDARDS.md`
- **Code Review:** `docs/governance/CODE_REVIEW_CHECKLIST.md`
- **Local Setup:** `README_LOCAL_SETUP.md`

---

**Last Updated:** 2026-01-12  
**Version:** 1.0

