---
id: TASK-New-7075
type: PLAN
status: DRAFT
created_at: 2025-12-28T22:22:33.805873
target_files:
  - src/agentic/core/plugins/simple_planner.py
  - src/agentic/mcp_server.py
  - src/agentic/core/plugins/model_router.py
  - requirements.txt
  - tests/test_optimization_trinity.py
---

# Task: TASK-OPT-001: Implement Claude Optimization Trinity

## Objective

Implement three critical Claude API features to achieve 70-90% cost reduction and eliminate JSON parsing errors:

1. **Prompt Caching** - Cache system prompts for 1 hour to reduce API costs by 90%
2. **Structured Outputs** - Guarantee JSON schema compliance to eliminate parsing errors
3. **Extended Thinking** - Enable transparent reasoning for better debugging and decision quality

This is Phase 0 (URGENT) from DEBATE-20251228174942 to stop cost bleeding.

## Approach

### Phase 1: Prompt Caching (Day 1 - 3 hours)
- Add `cache_control: {type: "ephemeral"}` to system prompts in SimplePlanner
- Add caching to MCP Server tool definitions
- Implement cache hit/miss tracking for cost analytics
- Test with actual API calls to measure cost reduction

### Phase 2: Structured Outputs (Day 2 - 2 hours)
- Update SimplePlanner to use `response_format: {type: "json_schema"}`
- Generate JSON schemas from Pydantic models (Plan, CodeResult, etc.)
- Add automatic validation and retry logic
- Test with complex plans to verify zero parse errors

### Phase 3: Extended Thinking (Day 2 - 2 hours)
- Add `thinking: {type: "enabled", budget_tokens: 10000}` to SimplePlanner
- Capture and log thinking output for debugging
- Expose thinking logs via MCP tool for transparency
- Test decision quality improvement

### Phase 4: Model Router Update (Day 3 - 1 hour)
- Update model_router.py to use latest Claude models:
  - Planning: claude-sonnet-4-5-20250929
  - Coding: claude-opus-4-5-20251101
- Verify SWE-bench capabilities (80.9% Opus, 77.2% Sonnet)

### Phase 5: Testing & Documentation (Day 3 - 2 hours)
- Create comprehensive test suite
- Document API cost savings
- Update configuration guide
- Add troubleshooting section

## Steps

1. **Setup & Investigation (30 min)**
   - Read SimplePlanner current implementation
   - Read MCP Server current implementation
   - Identify all LLM call sites
   - Check current Anthropic SDK version

2. **Prompt Caching Implementation (2.5 hours)**
   - Update SimplePlanner._create_plan() to add cache_control
   - Update MCP Server system prompts with caching
   - Add CacheAnalytics class to track hits/misses
   - Test caching behavior with repeated calls
   - Measure cost reduction (expect 70-90%)

3. **Structured Outputs Implementation (2 hours)**
   - Create schema generator from Pydantic models
   - Update SimplePlanner to use response_format
   - Add validation layer
   - Add retry logic for schema violations
   - Test with edge cases (complex nested plans)

4. **Extended Thinking Implementation (2 hours)**
   - Add thinking parameter to SimplePlanner calls
   - Create ThinkingLogger to capture reasoning
   - Add MCP tool: get_agent_thinking(task_id)
   - Test with complex architectural decisions
   - Verify reasoning quality improvement

5. **Model Router Update (1 hour)**
   - Update MODEL_CONFIGS in model_router.py
   - Add model version validation
   - Test backward compatibility
   - Document model selection logic

6. **Integration Testing (1.5 hours)**
   - Create test_optimization_trinity.py
   - Test all three features together
   - Test failure modes and edge cases
   - Verify no regressions in existing functionality

7. **Documentation & Metrics (0.5 hours)**
   - Document new configuration options
   - Add usage examples
   - Create cost comparison report
   - Update RUNBOOK.md with findings

## Risks & Mitigations

### Risk 1: Breaking Changes in Anthropic SDK
- **Mitigation:** Pin SDK version, test before upgrade
- **Fallback:** Feature flags to disable if needed

### Risk 2: Cache Invalidation Issues
- **Mitigation:** 1-hour TTL is short enough, monitor hit rates
- **Fallback:** Disable caching via config flag

### Risk 3: Schema Validation Too Strict
- **Mitigation:** Start with loose schemas, tighten gradually
- **Fallback:** Graceful degradation to current parsing

### Risk 4: Extended Thinking Token Budget Exceeded
- **Mitigation:** Set reasonable budget (10k tokens), monitor usage
- **Fallback:** Reduce budget or disable for simple tasks

### Risk 5: Model Version Incompatibility
- **Mitigation:** Test with both old and new models
- **Fallback:** Keep model version configurable

## Success Criteria

### Functional Requirements (Must Have)
- [ ] Prompt caching is active on all system prompts
- [ ] SimplePlanner returns valid JSON 100% of the time
- [ ] Extended thinking logs are captured and accessible
- [ ] All models updated to latest Claude 4.5 versions
- [ ] All existing tests pass (no regressions)

### Performance Requirements (Must Achieve)
- [ ] API cost reduction: 70-90% on repeated requests (measured)
- [ ] JSON parse error rate: 0% (down from current failures)
- [ ] Cache hit rate: >60% in production workloads
- [ ] Thinking overhead: <5% additional latency
- [ ] Model performance: SWE-bench scores match spec

### Quality Requirements (Must Have)
- [ ] Comprehensive test coverage (>80%)
- [ ] All features have feature flags for emergency disable
- [ ] Cost analytics dashboard shows savings
- [ ] Documentation complete and accurate
- [ ] No hardcoded API keys or secrets

### Integration Requirements (Must Work)
- [ ] Works with existing orchestrator_graph.py
- [ ] Compatible with current MCP tools
- [ ] No breaking changes to task workflow
- [ ] Backward compatible with existing configs
- [ ] Graceful degradation if features unavailable

### Deliverables (Must Provide)
- [ ] Updated src/agentic/core/plugins/simple_planner.py
- [ ] Updated src/agentic/mcp_server.py
- [ ] Updated src/agentic/core/plugins/model_router.py
- [ ] New tests/test_optimization_trinity.py
- [ ] Updated requirements.txt (if needed)
- [ ] COST_SAVINGS_REPORT.md in artifacts/
- [ ] Updated RUNBOOK.md with execution log

### Acceptance Test (Final Validation)
- [ ] Run a complete task end-to-end (PLAN -> EXECUTE -> VERIFY)
- [ ] Verify cache hit in second similar task (cost <10% of first)
- [ ] Verify no JSON parse errors in 10 consecutive runs
- [ ] Verify thinking logs captured and readable
- [ ] Verify models are Claude 4.5 (check API response)
- [ ] Generate cost comparison report showing 70%+ savings

