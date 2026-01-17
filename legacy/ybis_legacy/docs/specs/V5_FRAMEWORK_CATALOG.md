# V5 Framework Catalog
> Constitution-compliant framework recommendations for V5 tasks

**Status:** Draft  
**Date:** 2025-01-03  
**Constitution Compliance:** [OK] Free & Open-Source, [OK] Local-First, [OK] Plugin-First

---

## 📋 V5 Tasks & Framework Mapping

### 1. 📡 Multi-Model Router (Dynamic Model Selection)

**Task:** `V5-ROUTER-001` - Dynamic model selection based on task complexity, risk, and hardware

**Recommended Framework:** **LiteLLM** [OK] (Already in requirements.txt)

**Why:**
- [OK] **Free & Open-Source** (Apache 2.0)
- [OK] **Local-First Support:** Works with Ollama, vLLM, local models
- [OK] **Unified API:** Single interface for 100+ LLM providers
- [OK] **Cost Optimization:** Automatic fallback chains, budget tracking
- [OK] **Already Installed:** `litellm` in requirements.txt

**Current Status:**
- [OK] LiteLLM installed
- [WARN]️ Not fully integrated (model_router.py uses custom logic)
- [FAIL] No dynamic routing based on complexity

**Implementation Plan:**
```python
# src/agentic/core/plugins/model_router_v2.py
from litellm import Router, completion

class LiteLLMRouter:
    def __init__(self):
        self.router = Router(
            model_list=[
                {"model_name": "qwen2.5-coder:7b", "litellm_params": {"model": "ollama/qwen2.5-coder:7b"}},
                {"model_name": "qwen2.5-coder:32b", "litellm_params": {"model": "ollama/qwen2.5-coder:32b"}},
                # Fallback to cloud if local fails
                {"model_name": "claude-3-5-sonnet", "litellm_params": {"model": "anthropic/claude-3-5-sonnet-20241022"}},
            ],
            fallbacks=["qwen2.5-coder:7b", "qwen2.5-coder:32b", "claude-3-5-sonnet"],
            set_verbose=True
        )
    
    def get_model(self, task_complexity: str, risk: str) -> str:
        # Complexity-based routing
        if task_complexity == "HIGH" or risk == "HIGH":
            return "qwen2.5-coder:32b"  # More capable model
        return "qwen2.5-coder:7b"  # Faster, cheaper
```

**Additional Frameworks to Consider:**
- [OK] **AutoGPT:** If available for autonomous task execution -> **DIRECT INSTALL**
- [OK] **vLLM:** For local model serving -> **DIRECT INSTALL**

**Constitution Compliance:** [OK] [OK] [OK]

---

### 2. 🗣️ Debate System Modernization (Real-Time)

**Task:** `V5-DEBATE-001` - Modernize debate system with real-time voting, Redis pub/sub

**Recommended Framework:** **LangGraph** [OK] (Already in use) + **Redis** [OK]

**Why:**
- [OK] **LangGraph:** Already powering orchestrator_graph.py
- [OK] **Redis:** Free & open-source, perfect for pub/sub
- [OK] **Real-Time:** Redis Streams for event-driven debates
- [OK] **State Management:** LangGraph checkpoints for debate state

**Current Status:**
- [OK] LangGraph installed and used
- [WARN]️ Redis mentioned in legacy but not active
- [FAIL] Debate system is file-based (slow, not real-time)

**Implementation Plan:**
```python
# src/agentic/core/debate/debate_graph.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.redis import RedisSaver
import redis

class DebateOrchestrator:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.checkpointer = RedisSaver(self.redis_client)
        
        # Debate state machine
        self.graph = StateGraph(DebateState)
        self.graph.add_node("propose", self._propose_solution)
        self.graph.add_node("vote", self._collect_votes)
        self.graph.add_node("consensus", self._check_consensus)
        self.graph.add_edge("propose", "vote")
        self.graph.add_edge("vote", "consensus")
        self.graph.add_conditional_edges("consensus", self._should_continue)
        
    def _publish_event(self, event_type: str, data: dict):
        """Publish to Redis pub/sub for real-time updates"""
        self.redis_client.publish(f"debate:{self.debate_id}", json.dumps({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }))
```

**Additional Frameworks to Install:**
- [OK] **CrewAI:** Multi-agent coordination -> **DIRECT INSTALL** (auth workaround exists)
- [OK] **AutoGen:** Multi-agent conversations -> **DIRECT INSTALL**
- [OK] **Swarm:** Agent swarm orchestration -> **DIRECT INSTALL**
- [OK] **Redis Streams:** Already using Redis -> **ENABLED**

**Constitution Compliance:** [OK] [OK] [OK]

---

### 3. 🤖 Multi-Agent Coordination (Parallel Execution)

