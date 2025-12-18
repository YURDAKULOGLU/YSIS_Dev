# YBIS Agentic Architecture Reorganization Plan
**Tarih:** 13 Aralık 2025  
**Amaç:** Kapalı Beta → Açık Beta geçişinde "Balta Bileme"  
**Durum:** Closed Beta ✅ → Organization Phase → Open Beta

---

## 1. Mevcut Durum Özeti

### 1.1 Gemini Analizi Kritik Bulgular

| Bileşen | Durum | Notlar |
|---------|-------|--------|
| Mobile App | ✅ Production-Ready | Port-Adapter pattern, Optimistic UI çalışıyor |
| Web App | ❌ Boş Kabuk | packages/ui izole, hızlı scaffold mümkün |
| Constitution | ✅ Var ama Gömülü | `.YBIS_Dev/Meta/Governance/Standards/1_Anayasa` |
| Agent Prompts | ✅ 50+ Prompt | `.YBIS_Dev/Veriler/commands/` |
| Workflows | ✅ 15+ YAML | `.YBIS_Dev/Veriler/workflows/` |
| Local Runner | ✅ Var | `scripts/local-agent-runner.ts` |
| Orchestrator | ❌ Kör | `AGENT_REGISTRY.json` ve `AI_AGENT_PROTOCOLS.md` YOK |
| RAG Tables | ✅ Supabase'de | Ama agent'lar erişemiyor |

### 1.2 Kritik Eksikler (Gemini'nin Tespit Ettiği)

1. **AGENT_REGISTRY.json** - Orchestrator'ın agent listesi
2. **AI_AGENT_PROTOCOLS.md** - Agent iletişim protokolleri
3. **Workflow Runner** - YAML'ları execute edecek engine
4. **RAG Tool** - Agent'ların knowledge base'e erişimi
5. **Feedback Loop** - Self-correction mekanizması

---

## 2. Önerilen Klasör Yapısı

### 2.1 Yeni `.YBIS_Dev/` Mimarisi

