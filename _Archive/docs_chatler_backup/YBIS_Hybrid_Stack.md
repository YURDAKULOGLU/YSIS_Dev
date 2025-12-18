# YBIS Hybrid Agentic Stack
## "Best of All Worlds" Architecture

**Tarih:** 13 Aralık 2025  
**Versiyon:** 1.0  
**Kod Adı:** YBIS-OS

---

## 1. Stack Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         YBIS AGENTIC STACK                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 5: INTERFACE                                               │   │
│  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │   │
│  │ │ Claude.ai   │  │ Cursor IDE  │  │ CLI Runner  │               │   │
│  │ │ (MCP)       │  │ (.mdc)      │  │ (Python)    │               │   │
│  │ └─────────────┘  └─────────────┘  └─────────────┘               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 4: ORCHESTRATION                          [LangGraph]      │   │
│  │ ┌───────────────────────────────────────────────────────────┐   │   │
│  │ │  BMAD Workflow Engine                                      │   │   │
│  │ │  ├─ feature-development.yaml → FeatureDevGraph            │   │   │
│  │ │  ├─ code-review.yaml → CodeReviewGraph                    │   │   │
│  │ │  └─ brownfield-fullstack.yaml → BrownfieldGraph           │   │   │
│  │ └───────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 3: AGENTS                                 [PydanticAI]     │   │
│  │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐         │   │
│  │ │ Architect │ │ Developer │ │ QA        │ │ Reviewer  │         │   │
│  │ │ (Cloud)   │ │ (Hybrid)  │ │ (Local)   │ │ (Local)   │         │   │
│  │ └───────────┘ └───────────┘ └───────────┘ └───────────┘         │   │
│  │           Type-safe tools + Constitution enforcement             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 2: MEMORY & KNOWLEDGE                                      │   │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │   │
│  │ │ Mem0            │  │ Supabase        │  │ Zep/Graphiti    │   │   │
│  │ │ (Episodic)      │  │ (Semantic RAG)  │  │ (Future: Graph) │   │   │
│  │ │ User prefs,     │  │ Codebase,       │  │ Entity          │   │   │
│  │ │ past sessions   │  │ docs, specs     │  │ relations       │   │   │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 1: INFERENCE                                               │   │
│  │ ┌───────────────────────┐  ┌───────────────────────┐            │   │
│  │ │ CLOUD                 │  │ LOCAL (RTX 5090)      │            │   │
│  │ │ ├─ Claude Sonnet 4    │  │ ├─ DeepSeek-Coder 33B │            │   │
│  │ │ │  (Architecture)     │  │ │  (Code generation)  │            │   │
│  │ │ └─ Claude Opus 4.5    │  │ ├─ Qwen2.5-Coder 14B  │            │   │
│  │ │    (Critical only)    │  │ │  (Fast review)      │            │   │
│  │ │                       │  │ └─ Ollama runtime     │            │   │
│  │ └───────────────────────┘  └───────────────────────┘            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 0: INFRASTRUCTURE                                          │   │
│  │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐         │   │
│  │ │ MCP       │ │ LangSmith │ │ Supabase  │ │ Git       │         │   │
│  │ │ Protocol  │ │ Tracing   │ │ DB + Auth │ │ Version   │         │   │
│  │ └───────────┘ └───────────┘ └───────────┘ └───────────┘         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Selection Rationale

### 2.1 Orchestration: LangGraph ✅

| Criteria | Score | Reason |
|----------|-------|--------|
| BMAD YAML uyumu | ⭐⭐⭐⭐⭐ | State machine → Graph birebir mapping |
| Cyclic workflows | ⭐⭐⭐⭐⭐ | QA fail → Dev retry loop native |
| Observability | ⭐⭐⭐⭐⭐ | LangSmith integration |
| Community | ⭐⭐⭐⭐⭐ | 70M+ downloads/month |
| Local model support | ⭐⭐⭐⭐ | langchain-ollama |

**Alternatif değerlendirildi:** Agno (faster ama YAML parsing yok)

### 2.2 Agent Framework: PydanticAI ✅

| Criteria | Score | Reason |
|----------|-------|--------|
| Type safety | ⭐⭐⭐⭐⭐ | Constitution rules → Pydantic models |
| Model agnostic | ⭐⭐⭐⭐⭐ | Ollama, Claude, OpenAI... |
| Tool validation | ⭐⭐⭐⭐⭐ | Input/output schema enforcement |
| Learning curve | ⭐⭐⭐⭐ | Pydantic biliyorsan kolay |

**Alternatif değerlendirildi:** CrewAI (role-based ama type safety zayıf)

### 2.3 Memory: Mem0 + Supabase ✅

