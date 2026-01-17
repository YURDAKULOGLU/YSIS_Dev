# Chroma Vector Store Adapter

References:
- ../adapters/README.md
- ../../configs/adapters.yaml

**Type:** Vector Store Adapter  
**Maturity:** Beta  
**Default Enabled:** No

## Overview
ChromaDB provides local vector storage for embeddings and similarity search.

## Installation
```bash
pip install -e ".[adapters-chroma]"
```

## Configuration
```yaml
adapters:
  chroma_vector_store:
    enabled: true
```

## Notes
- Local-first; no external API key required.
- Use with LlamaIndex for RAG pipelines.
