# YBIS_Dev Bootstrap Master Plan
**Version:** 1.0
**Date:** 2025-12-15
**Status:** 🟢 ACTIVE EXECUTION
**Philosophy:** Self-Building System via Aggressive Dogfooding

---

## 🎯 Core Vision

**Goal:** Build a self-evolving AI development system where each tier uses the previous tier to build itself.

**Principle:** "Agents build agents" with strict gates and deterministic artifacts.

```
Tier 1 (Manual)
    ↓ (uses to build)
Tier 2 (Semi-auto with gates)
    ↓ (uses to build)
Tier 3 (Multi-agent with constitution)
    ↓ (uses to build)
Tier 4+ (Autonomous maintenance)
```

---

## 🏗️ Architecture (3 Layers)

### Layer A: Orchestration (Brain)
- **LangGraph** (orchestrator_v2.py)
- State machine with 7 phases + gates
- Deterministic artifact generation

### Layer B: Execution (Muscle)
- **Local Agents** (Ollama): Architect, Developer, QA
- **Sandbox** (isolated testing)
- **IntelligentRouter** (Cloud vs Local)

### Layer C: Coordination (Nervous System)
- **TASK_BOARD.md** (Lean Protocol)
- **Constitution v2.0** (Multi-agent governance)
- **MCP Server** (IDE bridges)

---

## 📋 Bootstrap Protocol (6-Step Loop)

Every task follows this cycle:

```
1. INSPECT  → Read current state (STATE_SNAPSHOT.json)
2. PLAN     → Generate execution plan (PLAN.md)
3. EXECUTE  → Run commands, write code (RUNBOOK.md)
4. VERIFY   → Gates: lint + test + smoke (EVIDENCE/logs.txt)
5. COMMIT   → If green: commit + tag (DECISIONS.json)
6. HANDOFF  → Generate next task
```

**Critical:** If VERIFY fails → Retry (max 2) or Rollback

---

## 🚀 Phase Breakdown

### Phase 0: Foundation + Gates (Days 1-2)
**Goal:** Transform orchestrator_v2.py into a gated, artifact-producing pipeline

**Current State:**
- ✅ orchestrator_v2.py exists (7 phases)
- ✅ Local agents work (tested)
- ❌ No gates between phases
- ❌ No artifact generation
- ❌ No TASK_BOARD integration

**Target State:**
- ✅ Gates after each phase
- ✅ Deterministic artifacts
- ✅ TASK_BOARD integration
- ✅ 80%+ success rate on simple tasks

**Deliverables:**
```
.sandbox/
├── STATE_SNAPSHOT.json    # Current repo state
├── PLAN.md                # What we're building
├── RUNBOOK.md             # Commands executed
├── DECISIONS.json         # Config choices made
└── EVIDENCE/
    ├── lint.log           # Linter output
    ├── test.log           # Test results
    └── smoke.log          # Smoke test output
```

**Success Metrics:**
- [ ] orchestrator completes 5 simple tasks
- [ ] At least 4/5 succeed (80% rate)
- [ ] All artifacts generated correctly
- [ ] No manual intervention during success cases

---

### Phase 1: Dogfooding Tier 2 (Days 3-5)
**Goal:** Use Tier 2 to improve Tier 2 itself

**Tasks (via TASK_BOARD):**
1. "Improve error messages in orchestrator_v2.py"
2. "Add retry backoff logic to developer agent"
3. "Optimize sandbox cleanup process"
4. "Add structured logging to all agents"
5. "Create health check endpoint for MCP server"

**Execution:**
- Each task goes through 6-step bootstrap protocol
- You review and approve at VERIFY gate
- System learns from failures

**Success Metrics:**
- [ ] 8/10 tasks complete successfully (80%)
- [ ] Average task time < 10 minutes
- [ ] Zero manual code fixes needed on success cases
- [ ] All failures have clear error messages

---

### Phase 2: Bootstrap Agent Creation (Days 6-8)
**Goal:** Create a dedicated "Bootstrap Agent" that manages framework installations

**Specification:**
```python
class BootstrapAgent:
    def inspect(self) -> StateSnapshot:
        """Analyze repo: OS, tools, configs, gaps"""

    def plan(self, target: str) -> Plan:
        """Generate installation plan for target framework"""

    def execute(self, plan: Plan) -> Result:
        """Run commands in sandbox"""

    def verify(self, result: Result) -> bool:
        """Run lint + test + smoke"""

    def commit(self, result: Result) -> None:
        """Commit if verify passed"""

    def handoff(self) -> Task:
        """Generate next framework installation task"""
```

**Implementation:**
- Use Tier 2 to write Bootstrap Agent
- Bootstrap Agent lives in `Agentic/Agents/bootstrap.py`
- Integrates with orchestrator_v2.py

**Test:**
- Use Bootstrap Agent to install a simple tool (e.g., prettier config)

**Success Metrics:**
- [ ] Bootstrap Agent successfully installs 1 tool
- [ ] All 6 protocol steps execute correctly
- [ ] Artifacts match specification
- [ ] Can handoff to next task automatically