| Layer | Tool | Use Case |
|-------|------|----------|
| Episodic | **Mem0** | User preferences, past sessions, learned patterns |
| Semantic | **Supabase pgvector** | Codebase RAG, documentation search |
| Relational | **Zep/Graphiti** (P2) | Entity relationships, impact analysis |

**Neden ikisi birden:**
- Mem0 → Agent'ın "kişisel hafızası" (bu user X, Y tercih ediyor)
- Supabase → Codebase knowledge (bu function nerede, ne yapıyor)

### 2.4 Local Inference: Ollama + RTX 5090 ✅

| Model | Size | VRAM | Use Case |
|-------|------|------|----------|
| DeepSeek-Coder-V2 | 33B Q4 | ~24GB | Primary code generation |
| Qwen2.5-Coder | 14B Q4 | ~10GB | Fast review, parallel tasks |
| DeepSeek-R1 | 32B Q4 | ~24GB | Complex reasoning (optional) |

**Routing logic:**
```python
if task.requires_architecture_decision:
    return "claude-sonnet-4"  # Cloud
elif task.is_code_generation:
    return "deepseek-coder-v2:33b"  # Local
elif task.is_quick_review:
    return "qwen2.5-coder:14b"  # Local, fast
else:
    return "deepseek-coder-v2:33b"  # Default local
```

### 2.5 Protocol: MCP ✅

**Neden MCP:**
- Claude Desktop/Code native support
- Tool definitions standardize
- Future-proof (Anthropic standard)

**MCP Servers:**
```
├── @anthropic/mcp-server-filesystem  # File operations
├── @supabase/mcp-server-supabase     # Database operations
├── ybis-mcp-server                   # Custom BMAD tools
└── git-mcp-server                    # Version control
```

### 2.6 Observability: LangSmith ✅

**Free tier features:**
- 5,000 traces/month
- Full trace visualization
- Basic analytics
- OpenTelemetry export

---

## 3. Directory Structure

```
.YBIS_Dev/
│
├── 📁 Stack/                        # 🔧 HYBRID STACK CORE
│   │
│   ├── 📁 langgraph/                # Orchestration Layer
│   │   ├── __init__.py
│   │   ├── config.py                # LangSmith, model configs
│   │   ├── state.py                 # Shared state definitions
│   │   ├── 📁 graphs/               # Workflow implementations
│   │   │   ├── base_graph.py        # Abstract base
│   │   │   ├── feature_dev.py       # feature-development.yaml
│   │   │   ├── code_review.py       # code-review.yaml
│   │   │   ├── brownfield.py        # brownfield-fullstack.yaml
│   │   │   └── bug_fix.py
│   │   └── 📁 nodes/                # Reusable graph nodes
│   │       ├── architect.py
│   │       ├── developer.py
│   │       ├── qa.py
│   │       └── reviewer.py
│   │
│   ├── 📁 agents/                   # PydanticAI Agents
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Abstract agent with Constitution
│   │   ├── architect.py             # System design agent
│   │   ├── developer.py             # Code generation agent
│   │   ├── qa_engineer.py           # Testing agent
│   │   ├── code_reviewer.py         # Review agent
│   │   └── 📁 schemas/              # Pydantic I/O schemas
│   │       ├── code_output.py       # Validated code output
│   │       ├── spec_output.py       # Spec document schema
│   │       └── review_output.py     # Code review schema
│   │
│   ├── 📁 memory/                   # Memory Layer
│   │   ├── __init__.py
│   │   ├── mem0_client.py           # Mem0 integration
│   │   ├── rag_client.py            # Supabase pgvector
│   │   ├── unified_memory.py        # Combined interface
│   │   └── 📁 indexers/             # RAG indexing scripts
│   │       ├── codebase_indexer.py
│   │       └── docs_indexer.py
│   │
│   ├── 📁 inference/                # Model Routing
│   │   ├── __init__.py
│   │   ├── router.py                # Intelligent model selection
│   │   ├── ollama_client.py         # Local model interface
│   │   ├── claude_client.py         # Cloud model interface
│   │   └── config.yaml              # Model configurations
│   │
│   ├── 📁 tools/                    # PydanticAI Tools
│   │   ├── __init__.py
│   │   ├── file_ops.py              # File read/write/search
│   │   ├── git_ops.py               # Git operations
│   │   ├── test_runner.py           # Execute tests
│   │   ├── lint_check.py            # TSC, ESLint
│   │   └── rag_search.py            # Memory search tool
│   │
│   ├── 📁 mcp/                      # MCP Servers
│   │   ├── README.md
│   │   ├── 📁 servers/
│   │   │   ├── ybis_server.py       # Custom YBIS MCP server
│   │   │   └── package.json         # MCP dependencies
│   │   └── 📁 configs/
│   │       └── claude_desktop.json  # Claude Desktop MCP config
│   │
│   └── 📁 observability/            # Tracing & Monitoring
│       ├── __init__.py
│       ├── langsmith_config.py
│       └── traces.py
│
├── 📁 BMAD/                         # Migrated from Veriler
│   ├── 📁 agents/                   # Agent persona definitions
│   ├── 📁 commands/                 # Executable prompts
│   ├── 📁 workflows/                # YAML state machines
│   ├── 📁 templates/                # Spec templates
│   ├── 📁 checklists/               # QA checklists
│   └── protocols.md                 # AI_AGENT_PROTOCOLS
│
├── 📁 Meta/                         # Governance
│   ├── Constitution.md              # Main rules
│   └── 📁 Assertions/               # Pydantic validators
│       ├── no_any.py
│       └── port_compliance.py
│
└── requirements.txt                 # Python dependencies
```

