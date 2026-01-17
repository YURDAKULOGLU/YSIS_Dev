# MODULE BOUNDARIES

> Bu doküman modüller arası bağımlılık kurallarını tanımlar.
> Import yapmadan önce bu kurallara bakılmalıdır.

**References:**
- CODEBASE_STRUCTURE.md
- CONSTITUTION.md

---

## 1. Dependency Hierarchy

```
Layer 0 (Foundation)
└── constants.py, contracts/

Layer 1 (Infrastructure)
└── syscalls/, data_plane/, control_plane/

Layer 2 (Services)
└── services/, adapters/

Layer 3 (Orchestration)
└── orchestrator/, workflows/

Layer 4 (Interface)
└── cli/, mcp_server
```

### 1.1 Import Rule

```
Yukarıdaki katman aşağıdaki katmandan import EDEBİLİR.
Aşağıdaki katman yukarıdaki katmandan import EDEMEZ.
```

**Örnek:**
```python
# DOĞRU - Layer 3 imports from Layer 1
from ybis.syscalls.fs import write_file

# YANLIŞ - Layer 1 imports from Layer 3
from ybis.orchestrator.planner import Planner  # FORBIDDEN!
```

---

## 2. Module Dependency Matrix

### 2.1 Can Import From (✓ = allowed)

| Module | constants | contracts | syscalls | data_plane | control_plane | services | adapters | orchestrator | workflows |
|--------|-----------|-----------|----------|------------|---------------|----------|----------|--------------|-----------|
| **constants** | - | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **contracts** | ✓ | - | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **syscalls** | ✓ | ✓ | - | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **data_plane** | ✓ | ✓ | ✓ | - | ✗ | ✗ | ✗ | ✗ | ✗ |
| **control_plane** | ✓ | ✓ | ✓ | ✗ | - | ✗ | ✗ | ✗ | ✗ |
| **services** | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✗ | ✗ | ✗ |
| **adapters** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✗ | ✗ |
| **orchestrator** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✗ |
| **workflows** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| **cli** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### 2.2 Special Rules

| From | To | Rule |
|------|-----|------|
| Any | `constants.py` | Always allowed |
| Any | `contracts/` | Always allowed |
| `adapters/` | External libs | Use lazy import |
| `orchestrator/` | `adapters/` | Via registry only |
| `services/` | `adapters/` | Via registry only |

---

## 3. Module Responsibilities

### 3.1 `constants.py`
```python
# CAN contain:
- PROJECT_ROOT
- Default paths
- Magic constants
- Feature flags

# CANNOT contain:
- Business logic
- Classes
- Functions (except simple getters)
- Imports from other ybis modules
```

### 3.2 `contracts/`
```python
# CAN contain:
- Pydantic models
- TypedDict definitions
- Enums
- Type aliases
- Validation logic

# CANNOT contain:
- Business logic
- Database operations
- External API calls
```

### 3.3 `syscalls/`
```python
# CAN contain:
- Guarded filesystem operations
- Guarded command execution
- Guarded git operations
- Journal event emission

# CANNOT contain:
- Business logic
- Direct external API calls
- Orchestration logic
```

### 3.4 `data_plane/`
```python
# CAN contain:
- Vector store operations
- Git worktree management
- File evidence operations

# CANNOT contain:
- Task/run coordination
- Business logic
- Direct LLM calls
```

### 3.5 `control_plane/`
```python
# CAN contain:
- Database operations
- Lease management
- Worker coordination
- Task/run state

# CANNOT contain:
- Execution logic
- File operations (except DB)
- External API calls
```

### 3.6 `services/`
```python
# CAN contain:
- Policy management
- Health monitoring
- Event bus
- MCP tools
- Internal services

# CANNOT contain:
- Workflow orchestration
- Direct adapter instantiation
```

### 3.7 `adapters/`
```python
# CAN contain:
- Third-party integrations
- External tool wrappers
- LLM provider adapters

# CANNOT contain:
- Core business logic
- Workflow definitions
- State management
```

### 3.8 `orchestrator/`
```python
# CAN contain:
- LangGraph workflow
- Node implementations
- State transitions
- Routing logic

# CANNOT contain:
- Direct adapter creation (use registry)
- Database schema
- Syscall implementation
```

### 3.9 `workflows/`
```python
# CAN contain:
- Workflow YAML parsing
- Workflow execution
- Node registry
- Conditional routing

# CANNOT contain:
- Node implementations (they go in orchestrator)
- Adapter logic
```

---

## 4. Circular Import Prevention

### 4.1 Common Patterns

