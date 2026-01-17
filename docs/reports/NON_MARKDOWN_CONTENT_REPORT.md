# Non-Markdown Content Report - Organs Documentation

**Date:** 2025-01-04  
**Status:** ✅ COMPLETED

## Overview

Markdown dosyaları dışında organların içinde bulunan tüm dokümantasyon ve öğrenme materyalleri.

## Content Types Found

### 1. Jupyter Notebooks (.ipynb) 📓
**Count:** 500+ notebooks

**Locations:**
- `autogen/python/docs/` - 50+ tutorial notebooks
- `dspy/docs/docs/tutorials/` - 20+ tutorial notebooks
- `embedchain/` - 30+ integration notebooks
- `EvoAgentX/docs/ColabNotebook/` - 16 tutorial notebooks (EN + ZH)
- `gpt-researcher/docs/` - Example notebooks
- `langroid/examples/` - Quick start notebooks
- `llamaindex/docs/examples/` - **200+ example notebooks** (agents, RAG, embeddings, vector stores, etc.)
- `mlflow/docs/` - 30+ tutorial notebooks
- `open-interpreter/examples/` - 10+ demo notebooks
- `semantic-kernel/` - 20+ getting started notebooks

**Content:**
- Tutorials and quick starts
- Integration examples
- API usage examples
- Cookbooks and recipes
- Multi-modal examples

### 2. ReStructuredText (.rst) 📄
**Count:** 100+ RST files

**Locations:**
- `mlflow/docs/api_reference/source/` - Complete API reference in RST format
- `agentforge/` - Some RST documentation

**Content:**
- Sphinx-based API documentation
- Complete Python API references
- REST API documentation

### 3. HTML Files (.html) 🌐
**Count:** 200+ HTML files

**Locations:**
- `agent-zero/webui/` - Complete web UI templates
- `autogen/python/docs/src/_templates/` - Documentation templates
- `babyagi/babyagi/dashboard/templates/` - Dashboard templates
- `chatdev/visualizer/static/` - Visualization tools
- `flowise/packages/ui/` - UI components
- `gpt-researcher/frontend/` - Frontend templates
- `llamaindex/docs/examples/` - Example HTML outputs
- `microsoft-agent-framework/python/packages/devui/` - Dev UI

**Content:**
- Web UI templates
- Dashboard interfaces
- Documentation templates
- Example outputs
- Visualization tools

### 4. PDF Files (.pdf) 📑
**Count:** 30+ PDF files

**Locations:**
- `autogen/dotnet/samples/dev-team/seed-memory/` - Sample PDFs
- `chatdev/MultiAgentEbook/images/` - E-book PDFs
- `EvoAgentX/examples/output/` - Generated PDF reports
- `gpt-researcher/tests/docs/` - Test PDFs
- `langroid/examples/extract/` - Sample PDFs for extraction
- `llamaindex/docs/examples/data/` - Sample 10K/10Q PDFs
- `memgpt/examples/notebooks/data/` - Handbook PDF
- `metagpt/docs/resources/workspace/` - Design PDFs
- `semantic-kernel/docs/code_maps/` - Code map PDFs

**Content:**
- Sample documents for testing
- Generated reports
- Design documents
- E-books
- Code maps

### 5. Examples Directories 📁
**Count:** 100+ example directories

**Major Example Collections:**
- `aiwaves-agents/examples/`
- `autogen/python/packages/autogen-ext/examples/`
- `babyagi/examples/`
- `chatdev/` - Complete software projects
- `embedchain/examples/` - Multiple integration examples
- `EvoAgentX/examples/` - Workflow examples
- `langroid/examples/` - Quick start examples
- `llama-agents/examples/` - Agent examples
- `llamaindex/docs/examples/` - **Massive collection** (agents, RAG, embeddings, vector stores, workflows)
- `memgpt/examples/` - Memory examples
- `metagpt/examples/` - Software development examples
- `mlflow/examples/` - ML tracking examples
- `open-interpreter/examples/` - OS control examples
- `opendevin/evaluation/benchmarks/` - Benchmark examples
- `reactive-agents/reactive_agents/examples/`

**Content:**
- Complete working examples
- Integration patterns
- Use case demonstrations
- Benchmark datasets
- Test projects

### 6. API Reference Directories 📚
**Count:** 50+ API directories

**Locations:**
- `agent-zero/python/api/`
- `agentforge/agentforge/api/`
- `autogen/dotnet/src/AutoGen/API/`
- `babyagi/babyagi/api/`
- `dspy/docs/docs/api/`
- `EvoAgentX/docs/api/`
- `gpt-researcher/docs/docs/reference/`
- `langfuse/web/src/app/api/`
- `mlflow/docs/api_reference/` - **Complete API reference**

**Content:**
- API endpoint definitions
- SDK documentation
- REST API specs
- Client libraries

### 7. Tutorials & Guides 📖
**Count:** 30+ tutorial directories

**Locations:**
- `auto-claude/guides/`
- `autogpt/classic/forge/tutorials/`
- `dspy/docs/docs/tutorials/`
- `gpt-researcher/docs/docs/gpt-researcher/getting-started/`
- `langroid/docs/tutorials/`
- `mlflow/docs/docs/classic-ml/tracking/tutorials/`
- `open-interpreter/docs/guides/`
- `open-interpreter/docs/getting-started/`

**Content:**
- Step-by-step guides
- Getting started tutorials
- Best practices
- Integration guides

### 8. Configuration Files ⚙️
**Types:** JSON, YAML, TOML

**Content:**
- Example configurations
- Schema definitions
- Integration configs
- Environment setups

## Summary Statistics

| Content Type | Count | Primary Use |
|-------------|-------|-------------|
| **Jupyter Notebooks** | 500+ | Tutorials, examples, cookbooks |
| **RST Files** | 100+ | API documentation (Sphinx) |
| **HTML Files** | 200+ | Web UIs, dashboards, templates |
| **PDF Files** | 30+ | Sample documents, reports, e-books |
| **Example Directories** | 100+ | Working code examples |
| **API Directories** | 50+ | API references, SDK docs |
| **Tutorial Directories** | 30+ | Step-by-step guides |

## Key Findings

### Most Comprehensive Documentation

1. **LlamaIndex** 🏆
   - 200+ Jupyter notebooks
   - Complete examples for every feature
   - Extensive API documentation

2. **AutoGen**
   - 50+ tutorial notebooks
   - Complete Python and .NET docs
   - Multiple example patterns

3. **MLflow**
   - Complete RST-based API reference
   - 30+ tutorial notebooks
   - Comprehensive guides

4. **EvoAgentX**
   - 16 tutorial notebooks (bilingual)
   - Complete API docs
   - Workflow examples

### Rich Example Collections

- **ChatDev**: Complete software projects (HTML games, websites)
- **MetaGPT**: Full software development examples
- **Embedchain**: Multiple integration patterns
- **Langroid**: Quick start examples with notebooks

### Web UI Resources

- **Agent-Zero**: Complete web UI template system
- **Flowise**: Full UI package
- **BabyAGI**: Dashboard templates
- **GPT-Researcher**: Frontend templates

## Recommendations

1. **Notebooks**: Convert key notebooks to markdown tutorials
2. **API Docs**: Extract API references from RST files
3. **Examples**: Index all example directories
4. **PDFs**: Use as test data for document processing
5. **HTML**: Reference for UI component patterns

---

**Total Non-MD Content:** 1000+ files  
**Most Valuable:** Jupyter Notebooks (500+)  
**Best Organized:** LlamaIndex, AutoGen, MLflow