---

## 4. Implementation Details

### 4.1 Core Dependencies

```txt
# requirements.txt

# Orchestration
langgraph>=0.2.0
langchain-core>=0.3.0
langsmith>=0.2.0

# Agent Framework
pydantic-ai>=0.1.0
pydantic>=2.0.0

# Memory
mem0ai>=1.0.0
supabase>=2.0.0

# Local Inference
langchain-ollama>=0.2.0
ollama>=0.3.0

# Cloud Inference
langchain-anthropic>=0.2.0
anthropic>=0.40.0

# Tools
gitpython>=3.1.0
python-dotenv>=1.0.0
rich>=13.0.0
httpx>=0.27.0

# MCP (optional, for server)
mcp>=1.0.0
```

### 4.2 Configuration

```python
# .YBIS_Dev/Stack/langgraph/config.py

import os
from pydantic_settings import BaseSettings

class YBISConfig(BaseSettings):
    """Central configuration for YBIS Agentic Stack"""
    
    # LangSmith
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
    langsmith_project: str = "ybis-agentic"
    langsmith_tracing: bool = True
    
    # Anthropic (Cloud)
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    cloud_model: str = "claude-sonnet-4-20250514"
    
    # Ollama (Local)
    ollama_host: str = "http://localhost:11434"
    local_primary_model: str = "deepseek-coder-v2:33b"
    local_fast_model: str = "qwen2.5-coder:14b"
    
    # Mem0
    mem0_api_key: str = os.getenv("MEM0_API_KEY", "")
    
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # Routing
    prefer_local: bool = True
    cloud_tasks: list[str] = ["architecture", "critical_decision", "complex_debug"]
    
    class Config:
        env_file = ".env"

config = YBISConfig()

# Enable LangSmith tracing
if config.langsmith_tracing:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = config.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = config.langsmith_project
```

### 4.3 Unified Memory Client

