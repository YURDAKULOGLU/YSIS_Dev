# Core Boundary Refactor Plan

## Overview

Core modules currently have direct adapter/service imports that violate the core boundary. These must be refactored to use the adapter registry pattern.

## Violations Detected

Lint detected the following violations:

1. **src/ybis/syscalls/exec.py:92** - `from ..adapters.e2b_sandbox import E2BSandboxAdapter`
2. **src/ybis/orchestrator/graph.py:120** - `from ..services.resilience import ...`
3. **src/ybis/orchestrator/graph.py:274,322,346** - `from ..adapters import ...`
4. **src/ybis/orchestrator/graph.py:616** - `from ..services.lesson_engine import ...`
5. **src/ybis/orchestrator/graph.py:664** - `from ..services.debate import ...`
6. **src/ybis/orchestrator/planner.py:12** - `from ..adapters.llamaindex_adapter import ...`
7. **src/ybis/orchestrator/planner.py:16** - `from ..services.code_graph import ...`
8. **src/ybis/orchestrator/planner.py:120** - `from ..services.resilience import ...`
9. **src/ybis/orchestrator/planner.py:248** - `from ..services.knowledge import ...`

## Refactoring Strategy

### 1. Adapter Imports → Registry Pattern

**Before:**
```python
from ..adapters import AiderExecutor
executor = AiderExecutor()
```

**After:**
```python
from ..adapters.registry import get_registry

registry = get_registry()
executor = registry.get("aider", adapter_type="executor")
if executor is None:
    # Fallback to default
    executor = registry.get("local_coder", adapter_type="executor")
```

### 2. Service Imports → Dependency Injection

**Before:**
```python
from ..services.resilience import ResilienceEngine
engine = ResilienceEngine()
```

**After:**
```python
# Pass service as parameter or use registry
def some_function(resilience_engine=None):
    if resilience_engine is None:
        from ..services.resilience import ResilienceEngine
        resilience_engine = ResilienceEngine()
    # Use engine
```

Or use service registry (to be implemented):
```python
from ..services.service_registry import get_service

resilience_engine = get_service("resilience")
```

## Implementation Steps

1. **Create Service Registry** (similar to adapter registry)
   - `src/ybis/services/service_registry.py`
   - Register core services (resilience, debate, lesson_engine, etc.)

2. **Refactor syscalls/exec.py**
   - Replace direct E2BSandboxAdapter import with registry.get("e2b_sandbox")

3. **Refactor orchestrator/graph.py**
   - Replace adapter imports with registry pattern
   - Replace service imports with service registry or DI

4. **Refactor orchestrator/planner.py**
   - Replace adapter/service imports with registry pattern

5. **Update Tests**
   - Mock registry in tests
   - Test fallback behavior

## Priority

- **High**: `syscalls/exec.py` (core enforcement boundary)
- **High**: `orchestrator/graph.py` (main workflow)
- **Medium**: `orchestrator/planner.py` (planning logic)

## Notes

- Some services (like `policy.py`) are considered core and can be imported directly
- Registry pattern allows graceful fallback when adapters are disabled
- Service registry pattern will be similar to adapter registry


