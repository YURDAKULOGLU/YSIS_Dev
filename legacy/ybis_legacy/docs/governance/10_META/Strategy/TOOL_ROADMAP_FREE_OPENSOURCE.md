# Tool Integration Roadmap (Free & Open-Source Only)

> **Strategic plan for plugin ecosystem - zero proprietary dependencies**

**Constraint:** All tools must be free, open-source, and self-hostable
**Philosophy:** Incremental dogfooding (use X to build Y)

---

## [TARGET] Framework Selection (Already Installed)

| Framework | License | Purpose | Status |
|-----------|---------|---------|--------|
| **LangGraph** | MIT | Workflow orchestration | [OK] Installed |
| **LangChain** | MIT | Tool ecosystem | [OK] Installed |
| **CrewAI** | MIT | Multi-agent | [OK] Installed |
| **ChromaDB** | Apache 2.0 | Vector store | [OK] Installed |
| **FastMCP** | MIT | MCP server | [OK] Installed |

---

## 📋 Tool Roadmap (Priority Order)

### Phase 1: Infrastructure (T-102)

#### 1.1 Plugin Core
**Build ourselves** (<500 lines)
- `ToolProtocol` interface
- `ToolRegistry` central registry
- `PluginLoader` auto-discovery

**Dependencies:** Python stdlib only
**Dogfooding:** N/A (foundation)

---

#### 1.2 LangFuse (Observability)
**Alternative to:** LangSmith (proprietary)
**License:** MIT
**Self-hosted:** [OK] Yes (Docker)

**What:**
- Trace all tool calls
- Track costs
- Monitor latency
- Debug workflows

**Setup:**
```bash
docker-compose up langfuse
# PostgreSQL + Next.js app
```

**Integration:**
```python
from langfuse import Langfuse

langfuse = Langfuse(host="http://localhost:3000")

@langfuse.observe()
async def invoke_tool(name, **kwargs):
    return await ToolRegistry.invoke(name, **kwargs)
```

**Cost:** Free (self-hosted)
**Dogfooding:** Track T-102 execution

---

#### 1.3 LiteLLM (LLM Proxy)
**License:** MIT
**Self-hosted:** [OK] Yes

**What:**
- Universal LLM interface (Ollama, OpenAI, Anthropic)
- Fallback & load balancing
- Cost tracking
- Caching

**Setup:**
```bash
# Local proxy
litellm --config litellm_config.yaml
```

**Config:**
```yaml
model_list:
  - model_name: main
    litellm_params:
      model: ollama/qwen2.5:32b
  - model_name: fallback
    litellm_params:
      model: ollama/qwen2.5:14b
```

**Cost:** Free
**Dogfooding:** Use for SimplePlanner LLM calls

---

### Phase 2: Deterministic Tools (T-103)

#### 2.1 LangChain Community Tools
**License:** MIT
**What's included:**
- File operations (read/write/search)
- Shell commands
- Calculator
- Wikipedia
- DuckDuckGo search (free!)
- Git operations

**Already installed:** [OK] Yes
**Count:** 50+ tools

**Integration:**
```python
from langchain_community.tools import (
    FileManagementToolkit,
    ShellTool,
    WikipediaQueryRun,
    DuckDuckGoSearchRun
)

# Wrap as plugins
ToolRegistry.register("@langchain/file", FileManagementToolkit())
ToolRegistry.register("@langchain/shell", ShellTool())
ToolRegistry.register("@langchain/wiki", WikipediaQueryRun())
ToolRegistry.register("@langchain/search", DuckDuckGoSearchRun())
```

**Cost:** Free
**Dogfooding:** Use @langchain/file to read/write T-103 artifacts

---

#### 2.2 MCP Servers (Anthropic)
**License:** MIT
**Self-hosted:** [OK] Yes (local processes)

**Available servers:**
- `@modelcontextprotocol/server-filesystem` (file ops)
- `@modelcontextprotocol/server-postgres` (DB)
- `@modelcontextprotocol/server-github` (Git)
- `@modelcontextprotocol/server-puppeteer` (web scraping)

**Setup:**
```bash
# Install MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-github
```