```python
# .YBIS_Dev/Stack/memory/unified_memory.py

from mem0 import MemoryClient
from supabase import create_client
from typing import Optional
import json

class UnifiedMemory:
    """
    Combines Mem0 (episodic) and Supabase (semantic) memory.
    
    - Mem0: User preferences, past sessions, learned patterns
    - Supabase: Codebase knowledge, documentation
    """
    
    def __init__(self, config):
        # Episodic memory (Mem0)
        self.mem0 = MemoryClient(api_key=config.mem0_api_key)
        
        # Semantic memory (Supabase pgvector)
        self.supabase = create_client(config.supabase_url, config.supabase_key)
    
    # ==================== EPISODIC (Mem0) ====================
    
    def remember_interaction(self, messages: list, user_id: str, agent_id: str):
        """Store conversation in episodic memory"""
        self.mem0.add(
            messages,
            user_id=user_id,
            agent_id=agent_id,
            metadata={"type": "interaction"}
        )
    
    def recall_user_context(self, query: str, user_id: str) -> list[dict]:
        """Retrieve relevant user memories"""
        results = self.mem0.search(query, user_id=user_id, limit=5)
        return results.get("results", [])
    
    def get_user_preferences(self, user_id: str) -> dict:
        """Get all stored preferences for a user"""
        memories = self.mem0.get_all(user_id=user_id)
        return {m["id"]: m["memory"] for m in memories.get("results", [])}
    
    # ==================== SEMANTIC (Supabase RAG) ====================
    
    def search_codebase(self, query: str, limit: int = 5) -> list[dict]:
        """Semantic search over indexed codebase"""
        # Using Supabase's match_documents function (pgvector)
        response = self.supabase.rpc(
            "match_documents",
            {
                "query_embedding": self._embed(query),
                "match_count": limit,
                "filter": {"type": "code"}
            }
        ).execute()
        return response.data
    
    def search_documentation(self, query: str, limit: int = 5) -> list[dict]:
        """Semantic search over documentation"""
        response = self.supabase.rpc(
            "match_documents",
            {
                "query_embedding": self._embed(query),
                "match_count": limit,
                "filter": {"type": "documentation"}
            }
        ).execute()
        return response.data
    
    def _embed(self, text: str) -> list[float]:
        """Generate embedding for text"""
        # Using Supabase's built-in embedding or external service
        # For now, placeholder - implement with your embedding model
        from langchain_ollama import OllamaEmbeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        return embeddings.embed_query(text)
    
    # ==================== UNIFIED INTERFACE ====================
    
    def get_context(
        self, 
        query: str, 
        user_id: str,
        include_code: bool = True,
        include_docs: bool = True,
        include_user: bool = True
    ) -> dict:
        """
        Get unified context from all memory sources.
        Returns structured context for agent consumption.
        """
        context = {}
        
        if include_user:
            context["user_memories"] = self.recall_user_context(query, user_id)
        
        if include_code:
            context["relevant_code"] = self.search_codebase(query)
        
        if include_docs:
            context["relevant_docs"] = self.search_documentation(query)
        
        return context
    
    def format_for_prompt(self, context: dict) -> str:
        """Format context for injection into prompt"""
        sections = []
        
        if context.get("user_memories"):
            memories = "\n".join(f"- {m['memory']}" for m in context["user_memories"])
            sections.append(f"## User Context\n{memories}")
        
        if context.get("relevant_code"):
            code_refs = "\n".join(
                f"- {c['metadata']['file_path']}: {c['content'][:200]}..." 
                for c in context["relevant_code"]
            )
            sections.append(f"## Relevant Code\n{code_refs}")
        
        if context.get("relevant_docs"):
            doc_refs = "\n".join(
                f"- {d['metadata']['title']}: {d['content'][:200]}..."
                for d in context["relevant_docs"]
            )
            sections.append(f"## Relevant Documentation\n{doc_refs}")
        
        return "\n\n".join(sections)
```

### 4.4 Model Router

```python
# .YBIS_Dev/Stack/inference/router.py

from enum import Enum
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

class TaskType(str, Enum):
    ARCHITECTURE = "architecture"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    QUICK_FIX = "quick_fix"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    CRITICAL_DECISION = "critical_decision"

class TaskComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RoutingDecision(BaseModel):
    model: str
    runtime: str  # "local" or "cloud"
    reason: str

class IntelligentRouter:
    """
    Routes tasks to appropriate models based on:
    - Task type
    - Complexity
    - Cost sensitivity
    - Latency requirements
    """
    
    def __init__(self, config):
        self.config = config
        
        # Initialize models
        self.local_primary = ChatOllama(
            model=config.local_primary_model,
            base_url=config.ollama_host,
            num_ctx=32768
        )
        
        self.local_fast = ChatOllama(
            model=config.local_fast_model,
            base_url=config.ollama_host,
            num_ctx=32768
        )
        
        self.cloud = ChatAnthropic(
            model=config.cloud_model,
            max_tokens=8192
        )
    
    def route(
        self, 
        task_type: TaskType,
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
        force_cloud: bool = False,
        force_local: bool = False
    ) -> tuple[ChatOllama | ChatAnthropic, RoutingDecision]:
        """
        Intelligently route to the best model for the task.
        Returns (model, decision).
        """
        
        # Force overrides
        if force_cloud:
            return self.cloud, RoutingDecision(
                model=self.config.cloud_model,
                runtime="cloud",
                reason="Forced cloud by user"
            )
        
        if force_local:
            return self.local_primary, RoutingDecision(
                model=self.config.local_primary_model,
                runtime="local",
                reason="Forced local by user"
            )
        
        # Critical tasks always go to cloud
        if complexity == TaskComplexity.CRITICAL or task_type in [
            TaskType.ARCHITECTURE, 
            TaskType.CRITICAL_DECISION
        ]:
            return self.cloud, RoutingDecision(
                model=self.config.cloud_model,
                runtime="cloud",
                reason=f"Critical task type: {task_type}"
            )
        
        # Quick tasks use fast local model
        if task_type in [TaskType.QUICK_FIX, TaskType.CODE_REVIEW] and \
           complexity in [TaskComplexity.LOW, TaskComplexity.MEDIUM]:
            return self.local_fast, RoutingDecision(
                model=self.config.local_fast_model,
                runtime="local",
                reason="Quick task, using fast model"
            )
        
        # Code generation uses primary local
        if task_type == TaskType.CODE_GENERATION:
            return self.local_primary, RoutingDecision(
                model=self.config.local_primary_model,
                runtime="local",
                reason="Code generation, using local primary"
            )
        
        # Default: local primary (cost savings)
        if self.config.prefer_local:
            return self.local_primary, RoutingDecision(
                model=self.config.local_primary_model,
                runtime="local",
                reason="Default local preference"
            )
        
        return self.cloud, RoutingDecision(
            model=self.config.cloud_model,
            runtime="cloud",
            reason="Default cloud"
        )
```

