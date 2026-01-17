# Vendor Research Implementation Plan

> **Date:** 2026-01-12  
> **Status:** 📋 Planning  
> **Priority:** Based on effort vs impact analysis

---

## Current Status Check

### ✅ Already Implemented
- `.pre-commit-config.yaml` - ✅ EXISTS
- `.devcontainer/` - ✅ EXISTS
- `.vscode/` - ✅ EXISTS
- `.github/workflows/` - ✅ EXISTS
- Ruff, Mypy - ✅ Already in use

### ❌ Issues Found
- **Duplicate retry logic:** `retry.py` (custom) vs `resilience.py` (tenacity) - NEEDS CONSOLIDATION
- **Missing security tools:** Bandit, Safety, detect-secrets
- **Missing advanced testing:** Hypothesis, mutmut
- **Missing documentation:** MkDocs
- **Disabled adapters:** EvoAgentX, LangFuse, OpenTelemetry

---

## Priority Matrix

### 🔴 CRITICAL - Fix Immediately (Low Effort, High Impact)

#### 1. Consolidate Retry Logic ⚠️
**Problem:** `retry.py` (custom) duplicates `resilience.py` (tenacity)  
**Impact:** Code duplication, maintenance burden  
**Effort:** 1-2 hours  
**Action:**
- [ ] Audit all `retry.py` usages
- [ ] Migrate to `resilience.py` (tenacity-based)
- [ ] Remove `retry.py`
- [ ] Update all imports

**Files to check:**
- `src/ybis/services/retry.py` (custom implementation)
- `src/ybis/services/resilience.py` (tenacity-based)
- `src/ybis/adapters/local_coder.py` (uses `retry.py`)

---

### 🟡 HIGH PRIORITY - Add This Week (Medium Effort, High Impact)

#### 2. Security Tools 🔒
**Why:** Security vulnerabilities are critical  
**Effort:** 2-3 hours  
**Tools:**
- [ ] **Bandit** - SAST for Python
- [ ] **Safety/pip-audit** - Dependency CVE scanning
- [ ] **detect-secrets** - Hardcoded secrets detection

**Implementation:**
```yaml
# .pre-commit-config.yaml additions
- repo: https://github.com/PyCQA/bandit
  hooks:
    - id: bandit
      args: ["-c", "pyproject.toml"]

- repo: https://github.com/Yelp/detect-secrets
  hooks:
    - id: detect-secrets

- repo: https://github.com/pyupio/safety
  hooks:
    - id: safety
```

#### 3. Advanced Testing 🧪
**Why:** Property-based testing finds 50x more bugs than unit tests  
**Effort:** 3-4 hours  
**Tools:**
- [ ] **Hypothesis** - Property-based testing
- [ ] **mutmut** - Mutation testing (test quality metrics)

**Implementation:**
```python
# tests/property/test_planner.py
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_planner_handles_any_input(text):
    # Property: Planner should never crash on valid input
    plan = plan_task(Task(objective=text))
    assert plan is not None
```

#### 4. Enable Disabled Adapters 🔌
**Why:** Observability is critical for production  
**Effort:** 2-3 hours  
**Adapters:**
- [ ] **EvoAgentX** - Workflow evolution (self-improvement)
- [ ] **LangFuse** - LLM observability (tracing, costs)
- [ ] **OpenTelemetry** - Distributed tracing

**Action:**
- Check why they're disabled
- Fix configuration issues
- Enable in policy/config

---

### 🟢 MEDIUM PRIORITY - Next Sprint (Higher Effort, Medium Impact)

#### 5. Documentation 📚
**Why:** Better docs = easier onboarding  
**Effort:** 4-6 hours  
**Tools:**
- [ ] **MkDocs + Material** - Beautiful documentation site
- [ ] **mkdocstrings** - Auto-generate API docs from docstrings

**Implementation:**
```yaml
# mkdocs.yml
site_name: YBIS Documentation
theme:
  name: material
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
```

#### 6. Prompt Optimization 🤖
**Why:** Better prompts = better LLM results  
**Effort:** 4-5 hours (research + integration)  
**Tool:**
- [ ] **DSPy** - Prompt optimization framework
- [ ] Research integration with `LLMPlanner`

**Action:**
- Research DSPy architecture
- Design integration with existing planner
- Implement optimizer for spec/plan generation

---

### 🔵 LOW PRIORITY - Evaluate Later (High Effort, Uncertain Impact)

#### 7. Multi-Agent Frameworks 🤝
**Why:** May replace current worker/debate system  
**Effort:** Research + evaluation (8+ hours)  
**Frameworks:**
- [ ] **CrewAI** - Multi-agent orchestration (vs current worker system)
- [ ] **AutoGen** - Multi-agent conversations (vs current debate system)

**Action:**
- Deep dive into architecture
- Compare with current implementation
- Decision: Replace or keep current?

#### 8. Enterprise Tools 💼
**Why:** May be overkill for current scale  
**Effort:** High (setup + licensing)  
**Tools:**
- [ ] **SonarQube** - Enterprise code quality
- [ ] **Schemathesis** - API property testing (for MCP)

**Action:**
- Evaluate cost/benefit
- Consider for production deployment

---

## Recommended Execution Order

### Week 1: Critical Fixes
1. ✅ Consolidate retry logic (Day 1)
2. ✅ Add security tools to pre-commit (Day 1-2)
3. ✅ Enable disabled adapters (Day 2-3)

### Week 2: Quality Improvements
4. ✅ Add Hypothesis for property-based testing (Day 1-2)
5. ✅ Add mutmut for mutation testing (Day 2-3)
6. ✅ Setup MkDocs documentation (Day 3-4)

### Week 3: Advanced Features
7. ⚠️ Research DSPy integration (Day 1-2)
8. ⚠️ Evaluate CrewAI/AutoGen (Day 3-4)

---

## Implementation Checklist

### Phase 1: Critical (This Week)
- [ ] Fix duplicate retry logic
- [ ] Add Bandit to pre-commit
- [ ] Add Safety/pip-audit to pre-commit
- [ ] Add detect-secrets to pre-commit
- [ ] Enable EvoAgentX adapter
- [ ] Enable LangFuse adapter
- [ ] Enable OpenTelemetry adapter

### Phase 2: Quality (Next Week)
- [ ] Add Hypothesis to tests
- [ ] Add mutmut to CI
- [ ] Setup MkDocs
- [ ] Add mkdocstrings plugin

### Phase 3: Advanced (Future)
- [ ] Research DSPy
- [ ] Evaluate CrewAI
- [ ] Evaluate AutoGen
- [ ] Consider SonarQube

---

## Notes

- **Constitution Compliance:** All additions must follow "Zero Reinvention" - use vendors, don't rebuild
- **Testing:** Each addition must have tests
- **Documentation:** Update docs as we add tools
- **CI/CD:** All new tools must be integrated into GitHub Actions

---

**Next Step:** Start with Phase 1, Critical fixes

