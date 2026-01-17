# Architecture Principles (Immutable)

> **Strategic design decisions that govern YBIS_Dev evolution**

**Last Updated:** 2025-12-20
**Status:** IMMUTABLE (requires consensus to change)

---

## [TARGET] Core Philosophy

### Principle 1: Plugin-First Architecture
**Dogma:** "Core is minimal, everything else is a plugin"

**Rationale:**
- Reduce coupling
- Enable framework switching
- Facilitate testing
- Support incremental evolution

**Example:**
```python
# [FAIL] BAD (hard-coded)
planner = SimplePlanner()
executor = AiderExecutor()

# [OK] GOOD (plugin-based)
planner = PluginRegistry.load("@llm/planner")
executor = PluginRegistry.load("@organs/aider")
```

---

### Principle 2: Free & Open-Source Only
**Dogma:** "No proprietary dependencies, no API keys for core functionality"

**Rationale:**
- Cost control
- No vendor lock-in
- Community-driven
- Self-hostable
- Transparency

**Allowed:**
- [OK] MIT/Apache/BSD licensed frameworks
- [OK] Self-hosted services
- [OK] Local execution (Ollama, Docker)

**Forbidden:**
- [FAIL] Proprietary APIs (OpenAI, Anthropic, Tavily)
- [FAIL] Cloud-only services (E2B, Firecrawl)
- [FAIL] Paid tiers as requirements

**Exceptions:**
- Optional plugins for paid services (user choice)
- Development tools (not runtime dependencies)

---

### Principle 3: Incremental Dogfooding
**Dogma:** "Use new framework X to build framework Y"

**Rationale:**
- Test as we build
- Discover issues early
- Prove value immediately
- Avoid "build and forget"

**Pattern:**
```
Phase 1: Add LangChain Tools
    ↓ (use @langchain/file-ops to build...)
Phase 2: Add MCP integration
    ↓ (use @mcp/filesystem to build...)
Phase 3: Add CrewAI orchestration
    ↓ (use CrewAI team to build...)
Phase 4: Next framework
```

**Anti-pattern:**
- Building all plugins then testing
- Adding frameworks "just in case"

---

### Principle 4: Deterministic-First
**Dogma:** "Prefer deterministic tools over LLM-based when possible"

**Rationale:**
- Cost efficiency (no LLM calls)
- Predictability
- Speed
- Debuggability

**Priority Order:**
1. **Pure functions** (calculator, file ops)
2. **Deterministic CLIs** (git, pytest)
3. **Rule-based systems** (linters, parsers)
4. **LLM-based** (planning, generation)

**Example:**
```python
# Prefer this
result = calculator.add(2, 2)  # Deterministic, free, fast

# Over this
result = llm.invoke("What is 2+2?")  # Non-deterministic, costs tokens, slow
```

---

### Principle 5: Observable by Default
**Dogma:** "All tool invocations must be traceable"

**Rationale:**
- Debugging
- Performance optimization
- Cost tracking
- Audit trail

**Implementation:**
```python
@trace_tool
async def invoke(tool_name: str, **kwargs):
    # Auto-logged to observability backend
    return await tool.execute(**kwargs)
```

**Requirements:**
- Every tool call logged
- Execution time tracked
- Errors captured
- Context preserved

---

### Principle 6: Test-First for AI Code
**Dogma:** "AI-generated code must include tests"

**Rationale:**
- AI makes mistakes (proven by T-100)
- Tests catch errors before merge
- Prevents regressions

**Enforcement:**
- Sentinel verification fails without tests
- Pre-commit hooks block untested code
- CI/CD requires test pass

---

### Principle 7: Async-First Execution
**Dogma:** "Long-running tasks must not block"

**Rationale:**
- User responsiveness
- Parallel execution
- Resource efficiency

**Implementation:**
- Use `auto_dispatcher.py` for heavy tasks
- All plugins expose async interface
- Dashboard shows real-time progress

---

### Principle 8: Agent-Agnostic Design
**Dogma:** "Any agent (human or AI) can use the system"

**Rationale:**
- Not locked to Claude/GPT
- Human operators can override
- Cross-agent collaboration

**Requirements:**
- File-based task queue
- Standard tool interface
- Clear documentation (AI_START_HERE.md)

---

## 🏗️ Architectural Layers

### Layer 1: Core (Minimal)
**What:** Plugin loader, registry, protocols
**Size:** <500 lines
**Dependencies:** Python stdlib only

### Layer 2: Infrastructure Plugins
**What:** Observability, LLM proxy, memory
**Examples:** LangFuse, LiteLLM, ChromaDB
**Constraint:** All free & open-source