### 4.5 PydanticAI Agent with Constitution

```python
# .YBIS_Dev/Stack/agents/base_agent.py

from pydantic_ai import Agent
from pydantic import BaseModel, field_validator
from typing import Optional
import re

# ==================== CONSTITUTION SCHEMAS ====================

class ConstitutionCompliantCode(BaseModel):
    """
    Output schema that enforces Constitution rules at type level.
    """
    code: str
    file_path: str
    explanation: str
    
    @field_validator('code')
    @classmethod
    def no_any_type(cls, v: str) -> str:
        """Constitution: No `any` type allowed"""
        if re.search(r':\s*any\b', v) or re.search(r'<any>', v):
            raise ValueError("Constitution violation: 'any' type is not allowed")
        return v
    
    @field_validator('code')
    @classmethod
    def no_ts_ignore(cls, v: str) -> str:
        """Constitution: No @ts-ignore allowed"""
        if '@ts-ignore' in v or '@ts-nocheck' in v:
            raise ValueError("Constitution violation: @ts-ignore is not allowed")
        return v
    
    @field_validator('code')
    @classmethod
    def no_console_log(cls, v: str) -> str:
        """Constitution: No console.log (use logger)"""
        if 'console.log' in v and 'logger' not in v.lower():
            raise ValueError("Constitution violation: Use logger instead of console.log")
        return v
    
    @field_validator('code')
    @classmethod
    def port_pattern_check(cls, v: str) -> str:
        """Constitution: External deps must be behind ports"""
        # Check for direct Supabase imports (should use port)
        if "from '@supabase/supabase-js'" in v or "from 'supabase'" in v:
            if "port" not in v.lower() and "adapter" not in v.lower():
                raise ValueError(
                    "Constitution violation: Direct Supabase import. "
                    "Use port/adapter pattern."
                )
        return v


class CodeReviewOutput(BaseModel):
    """Structured code review output"""
    approved: bool
    issues: list[str]
    suggestions: list[str]
    constitution_violations: list[str]
    security_concerns: list[str]


# ==================== BASE AGENT ====================

class YBISAgent:
    """
    Base agent with Constitution enforcement and memory integration.
    All YBIS agents inherit from this.
    """
    
    def __init__(
        self,
        agent_id: str,
        persona_path: str,
        router,
        memory,
        output_type: type[BaseModel]
    ):
        self.agent_id = agent_id
        self.router = router
        self.memory = memory
        
        # Load persona from BMAD
        self.persona = self._load_persona(persona_path)
        
        # Create PydanticAI agent
        self.agent = Agent(
            model=None,  # Will be set per-call via router
            output_type=output_type,
            system_prompt=self._build_system_prompt()
        )
    
    def _load_persona(self, path: str) -> dict:
        """Load agent persona from BMAD markdown file"""
        import yaml
        import re
        
        with open(path) as f:
            content = f.read()
        
        # Extract YAML block from markdown
        match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}
    
    def _build_system_prompt(self) -> str:
        """Build system prompt from persona + Constitution"""
        persona = self.persona.get("persona", {})
        
        return f"""You are {self.persona.get('agent', {}).get('name', 'YBIS Agent')}, 
a {persona.get('role', 'specialist')}.

## Style
{persona.get('style', 'Professional and precise')}

## Focus
{persona.get('focus', 'Quality and correctness')}

## Core Principles
{chr(10).join(f'- {p}' for p in persona.get('core_principles', []))}

## CONSTITUTION (NON-NEGOTIABLE)
You MUST follow these rules in ALL code you generate:
1. NO `any` type - use proper TypeScript types
2. NO `@ts-ignore` or `@ts-nocheck`
3. NO `console.log` - use the logger utility
4. External dependencies MUST use Port/Adapter pattern
5. UI components MUST come from `@ybis/ui`, never direct tamagui

Violations will cause automatic rejection.
"""
    
    async def run(
        self,
        task: str,
        user_id: str,
        context: Optional[dict] = None,
        task_type: str = "code_generation"
    ):
        """Execute agent with routing and memory"""
        
        # Get relevant memories
        memory_context = self.memory.get_context(
            query=task,
            user_id=user_id
        )
        
        # Route to appropriate model
        model, decision = self.router.route(
            task_type=task_type,
            complexity="medium"
        )
        
        # Enhance prompt with memory
        enhanced_task = f"""
{task}

## Context from Memory
{self.memory.format_for_prompt(memory_context)}
"""
        
        # Run agent
        result = await self.agent.run(
            enhanced_task,
            model=model
        )
        
        # Store interaction in memory
        self.memory.remember_interaction(
            messages=[
                {"role": "user", "content": task},
                {"role": "assistant", "content": str(result.output)}
            ],
            user_id=user_id,
            agent_id=self.agent_id
        )
        
        return result
```