**Integration:**
```python
from mcp import MCPServer

# Start server
mcp = MCPServer("filesystem", "mcp-server-filesystem /allowed/path")

# Auto-discover tools
for tool in mcp.list_tools():
    ToolRegistry.register(f"@mcp/{tool.name}", tool)
```

**Cost:** Free
**Dogfooding:** Use @mcp/filesystem for safe file operations

---

### Phase 3: AI Tools (T-104)

#### 3.1 CrewAI Tools
**License:** MIT
**Already installed:** [OK] Yes

**Tools included:**
- Code analysis
- File search (semantic)
- Web scraping
- JSON search
- CSV operations

**Integration:**
```python
from crewai_tools import (
    CodeAnalysisTool,
    FileReadTool,
    DirectoryReadTool,
    WebsiteSearchTool
)

ToolRegistry.register("@crewai/code-analysis", CodeAnalysisTool())
ToolRegistry.register("@crewai/file-read", FileReadTool())
ToolRegistry.register("@crewai/web-scrape", WebsiteSearchTool())
```

**Cost:** Free
**Dogfooding:** Use @crewai/code-analysis to analyze OrchestratorGraph

---

#### 3.2 Aider as Plugin
**License:** Apache 2.0
**Already used:** [OK] Yes (hard-coded)

**Refactor:**
```python
class AiderPlugin(ToolProtocol):
    name = "@aider/code-gen"
    deterministic = False

    async def invoke(self, task: str, files: List[str]):
        executor = AiderExecutor()
        return await executor.execute(task, files)
```

**Cost:** Free (uses local LLM)
**Dogfooding:** Use other tools to prepare Aider inputs

---

### Phase 4: Advanced Tools (T-105)

#### 4.1 Playwright (Web Automation)
**Alternative to:** Firecrawl (proprietary)
**License:** Apache 2.0

**What:**
- Web scraping
- Browser automation
- Screenshot capture
- PDF generation

**Setup:**
```bash
pip install playwright
playwright install
```

**Integration:**
```python
from playwright.async_api import async_playwright

class PlaywrightTool(ToolProtocol):
    async def invoke(self, url: str, action: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            return content

ToolRegistry.register("@playwright/scrape", PlaywrightTool())
```

**Cost:** Free
**Dogfooding:** Scrape documentation for research tasks

---

#### 4.2 SearxNG (Privacy Search)
**Alternative to:** Tavily (proprietary)
**License:** AGPLv3
**Self-hosted:** [OK] Yes (Docker)

**What:**
- Meta-search engine
- No tracking
- Aggregates Google, Bing, DuckDuckGo
- JSON API

**Setup:**
```bash
docker run -d -p 8080:8080 searxng/searxng
```

**Integration:**
```python
import httpx

class SearxNGTool(ToolProtocol):
    async def invoke(self, query: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "http://localhost:8080/search",
                params={"q": query, "format": "json"}
            )
            return r.json()

ToolRegistry.register("@searxng/search", SearxNGTool())
```

**Cost:** Free (self-hosted)
**Dogfooding:** Research best practices for T-106

---

#### 4.3 Docker (Sandbox)
**Alternative to:** E2B (cloud, proprietary)
**License:** Apache 2.0

**What:**
- Isolated code execution
- Multi-language support
- Resource limits

**Integration:**
```python
import docker

class DockerSandbox(ToolProtocol):
    async def invoke(self, code: str, language: str):
        client = docker.from_env()
        container = client.containers.run(
            image=f"{language}:latest",
            command=["python", "-c", code],
            detach=True,
            mem_limit="512m",
            network_disabled=True
        )
        logs = container.logs()
        container.remove()
        return logs

ToolRegistry.register("@docker/sandbox", DockerSandbox())
```

**Cost:** Free
**Dogfooding:** Run Aider in sandbox for safety

---

### Phase 5: Memory & Learning (T-106)

#### 5.1 mem0 (Memory Management)
**License:** Apache 2.0
**Self-hosted:** [OK] Yes

**What:**
- Long-term agent memory
- Context persistence
- Automatic summarization

**Setup:**
```bash
pip install mem0ai
```

