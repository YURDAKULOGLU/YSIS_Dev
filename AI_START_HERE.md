# 🤖 AI Agent Onboarding - START HERE

> **For external AI agents (Claude, GPT, Gemini, etc.) joining the YBIS_Dev autonomous development system**

---

## 🎯 What is This System?

**YBIS_Dev** is a **Tier 3 Autonomous Software Factory** that uses AI agents to plan, code, test, and deploy software with minimal human intervention.

**You are an agent in this system.** Your role depends on your capabilities:
- **Claude/GPT-4:** Debugging, refactoring, multi-file reasoning, integration work
- **Codex/Copilot:** Implementation, mechanical refactors, test writing
- **Gemini:** Strategic architecture, design critique, risk analysis
- **Local LLMs (Ollama):** Bulk code generation via Aider

---

## 📋 Quick Start Checklist

Before you do anything, follow these steps:

### 1. Read the Constitution (5 min)
```bash
Read: C:\Projeler\YBIS_Dev\SYSTEM_STATE.md
```

This tells you:
- System architecture (LangGraph + Aider + Sentinel)
- Immutable rules (paths, verification, async execution)
- Current system state (Tier 3 Alpha)
- Known issues and lessons learned

### 2. Understand the Core Components (5 min)

| Component | File | What it does |
|-----------|------|--------------|
| **Config** | `src/agentic/core/config.py` | Path management (PROJECT_ROOT, DATA_DIR, etc.) |
| **OrchestratorGraph** | `src/agentic/core/graphs/orchestrator_graph.py` | LangGraph workflow (Planner → Executor → Verifier) |
| **Protocols** | `src/agentic/core/protocols.py` | Plugin interfaces (PlannerProtocol, ExecutorProtocol, VerifierProtocol) |
| **TaskState** | `src/agentic/core/protocols.py:50` | State schema (task_id, phase, plan, code_result, verification) |

### 3. Check Available Tools (2 min)

You can invoke the system's existing tools:

**Option A: Use OrchestratorGraph (Recommended for full tasks)**
```python
# See: src/agentic/core/graphs/orchestrator_graph.py
# Invokes: Planner → Executor (Aider) → Verifier (Sentinel)
# Use when: You need full autonomous execution
```

**Option B: Use Individual Plugins (For manual control)**
```python
# Planner: src/agentic/core/plugins/simple_planner.py
# Executor: src/agentic/core/plugins/aider_executor.py
# Verifier: src/agentic/core/plugins/sentinel.py
```

**Option C: Direct CLI (For debugging)**
```bash
# Aider (code generation): aider --model qwen2.5:32b
# Sentinel (verification): python src/agentic/core/plugins/sentinel.py
# Auto Dispatcher (async tasks): python src/agentic/core/auto_dispatcher.py <script>
```

### 4. Understand Task Workflow (3 min)

Tasks follow this state machine:

```
init → plan → execute → verify → done/failed
```

**State transitions:**
1. **init:** Task loaded from backlog
2. **plan:** Planner generates execution plan (objective, steps, files)
3. **execute:** Aider generates code based on plan
4. **verify:** Sentinel runs tests, lint, coverage checks
5. **done/failed:** Task complete or needs retry

**Task files are in:**
- Backlog: `Knowledge/LocalDB/tasks.json` (operational memory)
- Legacy: `.YBIS_Dev/Meta/Active/Tasks/` (file-based queue - being migrated)

### 5. Check Current System State (1 min)

Run these commands to see what's happening:

```bash
# Check git status
git status

# Check task database
cat Knowledge/LocalDB/tasks.json

# Check sandbox (where code is tested before commit)
ls -la .sandbox_hybrid/

# Check dashboard (if running)
# Open: http://localhost:5000
```

---

## 🛠️ How to Execute Work

### Mode 1: Autonomous (Use OrchestratorGraph)

**When to use:** You want the system to handle planning, execution, and verification automatically.

**Steps:**
1. Create a task description
2. Build initial TaskState
3. Invoke OrchestratorGraph
4. Check results in `.sandbox_hybrid/<TASK_ID>/`