### 4.6 LangGraph Workflow (BMAD Integration)

```python
# .YBIS_Dev/Stack/langgraph/graphs/feature_dev.py

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langsmith import traceable

# State definition
class FeatureDevState(TypedDict):
    task: str
    user_id: str
    
    # Workflow state
    phase: Literal["analyze", "specify", "implement", "review", "complete"]
    iteration: int
    max_iterations: int
    
    # Artifacts
    spec: str
    code: dict[str, str]  # file_path: content
    review_result: dict
    
    # Context
    memory_context: dict
    decisions: list[str]
    blockers: list[str]
    
    # Status
    status: Literal["in_progress", "blocked", "completed", "failed"]


class FeatureDevelopmentGraph:
    """
    LangGraph implementation of BMAD feature-development.yaml workflow.
    
    Flow: Analyze → Specify → Implement → Review → (retry or complete)
    """
    
    def __init__(self, agents: dict, memory, router):
        self.agents = agents
        self.memory = memory
        self.router = router
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(FeatureDevState)
        
        # Add nodes (each maps to BMAD workflow step)
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("specify", self._specify_node)
        workflow.add_node("implement", self._implement_node)
        workflow.add_node("review", self._review_node)
        workflow.add_node("fix", self._fix_node)
        
        # Define flow
        workflow.set_entry_point("analyze")
        
        workflow.add_edge("analyze", "specify")
        workflow.add_edge("specify", "implement")
        workflow.add_edge("implement", "review")
        
        # Conditional: review pass/fail
        workflow.add_conditional_edges(
            "review",
            self._should_retry,
            {
                "retry": "fix",
                "complete": END,
                "escalate": END
            }
        )
        
        workflow.add_edge("fix", "implement")
        
        # Compile with checkpointing
        memory_saver = MemorySaver()
        return workflow.compile(checkpointer=memory_saver)
    
    @traceable(name="analyze_phase")
    async def _analyze_node(self, state: FeatureDevState) -> FeatureDevState:
        """BMAD: Architect analyzes the task"""
        architect = self.agents["architect"]
        
        result = await architect.run(
            task=f"Analyze this feature request and identify technical requirements:\n{state['task']}",
            user_id=state["user_id"],
            task_type="architecture"
        )
        
        state["decisions"].append(f"Analysis: {result.output}")
        state["phase"] = "specify"
        return state
    
    @traceable(name="specify_phase")
    async def _specify_node(self, state: FeatureDevState) -> FeatureDevState:
        """BMAD: Create technical specification"""
        architect = self.agents["architect"]
        
        result = await architect.run(
            task=f"""
            Based on the analysis, create a technical specification.
            
            Task: {state['task']}
            Analysis: {state['decisions'][-1]}
            
            Output a detailed spec following the BMAD spec template.
            """,
            user_id=state["user_id"],
            task_type="architecture"
        )
        
        state["spec"] = result.output.spec if hasattr(result.output, 'spec') else str(result.output)
        state["phase"] = "implement"
        return state
    
    @traceable(name="implement_phase")
    async def _implement_node(self, state: FeatureDevState) -> FeatureDevState:
        """BMAD: Developer implements the spec"""
        developer = self.agents["developer"]
        
        result = await developer.run(
            task=f"""
            Implement the following specification:
            
            {state['spec']}
            
            Follow all Constitution rules. Generate complete, working code.
            """,
            user_id=state["user_id"],
            task_type="code_generation"
        )
        
        # Constitution validation happens in PydanticAI schema
        state["code"][result.output.file_path] = result.output.code
        state["phase"] = "review"
        state["iteration"] += 1
        return state
    
    @traceable(name="review_phase")
    async def _review_node(self, state: FeatureDevState) -> FeatureDevState:
        """BMAD: QA and Code Review"""
        reviewer = self.agents["code_reviewer"]
        
        # Review all generated code
        all_code = "\n\n".join(
            f"// {path}\n{content}" 
            for path, content in state["code"].items()
        )
        
        result = await reviewer.run(
            task=f"""
            Review this code for:
            1. Constitution compliance
            2. Code quality
            3. Security issues
            4. Test coverage
            
            Code:
            {all_code}
            """,
            user_id=state["user_id"],
            task_type="code_review"
        )
        
        state["review_result"] = {
            "approved": result.output.approved,
            "issues": result.output.issues,
            "constitution_violations": result.output.constitution_violations
        }
        
        return state
    
    async def _fix_node(self, state: FeatureDevState) -> FeatureDevState:
        """Fix issues found in review"""
        developer = self.agents["developer"]
        
        result = await developer.run(
            task=f"""
            Fix these issues in the code:
            
            Issues: {state['review_result']['issues']}
            Constitution Violations: {state['review_result']['constitution_violations']}
            
            Current code:
            {state['code']}
            """,
            user_id=state["user_id"],
            task_type="code_generation"
        )
        
        state["code"][result.output.file_path] = result.output.code
        return state
    
    def _should_retry(self, state: FeatureDevState) -> str:
        """Decide whether to retry, complete, or escalate"""
        review = state["review_result"]
        
        if review["approved"]:
            state["status"] = "completed"
            return "complete"
        
        if state["iteration"] >= state["max_iterations"]:
            state["status"] = "failed"
            state["blockers"].append("Max iterations reached")
            return "escalate"
        
        return "retry"
    
    async def run(self, task: str, user_id: str) -> FeatureDevState:
        """Execute the full workflow"""
        initial_state = FeatureDevState(
            task=task,
            user_id=user_id,
            phase="analyze",
            iteration=0,
            max_iterations=3,
            spec="",
            code={},
            review_result={},
            memory_context={},
            decisions=[],
            blockers=[],
            status="in_progress"
        )
        
        config = {"configurable": {"thread_id": f"feature-{user_id}-{hash(task)}"}}
        
        final_state = await self.graph.ainvoke(initial_state, config)
        return final_state
```