**Integration:**
```python
from mem0 import Memory

memory = Memory()

ToolRegistry.register("@mem0/remember", MemoryTool(memory, action="add"))
ToolRegistry.register("@mem0/recall", MemoryTool(memory, action="search"))
```

**Cost:** Free (local vector DB)
**Dogfooding:** Remember T-106 decisions for future tasks

---

#### 5.2 Weights & Biases (Experiment Tracking)
**License:** Apache 2.0 (client)
**Self-hosted:** [WARN]️ Partial (client open-source, server proprietary)

**Alternative:** **MLflow** (fully open-source)
**License:** Apache 2.0
**Self-hosted:** [OK] Yes

**What:**
- Experiment tracking
- Metric visualization
- Model versioning

**Setup:**
```bash
pip install mlflow
mlflow server --host 0.0.0.0
```

**Integration:**
```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run():
    mlflow.log_metric("test_coverage", 0.85)
    mlflow.log_metric("retry_count", 2)
```

**Cost:** Free (self-hosted)
**Dogfooding:** Track T-106 metrics

---

## 🗺️ Execution Roadmap

### T-102: Plugin Core + Infrastructure (P0)
**Duration:** 1-2 days
**Deliverables:**
- Plugin architecture (ToolProtocol, Registry, Loader)
- LangFuse integration (observability)
- LiteLLM integration (LLM proxy)

**Dogfooding:** Track T-102 with LangFuse

---

### T-103: LangChain + MCP Tools (P0)
**Duration:** 1 day
**Deliverables:**
- LangChain Tools wrapped (50+ tools)
- MCP servers integrated (filesystem, github)

**Dogfooding:** Use @langchain/file for T-103 artifacts

---

### T-104: AI Tools (P1)
**Duration:** 1 day
**Deliverables:**
- CrewAI tools wrapped
- Aider plugin conversion

**Dogfooding:** Use @crewai/code-analysis to review T-104 code

---

### T-105: Advanced Tools (P1)
**Duration:** 2 days
**Deliverables:**
- Playwright integration (web scraping)
- SearxNG integration (search)
- Docker sandbox

**Dogfooding:** Scrape docs with Playwright for T-106 research

---

### T-106: Memory & Tracking (P2)
**Duration:** 1 day
**Deliverables:**
- mem0 integration
- MLflow tracking

**Dogfooding:** Track all T-106 experiments in MLflow

---

## [CHART] Tool Inventory (Free & Open-Source)

| Tool | Type | License | Self-Hosted | Deterministic | Cost |
|------|------|---------|-------------|---------------|------|
| **LangChain Tools** | Utilities | MIT | [OK] | [OK] | Free |
| **MCP Servers** | External | MIT | [OK] | [OK] | Free |
| **CrewAI Tools** | AI | MIT | [OK] | [WARN]️ | Free |
| **Aider** | Code Gen | Apache 2.0 | [OK] | [FAIL] | Free |
| **LangFuse** | Observability | MIT | [OK] | [OK] | Free |
| **LiteLLM** | LLM Proxy | MIT | [OK] | [OK] | Free |
| **Playwright** | Web | Apache 2.0 | [OK] | [OK] | Free |
| **SearxNG** | Search | AGPLv3 | [OK] | [WARN]️ | Free |
| **Docker** | Sandbox | Apache 2.0 | [OK] | [OK] | Free |
| **mem0** | Memory | Apache 2.0 | [OK] | [WARN]️ | Free |
| **MLflow** | Tracking | Apache 2.0 | [OK] | [OK] | Free |

**Total Tools:** 100+ (via LangChain + MCP + CrewAI)
**Total Cost:** $0
**Vendor Lock-in:** None

---

## [TARGET] Success Metrics

- [OK] Zero proprietary dependencies
- [OK] All tools self-hostable
- [OK] 100+ tools available via plugins
- [OK] Full observability (LangFuse)
- [OK] LLM abstraction (LiteLLM)
- [OK] Safe execution (Docker sandbox)
- [OK] Long-term memory (mem0)
- [OK] Experiment tracking (MLflow)

---

**Last Updated:** 2025-12-20
**Next Review:** After T-106 completion
