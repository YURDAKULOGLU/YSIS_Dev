# Library Recommendations for Steward OroYstein

**Date:** 2025-01-04  
**Status:** 📋 RECOMMENDATIONS

## Overview

Mevcut `requirements.txt`'e eklenebilecek kritik Python kütüphaneleri. Organlar (framework'ler) zaten indirildi, şimdi bunları kullanmak için gerekli library'leri ekliyoruz.

## Critical Missing Libraries

### 1. Vector Stores & RAG (High Priority) 🔴

**Current:** `chromadb` ✅

**Missing:**
```python
# Alternative vector stores
weaviate-client          # Weaviate vector database client
qdrant-client            # Qdrant vector database
pinecone-client          # Pinecone managed vector DB
faiss-cpu                # Facebook AI Similarity Search (local)
milvus                   # Milvus vector database
```

**RAG Frameworks:**
```python
llama-index              # 🏆 CRITICAL - Most comprehensive RAG framework
llama-index-core         # Core LlamaIndex
llama-index-llms-ollama  # Ollama integration
llama-index-embeddings   # Embedding integrations
haystack-ai              # Alternative RAG framework (Deepset)
```

**Why:** ChromaDB tek başına yeterli değil. LlamaIndex özellikle kritik çünkü 200+ notebook ve comprehensive RAG patterns içeriyor.

---

### 2. Local LLM Support (Critical) 🔴

**Current:** `langchain_ollama` ✅ (but no direct ollama client)

**Missing:**
```python
ollama                   # 🏆 CRITICAL - Direct Ollama client (local LLM)
vllm                     # vLLM for local model serving
text-generation-inference # HuggingFace TGI
```

**Why:** Local-first philosophy için Ollama client şart. `langchain_ollama` wrapper ama direct client daha esnek.

---

### 3. Additional LLM Providers (Medium Priority) 🟡

**Current:** `anthropic`, `openai`, `google-generativeai` ✅

**Missing:**
```python
cohere                   # Cohere API
mistralai                 # Mistral AI SDK
together                  # Together AI
groq                      # Groq (fast inference)
huggingface-hub          # HuggingFace models
```

**Why:** Model diversity ve fallback options için.

---

### 4. Document Processing (High Priority) 🔴

**Current:** `markdown-it-py`, `python-frontmatter` ✅

**Missing:**
```python
unstructured              # 🏆 CRITICAL - Universal document parser
pdfplumber                # PDF parsing
pypdf                     # PDF manipulation
python-docx               # Word document processing
openpyxl                  # Excel processing
pandoc                    # Document conversion
pypandoc                  # Pandoc Python wrapper
```

**Why:** Organlardaki PDF'leri ve dokümanları işlemek için gerekli.

---

### 5. Evaluation & Testing (High Priority) 🔴

**Current:** `pytest`, `pytest-asyncio` ✅

**Missing:**
```python
ragas                     # 🏆 RAG evaluation framework
trulens-eval              # LLM evaluation
langsmith                 # LangChain observability (optional, has free tier)
deepeval                  # Deep evaluation for LLM apps
uptrain                   # LLM evaluation platform
```

**Why:** RAG sistemlerini ve agent'ları evaluate etmek için kritik.

---

### 6. Prompt Engineering (Medium Priority) 🟡

**Current:** `instructor` ✅ (structured outputs)

**Missing:**
```python
guidance                  # Prompt programming framework
outlines                   # Structured generation
lm-format-enforcer        # Format enforcement
jsonformer                # JSON generation
```

**Why:** Daha iyi prompt engineering ve structured outputs için.

---

### 7. AI Engineering Tools (Medium Priority) 🟡

**Missing:**
```python
marvin                    # AI engineering framework
pydantic-ai               # Pydantic + AI integration
langchain-experimental    # Experimental LangChain features
```

**Why:** AI-first development patterns için.

---

### 8. Web Automation (Medium Priority) 🟡

**Current:** `selenium` ✅

**Missing:**
```python
playwright                # 🏆 Modern web automation (faster than Selenium)
beautifulsoup4            # ✅ Already in requirements
lxml                      # HTML/XML parsing (faster than bs4)
scrapy                    # Web scraping framework
```

**Why:** Playwright Selenium'dan daha modern ve hızlı.

---

### 9. Redis & Caching (Medium Priority) 🟡

**Current:** `celery[redis]` ✅ (but no direct redis client)

**Missing:**
```python
redis                     # Redis Python client
hiredis                   # Fast Redis parser
```

**Why:** Event bus ve caching için direct Redis client gerekli.

---

### 10. Code Analysis & AST (Low Priority) 🟢

**Current:** `tree-sitter`, `tree-sitter-language-pack` ✅

