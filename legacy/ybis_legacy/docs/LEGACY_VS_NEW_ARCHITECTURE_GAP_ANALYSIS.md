# Legacy vs New Architecture: Comprehensive Gap Analysis

**Date:** 2026-01-08  
**Purpose:** Identify all features from legacy (`src/agentic/`) that are missing or incomplete in new core (`src/ybis/`), and define an adapter-first, open-source integration path with full-scope parity.

---

## Executive Summary

The legacy architecture (`src/agentic/`) contains **23+ advanced features** that are either missing, incomplete, or significantly reduced in the new core (`src/ybis/`). This document provides a comprehensive analysis of each gap with migration recommendations.

**Critical Missing Features (Adapter-First, Full-Scope):**
1. MCP server with SSE streaming + minimal external tool surface
2. Spec-first validation/validator workflow (MVP compliance scoring)
3. Unified executor/adapter infrastructure (core stays thin)
4. Observability/health monitor + event bus (service/adapter)
5. MCP messaging/debate toolset (expose existing DebateEngine)

---

## 1. FastMCP-Based MCP Server + SSE Streaming

### Legacy Implementation (`src/agentic/mcp_server.py`)

**Features:**
- ✅ **FastMCP Framework:** Uses `mcp.server.fastmcp.FastMCP` for tool registration
- ✅ **27+ MCP Tools:** Comprehensive toolset including:
  - Task management (`get_tasks`, `claim_task`, `update_task_status`)
  - Agent registration (`register_agent`, `get_agents`, `agent_heartbeat`)
  - Code evolution (`evolve_code`, `deploy_swarm`, `arc_reason`)
  - Dependency analysis (`check_dependency_impact`, `find_circular_dependencies`)
  - Messaging (`send_message`, `read_inbox`, `ack_message`)
  - Debate system (`start_debate`, `reply_to_debate`, `ask_council`)
  - Memory tools (`add_to_memory`, `search_memory`)
  - Spec generation (`create_spec_kit`)
- ✅ **SSE Streaming:** Server-Sent Events for real-time updates (implied by FastMCP)
- ✅ **Bridge Integration:** EvoAgent, Swarm, Poetiq, Interpreter bridges
- ✅ **GraphDB Integration:** Neo4j-based dependency analysis
- ✅ **Cognee Integration:** Memory system with graph+vector search

**Code Structure:**
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("YBIS Factory Skills")

@mcp.tool()
def tool_name(...) -> str:
    """Tool description"""
    # Implementation
    return result

if __name__ == "__main__":
    mcp.run()  # Starts server with SSE support