### 4.7 MCP Server (Custom YBIS Tools)

```python
# .YBIS_Dev/Stack/mcp/servers/ybis_server.py

from mcp.server import Server
from mcp.types import Tool, TextContent
import json

app = Server("ybis-mcp")

@app.tool()
async def search_codebase(query: str, limit: int = 5) -> str:
    """
    Search the YBIS codebase using semantic search.
    Returns relevant code snippets and file paths.
    """
    from ..memory.unified_memory import UnifiedMemory
    memory = UnifiedMemory(config)
    
    results = memory.search_codebase(query, limit=limit)
    return json.dumps(results, indent=2)

@app.tool()
async def get_constitution_rules() -> str:
    """
    Get the current YBIS Constitution rules.
    All generated code must comply with these rules.
    """
    with open(".YBIS_Dev/Meta/Constitution.md") as f:
        return f.read()

@app.tool()
async def run_bmad_command(command: str, arguments: str = "") -> str:
    """
    Execute a BMAD command (e.g., 'architect', 'qa-gate', 'sindir').
    Commands are defined in .YBIS_Dev/BMAD/commands/
    """
    command_path = f".YBIS_Dev/BMAD/commands/{command}.md"
    
    try:
        with open(command_path) as f:
            prompt = f.read()
        
        # Replace $ARGUMENTS placeholder
        prompt = prompt.replace("$ARGUMENTS", arguments)
        return prompt
    except FileNotFoundError:
        return f"Command not found: {command}"

@app.tool()
async def get_workflow_status(workflow_id: str) -> str:
    """
    Get the current status of a running workflow.
    """
    # Integrate with LangGraph checkpointer
    pass

@app.tool()
async def list_available_agents() -> str:
    """
    List all available BMAD agents and their capabilities.
    """
    import os
    agents = []
    agents_dir = ".YBIS_Dev/BMAD/agents/"
    
    for f in os.listdir(agents_dir):
        if f.endswith(".md"):
            agents.append(f.replace(".md", ""))
    
    return json.dumps({"agents": agents})

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

### 4.8 Claude Desktop MCP Config

```json
// .YBIS_Dev/Stack/mcp/configs/claude_desktop.json
// Copy to: ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)

{
  "mcpServers": {
    "ybis": {
      "command": "python",
      "args": ["-m", "Stack.mcp.servers.ybis_server"],
      "cwd": "/path/to/your/project/.YBIS_Dev"
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-filesystem",
        "/path/to/your/project"
      ]
    },
    "supabase": {
      "command": "npx",
      "args": [
        "-y", 
        "@supabase/mcp-server-supabase",
        "--supabase-url", "YOUR_SUPABASE_URL",
        "--service-key", "YOUR_SERVICE_KEY"
      ]
    }
  }
}
```

---

## 5. Setup Script

```bash
#!/bin/bash
# setup_ybis_stack.sh

