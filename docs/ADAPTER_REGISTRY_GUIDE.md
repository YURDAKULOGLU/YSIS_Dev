# Adapter Registry Guide

## Overview

The adapter registry provides a policy-driven mechanism for managing external tool integrations. All adapters must be registered and enabled via policy configuration.

## Policy Configuration

Adapters are configured in policy profiles (`configs/profiles/*.yaml`):

```yaml
adapters:
  local_coder:
    enabled: true  # Default executor (always enabled)
  aider:
    enabled: false  # Optional executor
  e2b_sandbox:
    enabled: true  # Sandbox adapter
  neo4j_graph:
    enabled: false  # Graph store adapter
```

## Default Adapter List

### Executor Adapters
- **local_coder**: Default executor using Ollama (always enabled)
- **aider**: Aider-based code generation (optional)

### Sandbox Adapters
- **e2b_sandbox**: E2B cloud sandbox (optional, requires E2B_API_KEY)
- **local**: Built-in local subprocess sandbox (always available)

### Vector Store Adapters
- **chroma_vector_store**: ChromaDB integration (optional)
- **qdrant_vector_store**: Qdrant integration (optional)

### Graph Store Adapters
- **neo4j_graph**: Neo4j graph database (optional)

### LLM Adapters
- **llamaindex_adapter**: LlamaIndex integration (optional)

## Profile Defaults

### default.yaml
- `local_coder`: enabled
- `e2b_sandbox`: enabled (if sandbox.type is "e2b")
- All other adapters: disabled (opt-in)

### e2e.yaml
- `local_coder`: enabled
- All other adapters: disabled (minimal for testing)

### strict.yaml
- `local_coder`: enabled
- All optional adapters: disabled (maximum security)

## Using Adapters in Code

**❌ Wrong (Direct Import):**
```python
from ..adapters import AiderExecutor
executor = AiderExecutor()
```

**✅ Correct (Registry Pattern):**
```python
from ..adapters.registry import get_registry

registry = get_registry()
executor = registry.get("aider", adapter_type="executor")
if executor is None:
    # Fallback to default
    executor = registry.get("local_coder", adapter_type="executor")
```

## Bootstrap

Adapters are automatically registered during system initialization via `bootstrap_adapters()` in `src/ybis/services/adapter_bootstrap.py`.

## Validation

Use `validate_required_adapters()` to check that required adapters are available:

```python
from ..services.adapter_bootstrap import validate_required_adapters

missing = validate_required_adapters(["aider", "neo4j_graph"])
if missing:
    raise RuntimeError(f"Required adapters not available: {missing}")
```