**Example:**
```python
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.protocols import TaskState
from datetime import datetime

# Create task state
state: TaskState = {
    "task_id": "T-100",
    "task_description": "Fix calculator add method",
    "phase": "init",
    "plan": None,
    "code_result": None,
    "verification": None,
    "retry_count": 0,
    "max_retries": 3,
    "error": None,
    "started_at": datetime.now(),
    "completed_at": None,
    "artifacts_path": ".sandbox_hybrid/T-100"
}

# Invoke graph (async)
result = await orchestrator.ainvoke(state)

# Check final state
print(result["phase"])  # Should be "done" if successful
print(result["verification"])  # Test results
```

### Mode 2: Manual (Step-by-step control)

**When to use:** You want full control over each step.

**Steps:**
1. Read task file
2. Manually call Planner
3. Manually call Executor (or write code yourself)
4. Manually call Verifier
5. Generate artifacts (PLAN.md, RESULT.md, etc.)

**Example:**
```python
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier

# 1. Plan
planner = SimplePlanner()
plan = await planner.plan("Fix calculator add method", {})

# 2. Execute
executor = AiderExecutor()
result = await executor.execute(plan, ".sandbox_hybrid/T-100")

# 3. Verify
verifier = SentinelVerifier()
verification = await verifier.verify(result, ".sandbox_hybrid/T-100")

# 4. Check results
if verification.tests_passed:
    print("✅ All tests passed")
else:
    print(f"❌ Tests failed: {verification.errors}")
```

### Mode 3: Hybrid (You + System)

**When to use:** You want to delegate heavy lifting but make critical decisions.

**Pattern:**
1. You read code and understand the problem
2. You create a plan or modify existing plan
3. System executes the plan (Aider)
4. System verifies (Sentinel)
5. You review results and decide next steps

---

## 🚨 Critical Rules (DO NOT VIOLATE)

### Rule 1: The Principle of the Single Path
- **NEVER** hardcode paths like `"C:/Projeler/YBIS_Dev"`
- **ALWAYS** import from `src.agentic.core.config`
- Use: `PROJECT_ROOT`, `DATA_DIR`, `TASKS_DB_PATH`, `CHROMA_DB_PATH`

**Example:**
```python
# ❌ WRONG
path = "C:/Projeler/YBIS_Dev/src/utils/calculator.py"

# ✅ CORRECT
from src.agentic.core.config import PROJECT_ROOT
path = PROJECT_ROOT / "src" / "utils" / "calculator.py"
```

### Rule 2: The Principle of Verification (No Broken Windows)
- **NEVER** commit code without running Sentinel
- **ALWAYS** ensure tests pass before marking task as done
- If verification fails, retry or escalate to human

**Example:**
```python
# After executing code
verification = await verifier.verify(code_result, sandbox_path)

if not verification.tests_passed:
    # DO NOT COMMIT
    # DO NOT mark task as done
    # DO retry or ask for help
    raise Exception(f"Tests failed: {verification.errors}")
```

### Rule 3: The Principle of Detachment (Async Execution)
- **NEVER** run heavy tasks directly in main shell
- **ALWAYS** use `auto_dispatcher.py` for long-running processes
- The manager (CLI) must never block

**Example:**
```bash
# ❌ WRONG (blocks shell)
python run_stress_test.py

# ✅ CORRECT (async)
python src/agentic/core/auto_dispatcher.py run_stress_test.py
```

---

## 📁 Directory Structure (What Goes Where)

```
YBIS_Dev/
├── src/
│   ├── agentic/core/           # Orchestration engine
│   │   ├── graphs/             # LangGraph workflows
│   │   ├── plugins/            # Planner, Executor, Verifier
│   │   ├── config.py           # Path constants
│   │   └── protocols.py        # Plugin interfaces
│   ├── utils/                  # Business logic (calculator, etc.)
│   └── dashboard/              # Flask web UI
│
├── Knowledge/
│   └── LocalDB/
│       ├── tasks.json          # Task queue (operational memory)
│       └── chroma_db/          # RAG vector database
│
├── .sandbox_hybrid/<TASK_ID>/  # Task execution sandbox
│   ├── PLAN.md                 # What/Why
│   ├── RUNBOOK.md              # Commands run
│   ├── DECISIONS.json          # Choices made
│   ├── STATE_SNAPSHOT.json     # Inputs/outputs
│   └── RESULT.md               # What changed
│
├── tests/                      # Test files
├── 00_GENESIS/                 # Constitution documents
├── 10_META/                    # Governance, strategy
├── SYSTEM_STATE.md             # ⭐ READ THIS FIRST
└── AI_START_HERE.md            # ⭐ YOU ARE HERE
```