**Pattern 1: Protocol/Interface**
```python
# contracts/protocols.py
from typing import Protocol

class ExecutorProtocol(Protocol):
    async def execute(self, ctx: "RunContext", plan: "Plan") -> "ExecutorResult":
        ...

# orchestrator/planner.py
from ..contracts.protocols import ExecutorProtocol

class Planner:
    def __init__(self, executor: ExecutorProtocol):
        self.executor = executor
```

**Pattern 2: Lazy Import**
```python
# adapters/__init__.py
def get_aider_executor():
    from .aider import AiderExecutor
    return AiderExecutor
```

**Pattern 3: Type Checking Guard**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..orchestrator.planner import Planner

def some_function(planner: "Planner") -> None:
    ...
```

### 4.2 Detecting Circular Imports

```bash
# Check for circular imports
python -c "import ybis"  # Will fail if circular

# Use import-linter (recommended)
pip install import-linter
lint-imports
```

---

## 5. External Dependency Rules

### 5.1 Standard Library

```python
# Always OK
import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any
```

### 5.2 Core Dependencies (Always Available)

```python
# Pydantic - Data models
from pydantic import BaseModel

# LiteLLM - LLM abstraction
import litellm

# LangGraph - Workflow
from langgraph.graph import StateGraph
```

### 5.3 Optional Dependencies (Conditional Import)

```python
# WRONG - Will crash if not installed
from chromadb import Client

# RIGHT - Graceful degradation
try:
    from chromadb import Client
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    Client = None

def get_vector_store():
    if not CHROMA_AVAILABLE:
        raise RuntimeError("ChromaDB not installed")
    return Client()
```

### 5.4 Heavy Dependencies (Lazy Load)

```python
# WRONG - Slows startup
import torch  # Heavy!
import transformers  # Heavy!

# RIGHT - Lazy load
def get_embeddings():
    import torch  # Load only when needed
    from transformers import AutoModel
    ...
```

---

## 6. Import Style Guide

### 6.1 Import Order

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party
import litellm
from pydantic import BaseModel

# 3. Local - absolute
from ybis.constants import PROJECT_ROOT
from ybis.contracts.task import Task

# 4. Local - relative (within same package)
from .planner import Planner
from ..services.policy import PolicyProvider
```

### 6.2 Import Grouping

```python
# Group related imports
from ybis.contracts.task import Task, TaskStatus, TaskPriority
from ybis.contracts.run import Run, RunStatus

# NOT like this (too scattered)
from ybis.contracts.task import Task
from ybis.contracts.run import Run
from ybis.contracts.task import TaskStatus
from ybis.contracts.run import RunStatus
```

### 6.3 Wildcard Imports

```python
# YASAK
from ybis.contracts import *

# DOĞRU
from ybis.contracts import Task, Run, Plan
```

---

## 7. Boundary Violations

### 7.1 How to Detect

```python
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/seddonym/import-linter
    rev: v2.0
    hooks:
      - id: import-linter
```

```toml
# pyproject.toml
[tool.importlinter]
root_package = "ybis"

[[tool.importlinter.contracts]]
name = "Syscalls cannot import from orchestrator"
type = "forbidden"
source_modules = ["ybis.syscalls"]
forbidden_modules = ["ybis.orchestrator", "ybis.workflows"]

[[tool.importlinter.contracts]]
name = "Adapters cannot import from orchestrator"
type = "forbidden"
source_modules = ["ybis.adapters"]
forbidden_modules = ["ybis.orchestrator"]
```

### 7.2 Consequences of Violation

| Violation | Consequence |
|-----------|-------------|
| Upward import | CI fails |
| Circular import | CI fails |
| Wildcard import | Lint warning |
| Missing lazy load | Review comment |

---

## 8. Refactoring Guide

### 8.1 When You Need an Upward Import

If you think you need to import from a higher layer:

1. **Question the design:** Maybe the code belongs elsewhere
2. **Use Protocol:** Define interface in contracts/
3. **Use Dependency Injection:** Pass the dependency
4. **Use Registry:** Get adapter from registry

### 8.2 Example Refactoring

```python
# BEFORE - orchestrator imports from adapters directly
# orchestrator/graph.py
from ..adapters.local_coder import LocalCoderExecutor

executor = LocalCoderExecutor()  # Hard dependency!

# AFTER - orchestrator uses registry
# orchestrator/graph.py
from ..adapters.registry import get_registry

registry = get_registry()
executor = registry.get("local_coder", "executor")  # Pluggable!
```

---

## 9. Module Checklist

Before adding imports to a module:

- [ ] Is this import from an allowed layer?
- [ ] Will this create a circular dependency?
- [ ] Is this a heavy dependency that should be lazy-loaded?
- [ ] Is this an optional dependency with graceful fallback?
- [ ] Am I importing only what I need (no wildcards)?
- [ ] Is the import grouped and ordered correctly?