**Task:** `V5-MULTIAGENT-001` - Implement multi-agent coordinator with parallel execution

**Recommended Framework:** **LangGraph** [OK] (Multi-Agent Support)

**Why:**
- [OK] **Already Installed:** langgraph in requirements.txt
- [OK] **Multi-Agent Built-In:** LangGraph supports agent teams
- [OK] **Parallel Execution:** Async nodes run concurrently
- [OK] **State Sharing:** Shared state between agents
- [OK] **No New Dependencies:** Use existing LangGraph

**Current Status:**
- [OK] LangGraph installed
- [WARN]️ Currently single-agent (orchestrator_graph.py)
- [FAIL] No parallel agent execution

**Implementation Plan:**
```python
# src/agentic/core/graphs/multi_agent_graph.py
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent

class MultiAgentOrchestrator:
    def __init__(self):
        self.graph = StateGraph(MultiAgentState)
        
        # Create specialized agents
        self.planner_agent = create_react_agent(
            model=self.llm,
            tools=[planning_tools],
            state_modifier="You are a planning specialist..."
        )
        self.executor_agent = create_react_agent(
            model=self.llm,
            tools=[execution_tools],
            state_modifier="You are a code executor..."
        )
        self.verifier_agent = create_react_agent(
            model=self.llm,
            tools=[verification_tools],
            state_modifier="You are a quality verifier..."
        )
        
        # Parallel execution nodes
        self.graph.add_node("planner", self.planner_agent)
        self.graph.add_node("executor", self.executor_agent)
        self.graph.add_node("verifier", self.verifier_agent)
        
        # Parallel execution: all agents work simultaneously
        self.graph.add_edge("start", "planner")
        self.graph.add_edge("start", "executor")  # Can start in parallel
        self.graph.add_edge("start", "verifier")  # Can start in parallel
```

**Additional Frameworks to Install:**
- [OK] **CrewAI:** Role-based multi-agent -> **DIRECT INSTALL**
- [OK] **AutoGen:** Conversational multi-agent -> **DIRECT INSTALL**
- [OK] **Swarm:** Swarm intelligence -> **DIRECT INSTALL**
- [OK] **LangGraph Multi-Agent:** Native support, already installed -> **USE**

**Constitution Compliance:** [OK] [OK] [OK]

---

### 4. [CHART] Redis Event Bus (Full Integration)

**Task:** `V5-OBSERVE-001` - Full Redis Event Integration with Dashboard

**Recommended Framework:** **Redis** [OK] + **Redis Streams** [OK]

**Why:**
- [OK] **Free & Open-Source:** Redis is BSD licensed
- [OK] **Self-Hostable:** Run locally or in Docker
- [OK] **Event-Driven:** Perfect for pub/sub, streams
- [OK] **Observability:** Real-time event distribution
- [OK] **Already Mentioned:** Legacy code references Redis

**Current Status:**
- [WARN]️ Redis mentioned in legacy/99_ARCHIVE
- [FAIL] Not currently active
- [FAIL] No event bus implementation

**Implementation Plan:**
```python
# src/agentic/infrastructure/event_bus.py
import redis
import json
from typing import Callable, Dict
from dataclasses import dataclass

@dataclass
class Event:
    type: str
    source: str
    data: Dict
    timestamp: str

class RedisEventBus:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url)
        self.subscribers: Dict[str, list[Callable]] = {}
    
    def publish(self, event: Event):
        """Publish event to Redis pub/sub"""
        channel = f"ybis:events:{event.type}"
        self.redis.publish(channel, json.dumps(event.__dict__))
        
        # Also store in Redis Streams for replay
        self.redis.xadd("ybis:events:stream", {
            "type": event.type,
            "source": event.source,
            "data": json.dumps(event.data),
            "timestamp": event.timestamp
        })
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        
        # Redis pub/sub subscription
        pubsub = self.redis.pubsub()
        pubsub.subscribe(f"ybis:events:{event_type}")
        
        # Listen in background thread
        for message in pubsub.listen():
            if message['type'] == 'message':
                event = Event(**json.loads(message['data']))
                callback(event)
```

**Additional Frameworks to Consider:**
- [OK] **RabbitMQ:** If needed for advanced queuing -> **DIRECT INSTALL**
- [OK] **Kafka:** If needed for high-throughput -> **DIRECT INSTALL**
- [OK] **Redis:** Primary choice -> **DIRECT INSTALL**

**Constitution Compliance:** [OK] [OK] [OK]

---

### 5. 🧠 Lesson Engine Automation (LLM-Powered)

**Task:** `V5-LESSON-001` - Upgrade Lesson Engine with LLM-powered postmortem generation

**Recommended Framework:** **Ollama** [OK] (Already in use) + **Instructor** [OK] (Already in requirements.txt)

