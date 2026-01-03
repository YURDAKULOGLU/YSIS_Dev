# V5 Framework Catalog
> Constitution-compliant framework recommendations for V5 tasks

**Status:** Draft  
**Date:** 2025-01-03  
**Constitution Compliance:** ✅ Free & Open-Source, ✅ Local-First, ✅ Plugin-First

---

## 📋 V5 Tasks & Framework Mapping

### 1. 📡 Multi-Model Router (Dynamic Model Selection)

**Task:** `V5-ROUTER-001` - Dynamic model selection based on task complexity, risk, and hardware

**Recommended Framework:** **LiteLLM** ✅ (Already in requirements.txt)

**Why:**
- ✅ **Free & Open-Source** (Apache 2.0)
- ✅ **Local-First Support:** Works with Ollama, vLLM, local models
- ✅ **Unified API:** Single interface for 100+ LLM providers
- ✅ **Cost Optimization:** Automatic fallback chains, budget tracking
- ✅ **Already Installed:** `litellm` in requirements.txt

**Current Status:**
- ✅ LiteLLM installed
- ⚠️ Not fully integrated (model_router.py uses custom logic)
- ❌ No dynamic routing based on complexity

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
- ✅ **AutoGPT:** If available for autonomous task execution → **DIRECT INSTALL**
- ✅ **vLLM:** For local model serving → **DIRECT INSTALL**

**Constitution Compliance:** ✅ ✅ ✅

---

### 2. 🗣️ Debate System Modernization (Real-Time)

**Task:** `V5-DEBATE-001` - Modernize debate system with real-time voting, Redis pub/sub

**Recommended Framework:** **LangGraph** ✅ (Already in use) + **Redis** ✅

**Why:**
- ✅ **LangGraph:** Already powering orchestrator_graph.py
- ✅ **Redis:** Free & open-source, perfect for pub/sub
- ✅ **Real-Time:** Redis Streams for event-driven debates
- ✅ **State Management:** LangGraph checkpoints for debate state

**Current Status:**
- ✅ LangGraph installed and used
- ⚠️ Redis mentioned in legacy but not active
- ❌ Debate system is file-based (slow, not real-time)

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
- ✅ **CrewAI:** Multi-agent coordination → **DIRECT INSTALL** (auth workaround exists)
- ✅ **AutoGen:** Multi-agent conversations → **DIRECT INSTALL**
- ✅ **Swarm:** Agent swarm orchestration → **DIRECT INSTALL**
- ✅ **Redis Streams:** Already using Redis → **ENABLED**

**Constitution Compliance:** ✅ ✅ ✅

---

### 3. 🤖 Multi-Agent Coordination (Parallel Execution)

**Task:** `V5-MULTIAGENT-001` - Implement multi-agent coordinator with parallel execution

**Recommended Framework:** **LangGraph** ✅ (Multi-Agent Support)

**Why:**
- ✅ **Already Installed:** langgraph in requirements.txt
- ✅ **Multi-Agent Built-In:** LangGraph supports agent teams
- ✅ **Parallel Execution:** Async nodes run concurrently
- ✅ **State Sharing:** Shared state between agents
- ✅ **No New Dependencies:** Use existing LangGraph

**Current Status:**
- ✅ LangGraph installed
- ⚠️ Currently single-agent (orchestrator_graph.py)
- ❌ No parallel agent execution

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
- ✅ **CrewAI:** Role-based multi-agent → **DIRECT INSTALL**
- ✅ **AutoGen:** Conversational multi-agent → **DIRECT INSTALL**
- ✅ **Swarm:** Swarm intelligence → **DIRECT INSTALL**
- ✅ **LangGraph Multi-Agent:** Native support, already installed → **USE**

**Constitution Compliance:** ✅ ✅ ✅

---

### 4. 📊 Redis Event Bus (Full Integration)

**Task:** `V5-OBSERVE-001` - Full Redis Event Integration with Dashboard

**Recommended Framework:** **Redis** ✅ + **Redis Streams** ✅

**Why:**
- ✅ **Free & Open-Source:** Redis is BSD licensed
- ✅ **Self-Hostable:** Run locally or in Docker
- ✅ **Event-Driven:** Perfect for pub/sub, streams
- ✅ **Observability:** Real-time event distribution
- ✅ **Already Mentioned:** Legacy code references Redis

**Current Status:**
- ⚠️ Redis mentioned in legacy/99_ARCHIVE
- ❌ Not currently active
- ❌ No event bus implementation

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
- ✅ **RabbitMQ:** If needed for advanced queuing → **DIRECT INSTALL**
- ✅ **Kafka:** If needed for high-throughput → **DIRECT INSTALL**
- ✅ **Redis:** Primary choice → **DIRECT INSTALL**

**Constitution Compliance:** ✅ ✅ ✅

---

### 5. 🧠 Lesson Engine Automation (LLM-Powered)