```
.YBIS_Dev/
│
├── 📁 Agentic/                      # 🔧 OTOMASYON MOTORU
│   │
│   ├── 📁 Core/                     # LangGraph Orchestrator
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # Ana state machine
│   │   ├── state.py                 # State type definitions
│   │   ├── 📁 graphs/               # Workflow graph implementations
│   │   │   ├── feature_dev.py       # Feature development flow
│   │   │   ├── code_review.py       # Code review cycle
│   │   │   ├── bug_fix.py           # Bug fix flow
│   │   │   └── handoff.py           # Agent handoff logic
│   │   └── 📁 nodes/                # Reusable graph nodes
│   │       ├── architect.py
│   │       ├── developer.py
│   │       ├── qa.py
│   │       └── reviewer.py
│   │
│   ├── 📁 Agents/                   # Agent Persona Definitions
│   │   ├── registry.json            # 🔴 KRITIK: AGENT_REGISTRY
│   │   ├── protocols.md             # 🔴 KRITIK: AI_AGENT_PROTOCOLS
│   │   └── 📁 personas/             # Individual agent prompts
│   │       ├── orchestrator.md
│   │       ├── architect.md
│   │       ├── developer.md
│   │       ├── qa-engineer.md
│   │       ├── code-reviewer.md
│   │       └── documentation.md
│   │
│   ├── 📁 Tools/                    # Tool Implementations
│   │   ├── __init__.py
│   │   ├── file_ops.py              # Read/Write/Search files
│   │   ├── git_ops.py               # Git operations
│   │   ├── code_exec.py             # Safe code execution
│   │   ├── rag_search.py            # 🔴 EKSIK: RAG tool
│   │   ├── test_runner.py           # Run tests
│   │   └── lint_check.py            # TSC, ESLint checks
│   │
│   ├── 📁 MCP/                      # Model Context Protocol
│   │   ├── README.md
│   │   ├── 📁 servers/              # MCP Server configs
│   │   │   ├── supabase.json
│   │   │   ├── filesystem.json
│   │   │   └── git.json
│   │   └── 📁 clients/              # MCP Client implementations
│   │       └── unified_client.py
│   │
│   └── 📁 Local/                    # 🖥️ RTX 5090 / Ollama
│       ├── config.yaml              # Model configurations
│       ├── runner.py                # Python runner (LangGraph uyumlu)
│       ├── legacy_runner.ts         # Eski TS runner (referans)
│       └── 📁 models/               # Model-specific configs
│           ├── deepseek-coder.yaml
│           ├── qwen2.5-coder.yaml
│           └── codellama.yaml
│
├── 📁 Meta/                         # 🧠 GOVERNANCE & STRATEGY
│   │
│   ├── 📁 Governance/               # Anayasa & Kurallar
│   │   ├── Constitution.md          # Ana Anayasa (flattened)
│   │   ├── Standards.md             # Coding standards
│   │   └── 📁 Assertions/           # DSPy assertions for auto-enforcement
│   │       ├── no_any.py
│   │       ├── no_console_log.py
│   │       └── port_compliance.py
│   │
│   ├── 📁 Strategy/                 # Roadmap & Planning
│   │   ├── Roadmap.md
│   │   ├── Agent_Roster.md          # ACTIVE_AGENTS.md (moved)
│   │   └── Resource_Allocation.md   # Cloud vs Local decisions
│   │
│   └── 📁 Active/                   # Current Operation State
│       ├── TASK_BOARD.md            # Active tasks
│       ├── HANDOFF_LOG.md           # Agent handoffs
│       └── 📁 logs/                 # Structured logs
│           └── .gitkeep
│
├── 📁 Knowledge/                    # 📚 RAG & MEMORY
│   │
│   ├── 📁 RAG/                      # Vector Search
│   │   ├── config.yaml              # Embedding configs
│   │   └── indexer.py               # Code indexing script
│   │
│   ├── 📁 GraphRAG/                 # Entity Relationships
│   │   ├── schema.md                # Entity types
│   │   └── builder.py               # Graph builder
│   │
│   └── 📁 Context/                  # Reusable Context Chunks
│       ├── architecture.md          # System architecture summary
│       ├── tech_stack.md            # Technology decisions
│       └── conventions.md           # Naming conventions
│
├── 📁 Workflows/                    # 📋 EXECUTABLE WORKFLOWS
│   │
│   ├── 📁 definitions/              # YAML Workflow definitions
│   │   ├── feature-development.yaml
│   │   ├── code-review.yaml
│   │   ├── bug-fix.yaml
│   │   ├── refactor.yaml
│   │   └── documentation.yaml
│   │
│   ├── 📁 templates/                # Reusable templates
│   │   ├── spec-template.md
│   │   ├── pr-template.md
│   │   └── handoff-template.md
│   │
│   └── 📁 commands/                 # CLI-invokable commands
│       ├── architect.md
│       ├── develop.md
│       ├── review.md
│       ├── qa-gate.md
│       └── sindir.md                # Turkish: "digest/compress"
│
├── 📁 Skills/                       # 🎯 HIGH-LEVEL CAPABILITIES
│   │
│   ├── database-migration.md        # DB migration skill
│   ├── api-integration.md           # External API skill
│   ├── ui-component.md              # UI development skill
│   └── performance-optimization.md  # Perf tuning skill
│
└── 📁 _Archive/                     # 📦 HISTORICAL DATA
    ├── 125325kas2025/               # Old experiments
    └── legacy-prompts/              # Deprecated prompts
```

---

## 3. Framework Stack

### 3.1 Core Stack (Must Have)

| Layer | Framework | Rol | Neden |
|-------|-----------|-----|-------|
| **Orchestration** | LangGraph | State machine, cyclic workflows | YAML'lar zaten state machine, perfect fit |
| **Local LLM** | Ollama | RTX 5090 inference | Zaten runner.ts var, Python'a port |
| **Connectivity** | MCP | Universal tool layer | Anthropic standard, future-proof |
| **Vector DB** | Supabase pgvector | RAG storage | Zaten kullanılıyor |

### 3.2 Enhancement Stack (Nice to Have)

| Layer | Framework | Rol | Priority |
|-------|-----------|-----|----------|
| **Optimization** | DSPy | Prompt auto-tuning | P2 - Post-Beta |
| **Sandboxing** | E2B | Safe code execution | P2 - Security |
| **Graph Memory** | GraphRAG | Relational knowledge | P3 - Long term |
| **Observability** | LangSmith/Phoenix | Tracing | P2 - Debug |

### 3.3 RTX 5090 Local Stack