```

### New Core Implementation (`src/ybis/services/mcp_server.py`)

**Current State:**
- ❌ **No FastMCP:** Uses custom `MCPServer` class (not FastMCP framework)
- ❌ **Limited Tools:** Only 7 tools:
  - `task_create`, `task_status`, `artifact_read`, `approval_write`
  - `task_claim`, `task_complete`, `artifact_write`
- ❌ **No SSE:** No streaming support
- ❌ **No Bridge Integration:** Missing EvoAgent, Swarm, Poetiq bridges
- ❌ **No GraphDB Tools:** Missing dependency analysis tools
- ❌ **No Messaging Tools:** Missing `send_message`, `read_inbox`, etc.
- ❌ **No Debate Tools:** Missing `start_debate`, `reply_to_debate`, `ask_council`
- ❌ **No Memory Tools:** Missing `add_to_memory`, `search_memory`
- ❌ **No Spec Tools:** Missing `create_spec_kit`

**Gap Analysis:**
- **Missing:** 20+ MCP tools
- **Missing:** FastMCP framework integration
- **Missing:** SSE streaming capability
- **Missing:** Bridge integrations (EvoAgent, Swarm, Poetiq, Interpreter)
- **Missing:** GraphDB-based dependency analysis
- **Missing:** Cognee memory integration

**Migration Priority:** 🔴 **CRITICAL**

**Recommendation (Adapter-First, Full Scope):**
1. Adopt FastMCP framework for a modern SSE-compatible server
2. Implement the full MCP tool surface (parity with legacy feature set)
3. Add SSE streaming support early for external clients
4. Integrate bridges as adapters (not core)
5. Integrate GraphDB/Cognee as adapters behind policy flags

---

## 2. Spec-First Validation/Validator Workflow

### Legacy Implementation (`src/agentic/core/plugins/spec_first_workflow.py`)

**Features:**
- ✅ **SpecFirstWorkflow Class:** Complete orchestration engine
- ✅ **7-Phase Workflow:**
  1. SPEC GENERATION: Generate or validate SPEC.md exists
  2. SPEC VALIDATION: Parse and validate spec completeness
  3. PLAN CREATION: Create PLAN.md (existing planner)
  4. PLAN VALIDATION: Validate plan against spec requirements
  5. IMPLEMENTATION: Execute plan (existing executor)
  6. IMPL VALIDATION: Validate implementation against spec
  7. REPORTING: Generate compliance report
- ✅ **SpecValidator Class:** (`src/agentic/core/plugins/spec_validator.py`)
  - Parse SPEC.md files (extract requirements, criteria, constraints)
  - Validate plans against specs
  - Validate implementations against specs
  - Score compliance (0.0-1.0)
  - Generate validation reports
  - LLM-assisted semantic validation
- ✅ **SpecWriterAgent:** (`src/agentic/core/plugins/spec_writer_agent.py`)
  - Template-based generation (feature/refactor/bugfix/architecture)
  - LLM-powered placeholder filling
  - Interactive review and editing
  - Validation and quality checks
- ✅ **Spec Templates:** (`src/agentic/core/plugins/spec_templates.py`)
  - FEATURE_TEMPLATE
  - REFACTOR_TEMPLATE
  - BUGFIX_TEMPLATE
  - ARCHITECTURE_TEMPLATE
- ✅ **WorkflowConfig:** Configurable validation gates
- ✅ **WorkflowResult:** Comprehensive result reporting

**Code Structure:**
```python
class SpecFirstWorkflow:
    def __init__(self, config: WorkflowConfig, llm_provider=None):
        self.spec_writer = SpecWriterAgent(llm_provider)
        self.spec_validator = SpecValidator(llm_provider)
    
    async def execute(self, task_id: str, workspace_path: Path) -> WorkflowResult:
        # Phase 1: Generate/validate spec
        # Phase 2: Validate spec
        # Phase 3: Create plan
        # Phase 4: Validate plan
        # Phase 5: Execute
        # Phase 6: Validate implementation
        # Phase 7: Report
```

### New Core Implementation (`src/ybis/orchestrator/graph.py`)

**Current State:**
- ⚠️ **Partial Spec Generation:** `spec_node` generates `SPEC.md` but:
  - ❌ No spec validation
  - ❌ No plan validation against spec
  - ❌ No implementation validation against spec
  - ❌ No compliance scoring
  - ❌ No spec templates
  - ❌ No SpecWriterAgent
  - ❌ No SpecValidator
- ✅ **Spec Generation:** Basic LLM-based spec generation exists
- ❌ **No Validation Workflow:** Missing 7-phase validation pipeline

**Gap Analysis:**
- **Missing:** SpecValidator class
- **Missing:** SpecWriterAgent class
- **Missing:** Spec templates
- **Missing:** Plan validation against spec
- **Missing:** Implementation validation against spec
- **Missing:** Compliance scoring
- **Missing:** WorkflowConfig and WorkflowResult

**Migration Priority:** 🔴 **CRITICAL**

**Recommendation (Adapter-First, Full Scope):**
1. Implement `SpecValidator` with compliance scoring
2. Add full validation nodes to LangGraph (spec, plan, implementation)
3. Integrate score thresholds into gate logic
4. Provide SpecWriter/templating as optional adapters (open-source first)

---

## 3. Unified Executor/Adapter Infrastructure

### Legacy Implementation

**Features:**
- ✅ **ExecutorProtocol:** (`src/agentic/core/protocols.py`)
  - Standardized interface for all executors
  - `execute(plan, sandbox_path, error_history, retry_count) -> CodeResult`
- ✅ **Multiple Executors:**
  - `AiderExecutor` (`src/agentic/core/plugins/aider_executor.py`)
  - `AiderExecutorEnhanced` (`src/agentic/core/plugins/aider_executor_enhanced.py`)
  - `OpenHandsExecutor` (`src/agentic/core/executors/openhands_executor.py`)
  - `PatchExecutor` (`src/agentic/core/plugins/patch_executor.py`)
  - `SimpleExecutor` (`src/agentic/core/plugins/simple_executor.py`)
- ✅ **Plugin System:** (`src/agentic/core/plugin_system/`)
  - `ToolProtocol`: Base interface for tools
  - `ToolRegistry`: Central registry for tools
  - `PluginLoader`: Dynamic plugin loading
  - `observability.py`: Plugin observability
  - `llm_proxy.py`: LLM proxy for plugins
- ✅ **Built-in Tools:** (`src/agentic/core/plugins/builtin/`)
  - `calculator.py`
  - `file_ops.py`
  - `git_ops.py`
  - `open_swe.py`
- ✅ **Unified Interface:** All executors implement same protocol

**Code Structure:**
```python
class ExecutorProtocol(Protocol):
    async def execute(
        self, plan: Plan, sandbox_path: str,
        error_history: list[str] | None = None, retry_count: int = 0
    ) -> CodeResult:
        ...

