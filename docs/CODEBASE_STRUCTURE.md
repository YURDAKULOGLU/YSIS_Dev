# CODEBASE STRUCTURE

> Bu doküman repo'nun fiziksel yapısını tanımlar.
> Yeni dosya/dizin oluştururken bu kurallara uyulmalıdır.

**References:**
- CONSTITUTION.md (FOUNDING PRINCIPLES - Read First!)
- MODULE_BOUNDARIES.md
- NAMING_CONVENTIONS.md

---

## 0. FOUNDING PRINCIPLES (DNA)

Bu yapı iki temel prensibe dayanır (CONSTITUTION.md'de detaylı):

### 0.1 Self-Bootstrapping ("Dog Scales Dog")
**Sistem kendini kendi araçlarıyla geliştirmeli:**
- Yeni feature'lar YBIS orchestrator'ı kullanılarak eklenmeli
- External agent'lar (Claude, Gemini) YBIS'i MCP/CLI üzerinden kullanmalı
- Self-improve workflow kendini kullanarak çalışmalı
- Test'ler sistem kullanılarak otomatik çalışmalı

**Yapısal yansıma:**
- `scripts/ybis_run.py` → Tüm task'lar buradan çalışmalı
- `orchestrator/self_improve.py` → Sistem kendini iyileştirmeli
- `workflows/self_improve.yaml` → Self-improvement workflow'u

### 0.2 Zero Reinvention ("Vendor First")
**Hazır varsa kodlanmayacak, adapte edilecek:**
- Vendor install → `pip install X`, direkt kullan
- Adapter wrap → `adapters/` içinde thin wrapper
- Custom code → Sadece core abstractions (Task, Run, Workflow)

**Yapısal yansıma:**
- `adapters/` → Tüm external tool'lar burada (ChromaDB, LiteLLM, Aider, etc.)
- `vendors/` → Third-party vendor code (reference implementations)
- Custom code → Sadece `contracts/`, `orchestrator/`, `syscalls/` içinde

**Yeni component eklerken:**
1. Önce vendor araştır → `pip search`, GitHub, PyPI
2. Varsa adapter yaz → `adapters/<name>.py` (thin wrapper)
3. Yoksa minimal custom code → Sadece core abstractions için

---

## 1. Top-Level Directory Structure

```
YBIS_Dev/
├── src/ybis/              # Main source code (Python package)
├── cli/                   # CLI entry points
├── scripts/               # Standalone scripts
├── tests/                 # Test suite
├── docs/                  # Documentation
├── configs/               # Configuration files
├── platform_data/         # Runtime data (gitignored)
├── workspaces/            # Task workspaces (gitignored)
├── vendors/               # Third-party vendor code
├── legacy/                # DEPRECATED - Do not use
└── [config files]         # pyproject.toml, etc.
```

### 1.1 Protected Directories (Approval Required)

| Directory | Reason | Approver |
|-----------|--------|----------|
| `src/ybis/` | Core code | Human |
| `configs/` | System config | Human |
| `docs/governance/` | Rules | Human |
| `.github/` | CI/CD | Human |

### 1.2 Forbidden Directories (Never Write)

| Directory | Reason |
|-----------|--------|
| `legacy/` | Deprecated, read-only |
| `.venv/` | Virtual environment |
| `.git/` | Version control |
| `node_modules/` | JS dependencies |
| `__pycache__/` | Python cache |

### 1.3 Ephemeral Directories (Gitignored)

| Directory | Purpose |
|-----------|---------|
| `platform_data/` | Runtime state, DB, cache |
| `workspaces/` | Task execution spaces |
| `htmlcov/` | Coverage reports |
| `.pytest_cache/` | Test cache |

---

## 2. Source Code Structure (`src/ybis/`)

```
src/ybis/
├── __init__.py            # Package init (version, exports)
├── constants.py           # Global constants (PROJECT_ROOT, etc.)
│
├── orchestrator/          # Workflow orchestration
│   ├── graph.py           # LangGraph workflow definition
│   ├── planner.py         # Plan generation
│   ├── verifier.py        # Verification (lint, tests)
│   ├── self_improve.py    # Self-improvement loop
│   └── ...
│
├── adapters/              # External integrations (pluggable)
│   ├── registry.py        # Adapter registry
│   ├── local_coder.py     # Default executor (Ollama via LiteLLM)
│   ├── aider.py           # Aider executor (vendor: aider-chat)
│   ├── vector_store_*.py  # Vector stores (ChromaDB, Qdrant adapters)
│   ├── llamaindex_adapter.py  # LlamaIndex (vendor: llama-index)
│   └── ...                # ALL external tools go here (vendor first!)
│                           # Rule: If vendor exists, adapt it. Never rebuild.
│
├── services/              # Internal services
│   ├── policy.py          # Policy management
│   ├── event_bus.py       # Event publishing
│   ├── health_monitor.py  # Health checks
│   └── mcp_tools/         # MCP tool implementations
│
├── syscalls/              # Guarded operations (THE API)
│   ├── fs.py              # Filesystem operations
│   ├── exec.py            # Command execution
│   ├── git.py             # Git operations
│   └── journal.py         # Event journaling
│
├── control_plane/         # Coordination (DB-backed)
│   ├── db.py              # Database operations
│   └── lease.py           # Lease management
│
├── data_plane/            # Evidence (filesystem-backed)
│   ├── vector_store.py    # Vector store abstraction
│   └── git_workspace.py   # Worktree management
│
├── workflows/             # Workflow definitions
│   ├── registry.py        # Workflow registry
│   ├── runner.py          # Workflow execution
│   └── node_registry.py   # Node type registry
│
├── contracts/             # Pydantic models (schemas)
│   ├── task.py            # Task model
│   ├── run.py             # Run model
│   └── artifacts.py       # Artifact models
│
├── cli/                   # CLI commands
│   └── main.py            # CLI entry point
│
└── migrations/            # Database migrations
    └── *.py               # Migration files
```

### 2.1 Module Purposes

| Module | Purpose | Contains | Vendor Policy |
|--------|---------|----------|---------------|
| `orchestrator/` | Workflow logic | Nodes, routing, state | LangGraph (vendor) |
| `adapters/` | External tools | Third-party integrations | **ALL vendors here** |
| `services/` | Internal services | Policy, events, health | Custom (core logic) |
| `syscalls/` | Guarded API | All mutation operations | Custom (security layer) |
| `control_plane/` | Coordination | DB, leases, workers | SQLite (vendor) |
| `data_plane/` | Evidence | Files, vectors, workspaces | ChromaDB/Qdrant (vendor) |
| `workflows/` | Workflow defs | YAML-driven workflows | Custom (abstraction) |
| `contracts/` | Data models | Pydantic schemas | Pydantic (vendor) |

**Key Rule:** `adapters/` içindeki her şey vendor-based. Custom code sadece `orchestrator/`, `services/`, `syscalls/`, `contracts/` içinde.

### 2.2 File Placement Rules

| If you're adding... | Put it in... |
|---------------------|--------------|
| New orchestration node | `orchestrator/` |
| New external integration | `adapters/` |
| New internal service | `services/` |
| New guarded operation | `syscalls/` |
| New data model | `contracts/` |
| New MCP tool | `services/mcp_tools/` |
| New workflow | `configs/workflows/` |

---

## 3. Configuration Structure (`configs/`)

```
configs/
├── adapters.yaml          # Adapter catalog (source of truth)
├── settings.yaml          # Main settings
├── framework_docs.yaml    # Framework documentation config
├── workflow-registry.yaml # Workflow registry
│
├── profiles/              # Policy profiles
│   ├── default.yaml       # Default profile
│   └── strict.yaml        # Strict profile
│
└── workflows/             # Workflow definitions
    ├── schema.yaml        # Workflow schema
    └── ybis_native.yaml   # Native workflow
```

### 3.1 Config File Rules

| File | Purpose | Schema |
|------|---------|--------|
| `adapters.yaml` | Adapter definitions | Defined in file |
| `settings.yaml` | Runtime settings | `contracts/config.py` |
| `profiles/*.yaml` | Security profiles | `contracts/policy.py` |
| `workflows/*.yaml` | Workflow specs | `workflows/schema.yaml` |

---

## 4. Documentation Structure (`docs/`)

```
docs/
├── AGENTS.md              # Entry point (authority order)
├── CONSTITUTION.md        # Supreme law
├── DISCIPLINE.md          # Development rules
│
├── governance/            # Governance rules
│   ├── COMMIT_STANDARDS.md
│   ├── PR_STANDARDS.md
│   └── CODE_REVIEW_CHECKLIST.md
│
├── specs/                 # Technical specifications
│   ├── *_TASK.md          # Task specs (executor input)
│   └── README.md
│
├── adapters/              # Adapter documentation
│   └── *.md               # One per adapter
│
├── workflows/             # Workflow documentation
│   └── README.md
│
├── architecture/          # Architecture docs
│   └── SPINE_DEFINITION.md
│
├── reports/               # Generated reports
│   └── *.md               # Analysis outputs
│
└── legacy/                # Deprecated docs
    └── ...
```

### 4.1 Documentation Requirements

| Change Type | Required Docs |
|-------------|---------------|
| New adapter | `docs/adapters/<name>.md` |
| New workflow | `docs/workflows/<name>.md` |
| New syscall | Update `INTERFACES.md` |
| API change | Update `INTERFACES.md` |
| Config change | Update `OPERATIONS.md` |
| Breaking change | `docs/migrations/<name>.md` |

### 4.2 Doc File Naming

```
# Governance (rules) - UPPERCASE_SNAKE_CASE
CONSTITUTION.md
CODE_STANDARDS.md

# Technical specs - UPPERCASE_SNAKE_CASE with suffix
*_TASK.md
*_SPEC.md

# Reference docs - lowercase_snake_case
aider.md
neo4j_graph.md

# Reports - UPPERCASE with context
SYSTEM_AUDIT_REPORT.md
```

---

## 5. Test Structure (`tests/`)

```
tests/
├── conftest.py            # Shared fixtures
├── README.md              # Test guide
│
├── unit/                  # Unit tests
│   ├── test_planner.py
│   └── ...
│
├── integration/           # Integration tests
│   ├── test_workflow.py
│   └── ...
│
├── e2e/                   # End-to-end tests
│   └── test_full_run.py
│
├── golden/                # Golden/regression tests
│   └── test_golden_tasks.py
│
└── fixtures/              # Test data
    ├── plans/
    ├── tasks/
    └── responses/
```

### 5.1 Test File Naming

```python
# Pattern: test_<module>_<feature>.py
test_planner_rag_context.py
test_executor_file_edit.py
test_verifier_lint_check.py

# Test function pattern
def test_<what>_<scenario>_<expected>():
    ...
```

---

## 6. Scripts Structure (`scripts/`)

```
scripts/
├── ybis_run.py            # Single task runner (canonical)
├── ybis_worker.py         # Background worker
├── ybis.py                # CLI entry point
├── ybis_mcp_server.py     # MCP server
│
├── utils/                 # Utility scripts
│   └── *.py
│
└── missions/              # Mission scripts (testing)
    └── run_*.py
```

### 6.1 Script Naming

| Type | Pattern | Example |
|------|---------|---------|
| Entry point | `ybis_*.py` | `ybis_run.py` |
| Utility | `<action>_<target>.py` | `check_health.py` |
| Mission | `run_<mission>.py` | `run_stress_test.py` |

---

## 7. Workspace Structure (`workspaces/`)

```
workspaces/
├── <TASK_ID>/             # Per-task workspace
│   ├── runs/              # Immutable run history
│   │   └── <RUN_ID>/
│   │       ├── journal/   # Event log
│   │       │   └── events.jsonl
│   │       └── artifacts/ # Evidence
│   │           ├── plan.json
│   │           ├── executor_report.json
│   │           ├── verifier_report.json
│   │           └── gate_report.json
│   └── worktree/          # Git worktree (if used)
│
└── archive/               # Completed tasks
    └── YYYY/MM/<TASK_ID>/
```

### 7.1 Artifact Requirements

**Minimum artifacts per write-capable run:**
```
artifacts/
├── plan.json              # Execution plan
├── executor_report.json   # Execution result
├── patch.diff             # Changes made (if any)
├── patch_apply_report.json# Patch application result
├── verifier_report.json   # Lint + test results
└── gate_report.json       # Final gate decision
```

---

## 8. Adding New Components

### 8.1 New Adapter Checklist

**BEFORE coding, ask: Does a vendor/library solve this?**
- ✅ Yes → Install vendor, write thin adapter wrapper
- ❌ No → Are you SURE? Check PyPI, GitHub again
- ❌ Still no → OK, but this is rare!

```
1. Research vendor → pip search, GitHub, PyPI
2. Install vendor → pip install <vendor>
3. Create src/ybis/adapters/<name>.py (thin wrapper, ~50-200 lines)
4. Implement AdapterProtocol interface
5. Add entry to configs/adapters.yaml
6. Create docs/adapters/<name>.md (note vendor dependency)
7. Add tests/unit/test_adapter_<name>.py
8. Update ADAPTER_REGISTRY_GUIDE.md if needed
```

**Example:**
```python
# ❌ WRONG - Custom vector search (500+ lines)
class MyVectorStore:
    def search(self, query):
        # Custom implementation...

# ✅ RIGHT - Vendor adapter (50 lines)
from chromadb import Client

class ChromaAdapter:
    def __init__(self):
        self._client = Client()  # Vendor does the work
    def query(self, collection, query, top_k=5):
        return self._client.get_collection(collection).query(...)
```

### 8.2 New Service Checklist

```
1. Create src/ybis/services/<name>.py
2. Add journal events for all operations
3. Add health check method
4. Create unit tests
5. Update docs if user-facing
```

### 8.3 New Syscall Checklist

```
1. Create/update src/ybis/syscalls/<domain>.py
2. Add journal events (required)
3. Add permission checks (required)
4. Update docs/INTERFACES.md
5. Add contract tests
```

### 8.4 New Workflow Checklist

```
1. Create configs/workflows/<name>.yaml
2. Register nodes in node_registry.py
3. Create docs/workflows/<name>.md
4. Add golden test for workflow
5. Update WORKFLOWS.md
```

---

## 9. Anti-Patterns (What NOT to Do)

### 9.0 Principle Violations

**Self-Bootstrapping Violations:**
```bash
# ❌ WRONG - Bypassing system
python some_external_script.py  # Skips orchestrator

# ✅ RIGHT - Using system
python scripts/ybis_run.py TASK-123  # Goes through orchestrator
```

**Zero Reinvention Violations:**
```python
# ❌ WRONG - Rebuilding vector search
class MyVectorStore:
    def __init__(self):
        self.vectors = []
    def search(self, query):
        # 500 lines of custom similarity search...

# ✅ RIGHT - Using vendor
from chromadb import Client
class ChromaAdapter:
    def __init__(self):
        self._client = Client()  # Vendor does it
```

### 9.1 Directory Anti-Patterns

```
# WRONG - Flat structure
src/ybis/
├── planner.py
├── executor.py
├── helper1.py
├── helper2.py
├── utils.py
└── ...100 more files

# RIGHT - Grouped by domain
src/ybis/
├── orchestrator/
│   └── planner.py
├── executors/
│   └── local_coder.py
└── ...
```

### 9.2 File Anti-Patterns

```
# WRONG - God files
everything.py (5000+ lines)

# RIGHT - Single responsibility
planner.py (~300 lines)
plan_validator.py (~100 lines)
plan_context.py (~200 lines)
```

### 9.3 Import Anti-Patterns

```python
# WRONG - Circular imports
# planner.py
from .executor import Executor

# executor.py
from .planner import Planner  # Circular!

# RIGHT - Interface/Protocol
# protocols.py
class PlannerProtocol(Protocol): ...
class ExecutorProtocol(Protocol): ...

# executor.py
from .protocols import PlannerProtocol
```

---

## 10. File Size Guidelines

| File Type | Max Lines | Action if Exceeded |
|-----------|-----------|-------------------|
| Module | 500 | Split into submodules |
| Class | 300 | Extract helpers |
| Function | 50 | Extract subfunctions |
| Test file | 500 | Split by feature |
| Doc file | 1000 | Split into sections |

---

## 11. Checklist for New Files

Before creating a new file:

**FOUNDING PRINCIPLES CHECK:**
- [ ] **Self-Bootstrapping:** Will this be used by YBIS to develop YBIS?
- [ ] **Zero Reinvention:** Did I check for existing vendors/libraries first?
  - [ ] Searched PyPI: `pip search <keyword>`
  - [ ] Searched GitHub: `<keyword> python`
  - [ ] If vendor exists → Adapter in `adapters/`, not custom code

**STRUCTURAL CHECKS:**
- [ ] Does it belong in the right directory?
- [ ] Does the name follow conventions?
- [ ] Is there an existing file that should contain this?
- [ ] Will this create a circular import?
- [ ] Does it need a corresponding test file?
- [ ] Does it need documentation?
- [ ] Is it registered where needed (adapters.yaml, etc.)?

**VENDOR CHECK (for adapters):**
- [ ] Vendor installed: `pip install <vendor>`
- [ ] Thin wrapper only (~50-200 lines)
- [ ] AdapterProtocol implemented
- [ ] Vendor documented in adapter doc