**Missing:**
```python
ast-grep                  # AST-based code search
rope                      # Python refactoring library
jedi                      # Python autocompletion
```

**Why:** Code analysis ve refactoring için.

---

### 11. Memory & Context Management (High Priority) 🔴

**Current:** `mem0ai` ✅

**Missing:**
```python
memgpt                    # MemGPT for long-term memory
langchain-memory          # LangChain memory components
```

**Why:** Organlarda MemGPT var, library olarak da eklenmeli.

---

### 12. Monitoring & Observability (Medium Priority) 🟡

**Current:** `langfuse`, `loguru` ✅

**Missing:**
```python
prometheus-client         # Prometheus metrics
opentelemetry-api         # OpenTelemetry
opentelemetry-sdk         # OpenTelemetry SDK
```

**Why:** System monitoring ve metrics için.

---

### 13. Data Processing (Low Priority) 🟢

**Missing:**
```python
pandas                    # Data manipulation (if not already used)
numpy                     # Numerical computing
pyarrow                   # Apache Arrow (for data interchange)
```

**Why:** Data processing ve analysis için.

---

### 14. Async & Concurrency (Low Priority) 🟢

**Current:** `asyncio` (stdlib), `aiosqlite` ✅

**Missing:**
```python
aiohttp                   # Async HTTP client
aiofiles                  # Async file operations
```

**Why:** Better async patterns için.

---

## Recommended Installation Order

### Phase 1: Critical (Install Now) 🔴
```bash
pip install ollama llama-index llama-index-core llama-index-llms-ollama
pip install unstructured pdfplumber pypdf
pip install ragas trulens-eval
pip install weaviate-client qdrant-client
pip install playwright
pip install redis
```

### Phase 2: High Value (Install Soon) 🟡
```bash
pip install guidance outlines
pip install marvin pydantic-ai
pip install cohere mistralai together groq
pip install memgpt
```

### Phase 3: Nice to Have (Install Later) 🟢
```bash
pip install haystack-ai
pip install deepeval uptrain
pip install ast-grep rope jedi
pip install prometheus-client opentelemetry-api opentelemetry-sdk
```

## Updated requirements.txt Suggestion

```python
# ============================================================================
# CRITICAL ADDITIONS (Phase 1)
# ============================================================================

# Local LLM
ollama

# RAG & Vector Stores
llama-index
llama-index-core
llama-index-llms-ollama
llama-index-embeddings
weaviate-client
qdrant-client
faiss-cpu

# Document Processing
unstructured
pdfplumber
pypdf
python-docx
openpyxl

# Evaluation
ragas
trulens-eval

# Web Automation
playwright

# Redis
redis
hiredis

# ============================================================================
# HIGH VALUE ADDITIONS (Phase 2)
# ============================================================================

# Prompt Engineering
guidance
outlines

# AI Engineering
marvin
pydantic-ai

# Additional LLM Providers
cohere
mistralai
together
groq
huggingface-hub

# Memory
memgpt

# ============================================================================
# NICE TO HAVE (Phase 3)
# ============================================================================

# Alternative RAG
haystack-ai

# Additional Evaluation
deepeval
uptrain

# Code Analysis
ast-grep
rope
jedi

# Monitoring
prometheus-client
opentelemetry-api
opentelemetry-sdk

# Data Processing
pandas
numpy
pyarrow

# Async
aiohttp
aiofiles
```

## Integration Notes

### LlamaIndex Integration
- **Why Critical:** 200+ notebooks, comprehensive RAG patterns
- **Use Cases:** Document indexing, query engines, agents
- **Location:** Already in `organs/llamaindex/`

### Ollama Integration
- **Why Critical:** Local-first philosophy
- **Use Cases:** Local LLM inference, model testing
- **Note:** `langchain_ollama` wrapper var ama direct client daha esnek

### Unstructured Integration
- **Why Critical:** Universal document parser
- **Use Cases:** PDF, Word, HTML, etc. parsing
- **Supports:** 30+ document types

### Ragas Integration
- **Why Critical:** RAG evaluation standard
- **Use Cases:** Evaluate RAG pipelines, measure quality
- **Metrics:** Context precision, answer correctness, etc.

---

## Summary

**Total New Libraries:** ~40  
**Critical (Phase 1):** 10  
**High Value (Phase 2):** 10  
**Nice to Have (Phase 3):** 20

**Most Critical:**
1. `ollama` - Local LLM support
2. `llama-index` - Comprehensive RAG
3. `unstructured` - Document processing
4. `ragas` - RAG evaluation
5. `playwright` - Modern web automation

---

**Recommendation:** Phase 1'i hemen ekle, Phase 2'yi ihtiyaç duydukça, Phase 3'ü optional olarak bırak.