**Why:**
- [OK] **Ollama:** Already configured, local-first
- [OK] **Instructor:** Already in requirements.txt, structured outputs
- [OK] **No New Dependencies:** Use existing stack
- [OK] **Local-First:** No API keys needed

**Current Status:**
- [OK] Ollama configured
- [OK] Instructor in requirements.txt
- [WARN]️ Lesson Engine exists but uses basic patterns
- [FAIL] No LLM-powered postmortem generation

**Implementation Plan:**
```python
# src/agentic/core/intelligence/lesson_engine_v2.py
from instructor import Instructor
from ollama import Client

class LLMPoweredLessonEngine:
    def __init__(self):
        self.ollama = Client(host='http://localhost:11434')
        self.instructor = Instructor(
            client=self.ollama,
            mode=instructor.Mode.OLLAMA
        )
    
    def generate_postmortem(self, lesson: dict) -> Postmortem:
        """Generate structured postmortem using LLM"""
        prompt = f"""
        Analyze this task failure and generate a postmortem:
        
        Task ID: {lesson['task_id']}
        Status: {lesson['status']}
        Errors: {', '.join(lesson.get('errors', []))}
        
        Generate a structured postmortem with:
        - Root cause analysis
        - Contributing factors
        - Prevention strategies
        """
        
        postmortem = self.instructor.chat(
            model="qwen2.5-coder:32b",
            messages=[{"role": "user", "content": prompt}],
            response_model=Postmortem  # Pydantic model
        )
        
        return postmortem
    
    def cluster_errors(self, lessons: list[dict]) -> ErrorClusters:
        """Cluster similar errors using LLM"""
        # Use instructor for structured clustering
        clusters = self.instructor.chat(
            model="qwen2.5-coder:32b",
            messages=[{"role": "user", "content": self._build_clustering_prompt(lessons)}],
            response_model=ErrorClusters
        )
        return clusters
```

**Additional Frameworks to Consider:**
- [OK] **AutoGPT:** Autonomous task execution -> **DIRECT INSTALL** (if available)
- [OK] **Ollama + Instructor:** Primary choice -> **USE**

**Note:** OpenAI/Anthropic only as optional fallback (not core dependency)

**Constitution Compliance:** [OK] [OK] [OK]

---

## [CHART] Framework Summary

| Task | Framework | Status | Constitution | Notes |
|------|-----------|--------|--------------|-------|
| Multi-Model Router | **LiteLLM** | [OK] Installed | [OK][OK][OK] | Just needs integration |
| Debate System | **LangGraph + Redis** | [OK] LangGraph, [WARN]️ Redis | [OK][OK][OK] | Redis needs setup |
| Multi-Agent | **LangGraph** | [OK] Installed | [OK][OK][OK] | Native multi-agent support |
| Event Bus | **Redis** | [WARN]️ Mentioned | [OK][OK][OK] | Needs implementation |
| Lesson Engine | **Ollama + Instructor** | [OK] Both installed | [OK][OK][OK] | Just needs LLM integration |

---

## [TARGET] Implementation Priority

1. **LiteLLM Router** (Easiest - already installed)
2. **Redis Event Bus** (Foundation for others)
3. **LangGraph Multi-Agent** (Leverage existing)
4. **Debate System** (Uses Redis + LangGraph)
5. **Lesson Engine LLM** (Uses existing Ollama)

---

## [OK] Constitution Compliance Check

All recommended frameworks:
- [OK] **Free & Open-Source** (MIT/Apache/BSD licenses)
- [OK] **Local-First** (Ollama, Redis self-hosted)
- [OK] **Plugin-First** (All can be plugins)
- [OK] **No Proprietary APIs** (No OpenAI/Anthropic required)
- [OK] **Self-Hostable** (All run locally)

---

---

## [LAUNCH] FRAMEWORK INSTALLATION RULE (MANDATORY)

### Rule: "If It Exists, Install It"

**Principle:** If a framework exists that solves a specific problem, we install it directly. No "too complex" excuses. No "we'll build it ourselves" when a ready-made solution exists.

**Installation Checklist:**
1. [OK] **Framework exists?** -> Install it
2. [OK] **Free & Open-Source?** -> Install it
3. [OK] **Can run locally?** -> Install it
4. [OK] **Documentation available?** -> **AUTOMATIC DOWNLOAD** (see below)

**Examples:**
- AutoGPT exists for autonomous tasks? -> **INSTALL**
- CrewAI exists for multi-agent? -> **INSTALL** (auth workaround exists)
- Swarm exists for swarm intelligence? -> **INSTALL**
- AutoGen exists for conversations? -> **INSTALL**

**NO REJECTION REASONS:**
- [FAIL] "Too complex" -> NOT ACCEPTED
- [FAIL] "We can build it" -> NOT ACCEPTED (if framework exists)
- [FAIL] "It's overkill" -> NOT ACCEPTED (if it solves the problem)

