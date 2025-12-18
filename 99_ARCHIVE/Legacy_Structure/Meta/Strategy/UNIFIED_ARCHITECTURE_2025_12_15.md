# 🏗️ YBIS_Dev Unified Architecture

**Date:** 2025-12-15
**Status:** 🟡 INTEGRATION IN PROGRESS
**System:** Multi-Layer AI Development Assistant

---

## 🎯 System Purpose

`.YBIS_Dev` is a **unified, multi-layer AI development system** that orchestrates:
- **CLI Agents** (Claude, Gemini) - Strategic work via Anthropic/Google APIs
- **Local Agents** (Ollama) - Tactical work via local LLMs
- **MCP Servers** - Tool bridges for Cursor/VS Code/Claude Desktop
- **Multi-Agent Framework** - Constitutional coordination between agents

**NOT** three separate systems - they're **integrated layers** of one architecture.

---

## 📊 The 5-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 5: USER INTERFACES                                │
│ ├─ Cursor IDE (MCP)                                     │
│ ├─ VS Code (MCP)                                        │
│ ├─ Claude Desktop (MCP)                                 │
│ └─ CLI (Direct)                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: COORDINATION (Multi-Agent Framework)           │
│ ├─ Constitution v2.0 (Governance)                       │
│ ├─ TASK_BOARD.md (Lean Protocol v3.1)                   │
│ ├─ agent_messages.json (A2A Communication)              │
│ └─ auto_dispatcher.py (Task Assignment)                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: ORCHESTRATION (Workflow Engines)               │
│ ├─ orchestrator_v2.py (LangGraph - 7-phase)             │
│ ├─ planning_crew.py (CrewAI - Multi-agent)              │
│ └─ IntelligentRouter (Cloud vs Local routing)           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: EXECUTION (Agents)                             │
│ ├─ CLI Agents (Claude, Gemini) - via APIs               │
│ └─ Local Agents (Ollama) - Architect, Developer, QA     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 1: TOOLS & INFRASTRUCTURE                         │
│ ├─ MCP Server (ybis_server.py)                          │
│ ├─ Sandbox Manager (isolated testing)                   │
│ ├─ File Ops, Repo Mapper, Git Ops                       │
│ ├─ Local RAG (knowledge base)                           │
│ └─ AI_AGENT_PROTOCOLS.md (context loading)              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Layer Details

### Layer 1: Tools & Infrastructure (Tier 1)

**Purpose:** Foundation tools that ALL agents use.

**Components:**
```
Agentic/
├── MCP/
│   └── servers/ybis_server.py     # MCP protocol server
├── Tools/
│   ├── file_ops.py                # Read/write files
│   ├── repo_mapper.py             # Project structure scanning
│   ├── git_ops.py                 # Git operations
│   ├── sandbox_manager.py         # Isolated test environment
│   ├── local_rag.py               # Knowledge retrieval
│   └── code_exec.py               # Safe code execution
└── Veriler/
    └── AI_AGENT_PROTOCOLS.md      # Context loading rules
```

**Status:** ✅ ALL WORKING
- MCP server tested with Cursor
- Tools tested independently
- Sandbox operational

---

### Layer 2: Execution (Tier 2)

**Purpose:** Agent implementations that DO the work.

#### CLI Agents (Cloud)
```
Claude (Sonnet 4.5)
├─ Role: Strategic planning, architecture, documentation
├─ Access: Via Anthropic API
└─ Status: ✅ Active

Gemini (1.5 Flash)
├─ Role: Tactical implementation, testing, optimization
├─ Access: Via Google API
└─ Status: ✅ Active
```

#### Local Agents (Ollama)
```
Agentic/Agents/
├── architect.py         # Planning (uses Ollama)
├── developer.py         # Coding (uses Ollama)
├── qa.py                # Validation (uses Ollama)
└── base_agent.py        # Base class

Models:
├─ qwen2.5-coder:14b    # Primary (coding)
├─ llama3.2:latest      # General tasks
├─ llama3.2:3b          # Fast tasks
└─ deepseek-r1:32b      # Reasoning
```