**Task:** `V5-LESSON-001` - Upgrade Lesson Engine with LLM-powered postmortem generation

**Recommended Framework:** **Ollama** ✅ (Already in use) + **Instructor** ✅ (Already in requirements.txt)

**Why:**
- ✅ **Ollama:** Already configured, local-first
- ✅ **Instructor:** Already in requirements.txt, structured outputs
- ✅ **No New Dependencies:** Use existing stack
- ✅ **Local-First:** No API keys needed

**Current Status:**
- ✅ Ollama configured
- ✅ Instructor in requirements.txt
- ⚠️ Lesson Engine exists but uses basic patterns
- ❌ No LLM-powered postmortem generation

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
- ✅ **AutoGPT:** Autonomous task execution → **DIRECT INSTALL** (if available)
- ✅ **Ollama + Instructor:** Primary choice → **USE**

**Note:** OpenAI/Anthropic only as optional fallback (not core dependency)

**Constitution Compliance:** ✅ ✅ ✅

---

## 📊 Framework Summary

| Task | Framework | Status | Constitution | Notes |
|------|-----------|--------|--------------|-------|
| Multi-Model Router | **LiteLLM** | ✅ Installed | ✅✅✅ | Just needs integration |
| Debate System | **LangGraph + Redis** | ✅ LangGraph, ⚠️ Redis | ✅✅✅ | Redis needs setup |
| Multi-Agent | **LangGraph** | ✅ Installed | ✅✅✅ | Native multi-agent support |
| Event Bus | **Redis** | ⚠️ Mentioned | ✅✅✅ | Needs implementation |
| Lesson Engine | **Ollama + Instructor** | ✅ Both installed | ✅✅✅ | Just needs LLM integration |

---

## 🎯 Implementation Priority

1. **LiteLLM Router** (Easiest - already installed)
2. **Redis Event Bus** (Foundation for others)
3. **LangGraph Multi-Agent** (Leverage existing)
4. **Debate System** (Uses Redis + LangGraph)
5. **Lesson Engine LLM** (Uses existing Ollama)

---

## ✅ Constitution Compliance Check

All recommended frameworks:
- ✅ **Free & Open-Source** (MIT/Apache/BSD licenses)
- ✅ **Local-First** (Ollama, Redis self-hosted)
- ✅ **Plugin-First** (All can be plugins)
- ✅ **No Proprietary APIs** (No OpenAI/Anthropic required)
- ✅ **Self-Hostable** (All run locally)

---

---

## 🚀 FRAMEWORK INSTALLATION RULE (MANDATORY)

### Rule: "If It Exists, Install It"

**Principle:** If a framework exists that solves a specific problem, we install it directly. No "too complex" excuses. No "we'll build it ourselves" when a ready-made solution exists.

**Installation Checklist:**
1. ✅ **Framework exists?** → Install it
2. ✅ **Free & Open-Source?** → Install it
3. ✅ **Can run locally?** → Install it
4. ✅ **Documentation available?** → **AUTOMATIC DOWNLOAD** (see below)

**Examples:**
- AutoGPT exists for autonomous tasks? → **INSTALL**
- CrewAI exists for multi-agent? → **INSTALL** (auth workaround exists)
- Swarm exists for swarm intelligence? → **INSTALL**
- AutoGen exists for conversations? → **INSTALL**

**NO REJECTION REASONS:**
- ❌ "Too complex" → NOT ACCEPTED
- ❌ "We can build it" → NOT ACCEPTED (if framework exists)
- ❌ "It's overkill" → NOT ACCEPTED (if it solves the problem)

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
        # - LangGraph: https://langchain-ai.github.io/langgraph/ → scrape all pages
        # - LiteLLM: https://docs.litellm.ai/ → scrape all pages
        # - CrewAI: https://docs.crewai.com/ → scrape all pages
        # - AutoGPT: GitHub README + docs/ → download all
        pass
```

**Documentation Sources (Auto-Download):**
- ✅ **Official docs site** (scrape all pages)
- ✅ **GitHub README** (if exists)
- ✅ **GitHub docs/** folder (if exists)
- ✅ **API reference** (if available)
- ✅ **Examples** (if available)

**Storage:**
- `Knowledge/Frameworks/{framework_name}/docs/` → All markdown docs
- Auto-ingested into ChromaDB RAG
- Available to all agents via RAG search

**Benefits:**
- ✅ No "silly errors" from missing context
- ✅ Full framework knowledge in RAG
- ✅ Agents can reference framework docs
- ✅ Better code generation

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
1. ✅ **Install ALL recommended frameworks** (CrewAI, AutoGen, Swarm, AutoGPT if available)
2. ✅ **Create framework installer** with auto-doc download
3. ✅ **Download all framework docs** and ingest into RAG
4. ✅ **Start implementation** with full framework knowledge