```yaml
# .YBIS_Dev/Agentic/Local/config.yaml

hardware:
  gpu: "RTX 5090"
  vram: "32GB"
  
inference_backend: "ollama"  # veya vLLM for production

models:
  primary_coder:
    name: "deepseek-coder-v2:33b"
    context: 32768
    use_case: "Code generation, refactoring"
    
  fast_reviewer:
    name: "qwen2.5-coder:14b"
    context: 32768
    use_case: "Quick code review, linting"
    
  reasoning:
    name: "deepseek-r1:32b"  # veya qwq
    context: 32768
    use_case: "Complex problem solving"

routing_rules:
  - task: "code_generation"
    model: "primary_coder"
    fallback: "cloud_claude"
    
  - task: "quick_review"
    model: "fast_reviewer"
    fallback: null  # No cloud fallback
    
  - task: "architecture"
    model: "cloud_claude"  # Always cloud for critical decisions
    fallback: null
```

---

## 4. Migration Plan

### Phase 1: Consolidation (1-2 gün)

```bash
# 1. Yeni klasör yapısını oluştur
mkdir -p .YBIS_Dev/{Agentic/{Core/graphs,Core/nodes,Agents/personas,Tools,MCP/servers,MCP/clients,Local/models},Meta/{Governance/Assertions,Strategy,Active/logs},Knowledge/{RAG,GraphRAG,Context},Workflows/{definitions,templates,commands},Skills,_Archive}

# 2. Mevcut dosyaları taşı
mv .YBIS_Dev/Veriler/workflows/*.yaml .YBIS_Dev/Workflows/definitions/
mv .YBIS_Dev/Veriler/commands/*.md .YBIS_Dev/Workflows/commands/
mv .YBIS_Dev/Veriler/agents/*.md .YBIS_Dev/Agentic/Agents/personas/
mv .YBIS_Dev/Meta/Governance/Standards/1_Anayasa/README.md .YBIS_Dev/Meta/Governance/Constitution.md
mv .YBIS_Dev/Agentic/125325kas2025 .YBIS_Dev/_Archive/

# 3. Eski boş klasörleri temizle
rm -rf .YBIS_Dev/Veriler  # After backup!
```

### Phase 2: Critical Files (1 gün)

#### 4.2.1 AGENT_REGISTRY.json oluştur

```json
// .YBIS_Dev/Agentic/Agents/registry.json
{
  "version": "1.0.0",
  "updated": "2025-12-13",
  "agents": [
    {
      "id": "orchestrator",
      "name": "YBIS Orchestrator",
      "type": "coordinator",
      "runtime": "cloud",
      "model": "claude-sonnet-4",
      "persona": "./personas/orchestrator.md",
      "capabilities": ["task_routing", "agent_management", "workflow_execution"],
      "tools": ["file_ops", "git_ops", "agent_invoke"]
    },
    {
      "id": "architect",
      "name": "System Architect",
      "type": "specialist",
      "runtime": "cloud",
      "model": "claude-sonnet-4",
      "persona": "./personas/architect.md",
      "capabilities": ["system_design", "spec_writing", "impact_analysis"],
      "tools": ["file_ops", "rag_search"]
    },
    {
      "id": "developer",
      "name": "Senior Developer",
      "type": "specialist",
      "runtime": "hybrid",
      "model": {
        "local": "deepseek-coder-v2:33b",
        "cloud": "claude-sonnet-4"
      },
      "persona": "./personas/developer.md",
      "capabilities": ["code_generation", "refactoring", "debugging"],
      "tools": ["file_ops", "git_ops", "code_exec", "test_runner"]
    },
    {
      "id": "qa-engineer",
      "name": "QA Engineer",
      "type": "specialist",
      "runtime": "local",
      "model": "qwen2.5-coder:14b",
      "persona": "./personas/qa-engineer.md",
      "capabilities": ["test_writing", "bug_detection", "coverage_analysis"],
      "tools": ["file_ops", "test_runner", "lint_check"]
    },
    {
      "id": "code-reviewer",
      "name": "Code Reviewer",
      "type": "specialist",
      "runtime": "local",
      "model": "qwen2.5-coder:14b",
      "persona": "./personas/code-reviewer.md",
      "capabilities": ["code_review", "style_check", "security_audit"],
      "tools": ["file_ops", "lint_check", "rag_search"]
    },
    {
      "id": "documentation",
      "name": "Documentation Writer",
      "type": "specialist",
      "runtime": "local",
      "model": "qwen2.5:14b",
      "persona": "./personas/documentation.md",
      "capabilities": ["doc_generation", "readme_update", "api_docs"],
      "tools": ["file_ops", "rag_search"]
    }
  ],
  "routing": {
    "cost_sensitive": true,
    "prefer_local": true,
    "cloud_tasks": ["architecture", "critical_decisions", "complex_debugging"]
  }
}
```