**Status:**
- ✅ Architect, Developer, QA agents implemented
- ✅ AgentRunResult parsing fixed
- ✅ Tested with local Ollama models
- ⚠️ CrewAI integration partial (planning_crew.py exists)

---

### Layer 3: Orchestration (Tier 2-2.75)

**Purpose:** Coordinate agents through workflows.

#### orchestrator_v2.py (LangGraph)
**7-Phase Production Workflow:**
```
1. Init       → Setup sandbox, load context
2. Analyze    → Architect plans the solution
3. Execute    → Developer writes code (in sandbox)
4. Lint       → Syntax validation
5. QA         → QA agent tests
6. Approval   → Human reviews (Tier 2.5)
7. Commit     → Git operations
```

**Features:**
- ✅ Sandbox isolation (`.sandbox/`)
- ✅ Retry logic (max 3 attempts)
- ✅ Structured logging
- ✅ Context loading from AI_AGENT_PROTOCOLS.md
- ✅ Git integration

**Status:** 🟡 BUILT, TESTING IN PROGRESS

#### planning_crew.py (CrewAI)
**Multi-Agent Sequential Workflow:**
```
Product Owner → Analyzes requirements
      ↓
Architect     → Designs solution
      ↓
JSON Plan     → Returns structured plan
```

**Status:** 🟡 PROTOTYPE (not yet integrated with orchestrator_v2)

#### IntelligentRouter
**Cloud vs Local Routing:**
```python
router.py:
- Architecture tasks    → Claude (cloud)
- Critical decisions    → Claude (cloud)
- Coding tasks          → Ollama (local)
- Quick fixes           → Ollama (local)
```

**Status:** ✅ WORKING

---

### Layer 4: Coordination (Multi-Agent Framework)

**Purpose:** Govern how CLI agents (Claude + Gemini) collaborate.

**Constitution v2.0:**
```markdown
12 Articles:
├─ Article 1: Peer equality (no hierarchy)
├─ Article 2: Communication channels
├─ Article 3: Conflict resolution (intelligent merge)
├─ Article 4: Resource limits (10/20/50+ files)
├─ Article 5: Division of labor (strategic vs tactical)
├─ Article 10: Lean Protocol v3.1
└─ Article 12: Violation handling
```

**Communication Channels:**
```
Meta/Active/
├── TASK_BOARD.md           # Single source of truth (Lean v3.1)
├── agent_messages.json     # Agent-to-agent messages
├── agent_status.json       # Real-time status
├── communication_log.md    # Critical events only
└── auto_dispatcher.py      # Auto task assignment
```

**Task Board Protocol:**
```markdown
## NEW → IN PROGRESS → DONE
- Agents claim tasks by moving to IN PROGRESS
- Update status atomically
- Log only critical events ([START], [BLOCKER], [COMPLETE])
```

**Status:**
- ✅ Constitution v2.0 ratified
- ✅ All channels operational
- ⚠️ Never tested in practice (TASK-003 pending)

---

### Layer 5: User Interfaces

**Purpose:** How users interact with the system.

#### Cursor IDE (MCP)
```json
// Settings > MCP
{
  "name": "ybis-core",
  "command": "python.exe",
  "args": ["ybis_server.py"]
}
```
**Status:** ✅ CONFIGURED

#### VS Code (MCP)
```json
// .vscode/settings.json
{
  "mcp.servers": {
    "ybis-core": { ... }
  }
}
```
**Status:** 🟡 READY (not yet tested)

#### Claude Desktop (MCP)
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "ybis-core": { ... }
  }
}
```
**Status:** ✅ CONFIGURED

#### Direct CLI
```bash
python orchestrator_v2.py
python planning_crew.py
```
**Status:** ✅ WORKING

---

## 🔄 Data Flow Example

**Scenario:** User asks Claude to "Add user authentication"

```
1. USER (Cursor)
   ↓ (MCP call)
2. MCP Server (ybis_server.py)
   ↓ (get_next_task)
