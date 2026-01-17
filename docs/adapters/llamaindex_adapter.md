# LlamaIndex Adapter

**Type:** LLM Adapter  
**Maturity:** Beta  
**Default Enabled:** No

## Overview

LlamaIndex Adapter provides integration with the LlamaIndex framework for advanced RAG (Retrieval-Augmented Generation) and context management. It enables sophisticated document indexing, querying, and context injection for LLM calls.

## Features

- ✅ Document indexing and retrieval
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Context management
- ✅ Vector store integration
- ✅ Query engines

## Installation

### Prerequisites

1. **Python Package:** Install LlamaIndex dependencies

```bash
# Install adapter dependencies
pip install -e ".[adapters-llamaindex]"

# Or install directly
pip install "llama-index>=0.10.0,<0.11.0"
pip install "llama-index-core>=0.10.0,<0.11.0"
```

## Configuration

### Policy Configuration

```yaml
# configs/profiles/default.yaml
adapters:
  llamaindex_adapter:
    enabled: true  # Enable LlamaIndex adapter
```

### Environment Variables

```bash
# Optional: LlamaIndex-specific configuration
export LLAMA_INDEX_CACHE_DIR="/path/to/cache"
```

## Usage

### Via Adapter Registry

```python
from src.ybis.adapters.registry import get_registry
from src.ybis.services.adapter_bootstrap import bootstrap_adapters

bootstrap_adapters()
registry = get_registry()
adapter = registry.get("llamaindex_adapter")

if adapter and adapter.is_available():
    # Use LlamaIndex adapter
    # (Implementation details depend on adapter interface)
    pass
```

### Direct Usage

```python
from src.ybis.adapters.llamaindex_adapter import LlamaIndexAdapter

adapter = LlamaIndexAdapter()
if adapter.is_available():
    # Use adapter for RAG operations
    # (Implementation details depend on adapter interface)
    pass
```

## Capabilities

- **Document Indexing:** Index documents for semantic search
- **RAG:** Retrieve relevant context for LLM calls
- **Context Management:** Manage and inject context into prompts
- **Query Engines:** Build query engines for specific use cases

## Limitations

- Requires LlamaIndex installation
- Beta maturity (may have limitations)
- May require vector store adapter (Chroma, Qdrant) for full functionality

## Integration with Vector Stores

LlamaIndex adapter can work with vector store adapters:

```yaml
# configs/profiles/default.yaml
adapters:
  llamaindex_adapter:
    enabled: true
  chroma_vector_store:  # Or qdrant_vector_store
    enabled: true
```

## Troubleshooting

### Import Errors

**Error:** `ImportError: No module named 'llama_index'`

**Solution:**
```bash
pip install "llama-index>=0.10.0,<0.11.0"
```

### Vector Store Not Found

**Error:** Vector store adapter not available

**Solution:**
- Enable a vector store adapter (Chroma or Qdrant)
- Ensure vector store dependencies are installed

## See Also

- [Adapter Catalog](../../configs/adapters.yaml)
- [Vector Store Adapters](chroma_vector_store.md)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)


