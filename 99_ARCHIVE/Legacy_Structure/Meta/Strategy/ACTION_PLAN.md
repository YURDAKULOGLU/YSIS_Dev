# .YBIS_Dev Action Plan - Concrete Steps

**Goal:** Get to Tier 2.5 MVP and stop there
**Timeline:** Start after tool calling bug fixed

---

## ✅ DONE (Today)

- [x] Organized "chat dev.md" → RESEARCH_NOTES.md
- [x] Created README.md with clear MVP scope
- [x] Cleaned up legacy folders (125325kas2025, ysis_agentic)
- [x] Created TIER_2.5_MVP_PLAN.md
- [x] Made Constitution.md visible in root

---

## 🎯 TIER 1: The Sensor (Days 1-3)

### Day 1: Setup
**Duration:** 2-3 hours

```bash
# 1. Create Python environment
cd .YBIS_Dev
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
pip install fastmcp python-dotenv gitignore-parser rich

# 3. Create .env file
echo "ANTHROPIC_API_KEY=your-key" > .env

# 4. Test fastmcp
python -c "import fastmcp; print('OK')"
```

**Deliverable:** Working Python environment

---

### Day 2: MCP Server
**Duration:** 4-6 hours

**File:** `.YBIS_Dev/Agentic/server.py`

```python
from fastmcp import FastMCP
import os
from pathlib import Path
from gitignore_parser import parse_gitignore

mcp = FastMCP("YBIS_Dev")

@mcp.tool()
def list_project_structure(max_depth: int = 3) -> str:
    """Returns YBIS project file tree"""
    # Implementation here
    pass

@mcp.tool()
def read_files(paths: list[str]) -> dict[str, str]:
    """Reads multiple files and returns content"""
    # Implementation here
    pass

@mcp.tool()
def append_log(message: str) -> str:
    """Appends to session log"""
    # Implementation here
    pass

if __name__ == "__main__":
    mcp.run()
```

**Test:**
```bash
# Terminal 1: Start server
python .YBIS_Dev/Agentic/server.py

# Terminal 2: Test with MCP inspector
# (or wait for Cursor integration)
```

**Deliverable:** Working MCP server

---

### Day 3: Cursor Integration
**Duration:** 2-4 hours

**Steps:**
1. Open Cursor settings
2. Go to MCP section
3. Add new server:
   ```json
   {
     "mcpServers": {
       "YBIS_Dev": {
         "command": "python",
         "args": ["C:/Projeler/YBIS/.YBIS_Dev/Agentic/server.py"]
       }
     }
   }
   ```
4. Restart Cursor
5. Test: `@YBIS_Dev list project structure`

**Deliverable:** Cursor can call your tools

**Checkpoint:** If this doesn't work, debug before Tier 2.

---

## 🎯 TIER 2: The Loop (Days 4-8)

### Day 4-5: LangGraph Setup
**Duration:** 6-8 hours

```bash
# Install LangGraph
pip install langgraph langchain-core langchain-anthropic

# Create state machine files
mkdir -p .YBIS_Dev/Agentic/Core/nodes
```

**Files to create:**
1. `Core/state.py` - State definition
2. `Core/nodes/planner.py` - Planning node
3. `Core/nodes/executor.py` - Code execution node
4. `Core/nodes/reviewer.py` - Error checking node
5. `Core/orchestrator.py` - Main graph

**Deliverable:** Standalone LangGraph that works in terminal

---

### Day 6-7: Self-Correction Logic
**Duration:** 6-8 hours

**Add to orchestrator:**
- Retry mechanism (max 3)
- Error detection (syntax check via `tsc --noEmit`)
- Loop routing (error → back to executor)

**Test:**
```bash
python .YBIS_Dev/Agentic/Core/orchestrator.py \
  --task "Create broken TypeScript file"

# Expected: Should detect error and retry
```

**Deliverable:** Self-correcting code generation

---

### Day 8: Integration
**Duration:** 4-6 hours

**Connect Tier 2 to Tier 1:**
- Add `execute_task()` tool to server.py
- Call orchestrator from MCP server
- Test in Cursor

**Deliverable:** Cursor → MCP → LangGraph works

**Checkpoint:** Complete one simple task end-to-end.

---

## 🎯 TIER 2.5: Human-in-the-Loop (Days 9-11)

### Day 9: Approval System
**Duration:** 4-6 hours

**Add to orchestrator:**
```python
def request_approval(plan: str) -> bool:
    """Shows plan and waits for approval"""
    print(f"\n{'='*50}")
    print("📋 PLAN:")
    print(plan)
    print(f"{'='*50}\n")
    response = input("Approve? (y/n): ")
    return response.lower() == 'y'
```

**Test:** Verify you can reject plans

---

### Day 10: Safety Features
**Duration:** 4-6 hours

**Add:**
- Max retries limit (3)
- Max files changed limit (10)
- Destructive command blocking
- Cost tracking (basic)

**Test:** Try to trigger safety limits

---

### Day 11: Polish & Real Test
**Duration:** 4-6 hours

**Tasks:**
1. Improve logging
2. Add error messages
3. Write usage guide
4. **REAL TEST:** Use it to create a new component in YBIS

**Success = You complete a real YBIS task using @YBIS_Dev**

---

## 🛑 STOP HERE

**After Day 11:**
- ✅ MVP is done
- ✅ Tool works in production
- 🛑 **STOP building .YBIS_Dev**
- 🚀 **START using it for YBIS development**

**No Tier 3. No Tier 10. We stop at 2.5.**

---

## 📊 Success Metrics

MVP is successful if:
- [ ] Cursor integration works
- [ ] Can complete real YBIS task
- [ ] Human approval works
- [ ] Self-corrects syntax errors
- [ ] Doesn't run away (safety limits work)
- [ ] You actually use it (not shelf-ware)

---

## 🚨 Failure Conditions

Stop and reassess if:
- Day 5 and Tier 1 still not working → Problem with MCP
- Day 10 and no self-correction → LangGraph issue
- Day 11 and Cursor integration broken → Architecture problem

**Don't be afraid to stop and pivot.**

---

## 📝 Daily Checklist

Each day:
- [ ] Log time spent
- [ ] Commit to git
- [ ] Test what you built
- [ ] Update this plan with learnings

---

**Next Action:** Wait for tool calling bug fix, then start Day 1.

**Last Updated:** 2025-12-14