#### 4.2.2 AI_AGENT_PROTOCOLS.md oluştur

```markdown
// .YBIS_Dev/Agentic/Agents/protocols.md

# AI Agent Communication Protocols v1.0

## 1. Temel İlkeler

### 1.1 Constitution Compliance
Tüm agent'lar `.YBIS_Dev/Meta/Governance/Constitution.md` kurallarına MUTLAK uyar.
Violation = Immediate task rejection.

### 1.2 Zero Tolerance Rules
- ❌ `any` type kullanımı
- ❌ `@ts-ignore` kullanımı
- ❌ `console.log` (sadece `logger` kullan)
- ❌ Direct vendor imports (Port pattern zorunlu)

## 2. İletişim Protokolü

### 2.1 Task Handoff Format
```yaml
handoff:
  from: "<agent_id>"
  to: "<agent_id>"
  task_id: "<uuid>"
  context:
    files_modified: []
    decisions_made: []
    blockers: []
  status: "ready" | "blocked" | "review_needed"
```

### 2.2 Feedback Loop
```
Developer -> Code -> QA Check -> FAIL -> Developer (max 3 iterations)
                             -> PASS -> Code Review -> FAIL -> Developer
                                                    -> PASS -> Merge Ready
```

## 3. Escalation Rules

| Condition | Action |
|-----------|--------|
| 3x QA Fail | Escalate to Architect |
| Security Issue | Immediate halt, notify human |
| Constitution Violation | Auto-reject, log incident |
| Model uncertainty > 0.7 | Request human review |

## 4. Tool Usage Rules

### 4.1 File Operations
- ALWAYS read before write
- NEVER overwrite without diff check
- Use atomic operations for critical files

### 4.2 Git Operations
- Branch naming: `agent/<agent_id>/<task_id>`
- Commit format: `[<agent_id>] <type>: <message>`
- NO force push ever

### 4.3 Code Execution
- Sandbox required for untrusted code
- Timeout: 30s default, 120s max
- Memory limit: 512MB
```

### Phase 3: LangGraph Setup (2-3 gün)

#### 4.3.1 Python Environment

```bash
# .YBIS_Dev/Agentic/ içinde
cd .YBIS_Dev/Agentic

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # veya Windows: .venv\Scripts\activate

# Core dependencies
pip install langgraph langchain-core langchain-anthropic langchain-ollama
pip install pydantic python-dotenv rich

# Optional enhancements
pip install dspy-ai  # Prompt optimization
pip install arize-phoenix  # Observability
```

#### 4.3.2 Basic Orchestrator