---

### Phase 3: Framework Integration (Days 9-12)
**Goal:** Use Bootstrap Agent to install and integrate missing frameworks

**Target Frameworks (prioritized):**
1. **CrewAI integration** → into orchestrator analyze phase
2. **E2B sandbox** → replace local docker (optional)
3. **Open SWE** → for GitHub PR automation
4. **Mem0** → for agent memory (Tier 4)

**Execution:**
- Bootstrap Agent installs one framework at a time
- Each installation follows 6-step protocol
- Tests integration after each install

**Success Metrics:**
- [ ] CrewAI integrated and tested
- [ ] Open SWE can open 1 PR automatically
- [ ] Each framework has passing smoke tests
- [ ] System remains stable after each addition

---

### Phase 4: Multi-Agent Activation (Days 13-15)
**Goal:** Activate Constitution v2.0 and test parallel execution

**Tasks:**
1. Test TASK-003: Multi-Agent Parallel Execution
2. Claude + Gemini work on different tasks simultaneously
3. Test conflict resolution (same file edit)
4. Test handoff protocol

**Constitution Tests:**
- Peer equality enforcement
- Intelligent merge on conflicts
- Resource limits (10/20/50 file tiers)
- Communication via agent_messages.json

**Success Metrics:**
- [ ] 2 agents work in parallel without interference
- [ ] Conflict resolution works (1 test case)
- [ ] Handoff protocol executes correctly
- [ ] All communication logged properly

---

### Phase 5: Autonomous Maintenance (Days 16+)
**Goal:** System maintains and improves itself

**Tier 4 Features:**
1. **Code Health Scanner** → identifies tech debt
2. **Scheduled Refactoring** → nightly cleanup jobs
3. **Dependency Updates** → automated PR creation
4. **Performance Monitoring** → tracks system metrics

**Implementation:**
- Use Tier 2+3 to build Tier 4 features
- Bootstrap Agent installs monitoring tools
- Sentinel agent watches for maintenance tasks

**Success Metrics:**
- [ ] System runs 1 maintenance task automatically
- [ ] Nightly refactor completes without human input
- [ ] Code health score improves over 1 week
- [ ] You only intervene 10% of the time

---

## 📊 Artifact Specifications

### STATE_SNAPSHOT.json
```json
{
  "timestamp": "2025-12-15T14:30:00Z",
  "repo_root": "/c/Projeler/YBIS",
  "os": "Windows 11",
  "tools": {
    "node": "20.11.0",
    "pnpm": "8.15.0",
    "python": "3.11.7",
    "docker": "24.0.7",
    "ollama": "0.1.20"
  },
  "git": {
    "branch": "main",
    "uncommitted": 45,
    "untracked": 23
  },
  "current_tier": "2.0",
  "active_agents": ["claude", "orchestrator_v2"],
  "pending_tasks": 8,
  "last_success": "2025-12-15T13:45:00Z"
}
```

### PLAN.md
```markdown
# Task: [TASK_ID]

## Objective
[Clear statement of what we're building]

## Context
- Current state: [description]
- Gap: [what's missing]
- Dependencies: [required tools/frameworks]

## Approach
1. Step 1: [action]
2. Step 2: [action]
3. Step 3: [action]

## Files to Modify
- `path/to/file1.ts` → [change description]
- `path/to/file2.py` → [change description]

## Risks
- Risk 1: [mitigation strategy]
- Risk 2: [mitigation strategy]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### RUNBOOK.md
```markdown
# Execution Log: [TASK_ID]

## Commands Executed

### Step 1: Setup
```bash
cd /c/Projeler/YBIS/.YBIS_Dev
source Agentic/.venv/bin/activate
```

### Step 2: Install dependencies
```bash
pip install langgraph==0.2.0
```
Output: [truncated log]

### Step 3: Write code
File: `Agentic/Core/orchestrator_v2.py`
Lines: 45-67
Action: Added gate validation

### Step 4: Test
```bash
python -m pytest tests/test_gates.py
```
Output: 3 passed, 0 failed

## Artifacts Generated
- STATE_SNAPSHOT.json (updated)
- EVIDENCE/lint.log (clean)
- EVIDENCE/test.log (3 passed)
```

### DECISIONS.json
```json
{
  "task_id": "TASK-GATE-001",
  "timestamp": "2025-12-15T15:00:00Z",
  "decisions": [
    {
      "question": "Which retry strategy?",
      "options": ["exponential backoff", "fixed delay", "no retry"],
      "chosen": "exponential backoff",
      "rationale": "More resilient under load"
    },
    {
      "question": "Max retry count?",
      "options": [2, 3, 5],
      "chosen": 3,
      "rationale": "Balance between persistence and speed"
    }
  ],
  "config_changes": {
    "orchestrator.max_retries": 3,
    "orchestrator.backoff_factor": 2.0
  }
}
```

### EVIDENCE/lint.log
```
Running ESLint...
✓ 0 errors, 0 warnings

