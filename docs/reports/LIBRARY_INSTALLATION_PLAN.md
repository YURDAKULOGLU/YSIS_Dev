# Library Installation Plan - Steward OroYstein

**Date:** 2025-01-04  
**Status:** 📋 READY TO INSTALL

## Already Installed ✅

- `ollama` (0.6.1) ✅
- `playwright` (1.57.0) ✅
- `qdrant-client` (1.16.2) ✅
- `langchain-ollama` (1.0.1) ✅

## To Install (Critical) 🔴

### 1. RAG & Vector Stores
```bash
pip install llama-index llama-index-core llama-index-llms-ollama llama-index-embeddings-huggingface
pip install weaviate-client faiss-cpu
```

**Why:**
- LlamaIndex: 200+ notebooks, comprehensive RAG patterns
- Weaviate: Alternative vector store
- FAISS: Local vector search

### 2. Document Processing
```bash
pip install unstructured pdfplumber pypdf python-docx openpyxl
```

**Why:**
- Unstructured: Universal document parser (30+ formats)
- PDF processing: Organlardaki PDF'leri işlemek için
- Office docs: Word, Excel support

### 3. Evaluation
```bash
pip install ragas trulens-eval
```

**Why:**
- Ragas: RAG evaluation standard
- Trulens: LLM evaluation framework

### 4. Prompt Engineering
```bash
pip install guidance outlines
```

**Why:**
- Guidance: Prompt programming
- Outlines: Structured generation

### 5. AI Engineering
```bash
pip install marvin pydantic-ai
```

**Why:**
- Marvin: AI engineering framework
- Pydantic-AI: Pydantic + AI integration

### 6. Additional LLM Providers
```bash
pip install cohere mistralai together groq huggingface-hub
```

**Why:**
- Model diversity
- Fallback options
- Local model support (HuggingFace)

### 7. Memory
```bash
pip install memgpt
```

**Why:**
- Long-term memory for agents
- Already in `organs/memgpt/`

### 8. Infrastructure
```bash
pip install redis hiredis aiohttp aiofiles
```

**Why:**
- Redis: Event bus, caching
- Async: Better async patterns

### 9. Monitoring
```bash
pip install prometheus-client opentelemetry-api opentelemetry-sdk
```

**Why:**
- Metrics collection
- Distributed tracing

## Installation Command (All at Once)

```bash
pip install \
  llama-index llama-index-core llama-index-llms-ollama llama-index-embeddings-huggingface \
  weaviate-client faiss-cpu \
  unstructured pdfplumber pypdf python-docx openpyxl \
  ragas trulens-eval \
  guidance outlines \
  marvin pydantic-ai \
  cohere mistralai together groq huggingface-hub \
  memgpt \
  redis hiredis \
  aiohttp aiofiles \
  prometheus-client opentelemetry-api opentelemetry-sdk
```

## Verification

After installation, verify with:
```python
import llama_index
import unstructured
import ragas
import guidance
import marvin
import memgpt
import redis
```

## Integration Points

### LlamaIndex
- **Location:** `organs/llamaindex/` (already cloned)
- **Use:** RAG pipelines, document indexing, query engines
- **Examples:** 200+ notebooks in `organs/llamaindex/docs/examples/`

### Unstructured
- **Use:** Parse PDFs, Word docs, HTML from organs
- **Formats:** 30+ document types

### Ragas
- **Use:** Evaluate RAG pipelines
- **Metrics:** Context precision, answer correctness, faithfulness

### MemGPT
- **Location:** `organs/memgpt/` (already cloned)
- **Use:** Long-term agent memory

---

**Total New Libraries:** ~25  
**Status:** Ready to install

