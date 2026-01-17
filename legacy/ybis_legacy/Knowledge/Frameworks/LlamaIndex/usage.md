# LlamaIndex Integration Guide (YBIS v5.0)

## Overview
LlamaIndex is our primary data framework for LLM applications. 
It connects external data (Knowledge/) to LLMs.

## Key Components
- **VectorStoreIndex:** Local search via Qdrant/Chroma.
- **QueryEngine:** Natural language interface to your data.
- **Workflows:** LangGraph-compatible stateful orchestration.

## Usage in YBIS
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('Knowledge/Context').load_data()
index = VectorStoreIndex.from_documents(documents)
```