Running Pylint...
Your code has been rated at 9.8/10
```

### EVIDENCE/test.log
```
============================= test session starts ==============================
collected 8 items

tests/test_gates.py::test_analyze_gate PASSED           [ 12%]
tests/test_gates.py::test_execute_gate PASSED           [ 25%]
tests/test_gates.py::test_verify_gate PASSED            [ 37%]
...

======================== 8 passed in 2.45s =================================
```

### EVIDENCE/smoke.log
```
[SMOKE TEST] Starting orchestrator with toy task...
[SMOKE TEST] Task: "Create hello.py in sandbox"
[SMOKE TEST] Phase: init → PASS
[SMOKE TEST] Phase: analyze → PASS (gate: valid plan ✓)
[SMOKE TEST] Phase: execute → PASS (gate: syntax check ✓)
[SMOKE TEST] Phase: verify → PASS (gate: tests pass ✓)
[SMOKE TEST] Phase: commit → PASS
[SMOKE TEST] ✅ SMOKE TEST PASSED (3.2s)
```

---

## 🚦 Gate Specifications

### Gate 1: After Analyze
```python
def validate_plan(analysis: AnalysisResult) -> bool:
    """Ensure plan is actionable"""
    checks = [
        len(analysis.technical_requirements) > 0,
        len(analysis.files_to_modify) > 0,
        analysis.explanation is not None,
        all(os.path.exists(f) for f in analysis.dependencies)
    ]
    return all(checks)
```

### Gate 2: After Execute
```python
def validate_code(code: str, language: str) -> bool:
    """Ensure code compiles/parses"""
    if language == "python":
        try:
            compile(code, "<string>", "exec")
            return True
        except SyntaxError:
            return False
    elif language == "typescript":
        result = subprocess.run(["tsc", "--noEmit"], capture_output=True)
        return result.returncode == 0
```

### Gate 3: After QA
```python
def validate_tests(test_result: TestResult) -> bool:
    """Ensure tests pass"""
    return (
        test_result.passed > 0 and
        test_result.failed == 0 and
        test_result.coverage >= 0.7
    )
```

---

## 📈 Success Metrics Dashboard

| Phase | Metric | Target | Current |
|-------|--------|--------|---------|
| Phase 0 | Success rate | 80% | - |
| Phase 0 | Avg task time | <10min | - |
| Phase 0 | Manual fixes | 0 | - |
| Phase 1 | Success rate | 80% | - |
| Phase 1 | Tasks completed | 10 | - |
| Phase 2 | Bootstrap installs | 1 | - |
| Phase 3 | Frameworks integrated | 3 | - |
| Phase 4 | Parallel tasks | 2 | - |
| Phase 5 | Auto maintenance | 1/day | - |

---

## 🛠️ Runbook Commands

### Start Orchestrator
```bash
cd /c/Projeler/YBIS/.YBIS_Dev
.YBIS_Dev/Agentic/.venv/Scripts/python Agentic/Core/orchestrator_v2.py
```

### Run Single Task
```bash
python Agentic/Core/orchestrator_v2.py --task "TASK-001"
```

### Generate Artifacts
```bash
python Agentic/Tools/artifact_generator.py --task-id TASK-001
```

### Run Gates Only
```bash
python Agentic/Core/gates.py --phase analyze --input .sandbox/analysis.json
```

### Check System Health
```bash
python Agentic/Tools/health_check.py
```

---

## 🎯 Immediate Next Steps (Day 1)

### Step 1: Create Gate Implementation (2 hours)
```
File: Agentic/Core/gates.py
Content: validate_plan(), validate_code(), validate_tests()
```

### Step 2: Update orchestrator_v2.py (3 hours)
```
Add gate checks after analyze_node, execute_node, qa_node
Add retry logic (max 3, exponential backoff)
Add artifact generation calls
```

### Step 3: Create Artifact Generator (2 hours)
```
File: Agentic/Tools/artifact_generator.py
Generate STATE_SNAPSHOT, PLAN, RUNBOOK, DECISIONS, EVIDENCE
```

### Step 4: Test with Simple Task (1 hour)
```
Task: "Add a constant to mathUtils.ts"
Expected: All gates pass, all artifacts generated
```

---

## 🔄 Daily Workflow (Once Phase 0 Complete)

**Morning:**
1. Check TASK_BOARD.md for pending tasks
2. Claim 1 task (move to IN PROGRESS)
3. Run orchestrator with task ID

**During Execution:**
- Monitor gates (should be automatic)
- Intervene only if gate fails 3 times
- Review artifacts in .sandbox/

**Evening:**
1. Review completed tasks (move to DONE)
2. Check success metrics
3. Update BOOTSTRAP_MASTER_PLAN.md status

---

## 📝 Amendment Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2025-12-15 | 1.0 | Initial master plan | Claude |

---

**Last Updated:** 2025-12-15
**Next Review:** After Phase 0 completion
**Status:** Ready for Phase 0 execution
