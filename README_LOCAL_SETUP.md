# Local Development Setup Guide

> **Constitution V3.0 Compliant** - Local development quality gates

This guide helps you set up YBIS for local development with all quality gates enabled.

---

## Quick Start

```bash
# 1. Clone and setup
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

---

## Development Tools

### Pre-commit Hooks

**Constitution V3.0 compliant quality gates:**

- ✅ **Ruff** - Fast linting and formatting (Constitution V.1)
- ✅ **Mypy** - Type checking (Constitution IV.4)
- ✅ **Import-linter** - Module boundary enforcement (Constitution III.5)
- ✅ **Emoji check** - No emojis in code (Constitution VI.2)
- ✅ **Commit message validation** - Git discipline (Constitution X.1)

**Run manually:**
```bash
pre-commit run --all-files
```

**Skip hooks (not recommended):**
```bash
git commit --no-verify
```

### VS Code Setup

1. **Install recommended extensions:**
   - Open VS Code in project root
   - VS Code will prompt to install recommended extensions
   - Or: `Ctrl+Shift+P` → "Extensions: Show Recommended Extensions"

2. **Settings are auto-configured:**
   - Ruff linting enabled
   - Mypy type checking enabled
   - Format on save enabled
   - Import organization enabled

3. **Tasks available:**
   - `Ctrl+Shift+P` → "Tasks: Run Task"
   - Select: "Lint (ruff)", "Type Check (mypy)", "Run Tests", etc.

### DevContainer (Optional)

**For consistent development environment:**

```bash
# Open in DevContainer
# VS Code will prompt to "Reopen in Container"
# Or: Ctrl+Shift+P → "Dev Containers: Reopen in Container"
```

**Features:**
- Python 3.11 pre-installed
- Docker-in-Docker support
- All extensions pre-installed
- Auto-runs `pip install -e ".[dev]"` on creation

---

## Quality Gates

### Before Every Commit

**Automatic (pre-commit hooks):**
- ✅ Ruff linting
- ✅ Ruff formatting
- ✅ Mypy type checking
- ✅ Import boundary checks
- ✅ Emoji detection
- ✅ Commit message format

**Manual (recommended):**
```bash
# Run tests
pytest tests/unit/ -v

# Check coverage
pytest tests/ --cov=src/ybis --cov-report=term

# Security scan
bandit -r src/ybis
```

### Before Every PR

**Checklist:**
- [ ] All pre-commit hooks pass
- [ ] All tests pass
- [ ] Type checking passes (`mypy src/ybis`)
- [ ] Import boundaries respected (`lint-imports`)
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow format (see `docs/governance/COMMIT_STANDARDS.md`)

---

## Troubleshooting

### Pre-commit Hooks Not Running

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### Mypy Errors

```bash
# Check specific file
mypy src/ybis/orchestrator/planner.py

# Ignore specific errors (temporary)
# Add to pyproject.toml: [tool.mypy.overrides]
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

## Local CI/CD

**Run CI checks locally:**

```bash
# All checks
pre-commit run --all-files

# Specific check
pre-commit run ruff --all-files
pre-commit run mypy --all-files
pre-commit run import-linter --all-files
```

**GitHub Actions equivalent:**
```bash
# Install act (GitHub Actions locally)
# https://github.com/nektos/act

act -j lint
act -j type-check
act -j test
```

---

## Constitution V3.0 Compliance

All local tools enforce Constitution V3.0 rules:

| Rule | Tool | Enforcement |
|------|------|-------------|
| IV.4 Type Safety | Mypy | Pre-commit + CI |
| III.5 Layer Discipline | Import-linter | Pre-commit + CI |
| V.1 Test Pyramid | Pytest | Pre-commit + CI |
| VI.2 Naming | Emoji check | Pre-commit |
| X.1 Git Discipline | Commit validator | Pre-commit |

---

## Next Steps

1. **Read Constitution:** `docs/CONSTITUTION.md`
2. **Read Discipline:** `docs/DISCIPLINE.md`
3. **Read Standards:** `docs/governance/COMMIT_STANDARDS.md`
4. **Start coding:** Follow pre-implementation checklist in `DISCIPLINE.md`

---

**Last Updated:** 2026-01-12  
**Version:** 1.0