```python
# .YBIS_Dev/Agentic/Core/orchestrator.py

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import json
import os

# State Definition
class AgentState(TypedDict):
    task: str
    task_type: Literal["feature", "bugfix", "refactor", "review"]
    current_agent: str
    iteration: int
    max_iterations: int
    files_context: list[str]
    decisions: list[str]
    status: Literal["in_progress", "blocked", "completed", "failed"]
    output: str

# Load Agent Registry
def load_registry():
    registry_path = os.path.join(os.path.dirname(__file__), 
                                  "../Agents/registry.json")
    with open(registry_path) as f:
        return json.load(f)

REGISTRY = load_registry()

# Node Functions
def architect_node(state: AgentState) -> AgentState:
    """Architect analyzes and creates spec"""
    # TODO: Implement with actual LLM call
    print(f"[Architect] Analyzing: {state['task']}")
    state["decisions"].append("spec_created")
    state["current_agent"] = "developer"
    return state

def developer_node(state: AgentState) -> AgentState:
    """Developer implements the spec"""
    print(f"[Developer] Implementing: {state['task']}")
    state["decisions"].append("code_written")
    state["current_agent"] = "qa-engineer"
    state["iteration"] += 1
    return state

def qa_node(state: AgentState) -> AgentState:
    """QA runs tests and checks"""
    print(f"[QA] Testing iteration {state['iteration']}")
    # Simulated pass/fail
    passed = state["iteration"] >= 2  # Pass on 2nd try
    if passed:
        state["decisions"].append("qa_passed")
        state["current_agent"] = "code-reviewer"
    else:
        state["decisions"].append("qa_failed")
        state["current_agent"] = "developer"
    return state

def reviewer_node(state: AgentState) -> AgentState:
    """Code reviewer checks quality"""
    print(f"[Reviewer] Reviewing code")
    state["decisions"].append("review_passed")
    state["status"] = "completed"
    return state

# Routing Logic
def route_next(state: AgentState) -> str:
    if state["status"] == "completed":
        return END
    if state["iteration"] >= state["max_iterations"]:
        state["status"] = "failed"
        return END
    return state["current_agent"]

# Build Graph
def build_feature_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("architect", architect_node)
    workflow.add_node("developer", developer_node)
    workflow.add_node("qa-engineer", qa_node)
    workflow.add_node("code-reviewer", reviewer_node)
    
    # Add edges
    workflow.set_entry_point("architect")
    workflow.add_conditional_edges("architect", route_next)
    workflow.add_conditional_edges("developer", route_next)
    workflow.add_conditional_edges("qa-engineer", route_next)
    workflow.add_conditional_edges("code-reviewer", route_next)
    
    # Compile with memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Main execution
if __name__ == "__main__":
    graph = build_feature_graph()
    
    initial_state = AgentState(
        task="Implement user profile settings screen",
        task_type="feature",
        current_agent="architect",
        iteration=0,
        max_iterations=5,
        files_context=[],
        decisions=[],
        status="in_progress",
        output=""
    )
    
    config = {"configurable": {"thread_id": "test-1"}}
    
    for event in graph.stream(initial_state, config):
        print(f"Event: {event}")
```

### Phase 4: Local Runner Integration (1-2 gün)

```python
# .YBIS_Dev/Agentic/Local/runner.py

from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import yaml
import os

class HybridModelRouter:
    """Routes tasks to local or cloud models based on config"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.local_models = {}
        self.cloud_model = None
        self._init_models()
    
    def _init_models(self):
        # Initialize local models (Ollama)
        for model_key, model_config in self.config["models"].items():
            if isinstance(model_config.get("name"), str):
                self.local_models[model_key] = ChatOllama(
                    model=model_config["name"],
                    num_ctx=model_config.get("context", 8192)
                )
        
        # Initialize cloud model
        self.cloud_model = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            max_tokens=8192
        )
    
    def route(self, task_type: str, complexity: str = "medium") -> ChatOllama | ChatAnthropic:
        """Route to appropriate model based on task"""
        
        # Always use cloud for critical tasks
        cloud_tasks = self.config["routing"].get("cloud_tasks", [])
        if task_type in cloud_tasks:
            return self.cloud_model
        
        # Use local for cost-sensitive tasks
        if self.config["routing"].get("prefer_local", True):
            if task_type == "code_generation":
                return self.local_models.get("primary_coder", self.cloud_model)
            elif task_type == "quick_review":
                return self.local_models.get("fast_reviewer", self.cloud_model)
            elif task_type == "reasoning":
                return self.local_models.get("reasoning", self.cloud_model)
        
        return self.cloud_model
    
    async def invoke(self, task_type: str, system_prompt: str, user_message: str):
        """Invoke the appropriate model"""
        model = self.route(task_type)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        response = await model.ainvoke(messages)
        return response.content

# Usage example
if __name__ == "__main__":
    import asyncio
    
    router = HybridModelRouter()
    
    async def test():
        # This will use local DeepSeek
        result = await router.invoke(
            task_type="code_generation",
            system_prompt="You are a senior TypeScript developer.",
            user_message="Write a React hook for debouncing input."
        )
        print(result)
    
    asyncio.run(test())
```

---

## 5. MCP Integration

### 5.1 MCP Server Configs

```json
// .YBIS_Dev/Agentic/MCP/servers/supabase.json
{
  "name": "supabase-mcp",
  "version": "1.0.0",
  "description": "MCP server for Supabase operations",
  "tools": [
    {
      "name": "query_database",
      "description": "Execute a read-only SQL query",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "params": { "type": "array" }
        },
        "required": ["query"]
      }
    },
    {
      "name": "search_vectors",
      "description": "Semantic search in vector store",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "table": { "type": "string" },
          "limit": { "type": "integer", "default": 10 }
        },
        "required": ["query"]
      }
    }
  ]
}
```