### Layer 3: Tool Plugins
**What:** Deterministic tools (file, git, calculator)
**Examples:** LangChain Tools, MCP servers
**Constraint:** Local execution preferred

### Layer 4: AI Plugins
**What:** LLM-based tools (planning, code gen)
**Examples:** Aider, SimplePlanner, CrewAI
**Constraint:** Local LLMs default (Ollama)

### Layer 5: Workflow Plugins
**What:** Multi-step orchestrations
**Examples:** OrchestratorGraph, CrewAI teams
**Constraint:** Composable from lower layers

---

## 📋 Decision Framework

**When adding a new dependency, ask:**

1. [OK] Is it free & open-source?
2. [OK] Can it run locally/self-hosted?
3. [OK] Does it fit the plugin model?
4. [OK] Is there dogfooding potential?
5. [OK] Does it replace proprietary tool?

**If all YES -> Add it**
**If any NO -> Find alternative or build minimal version**

---

## 🔄 Evolution Process

### Adding New Framework
1. **Propose:** Write architecture doc (why, how, alternatives)
2. **Review:** Check against principles
3. **Prototype:** Build minimal plugin
4. **Dogfood:** Use it to build next plugin
5. **Document:** Update AI_START_HERE.md
6. **Maintain:** Monitor usage, deprecate if unused

### Removing Framework
1. **Justify:** Why is it obsolete/problematic?
2. **Migrate:** Provide alternative plugin
3. **Deprecate:** Mark as deprecated (1 version)
4. **Remove:** Delete in next version

---

## 🎓 Design Patterns

### Pattern 1: Unified Tool Interface
```python
class ToolProtocol(Protocol):
    name: str
    deterministic: bool
    async def invoke(self, **kwargs) -> Any: ...
```

**All tools (LangChain, MCP, CrewAI, custom) implement this.**

### Pattern 2: Plugin Registration
```python
# Auto-discover plugins
PluginLoader.discover("plugins/")

# Manual registration
ToolRegistry.register("@math/calculator", CalculatorTool())
```

### Pattern 3: Capability-Based Access
```python
# Agents have capabilities
AgentCapabilities.grant("claude", tools=["@file/read", "@git/status"])
AgentCapabilities.grant("aider", tools=["@file/*", "@git/*"])
```

### Pattern 4: Traced Execution
```python
# All tool calls auto-traced
with trace_context(task_id="T-100"):
    result = await ToolRegistry.invoke("@aider/code-gen", ...)
    # Logged to LangFuse/wandb
```

---

## 🚫 Anti-Patterns (Forbidden)

### Anti-Pattern 1: Hard-Coded Dependencies
```python
# [FAIL] BAD
from openai import OpenAI
client = OpenAI(api_key="...")
```

**Why:** Vendor lock-in, not free & open-source

### Anti-Pattern 2: Synchronous Blocking
```python
# [FAIL] BAD
result = expensive_llm_call()  # Blocks for 30 seconds
```

**Why:** User waits, no parallelism

### Anti-Pattern 3: Untestable Code
```python
# [FAIL] BAD
# No tests for this function
def critical_logic():
    ...
```

**Why:** Regressions inevitable

### Anti-Pattern 4: Direct LLM for Deterministic Tasks
```python
# [FAIL] BAD
result = llm.invoke("Calculate 2+2")

# [OK] GOOD
result = calculator.add(2, 2)
```

**Why:** Waste of tokens, unreliable

---

## [CHART] Success Metrics

**Architecture health indicators:**
- [OK] Core code <500 lines (minimal)
- [OK] 90%+ functionality in plugins
- [OK] Zero proprietary dependencies in core
- [OK] 100% tool call observability
- [OK] All AI code has tests
- [OK] CI/CD passes (tests + verification)

**Quality gates:**
- Pre-commit: Emoji check, test coverage
- CI: Full test suite, Sentinel verification
- Deployment: Performance benchmarks

---

## 🔐 Security Principles

### Principle 9: Sandboxed Execution
**Dogma:** "Untrusted code runs in isolation"

**Implementation:**
- Docker containers for code execution
- File system isolation
- Network restrictions

### Principle 10: Principle of Least Privilege
**Dogma:** "Tools only access what they need"

**Example:**
```python
# @file/read can only read, not write
# @git/status can only read status, not commit
```

---

## 📚 References

- **SYSTEM_STATE.md** - Current system architecture
- **CODE_STANDARDS.md** - Coding rules (emoji ban, etc.)
- **AI_START_HERE.md** - Agent onboarding
- **EVOLUTION_PLAN.md** - Plugin roadmap

---

**These principles are IMMUTABLE without consensus.**
**Breaking a principle requires architectural review.**

---

**Approved by:** Claude (Strategic Architect)
**Date:** 2025-12-20
**Version:** 1.0.0