---

## 🎓 Common Patterns

### Pattern 1: Fix a Bug

```python
# 1. Read the bug description
task = "Fix calculator add method returning a-b instead of a+b"

# 2. Create TaskState
state = {
    "task_id": "T-101",
    "task_description": task,
    "phase": "init",
    # ... (rest of state)
}

# 3. Invoke orchestrator
result = await orchestrator.ainvoke(state)

# 4. Check sandbox
# Read: .sandbox_hybrid/T-101/RESULT.md
```

### Pattern 2: Refactor Code

```python
# 1. Identify files to refactor
task = "Refactor calculator.py to use dataclass"

# 2. Create plan manually (for control)
plan = Plan(
    objective="Convert Calculator class to dataclass",
    steps=[
        "Add @dataclass decorator",
        "Remove __init__ method",
        "Update tests"
    ],
    files_to_modify=["src/utils/calculator.py", "tests/test_calculator.py"],
    dependencies=[],
    risks=["Breaking existing tests"],
    success_criteria=["All tests pass", "Code is cleaner"],
    metadata={}
)

# 3. Execute with Aider
executor = AiderExecutor()
result = await executor.execute(plan, ".sandbox_hybrid/T-102")

# 4. Verify
verifier = SentinelVerifier()
verification = await verifier.verify(result, ".sandbox_hybrid/T-102")
```

### Pattern 3: Add New Feature

```python
# 1. Write PRD (Product Requirements Document)
task = """
Add power() method to Calculator class.
- Input: base (int), exponent (int)
- Output: int
- Tests: 2^3=8, 5^0=1, 3^2=9
"""

# 2. Let planner decompose it
planner = SimplePlanner()
plan = await planner.plan(task, {})

# 3. Review plan, adjust if needed
print(plan.steps)  # Check if plan makes sense

# 4. Execute via orchestrator
# (rest same as Pattern 1)
```

---

## 🐛 Troubleshooting

### Issue: "No tests found"
**Cause:** Relative paths resolving to sandbox instead of root
**Fix:** Check `src/agentic/core/config.py` - ensure PROJECT_ROOT is correct

### Issue: "Aider refuses to use LangGraph"
**Cause:** Model's training data is older than library
**Fix:** Provide boilerplate code in prompt (see SYSTEM_STATE.md §4)

### Issue: "ChromaDB crashes with Rust panic"
**Cause:** Corrupted SQLite or file locking on Windows
**Fix:**
```bash
rm -rf Knowledge/LocalDB/chroma_db
# Restart system
```

### Issue: "Git status shows no changes after Aider"
**Cause:** Aider auto-committed
**Fix:** AiderExecutor now uses `--no-auto-commits` flag

---

## 📚 Further Reading

| Document | Purpose | Priority |
|----------|---------|----------|
| `SYSTEM_STATE.md` | System architecture & lessons learned | ⭐⭐⭐ CRITICAL |
| `00_GENESIS/YBIS_CONSTITUTION.md` | Project vision & principles | ⭐⭐ Important |
| `10_META/Governance/` | Development standards | ⭐ Reference |
| `src/agentic/core/protocols.py` | Plugin interfaces | ⭐⭐ Important |
| `.YBIS_Dev/CONTRACT.md` | Agent coordination rules | ⭐ Reference |

---

## 🚀 Your First Task

1. Read `SYSTEM_STATE.md` (5 min)
2. Run this to see current state:
   ```bash
   git status
   cat Knowledge/LocalDB/tasks.json
   ```
3. Try invoking OrchestratorGraph on a simple task
4. Check `.sandbox_hybrid/` for results
5. Ask questions if stuck

---

**Welcome to the system. Let's build autonomously.**