### 5.2 Filesystem MCP

```json
// .YBIS_Dev/Agentic/MCP/servers/filesystem.json
{
  "name": "filesystem-mcp",
  "version": "1.0.0",
  "tools": [
    {
      "name": "read_file",
      "description": "Read file contents",
      "inputSchema": {
        "type": "object",
        "properties": {
          "path": { "type": "string" }
        },
        "required": ["path"]
      }
    },
    {
      "name": "write_file",
      "description": "Write content to file",
      "inputSchema": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "content": { "type": "string" }
        },
        "required": ["path", "content"]
      }
    },
    {
      "name": "search_files",
      "description": "Search for files matching pattern",
      "inputSchema": {
        "type": "object",
        "properties": {
          "pattern": { "type": "string" },
          "directory": { "type": "string", "default": "." }
        },
        "required": ["pattern"]
      }
    }
  ]
}
```

---

## 6. Öncelik Sıralaması

### 6.1 Hemen Yapılacaklar (Bu Hafta)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 1 | Klasör yapısını oluştur | 2 saat | 🔴 Kritik |
| 2 | Dosyaları yeni lokasyonlara taşı | 2 saat | 🔴 Kritik |
| 3 | AGENT_REGISTRY.json oluştur | 3 saat | 🔴 Kritik |
| 4 | AI_AGENT_PROTOCOLS.md oluştur | 2 saat | 🔴 Kritik |
| 5 | LangGraph environment setup | 2 saat | 🟡 Yüksek |

### 6.2 Kısa Vadeli (2 Hafta)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 6 | Basic orchestrator implement | 1 gün | 🟡 Yüksek |
| 7 | Local runner Python port | 1 gün | 🟡 Yüksek |
| 8 | RAG tool implement | 1 gün | 🟡 Yüksek |
| 9 | İlk workflow test | 0.5 gün | 🟡 Yüksek |

### 6.3 Orta Vadeli (1 Ay - Open Beta'ya kadar)

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 10 | MCP integration | 2 gün | 🟢 Normal |
| 11 | DSPy assertions | 2 gün | 🟢 Normal |
| 12 | Web dashboard (Mission Control) | 3 gün | 🟢 Normal |
| 13 | Full workflow coverage | 3 gün | 🟢 Normal |

---

## 7. Başarı Metrikleri

### 7.1 Organization Phase Complete When:

- [ ] Tüm dosyalar yeni lokasyonlarda
- [ ] AGENT_REGISTRY.json çalışıyor
- [ ] AI_AGENT_PROTOCOLS.md tamamlandı
- [ ] LangGraph basic graph çalışıyor
- [ ] Local runner (5090) test edildi
- [ ] En az 1 workflow end-to-end çalıştı

### 7.2 Open Beta Ready When:

- [ ] 3+ workflow automated
- [ ] RAG tool functional
- [ ] Self-correction loop çalışıyor
- [ ] Basic observability var
- [ ] Web app scaffold complete

---

## 8. Risk ve Mitigasyon

| Risk | Olasılık | Etki | Mitigasyon |
|------|----------|------|------------|
| LangGraph learning curve | Orta | Orta | Basit graph'tan başla, iterate et |
| Local model quality | Orta | Yüksek | Cloud fallback her zaman aktif |
| Over-engineering | Yüksek | Yüksek | MVP mindset, feature freeze |
| Context window limits | Düşük | Orta | RAG + chunking strategy |

---

## Appendix A: Quick Reference Commands

```bash
# Start Ollama with specific model
ollama run deepseek-coder-v2:33b

# Test LangGraph setup
cd .YBIS_Dev/Agentic && python -m Core.orchestrator

# Run local runner
python -m Local.runner

# Index codebase for RAG
python -m Knowledge.RAG.indexer --path ../apps/mobile/src
```

## Appendix B: Environment Variables

```bash
# .env.local (or .YBIS_Dev/.env)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...  # For embeddings if needed
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
OLLAMA_HOST=http://localhost:11434
```

---

**Son Güncelleme:** 13 Aralık 2025  
**Sonraki Review:** Open Beta öncesi