class AiderExecutor(ExecutorProtocol):
    async def execute(self, plan, sandbox_path, ...):
        # Aider-specific implementation
        return CodeResult(...)
```

### New Core Implementation (`src/ybis/adapters/`)

**Current State:**
- ✅ **ExecutorProtocol:** (`src/ybis/contracts/protocol.py`)
  - Similar interface exists
- ✅ **LocalCoderExecutor:** (`src/ybis/adapters/local_coder.py`)
  - Native Ollama-based executor
- ⚠️ **AiderExecutor:** (`src/ybis/adapters/aider.py`)
  - Exists but minimal
- ❌ **No Plugin System:** Missing plugin infrastructure
- ❌ **No Tool Registry:** Missing centralized tool registry
- ❌ **No Plugin Loader:** Missing dynamic plugin loading
- ❌ **No Built-in Tools:** Missing calculator, file_ops, git_ops
- ❌ **No OpenHandsExecutor:** Missing OpenHands integration
- ❌ **No PatchExecutor:** Missing patch-based executor

**Gap Analysis:**
- **Missing:** Plugin system infrastructure
- **Missing:** Tool registry
- **Missing:** Plugin loader
- **Missing:** Built-in tools
- **Missing:** OpenHands executor
- **Missing:** Patch executor
- **Missing:** Enhanced Aider executor

**Migration Priority:** 🟡 **HIGH**

**Recommendation:**
1. Port plugin system to `src/ybis/adapters/plugin_system/`
2. Port tool registry and loader
3. Port built-in tools
4. Add OpenHands executor adapter
5. Add patch executor adapter
6. Enhance Aider executor

---

## 4. Observability/Health Monitor + Event Bus

### Legacy Implementation

**Health Monitor:**
- ✅ **HealthMonitor Class:** (`src/agentic/core/plugins/health_monitor.py`)
  - System health checks with auto-remediation
  - Checks: RAG index health, execution metrics, error patterns, config issues
  - Auto-creates remediation tasks
  - Generates health reports
- ✅ **Dashboard Component:** (`src/dashboard/components/health_monitor.py`)
  - Streamlit-based health dashboard
  - Task statistics
  - Debate statistics
  - CPU/RAM monitoring
  - Integrity checklist

**Event Bus:**
- ✅ **EventBus Class:** (`src/agentic/infrastructure/redis_queue.py`)
  - Redis-based pub/sub for system observability
  - Thread-safe singleton
  - Supports sync and async operations
  - Standardized event types (task.created, task.completed, etc.)
  - Event namespace support
- ✅ **Unified Message Manager:** (`src/agentic/infrastructure/unified_message_manager.py`)
  - Single interface for multiple backends (Redis, file-based, DB, SPADE XMPP, MCP)
  - Backend abstraction
  - Automatic fallback

**Observability:**
- ✅ **YBISTracer:** (`src/agentic/core/observability/tracer.py`)
  - Langfuse integration
  - Tracing for LLM calls and workflows
  - Graceful degradation

**Code Structure:**
```python
# Event Bus
from src.agentic.infrastructure.redis_queue import event_bus
event_bus.publish("task.completed", {"task_id": "TASK-123"})

# Health Monitor
monitor = HealthMonitor(auto_create_tasks=True)
issues = monitor.run_all_checks()

