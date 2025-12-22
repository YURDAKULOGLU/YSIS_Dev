# MEM0 FULL CONFIGURATION GUIDE (LOCAL SETUP)

Based on official documentation searches (2025-12-22).

## 1. LLM (Ollama)
```python
"llm": {
    "provider": "ollama",
    "config": {
        "model": "qwen2.5-coder:32b",
        "temperature": 0.1,
        "max_tokens": 2000,
        "ollama_base_url": "http://localhost:11434"  # CRITICAL: Not 'base_url'
    }
}
```

## 2. Vector Store (Chroma)
```python
"vector_store": {
    "provider": "chroma",
    "config": {
        "collection_name": "ybis_mem0",
        "path": "Knowledge/LocalDB/chroma_db",
        # Optional: "host": "localhost", "port": 8000 (if running server)
    }
}
```

## 3. Embedder (HuggingFace Local)
```python
"embedder": {
    "provider": "huggingface",
    "config": {
        "model": "all-MiniLM-L6-v2"
        # Optional: "embedding_dims": 384
    }
}
```

## 4. Embedder (Ollama Local)
Alternative if you want everything on Ollama:
```python
"embedder": {
    "provider": "ollama",
    "config": {
        "model": "nomic-embed-text",
        "ollama_base_url": "http://localhost:11434"
    }
}
```
