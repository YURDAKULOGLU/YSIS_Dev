---
id: TASK-New-9134
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-28T23:19:09.636528
updated_at: 2025-12-28T23:20:00
target_files:
  - src/agentic/core/graphs/orchestrator_graph.py
  - src/agentic/core/plugins/smart_planner.py
  - src/agentic/core/config.py
  - scripts/run_orchestrator.py
---

# Task: Optimization Trinity Activation (Claude Only)

## Objective

**Goal:** Integrate LiteLLM Universal Provider into production orchestrator with Optimization Trinity features (Prompt Caching, Structured Outputs, Extended Thinking) enabled for Claude API, with graceful fallback to Ollama.

**Context:**
- TASK-New-7075 completed: LiteLLM implementation done, 22/22 tests passing
- SimplePlannerV2 exists but NOT wired to orchestrator
- Current system uses SmartPlanner → Ollama direct (no Trinity features)
- Need to integrate WITHOUT breaking existing system

**Success Definition:**
- Orchestrator uses UniversalLLMProvider (feature-flagged)
- Prompt caching active (90% cost reduction on Claude)
- Structured outputs active (zero JSON errors)
- Extended thinking available (Claude only)
- Ollama fallback works (existing system preserved)
- Metrics tracked (cost, latency, parse errors)

---

## Approach

### Strategy: Feature-Flagged Integration

**Key Principle:** Zero breaking changes, gradual rollout, easy rollback

```python
# Feature flag approach
YBIS_USE_LITELLM = os.getenv("YBIS_USE_LITELLM", "false")

if YBIS_USE_LITELLM == "true":
    # New path: UniversalLLMProvider
    planner = SimplePlannerV2()
else:
    # Old path: SmartPlanner (Ollama)
    planner = SmartPlanner()
```

**Benefits:**
1. ✅ No forced migration (default = old system)
2. ✅ Gradual testing (opt-in per run)
3. ✅ Easy rollback (flip env var)
4. ✅ Side-by-side comparison (metrics)
5. ✅ User choice preserved

---

## Steps

### **Phase 1: Configuration & Feature Flags (1-2 hours)**

**1.1 Add Feature Flags to config.py**
- Add `USE_LITELLM` flag (default: false)
- Add `LITELLM_PROVIDER` selection (default: auto)
- Add `LITELLM_QUALITY` level (high/medium/low)
- Add `ENABLE_PROMPT_CACHING` (default: true)
- Add `ENABLE_STRUCTURED_OUTPUT` (default: true)
- Add `ENABLE_EXTENDED_THINKING` (default: false)

**1.2 Environment Variables**
```bash
# Feature toggle
YBIS_USE_LITELLM=false          # Enable LiteLLM (default: false)

# Provider selection
YBIS_LITELLM_PROVIDER=auto      # auto|claude|openai|gemini|ollama
YBIS_LITELLM_QUALITY=high       # high|medium|low

# Feature toggles
YBIS_ENABLE_CACHING=true        # Prompt caching (default: true)
YBIS_ENABLE_STRUCTURED=true     # Structured outputs (default: true)
YBIS_ENABLE_THINKING=false      # Extended thinking (default: false)
```

**Expected Output:**
- `src/agentic/core/config.py` updated with flags
- Clear documentation of env vars

---

### **Phase 2: Orchestrator Integration (2-3 hours)**

**2.1 Update orchestrator_graph.py**
- Import both SmartPlanner and SimplePlannerV2
- Add provider selection logic
- Add feature detection
- Preserve existing behavior if flag=false

**2.2 Wire SimplePlannerV2**
```python
# In orchestrator_graph.py
from src.agentic.core.config import USE_LITELLM

if USE_LITELLM:
    from src.agentic.core.plugins.simple_planner_v2 import SimplePlannerV2
    planner = SimplePlannerV2(
        quality=config.LITELLM_QUALITY
    )
else:
    from src.agentic.core.plugins.smart_planner import SmartPlanner
    planner = SmartPlanner()
```

**2.3 Update run_orchestrator.py**
- Add flag logging (show which path is active)
- Add provider status check
- Add fallback warnings

**Expected Output:**
- Orchestrator supports both paths
- Clear logging of active path
- Zero breaking changes to existing workflow

---

### **Phase 3: Metrics & Observability (1-2 hours)**

**3.1 Add Metrics Collection**
- Track cost per request
- Track latency per request
- Track cache hit rate (Claude only)
- Track JSON parse errors (before/after)
- Track provider used

**3.2 Create Metrics Reporter**
```python
class OptimizationMetrics:
    def __init__(self):
        self.total_cost = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.parse_errors = 0
        self.requests_by_provider = {}

    def report(self) -> Dict[str, Any]:
        # Return metrics summary
        pass
```

**3.3 Add to RUNBOOK.md**
- Log metrics after each plan generation
- Show cost savings vs. non-cached
- Show parse error rate

**Expected Output:**
- Comprehensive metrics tracking
- Clear reporting in RUNBOOK.md
- Ability to compare old vs new path

---

### **Phase 4: Testing & Validation (2-3 hours)**

**4.1 Test Suite**
- Test with flag=false (should use SmartPlanner)
- Test with flag=true (should use SimplePlannerV2)
- Test fallback (API fail → Ollama)
- Test metrics collection
- Test each Trinity feature independently