# Unified Message Manager
manager = UnifiedMessageManager(default_backend="redis")
await manager.send(message, backend="redis")
```

### New Core Implementation

**Current State:**
- ❌ **No Health Monitor:** Missing health monitoring system
- ❌ **No Event Bus:** Missing Redis-based event bus
- ❌ **No Unified Message Manager:** Missing messaging abstraction
- ⚠️ **Minimal Observability:** Only journal events (no pub/sub)
- ❌ **No Dashboard Health Component:** Missing health dashboard
- ❌ **No Tracer:** Missing Langfuse integration

**Gap Analysis:**
- **Missing:** HealthMonitor class
- **Missing:** EventBus class
- **Missing:** UnifiedMessageManager class
- **Missing:** Redis pub/sub infrastructure
- **Missing:** Standardized event types
- **Missing:** Health dashboard component
- **Missing:** Langfuse tracer

**Migration Priority:** 🟡 **HIGH**

**Recommendation:**
1. Port EventBus to `src/ybis/services/event_bus.py`
2. Port HealthMonitor to `src/ybis/services/health_monitor.py`
3. Port UnifiedMessageManager to `src/ybis/services/messaging.py`
4. Add event publishing to all syscalls
5. Add health dashboard component
6. Integrate Langfuse tracer

---

## 5. Deep LlamaIndex/Knowledge Integration

### Legacy Implementation

**RAG Integration:**
- ✅ **LocalRAG:** (`src/agentic/tools/local_rag.py`)
  - ChromaDB-based vector store
  - Ollama embeddings (nomic-embed-text)
  - Code-aware document indexing
  - Semantic search for context retrieval
  - Whitelist/blacklist pattern filtering
  - Relevance threshold gating
- ✅ **RAGAwarePlanner:** (`src/agentic/core/plugins/rag_aware_planner.py`)
  - Wraps base planner with RAG context
  - Queries RAG for similar past tasks
  - Injects retrieved context into planning
- ✅ **RAGMemory:** (`src/agentic/core/plugins/rag_memory.py`)
  - Persistent RAG-based memory
  - Success/failure learning
- ✅ **Delta Ingestion:** Automatic delta-ingestion of modified files
- ✅ **Knowledge Base:** Persistent knowledge base with codebase context

**LlamaIndex Integration:**
- ⚠️ **LlamaIndex Adapter:** (`src/ybis/adapters/llamaindex_adapter.py`)
  - Exists in new core but minimal
  - Only basic indexing

**Code Structure:**
```python
# LocalRAG
rag = LocalRAG()
rag.index_directory("src/")
results = rag.query("How does task execution work?", n_results=5)

# RAGAwarePlanner
planner = RAGAwarePlanner(base_planner, rag_memory)
plan = await planner.plan(task, context)
```

### New Core Implementation

**Current State:**
- ⚠️ **VectorStore:** (`src/ybis/data_plane/vector_store.py`)
  - Basic ChromaDB integration
  - Missing whitelist/blacklist filtering
  - Missing relevance threshold gating
  - Missing code-aware indexing
- ⚠️ **LlamaIndex Adapter:** (`src/ybis/adapters/llamaindex_adapter.py`)
  - Basic indexing exists
  - Missing advanced context management
  - Missing query optimization
- ❌ **No RAGAwarePlanner:** Missing RAG-aware planning wrapper
- ❌ **No RAGMemory:** Missing RAG-based memory system
- ❌ **No Delta Ingestion:** Missing automatic delta-ingestion
- ❌ **No LocalRAG Tool:** Missing comprehensive RAG tool

**Gap Analysis:**
- **Missing:** LocalRAG tool with filtering
- **Missing:** RAGAwarePlanner wrapper
- **Missing:** RAGMemory system
- **Missing:** Delta ingestion
- **Missing:** Advanced LlamaIndex features
- **Missing:** Code-aware indexing

**Migration Priority:** 🟡 **MEDIUM**

**Recommendation:**
1. Port LocalRAG to `src/ybis/services/local_rag.py`
2. Port RAGAwarePlanner to `src/ybis/orchestrator/rag_aware_planner.py`
3. Port RAGMemory to `src/ybis/services/rag_memory.py`
4. Add delta ingestion to workspace changes
5. Enhance LlamaIndex adapter with advanced features

---

## 6. MCP Messaging/Debate Toolset

### Legacy Implementation (`src/agentic/mcp_server.py`)

**Messaging Tools:**
- ✅ `send_message`: Send message to agent or broadcast
- ✅ `read_inbox`: Read messages for agent
- ✅ `ack_message`: Acknowledge message
- ✅ Message types: direct, broadcast, debate, task_assignment
- ✅ Priority levels: CRITICAL, HIGH, NORMAL, LOW
- ✅ Reply threading support
- ✅ Tags and metadata

**Debate Tools:**
- ✅ `start_debate`: Start debate with topic and proposal
- ✅ `reply_to_debate`: Reply to existing debate
- ✅ `ask_council`: Ask LLM Council for consensus
- ✅ Debate archiving in `Knowledge/Messages/debates/`
- ✅ Debate status tracking (open/closed)
- ✅ Council bridge integration (3-stage deliberation)

**Code Structure:**
```python
@mcp.tool()
def send_message(to: str, subject: str, content: str, ...) -> str:
    # Insert into messages table
    # Broadcast via event bus
    return "SUCCESS: Message sent"

