# Adapter Documentation

This directory contains usage guides and examples for each YBIS adapter.

## Available Adapters

### Executor Adapters

- **[local_coder.md](local_coder.md)** - Native Ollama-based code executor (Stable, Default)
- **[aider.md](aider.md)** - Aider-based executor with advanced editing (Beta, Optional)

### Sandbox Adapters

- **[e2b_sandbox.md](e2b_sandbox.md)** - E2B cloud sandbox for isolated execution (Stable, Optional)

### Vector Store Adapters

- **[chroma_vector_store.md](chroma_vector_store.md)** - ChromaDB vector store (Beta, Optional)
- **[qdrant_vector_store.md](qdrant_vector_store.md)** - Qdrant vector store (Beta, Optional)

### Graph Store Adapters

- **[neo4j_graph.md](neo4j_graph.md)** - Neo4j graph database for dependency tracking (Beta, Optional)

### LLM Adapters

- **[llamaindex_adapter.md](llamaindex_adapter.md)** - LlamaIndex integration (Beta, Optional)

### Event Bus Adapters

- **[redis_event_bus.md](redis_event_bus.md)** - Redis event bus (Stable, Optional)

## Quick Start

1. **Check Adapter Catalog:**
   ```bash
   cat configs/adapters.yaml
   ```

2. **Enable Adapter in Policy:**
   ```yaml
   # configs/profiles/default.yaml
   adapters:
     adapter_name:
       enabled: true
   ```

3. **Install Dependencies:**
   ```bash
   # Install specific adapter
   pip install -e ".[adapters-chroma]"
   
   # Or install all adapters
   pip install -e ".[all-adapters]"
   ```

4. **Verify Adapter:**
   ```python
   from src.ybis.adapters.registry import get_registry
   from src.ybis.services.adapter_bootstrap import bootstrap_adapters
   
   bootstrap_adapters()
   registry = get_registry()
   adapter = registry.get("adapter_name")
   
   if adapter and adapter.is_available():
       print("Adapter is ready!")
   ```

## Adding a New Adapter

See [Adapter Registry Guide](../ADAPTER_REGISTRY_GUIDE.md) for instructions on adding a new adapter.

## Related Documentation

- [Adapter Catalog](../../configs/adapters.yaml) - Source of truth for all adapters
- [Adapter Registry Guide](../ADAPTER_REGISTRY_GUIDE.md) - How to use the adapter registry
- [Lifecycle Policy](LIFECYCLE_POLICY.md) - Adapter deprecation and versioning
- [Adapter Conformance Tests](../../tests/adapters/) - Test suite for adapters