3. TASK_BOARD.md
   ↓ (create TASK-004)
4. Claude (CLI Agent)
   ↓ (claims task)
5. IntelligentRouter
   ↓ (routes to orchestrator_v2.py)
6. orchestrator_v2.py
   ├─ Init: Setup sandbox
   ├─ Analyze: Architect plans (uses Ollama)
   ├─ Execute: Developer codes (uses Ollama)
   ├─ Lint: Validates syntax
   ├─ QA: Tests (uses Ollama)
   ├─ Approval: Claude shows plan to USER
   └─ Commit: Git operations
7. TASK_BOARD.md (updated to DONE)
8. communication_log.md ([COMPLETE])
```

---

## 🚧 Integration Gaps (Current Issues)

### 1. CrewAI ↔ orchestrator_v2.py Integration
**Problem:** CrewAI (planning_crew.py) exists but doesn't integrate with orchestrator_v2.py

**Impact:** Can't use CrewAI's multi-agent capabilities within the 7-phase workflow

**Fix Needed:**
```python
# In orchestrator_v2.py analyze_node():
from Agentic.Crews.planning_crew import PlanningCrew

async def analyze_node(state: AgentState):
    # Use CrewAI for planning phase
    crew = PlanningCrew()
    result = crew.run(state['task'])
    # Parse result into state['plan']
```

**Status:** 🔴 NOT DONE

---

### 2. Multi-Agent Coordination ↔ Orchestrator
**Problem:** TASK_BOARD.md and Constitution exist, but orchestrator_v2.py doesn't integrate with them

**Impact:** Can't run Claude + Gemini in parallel on different tasks

**Fix Needed:**
```python
# When orchestrator_v2.py starts:
1. Check TASK_BOARD.md for assigned task
2. Update agent_status.json (set status to "working")
3. Log to communication_log.md ([START])
4. Execute workflow
5. Update TASK_BOARD.md (move to DONE)
6. Update agent_status.json (set status to "idle")
7. Log to communication_log.md ([COMPLETE])
```

**Status:** 🔴 NOT DONE

---

### 3. MCP ↔ Multi-Agent Coordination
**Problem:** MCP server can create tasks, but doesn't integrate with TASK_BOARD.md

**Impact:** Tasks from Cursor don't appear in TASK_BOARD.md for agent coordination

**Fix Needed:**
```python
# In ybis_server.py add_tool():
@server.add_tool()
async def create_task(title: str, description: str, priority: str):
    # 1. Add to TASK_BOARD.md
    # 2. Notify agents via agent_messages.json
    # 3. auto_dispatcher.py assigns to available agent