@mcp.tool()
def start_debate(topic: str, proposal: str, ...) -> str:
    # Archive debate
    # Broadcast via messaging
    return "SUCCESS: Debate started"
```

### New Core Implementation (`src/ybis/services/mcp_server.py`)

**Current State:**
- ❌ **No Messaging Tools:** Missing all messaging tools
- ❌ **No Debate Tools:** Missing all debate tools
- ✅ **Debate Engine:** (`src/ybis/services/debate.py`)
  - Exists but not exposed via MCP
  - No debate archiving
  - No debate status tracking
- ❌ **No Message Database:** Missing messages table
- ❌ **No Council Integration:** Missing council bridge

**Gap Analysis:**
- **Missing:** All messaging MCP tools
- **Missing:** All debate MCP tools
- **Missing:** Messages database schema
- **Missing:** Debate archiving system
- **Missing:** Council bridge integration

**Migration Priority:** 🟡 **HIGH**

**Recommendation (Adapter-First, Full Scope):**
1. Add messages table to control plane DB
2. Expose messaging + debate tools via MCP (full legacy parity)
3. Integrate DebateEngine with MCP tools
4. Add debate archiving system
5. Keep council bridge as optional adapter

---

## 7. Additional Missing Features

### 7.1 Code Graph & Dependency Analysis

**Legacy:**
- ✅ **CodeGraph:** (`src/agentic/skills/code_graph.py`)
  - Extracts classes, functions, calls
  - Dependency mapping
- ✅ **GraphDB:** (`src/agentic/infrastructure/graph_db.py`)
  - Neo4j-based dependency graph
  - Impact analysis
  - Circular dependency detection
  - Critical files identification

**New Core:**
- ✅ **CodeGraph:** (`src/ybis/services/code_graph.py`)
  - Exists but uses Pyan (not Neo4j)
  - Missing GraphDB integration
  - Missing Neo4j-based analysis

**Gap:** Missing Neo4j GraphDB integration

---

### 7.2 Model Router

**Legacy:**
- ✅ **ModelRouter:** (`src/agentic/core/plugins/model_router.py`)
  - Routes requests to appropriate LLM
  - Cost optimization
  - Quality-based routing

**New Core:**
- ❌ **Missing:** No model router

**Gap:** Missing model routing system

---

### 7.3 Task Board Manager

**Legacy:**
- ✅ **TaskBoardManager:** (`src/agentic/core/plugins/task_board_manager.py`)
  - Task board management
  - Self-healing capabilities
  - Stale task detection

**New Core:**
- ⚠️ **Partial:** Staleness detector exists but no task board manager

**Gap:** Missing task board management

---

### 7.4 Story Sharder

**Legacy:**
- ✅ **StorySharder:** (`src/agentic/core/plugins/story_sharder.py`)
  - Breaks large tasks into smaller stories
  - Story prioritization

**New Core:**
- ❌ **Missing:** No story sharding

**Gap:** Missing task decomposition

---

### 7.5 Plan Processor

**Legacy:**
- ✅ **PlanProcessor:** (`src/agentic/core/plugins/plan_processor.py`)
  - Processes plans with glob patterns
  - Resolves file paths
  - Validates plan structure

**New Core:**
- ❌ **Missing:** No plan processor

**Gap:** Missing plan processing

---

### 7.6 Context Limiter

**Legacy:**
- ✅ **ContextLimiter:** (`src/agentic/core/plugins/context_limiter.py`)
  - Limits context size for LLM calls
  - Token optimization

**New Core:**
- ❌ **Missing:** No context limiter

**Gap:** Missing context optimization

---

### 7.7 Git Manager

**Legacy:**
- ✅ **GitManager:** (`src/agentic/core/plugins/git_manager.py`)
  - Advanced Git operations
  - Commit management
  - Branch management

**New Core:**
- ⚠️ **Basic:** Only basic git syscalls exist

**Gap:** Missing advanced Git management

---

### 7.8 Artifact Generator

**Legacy:**
- ✅ **ArtifactGenerator:** (`src/agentic/core/plugins/artifact_generator.py`)
  - Generates comprehensive artifacts
  - Report generation

**New Core:**
- ⚠️ **Partial:** Basic artifacts exist but not comprehensive

**Gap:** Missing comprehensive artifact generation

---

### 7.9 CrewAI Integration

**Legacy:**
- ✅ **CrewAI Executor:** (`src/agentic/core/plugins/crewai_executor.py`)
- ✅ **CrewAI Planner:** (`src/agentic/core/plugins/crewai_planner.py`)
- ✅ **CrewAI Bridge:** (`src/agentic/bridges/crewai_bridge.py`)

**New Core:**
- ❌ **Missing:** No CrewAI integration

**Gap:** Missing CrewAI multi-agent framework

---

### 7.10 Docker Executor

**Legacy:**
- ✅ **DockerExecutor:** (`src/agentic/core/plugins/docker_executor.py`)
  - Docker-based sandbox execution

**New Core:**
- ⚠️ **Partial:** E2B sandbox exists but no Docker executor

**Gap:** Missing Docker-based execution

---

## Summary Table

| Feature | Legacy | New Core | Priority | Status |
|---------|--------|----------|----------|--------|
| FastMCP Server | ✅ 27+ tools | ❌ 7 tools | 🔴 CRITICAL | Missing |
| SSE Streaming | ✅ | ❌ | 🔴 CRITICAL | Missing |
| Spec Validator | ✅ | ❌ | 🔴 CRITICAL | Missing |
| Spec Writer Agent | ✅ | ❌ | 🔴 CRITICAL | Missing |
| Plan Validation | ✅ | ❌ | 🔴 CRITICAL | Missing |
| Implementation Validation | ✅ | ❌ | 🔴 CRITICAL | Missing |
| Plugin System | ✅ | ❌ | 🟡 HIGH | Missing |
| Tool Registry | ✅ | ❌ | 🟡 HIGH | Missing |
| Event Bus | ✅ | ❌ | 🟡 HIGH | Missing |
| Health Monitor | ✅ | ❌ | 🟡 HIGH | Missing |
| Unified Message Manager | ✅ | ❌ | 🟡 HIGH | Missing |
| Messaging MCP Tools | ✅ | ❌ | 🟡 HIGH | Missing |
| Debate MCP Tools | ✅ | ❌ | 🟡 HIGH | Missing |
| LocalRAG Tool | ✅ | ⚠️ Basic | 🟡 MEDIUM | Partial |
| RAGAwarePlanner | ✅ | ❌ | 🟡 MEDIUM | Missing |
| RAGMemory | ✅ | ❌ | 🟡 MEDIUM | Missing |
| GraphDB (Neo4j) | ✅ | ❌ | 🟡 MEDIUM | Missing |
| Model Router | ✅ | ❌ | 🟢 LOW | Missing |
| Task Board Manager | ✅ | ⚠️ Partial | 🟢 LOW | Partial |
| Story Sharder | ✅ | ❌ | 🟢 LOW | Missing |
| Plan Processor | ✅ | ❌ | 🟢 LOW | Missing |
| Context Limiter | ✅ | ❌ | 🟢 LOW | Missing |
| Git Manager | ✅ | ⚠️ Basic | 🟢 LOW | Partial |
| Artifact Generator | ✅ | ⚠️ Partial | 🟢 LOW | Partial |
| CrewAI Integration | ✅ | ❌ | 🟢 LOW | Missing |
| Docker Executor | ✅ | ⚠️ E2B | 🟢 LOW | Partial |

---

## Migration Roadmap

### Phase 1: Critical Features (Week 1-2)
1. FastMCP server migration (full tool surface + SSE)
2. Spec validation full workflow with gate integration
3. Event bus as a service/adapter (not core)

### Phase 2: High Priority (Week 3-4)
1. Plugin system (adapter registry)
2. Health monitor service
3. Messaging/debate tools parity
4. Unified message manager (adapter)

### Phase 3: Medium Priority (Week 5-6)
1. Deep RAG integration (policy-gated)
2. GraphDB integration (adapter)
3. Advanced LlamaIndex features (adapter)

### Phase 4: Low Priority (Week 7+)
1. Model router
2. Story sharder
3. CrewAI integration
4. Other missing features

---

## Recommendations

1. **Prioritize FastMCP Migration:** External interface should be SSE-ready with full tool surface parity
2. **Implement Spec Validation Workflow:** Full spec/plan/implementation compliance with gate integration
3. **Add Event Bus as Service:** Keep core thin; use adapter pattern
4. **Port Plugin System as Registry:** Extensibility without core bloat
5. **Integrate Health Monitor as Service:** Production ops without core coupling

---

## Adapter-First, Open-Source Integration Policy

**Principle:** Legacy code is read-only reference. New capabilities MUST be integrated through adapters to mature open-source tools where possible. Core remains minimal (policy, gates, syscalls, contracts).

**Implications:**
- Prefer open-source libraries/frameworks for MCP, spec validation, messaging, vector/graph stores.
- Build adapters around these tools; do not copy legacy implementations.
- Keep feature toggles in policy and run adapters only when enabled.

---

## Enforcement Plan (Non-Negotiable)

**Policy Gates**
- Add spec compliance scoring into `gate_report.json` and block on failure.
- Enforce protected paths and adapter enablement via policy.

**Core Boundary Lint**
- Add a static lint script to prevent adapter/service imports inside core modules.
- Fail CI if core modules import adapter packages directly.

**Adapter Registry**
- Create a registry module to explicitly register and enable adapters.
- Policy selects adapters by name; no direct instantiation in core.

**CI**
- Add CI workflow to run verifier + gate checks on PRs.
- Block merges if gates fail or core boundary lint fails.

---

## Risk Register

1) **God Object Regression**
- Risk: MCP server or orchestrator becomes a monolith.
- Mitigation: Tool modules in adapters; keep server thin.

2) **Adapter-First Drift**
- Risk: Legacy patterns reintroduced into core.
- Mitigation: Core boundary lint + codeowner review.

3) **Spec-First Becomes Optional**
- Risk: Specs exist but no enforcement.
- Mitigation: Gate spec compliance score with hard threshold.

4) **CI Bypass**
- Risk: Manual changes merge without gates.
- Mitigation: Mandatory CI + protected branch rules.

5) **Optional Adapters Become Required**
- Risk: Hidden dependency coupling to optional services.
- Mitigation: Policy-gated adapter selection + explicit dependency extras.

---

## Executor Task List (Adapter-First, Full-Scope)

**Rules:** Legacy is read-only. No code copy. Use open-source libs via adapters. All changes must respect syscalls, policy gating, and protected paths.

### Task A: MCP FastMCP Server (Full Tool Surface)
**Objective:** Replace the thin MCP class with a FastMCP-based server that exposes the full tool set via adapters.
**Deliverables:**
- `src/ybis/services/mcp_server.py` (FastMCP runner + tool registration)
- `src/ybis/services/mcp_tools/` (tool modules organized by domain)
- `scripts/ybis_mcp_server.py` entrypoint to run the server
- `docs/mcp/TOOLS_REFERENCE.md` (list of tools + inputs/outputs)
**Requirements:**
- SSE enabled.
- Tools include: task/claim/status/complete, artifact_read/write, approval_write, messaging, debate, memory (adapter stubs ok), dependency/graph analysis.
- Adapters only: no legacy code copy.

### Task B: Spec-First Validation Workflow (Full Scope)
**Objective:** Add full spec validation pipeline into the LangGraph workflow.
**Deliverables:**
- `src/ybis/orchestrator/spec_validator.py` (spec parsing + compliance scoring)
- `src/ybis/orchestrator/spec_templates.py` (feature/refactor/bugfix/arch templates or adapter hooks)
- New graph nodes: `validate_spec_node`, `validate_plan_node`, `validate_impl_node`
- Gate integration: compliance score in `gate_report.json`
**Requirements:**
- Spec/plan/implementation validation phases must run end-to-end.
- Score thresholds configurable in policy.

### Task C: Messaging + Debate MCP Tools
**Objective:** Expose messaging and debate flows via MCP tools using adapters.
**Deliverables:**
- Messages table in control-plane DB (migration + schema)
- MCP tools: `send_message`, `read_inbox`, `ack_message`, `start_debate`, `reply_to_debate`
- Debate archive in `workspaces/<task>/runs/<run>/artifacts/` or `docs/debates/`
**Requirements:**
- Adapter-first: use existing DebateEngine, add storage/transport adapters as needed.

### Task D: Observability/Event Bus Service
**Objective:** Add observability as a service (not core) with adapter hooks.
**Deliverables:**
- `src/ybis/services/event_bus.py` (interface + adapter registry)
- `src/ybis/services/health_monitor.py` (health checks + run telemetry)
- Policy toggles for enabling/disabling adapters
**Requirements:**
- No direct legacy port; use OSS adapters (e.g., Redis, NATS) if enabled.

### Task E: Memory + Graph Adapters
**Objective:** Implement adapters for vector + graph backends (policy-gated).
**Deliverables:**
- `src/ybis/adapters/vector_store_*` (Chroma/Qdrant)
- `src/ybis/adapters/graph_store_*` (Neo4j)
- Policy-driven selection and graceful fallback
**Requirements:**
- No warnings in default/e2e when adapters are disabled.

### Task F: Unified Executor Registry
**Objective:** Provide a unified executor interface with adapter-based executors.
**Deliverables:**
- `src/ybis/executors/registry.py` (executor registry + interface)
- Adapters: Aider/OpenHands/Docker (stubs ok)
**Requirements:**
- Policy selects executor by name.

### Task G: Framework Docs Auto-Sync
**Objective:** Auto-download framework docs to local cache on install.
**Deliverables:**
- `scripts/framework_docs_sync.py`
- `configs/framework_docs.yaml`
- Local cache: `docs/frameworks/<name>/`
**Requirements:**
- Policy gating for network access.
- Version/commit metadata file per framework.

### Task H: Task Board Manager + Story Sharder
**Objective:** Restore task-board and sharding capabilities as services/adapters.
**Deliverables:**
- `src/ybis/services/task_board.py`
- `src/ybis/services/story_sharder.py`
**Requirements:**
- Adapter-first; no legacy copy.

### Task I: Model Router
**Objective:** Add model router with cost/latency policies.
**Deliverables:**
- `src/ybis/services/model_router.py`
- Policy configuration (models/tiers/routing rules)
**Requirements:**
- Works with local-only providers by default.

### Task J: Verification & Artifact Expansion
**Objective:** Expand verification artifacts and quality evidence.
**Deliverables:**
- `artifacts/` schema updates (if needed)
- Additional reports (dependency impact, spec compliance summary)
**Requirements:**
- Deterministic outputs, no legacy code copy.

---

## Execution Order (Recommended)
1. Task A (FastMCP server + tool surface)
2. Task B (Spec-first validation)
3. Task C (Messaging/debate)
4. Task D (Observability/event bus)
5. Task E (Memory/graph adapters)
6. Task F (Unified executor registry)
7. Task G (Docs auto-sync)
8. Task H (Task board + story sharder)
9. Task I (Model router)
10. Task J (Verification/artifacts expansion)

---

## Conclusion

The new core (`src/ybis/`) is **architecturally sound** but **functionally incomplete** compared to legacy (`src/agentic/`). **23+ features** need to be migrated or re-implemented to achieve feature parity.

**Estimated Migration Effort:** 6-8 weeks for critical and high-priority features.

---

## References

- **Legacy MCP Server:** `src/agentic/mcp_server.py`
- **Legacy Spec Workflow:** `src/agentic/core/plugins/spec_first_workflow.py`
- **Legacy Event Bus:** `src/agentic/infrastructure/redis_queue.py`
- **Legacy Health Monitor:** `src/agentic/core/plugins/health_monitor.py`
- **New Core MCP:** `src/ybis/services/mcp_server.py`
- **New Core Orchestrator:** `src/ybis/orchestrator/graph.py`


