# Qdrant Vector Store Adapter

References:
- ../adapters/README.md
- ../../configs/adapters.yaml

**Type:** Vector Store Adapter  
**Maturity:** Beta  
**Default Enabled:** No

## Overview
Qdrant provides a vector database with optional remote deployments.

## Installation
```bash
pip install -e ".[adapters-qdrant]"
```

## Configuration
```yaml
adapters:
  qdrant_vector_store:
    enabled: true
```

## Notes
- Local Qdrant can run without API keys.
- Cloud Qdrant requires API keys (avoid if local-only policy).