```

**Status:** 🔴 NOT DONE

---

### 4. Agent Profile ↔ Constitution Sync
**Problem:** Constitution says signed, profiles say `constitution_signed: false`

**Impact:** Inconsistent state tracking

**Fix:**
```bash
# Update Meta/Agents/*/profile.json
"constitution_signed": true,
"constitution_version": "2.0"
```

**Status:** 🔴 NOT DONE

---

### 5. Tier 2.75 ↔ CrewAI Decision
**Problem:** Two orchestration systems (LangGraph vs CrewAI) - unclear which is primary

**Impact:** Developer confusion, potential duplicate work

**Solution Options:**
- **A:** Use orchestrator_v2.py as primary, CrewAI for planning phase only
- **B:** Replace orchestrator_v2.py with CrewAI completely
- **C:** Keep both, use IntelligentRouter to choose based on task type

**Recommendation:** Option A (hybrid)

**Status:** 🟡 DECISION NEEDED

---

## 🎯 Integration Roadmap

### Phase 1: Fix Critical Gaps (1-2 hours)
```
1. Update agent profiles (constitution_signed: true)
2. Integrate orchestrator_v2.py with TASK_BOARD.md
3. Test TASK-003 (Multi-Agent Parallel Execution)
```

### Phase 2: CrewAI Integration (2-3 hours)
```
1. Integrate planning_crew.py into orchestrator_v2.py analyze phase
2. Test hybrid LangGraph + CrewAI workflow
3. Document when to use which orchestrator
```

### Phase 3: MCP ↔ Multi-Agent Bridge (2 hours)
```
1. Add create_task tool to MCP server
2. Connect to TASK_BOARD.md
3. Enable auto_dispatcher.py automatic assignment
```

### Phase 4: Documentation Update (1 hour)
```
1. Update README.md to reflect unified architecture
2. Archive outdated STATUS.md sections
3. Create QUICK_START.md for new users
```

---

## 📝 Current Task Status

From `TASK_BOARD.md`:

### ✅ DONE
- TASK-001: Finalize Multi-Agent Constitution

### 📋 NEW (Ready)
- **TASK-002:** Build Tier 3 Memory System (Mem0 integration)
- **TASK-003:** Test Multi-Agent Parallel Execution ⚠️ CRITICAL

### 🔄 Recommended Next
- **TASK-004:** Integrate CrewAI with orchestrator_v2.py
- **TASK-005:** Connect MCP server to TASK_BOARD.md
- **TASK-006:** Update README.md to unified architecture

---

## 🏆 What's Actually Working Right Now

### ✅ Production Ready
1. **MCP Server** - Cursor can call tools
2. **IntelligentRouter** - Cloud/Local routing works
3. **Local Agents** - Architect, Developer, QA tested with Ollama
4. **Sandbox** - Isolated testing operational
5. **Constitution v2.0** - Governance rules defined

### 🟡 Partially Working
1. **orchestrator_v2.py** - Built but not integrated with TASK_BOARD
2. **Multi-Agent Framework** - Framework ready, never tested in practice
3. **CrewAI** - Prototype exists, not integrated

### 🔴 Conceptual Only
1. **Tier 3+ (Memory, GraphRAG)** - Roadmap exists, no code
2. **Parallel Agent Execution** - TASK-003 pending
3. **MCP ↔ TASK_BOARD bridge** - Not implemented

---

## 🚀 Quick Start (After Integration)

**For Claude/Gemini (CLI Agents):**
```bash
# 1. Check task board
cat Meta/Active/TASK_BOARD.md

# 2. Claim a task (update status to IN PROGRESS)

# 3. Run orchestrator
cd Agentic
python Core/orchestrator_v2.py

# 4. Complete task (update TASK_BOARD to DONE)
```

**For Local Agents:**
```bash
# Via CrewAI
python test_crew.py
```

**For Cursor Users:**
```
1. Ensure MCP server configured
2. Chat: "@ybis-core create task: Add login feature"
3. System auto-assigns to available agent
4. Agent executes via orchestrator_v2.py
5. You review and approve
```

---

## 📊 System Health Dashboard

| Component | Status | Last Tested | Issues |
|-----------|--------|-------------|--------|
| MCP Server | ✅ | 2025-12-14 | None |
| orchestrator_v2.py | 🟡 | 2025-12-15 | Not integrated with TASK_BOARD |
| Local Agents | ✅ | 2025-12-15 | AgentRunResult fixed |
| CrewAI | 🟡 | Never | Not integrated |
| Multi-Agent Framework | 🟡 | Never | TASK-003 pending |
| IntelligentRouter | ✅ | 2025-12-15 | None |
| Sandbox | ✅ | 2025-12-14 | None |
| Constitution | ✅ | 2025-12-15 | Profile sync needed |

---

## 🎓 Key Insights

1. **Not Fragmented** - All systems designed to work together, just integration incomplete
2. **CrewAI = Enhancement** - Added to solve Tier 2.75 issues, not replacement
3. **Multi-Agent = Coordination Layer** - For CLI agents (Claude + Gemini), not local
4. **MCP = Bridge** - Connects user interfaces to system
5. **orchestrator_v2.py = Core Engine** - 7-phase workflow is the execution layer

---

**Next Critical Action:** Complete TASK-003 (parallel execution test) to validate multi-agent framework actually works in practice.

---

**Last Updated:** 2025-12-15
**By:** Claude (Unified architecture analysis)