**4.2 Integration Tests**
```python
# Test 1: Feature flag off (existing system)
assert orchestrator uses SmartPlanner
assert no LiteLLM calls

# Test 2: Feature flag on (new system)
assert orchestrator uses SimplePlannerV2
assert LiteLLM is called
assert metrics are tracked

# Test 3: Claude API available
assert prompt caching is used
assert structured outputs enabled
assert cost < non-cached cost

# Test 4: Claude API not available
assert fallback to Ollama
assert system still works
assert no errors
```

**4.3 Manual Validation**
- Run 5 tasks with flag=false → verify old behavior
- Run 5 tasks with flag=true → verify new behavior
- Compare metrics (cost, quality, errors)
- Verify cache hits on repeated prompts

**Expected Output:**
- Comprehensive test coverage
- Both paths verified working
- Metrics prove cost savings
- Zero regressions

---

### **Phase 5: Documentation & Rollout (1 hour)**

**5.1 Update Documentation**
- Update README with feature flag usage
- Document how to enable Trinity features
- Add migration guide (old → new)
- Add troubleshooting guide

**5.2 Create RESULT.md**
- Document integration approach
- Show before/after metrics
- Provide rollout recommendations
- Document known limitations

**5.3 Rollout Strategy**
```
Week 1: Internal testing (flag=true for 10% of runs)
Week 2: Expanded testing (flag=true for 50% of runs)
Week 3: Production ready (default=true if metrics good)
Week 4: Deprecate old path (remove SmartPlanner)
```

**Expected Output:**
- Clear documentation
- Phased rollout plan
- Success metrics defined

---

## Risks & Mitigations

### Risk 1: Breaking Existing System
**Impact:** HIGH
**Probability:** LOW (with feature flag)
**Mitigation:**
- Feature flag defaults to false (existing system)
- Side-by-side testing before switching
- Easy rollback (flip flag)
- Comprehensive tests for both paths

### Risk 2: LiteLLM Dependency Failure
**Impact:** MEDIUM
**Probability:** LOW
**Mitigation:**
- Automatic fallback to Ollama
- Comprehensive error handling in provider
- 22/22 tests already passing
- Production-proven library (10k+ stars)

### Risk 3: Cost Explosion (API calls)
**Impact:** MEDIUM
**Probability:** LOW (with caching)
**Mitigation:**
- Prompt caching reduces costs by 90%
- Default to Ollama (free) if no API key
- Cost tracking and alerts
- User controls via env vars

### Risk 4: Metrics Overhead
**Impact:** LOW
**Probability:** MEDIUM
**Mitigation:**
- Lightweight metrics (dict updates)
- Optional (can disable via flag)
- Only log summary, not every detail

### Risk 5: Feature Detection Bugs
**Impact:** LOW
**Probability:** LOW
**Mitigation:**
- Feature detection already implemented in LiteLLM
- Tested in 22 unit tests
- Graceful degradation (features → off if unsupported)

---

## Success Criteria

### Must-Have (Phase Gate):
- ✅ Feature flag implemented and working
- ✅ Both paths (old/new) work correctly
- ✅ Prompt caching reduces cost by >80%
- ✅ Structured outputs reduce parse errors to <1%
- ✅ Ollama fallback works (no API key needed)
- ✅ Zero breaking changes to existing system
- ✅ Comprehensive tests pass
- ✅ Documentation complete

### Nice-to-Have:
- Extended thinking examples in RUNBOOK
- Performance benchmarks (old vs new)
- Cost comparison dashboard
- Auto-switching based on task complexity

### Metrics Targets:
- **Cost Reduction:** >80% with caching (vs. non-cached)
- **Parse Errors:** <1% (vs. 5-10% with old system)
- **Latency:** <5s average (cached), <10s (uncached)
- **Availability:** 99%+ (with Ollama fallback)
- **Cache Hit Rate:** >70% on repeated patterns

---

## Timeline

**Total Estimated Time:** 7-11 hours

- Phase 1 (Config): 1-2 hours
- Phase 2 (Integration): 2-3 hours
- Phase 3 (Metrics): 1-2 hours
- Phase 4 (Testing): 2-3 hours
- Phase 5 (Docs): 1 hour

**Target Completion:** Within 1-2 days

---

## Dependencies

### Completed:
- ✅ TASK-New-7075 (LiteLLM implementation)
- ✅ SimplePlannerV2 (tested, working)
- ✅ UniversalLLMProvider (22/22 tests pass)

### Blockers:
- ⚠️ Waiting on DEBATE-20251228223115 decision (use LiteLLM or manual?)
- ⚠️ If manual provider chosen, this task needs redesign

### Parallel Work:
- Gemini: TASK-New-7553 (Langfuse observability)
- Codex: TASK-New-4130 (Provider abstraction)

**Coordination:**
- Need to align with Codex on provider abstraction
- Langfuse integration can happen in parallel
- No conflicts expected

---

## Notes

### Key Decisions:
1. **Feature Flag Strategy:** Default OFF, gradual rollout
2. **Provider Selection:** Auto-detect best available
3. **Fallback Chain:** API → CLI → Ollama
4. **Metrics:** Lightweight, optional, summary-only

### Technical Debt:
- SmartPlanner will be deprecated after successful rollout
- Need to add more comprehensive integration tests
- Consider adding provider health checks

### Future Enhancements:
- Auto-switch provider based on task complexity
- Multi-provider consensus (use 2+ providers, compare)
- Advanced caching strategies (semantic similarity)
- Cost budgets and alerts

---

**Status:** Ready to begin implementation
**Next Step:** Phase 1 - Add feature flags to config.py
