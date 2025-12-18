# Tier 2.5 MVP Plan - "Hybrid Intelligence"

**Target:** Production-ready development assistant for YBIS
**Timeline:** 11 days (Tier 1: 3d, Tier 2: 5d, Tier 2.5: 3d)
**Start Date:** After tool calling bug fixed

---

## 🎯 MVP Definition

### Philosophy
"Smart assistant that asks before acting, not autonomous agent"

### Success Criteria
- [ ] Works in Cursor via MCP
- [ ] Can analyze YBIS codebase
- [ ] Plans changes with human approval
- [ ] Self-corrects syntax errors (max 3 retries)
- [ ] Logs all actions
- [ ] No infinite loops or runaway costs

---

## 📋 Tier Breakdown

### Tier 1: The Sensor (Days 1-3)

**Goal:** Make Cursor "see" the YBIS project

**Deliverables:**
```python
# .YBIS_Dev/Agentic/server.py
# MCP Server with 3 tools:

1. list_project_structure()
   - Returns file tree (respects .gitignore)
   - Max depth: 3 levels

2. read_files(paths: list[str])
   - Reads multiple files
   - Returns content with line numbers

3. append_log(message: str)
   - Writes to .YBIS_Dev/logs/session.log
   - Includes timestamp
```

**Test:**
```
User in Cursor: "@YBIS_Dev show me the structure of apps/mobile"
Expected: Tree view of mobile app structure
```

**Tech Stack:**
- `fastmcp` (MCP server library)
- `pathlib` (file operations)
- `gitignore_parser` (respect .gitignore)

**Exit Criteria:**
- ✅ MCP server starts without errors
- ✅ Cursor can call all 3 tools
- ✅ Returns correct data

---

### Tier 2: The Loop (Days 4-8)

**Goal:** Self-correcting code generation

**Architecture:**
```
LangGraph State Machine:

┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PLANNER    │ ← "Break task into steps"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EXECUTOR   │ ← "Write code"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  REVIEWER   │ ← "Check for errors"
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
 ERROR    SUCCESS
   │       │
   │       ▼
   │     END
   │
   └─► EXECUTOR (retry, max 3)
```

**State Definition:**
```python
class State(TypedDict):
    task: str
    plan: list[str]
    code: str
    errors: list[str]
    retry_count: int
    status: Literal["planning", "executing", "reviewing", "done", "failed"]
```

**Deliverables:**
```python
# .YBIS_Dev/Agentic/Core/orchestrator.py
# .YBIS_Dev/Agentic/Core/state.py
# .YBIS_Dev/Agentic/Core/nodes/planner.py
# .YBIS_Dev/Agentic/Core/nodes/executor.py
# .YBIS_Dev/Agentic/Core/nodes/reviewer.py
```

**Test:**
```python
# Terminal test (not Cursor yet)
python .YBIS_Dev/Agentic/Core/orchestrator.py \
  --task "Create a hello_world.ts file in src/"

Expected:
1. Plans steps
2. Writes file
3. Checks syntax (via tsc --noEmit)
4. Reports success or retries
```

**Exit Criteria:**
- ✅ Can complete simple file creation
- ✅ Detects syntax errors
- ✅ Retries up to 3 times
- ✅ Stops after 3 failures

---

### Tier 2.5: Human-in-the-Loop (Days 9-11)

**Goal:** Make it production-safe

**Added Features:**

#### 1. Approval Checkpoints
```python
# Before executing any code:
def request_approval(plan: str) -> bool:
    """
    Shows plan to user in Cursor
    Waits for approval
    """
    print(f"📋 Plan:\n{plan}\n")
    print("⚠️  Approve? (y/n): ")
    return input().lower() == 'y'
```

#### 2. Safety Limits
```python
MAX_RETRIES = 3
MAX_FILES_CHANGED = 10  # Abort if plan touches too many files
DESTRUCTIVE_COMMANDS = ["rm", "del", "drop", "truncate"]
```