---

## 📚 AUTOMATIC DOCUMENTATION DOWNLOAD (MANDATORY)

### Rule: "Every Framework = Full Documentation in RAG"

**Principle:** When installing any framework, automatically download ALL its documentation as markdown and ingest into RAG. This prevents "silly errors" and provides full context.

**Implementation:**
```python
# src/agentic/core/plugins/framework_installer.py
class FrameworkInstaller:
    def install_framework(self, framework_name: str):
        # 1. Install via pip/conda
        subprocess.run(["pip", "install", framework_name])
        
        # 2. Download documentation
        docs = self._download_docs(framework_name)
        
        # 3. Convert to markdown
        markdown_docs = self._convert_to_markdown(docs)
        
        # 4. Ingest into RAG
        self._ingest_to_rag(framework_name, markdown_docs)
    
    def _download_docs(self, framework_name: str) -> dict:
        """Download all documentation from framework's docs site"""
        # Examples:
        # - LangGraph: https://langchain-ai.github.io/langgraph/ -> scrape all pages
        # - LiteLLM: https://docs.litellm.ai/ -> scrape all pages
        # - CrewAI: https://docs.crewai.com/ -> scrape all pages
        # - AutoGPT: GitHub README + docs/ -> download all
        pass
```

**Documentation Sources (Auto-Download):**
- [OK] **Official docs site** (scrape all pages)
- [OK] **GitHub README** (if exists)
- [OK] **GitHub docs/** folder (if exists)
- [OK] **API reference** (if available)
- [OK] **Examples** (if available)

**Storage:**
- `Knowledge/Frameworks/{framework_name}/docs/` -> All markdown docs
- Auto-ingested into ChromaDB RAG
- Available to all agents via RAG search

**Benefits:**
- [OK] No "silly errors" from missing context
- [OK] Full framework knowledge in RAG
- [OK] Agents can reference framework docs
- [OK] Better code generation

---

## 🐳 Docker Integration

### All Services in Docker

**Current Docker Services:**
- [OK] **Redis** -> Event bus, pub/sub
- [OK] **Neo4j** -> Graph database
- [OK] **ChromaDB** -> Vector DB (RAG)
- [OK] **Ollama** -> Local LLM server

**Benefits:**
- [OK] Consistent environment
- [OK] Easy setup (`docker-compose up`)
- [OK] Data persistence (volumes)
- [OK] Health checks
- [OK] Local-first (all self-hosted)

**See:** `docs/specs/V5_DOCKER_STRATEGY.md` for full Docker strategy

---

## 📚 Framework Documentation URLs (Auto-Download List)

When installing these frameworks, automatically download their full documentation:

| Framework | Docs URL | Download Method |
|-----------|----------|-----------------|
| **LangGraph** | https://langchain-ai.github.io/langgraph/ | Scrape all pages |
| **LiteLLM** | https://docs.litellm.ai/ | Scrape all pages |
| **Redis** | https://redis.io/docs/ | Scrape all pages |
| **CrewAI** | https://docs.crewai.com/ | Scrape all pages |
| **AutoGen** | https://microsoft.github.io/autogen/ | Scrape all pages |
| **Swarm** | GitHub README + docs/ | Download all |
| **AutoGPT** | GitHub README + docs/ | Download all |
| **Instructor** | GitHub README + docs/ | Download all |
| **Ollama** | https://ollama.ai/docs/ | Scrape all pages |
| **Temporal** | https://docs.temporal.io/ | Scrape all pages |
| **Ray** | https://docs.ray.io/ | Scrape all pages |
| **Prefect** | https://docs.prefect.io/ | Scrape all pages |
| **SPADE** | https://spadeagents.eu/docs/ | Scrape all pages |
| **Celery** | https://docs.celeryproject.org/ | Scrape all pages |

**Implementation:** Create `scripts/download_framework_docs.py` that:
1. Takes framework name
2. Downloads all docs (scrape or GitHub)
3. Converts to markdown
4. Stores in `Knowledge/Frameworks/{name}/docs/`
5. Ingests into RAG

---

## 📚 References

- **Architecture Principles:** `docs/governance/00_GENESIS/ARCHITECTURE_PRINCIPLES.md`
- **Constitution:** `docs/governance/YBIS_CONSTITUTION.md`
- **Current Stack:** `requirements.txt`
- **Framework Docs (Auto-Download):** See table above

---

**Next Steps:**
1. [OK] **Install ALL recommended frameworks** (CrewAI, AutoGen, Swarm, AutoGPT if available)
2. [OK] **Create framework installer** with auto-doc download
3. [OK] **Download all framework docs** and ingest into RAG
4. [OK] **Start implementation** with full framework knowledge