echo "🚀 Setting up YBIS Hybrid Agentic Stack..."

# 1. Create directory structure
echo "📁 Creating directories..."
mkdir -p .YBIS_Dev/Stack/{langgraph/graphs,langgraph/nodes,agents/schemas,memory/indexers,inference,tools,mcp/servers,mcp/configs,observability}
mkdir -p .YBIS_Dev/{BMAD/{agents,commands,workflows,templates,checklists},Meta/Assertions}

# 2. Create virtual environment
echo "🐍 Setting up Python environment..."
cd .YBIS_Dev/Stack
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
echo "📦 Installing dependencies..."
pip install langgraph langchain-core langsmith
pip install pydantic-ai pydantic
pip install mem0ai supabase
pip install langchain-ollama langchain-anthropic
pip install gitpython python-dotenv rich httpx
pip install mcp

# 4. Create .env template
echo "🔐 Creating .env template..."
cat > .env.template << 'EOF'
# LangSmith
LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_PROJECT=ybis-agentic

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-key

# Mem0
MEM0_API_KEY=your-mem0-key

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Ollama (local)
OLLAMA_HOST=http://localhost:11434
EOF

# 5. Pull Ollama models
echo "🤖 Pulling local models (this may take a while)..."
ollama pull deepseek-coder-v2:33b
ollama pull qwen2.5-coder:14b
ollama pull nomic-embed-text

# 6. Verify setup
echo "✅ Verifying installation..."
python -c "import langgraph; import pydantic_ai; import mem0; print('All packages installed!')"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.template to .env and fill in your API keys"
echo "2. Migrate BMAD files from Veriler/ to BMAD/"
echo "3. Create AGENT_REGISTRY.json and protocols.md"
echo "4. Run: python -m Stack.langgraph.graphs.feature_dev"
```

---

## 6. Quick Start Guide

### Step 1: Environment Setup
```bash
cd .YBIS_Dev/Stack
source .venv/bin/activate
cp .env.template .env
# Edit .env with your API keys
```

### Step 2: Test Local Models
```bash
# Test Ollama
curl http://localhost:11434/api/tags

# Test model
ollama run deepseek-coder-v2:33b "Write a hello world in TypeScript"
```

### Step 3: Test Memory
```python
from memory.unified_memory import UnifiedMemory
from langgraph.config import config

memory = UnifiedMemory(config)

# Test Mem0
memory.remember_interaction(
    messages=[{"role": "user", "content": "I prefer functional programming"}],
    user_id="test_user",
    agent_id="test"
)

# Recall
memories = memory.recall_user_context("programming style", "test_user")
print(memories)
```

### Step 4: Run a Workflow
```python
from langgraph.graphs.feature_dev import FeatureDevelopmentGraph
from agents import architect, developer, code_reviewer
from memory.unified_memory import UnifiedMemory
from inference.router import IntelligentRouter

# Initialize
router = IntelligentRouter(config)
memory = UnifiedMemory(config)

agents = {
    "architect": architect,
    "developer": developer,
    "code_reviewer": code_reviewer
}

# Create and run graph
graph = FeatureDevelopmentGraph(agents, memory, router)
result = await graph.run(
    task="Add dark mode toggle to settings screen",
    user_id="yurdakul"
)

print(f"Status: {result['status']}")
print(f"Generated files: {list(result['code'].keys())}")
```

---

## 7. Migration Checklist

- [ ] Create directory structure
- [ ] Install dependencies
- [ ] Configure .env
- [ ] Pull Ollama models
- [ ] Migrate Veriler/ → BMAD/
- [ ] Create AGENT_REGISTRY.json
- [ ] Create protocols.md
- [ ] Index codebase for RAG
- [ ] Test memory integration
- [ ] Test single agent
- [ ] Test full workflow
- [ ] Configure MCP for Claude Desktop
- [ ] Enable LangSmith tracing

---

## 8. Cost Estimation

| Component | Free Tier | Paid |
|-----------|-----------|------|
| LangSmith | 5K traces/month | $39/month |
| Mem0 | 1K memories | $29/month |
| Claude API | - | ~$3/1M tokens |
| Supabase | 500MB, 50K requests | $25/month |
| Ollama | ∞ (local) | $0 |

**Estimated monthly cost (heavy usage):** ~$50-100

**With local-first strategy:** ~$20-50 (most inference local)

---

*YBIS Hybrid Stack v1.0 - December 2025*