#### 3. Logging
```python
# .YBIS_Dev/logs/YYYY-MM-DD_HH-MM-SS.log
# Format:
[2025-12-14 15:30:00] TASK: Create login component
[2025-12-14 15:30:05] PLAN: 1. Create file, 2. Add imports...
[2025-12-14 15:30:10] APPROVAL: Granted
[2025-12-14 15:30:15] EXECUTE: Writing to src/components/Login.tsx
[2025-12-14 15:30:20] REVIEW: Syntax OK
[2025-12-14 15:30:25] SUCCESS
```

#### 4. Cursor Integration
```python
# Update server.py to call orchestrator
@mcp.tool()
def execute_task(task: str) -> str:
    """
    Executes a development task with approval workflow
    """
    result = orchestrator.run(task)
    return format_result(result)
```

**Test Scenario:**
```
User in Cursor:
"@YBIS_Dev create a new Button component in packages/ui/src/components"

Expected Flow:
1. System analyzes project structure
2. Plans: "Create Button.tsx, add to index.ts, write test"
3. Shows plan in Cursor
4. Waits for user approval
5. Executes step by step
6. Reports result
```

**Exit Criteria:**
- ✅ Works end-to-end in Cursor
- ✅ User can approve/reject plans
- ✅ Logs everything
- ✅ Handles errors gracefully
- ✅ Completes real YBIS task successfully

---

## 📦 Dependencies

### Python Packages
```txt
# requirements.txt
fastmcp>=0.2.0
langgraph>=0.2.0
langchain-core>=0.3.0
langchain-openai>=0.2.0
anthropic>=0.40.0
gitignore-parser>=0.1.0
python-dotenv>=1.0.0
rich>=13.0.0
```

### Environment Variables
```bash
# .YBIS_Dev/.env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
DEFAULT_MODEL=claude-3-5-sonnet-20241022
COST_LIMIT_DAILY=5.00  # USD
```

---

## 🚦 Milestones & Checkpoints

### Milestone 1: Tier 1 Complete (Day 3)
- [ ] MCP server responds to Cursor
- [ ] Can read YBIS file structure
- [ ] Logs working

**Checkpoint:** If Cursor can't connect, stop and debug. Don't proceed to Tier 2.

---

### Milestone 2: Tier 2 Complete (Day 8)
- [ ] LangGraph loop works standalone
- [ ] Can self-correct syntax errors
- [ ] Retry logic functional

**Checkpoint:** If it can't fix a simple syntax error in 3 tries, revisit Reviewer node.

---

### Milestone 3: MVP Complete (Day 11)
- [ ] Full Cursor integration
- [ ] Human approval works
- [ ] Completed real YBIS task

**Checkpoint:** If any safety feature fails (approval, limits, logging), fix before declaring MVP done.

---

## 🛑 Stop Conditions

**When to STOP and NOT proceed:**
1. Cost exceeds $5/day (API bills)
2. Loop becomes infinite (add circuit breaker)
3. Human approval ignored (critical safety bug)
4. Tool calling bug in YBIS not fixed yet (dependency)

**Remember:** This is MVP. If Tier 2.5 works, we STOP. No Tier 3.

---

## 📊 Post-MVP (After YBIS Production)

**Only consider these if MVP proves useful:**
- Tier 3: Memory (Mem0) - Remember user preferences
- Tier 4: Code understanding (Tree-sitter) - Smarter analysis
- Tier 6: Knowledge graph (GraphRAG) - Dependency tracking

**But:** These are NOT required for "bileme dönemini bitirmek"

---

## 🎬 Next Steps (After Tool Calling Fixed)

1. **Day 1:**
   - Set up Python environment
   - Install fastmcp
   - Write basic MCP server

2. **Day 2:**
   - Implement 3 tools
   - Test with Cursor

3. **Day 3:**
   - Debug any issues
   - Polish logging
   - Milestone 1 checkpoint

---

**Last Updated:** 2025-12-14
**Status:** Planning Complete
**Waiting For:** Tool calling bug fix in YBIS
