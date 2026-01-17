# YBIS Task Creation Standard

**Date:** 2026-01-10  
**Purpose:** Define standards for creating native YBIS tasks that are comprehensive, not shallow.

---

## Principle: Evidence-First, Not Shallow

**❌ Shallow Task (BAD):**
```
Title: "Fix bug"
Objective: "Fix the bug in test execution"
Priority: "HIGH"
```

**✅ Comprehensive Task (GOOD):**
```
Title: "Fix MCP Test Execution Timeout in Thread Pool"
Objective: |
  Fix the timeout issue in MCP test execution when running tests via thread pool.
  The issue occurs in `src/ybis/services/mcp_tools/test_tools.py` where `asyncio.to_thread()`
  or `loop.run_in_executor()` causes subprocess.run() to timeout after 10 seconds, even though
  direct execution completes in ~2 seconds.
  
  Requirements:
  - Investigate why thread pool execution times out
  - Fix the timeout mechanism
  - Ensure tests complete in <5 seconds via MCP
  - Add proper error handling and logging
  - Update documentation
  
  Success Criteria:
  - Tests run via MCP complete successfully
  - No timeout errors
  - Execution time <5 seconds
  - All existing tests pass
Priority: "HIGH"
```

---

## Task Structure

### 1. Title
- **Format:** `[Category]: [Specific Action] [Context]`
- **Examples:**
  - `Fix: MCP Test Execution Timeout in Thread Pool`
  - `Feature: Add Streaming Output Support to MCP Tools`
  - `Refactor: Optimize Adapter Availability Check with Better Caching`
  - `Integration: Complete EvoAgentX Real Evolution Implementation`

### 2. Objective (Detailed)
Must include:
- **Problem Statement:** What is the issue/need?
- **Context:** Where does this occur? What files/modules are involved?
- **Requirements:** What must be done?
- **Success Criteria:** How do we know it's done?
- **Dependencies:** What other tasks/features does this depend on?
- **Risks:** What could go wrong?

### 3. Priority
- **HIGH:** Critical bugs, security issues, blocking features
- **MEDIUM:** Important improvements, non-blocking features
- **LOW:** Nice-to-have, optimizations, documentation

### 4. Workflow Selection
- **`self_develop`:** For self-development tasks (recommended)
- **`ybis_native`:** For standard development tasks
- **`self_improve`:** For vendor-based self-improvement

---

## Task Creation Template

```python
task_create(
    title="[Category]: [Specific Action] [Context]",
    objective="""
# Problem Statement
[Clear description of the problem or need]

# Context
- Files involved: [list files]
- Modules affected: [list modules]
- Related issues: [link to related tasks/issues]

# Requirements
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

# Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

# Dependencies
- [Dependency 1]
- [Dependency 2]

# Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

# Implementation Notes
[Any additional context, constraints, or considerations]
""",
    priority="HIGH|MEDIUM|LOW"
)
```

---

## Examples

### Example 1: Bug Fix

```python
task_create(
    title="Fix: MCP Test Execution Timeout in Thread Pool",
    objective="""
# Problem Statement
MCP test execution times out when running tests via thread pool. Direct execution 
completes in ~2 seconds, but thread pool execution times out after 10 seconds.

# Context
- File: `src/ybis/services/mcp_tools/test_tools.py`
- Function: `run_tests()` - uses `asyncio.to_thread()` or `loop.run_in_executor()`
- Related: Test execution optimization (parallel adapter checks work fine)

# Requirements
1. Investigate why thread pool execution times out
2. Fix timeout mechanism (possibly use direct subprocess.run() since tests are fast)
3. Ensure tests complete in <5 seconds via MCP
4. Add proper error handling and logging
5. Update documentation

# Success Criteria
- [ ] Tests run via MCP complete successfully
- [ ] No timeout errors
- [ ] Execution time <5 seconds
- [ ] All existing tests pass
- [ ] Documentation updated

# Dependencies
- Test execution optimization (already done - tests are fast now)

# Risks
- Risk: Breaking existing test execution
  Mitigation: Test thoroughly, keep fallback mechanisms
- Risk: Performance regression
  Mitigation: Benchmark before/after

# Implementation Notes
- Tests are now fast (~2 seconds) due to parallel adapter checks
- May not need thread pool at all - direct subprocess.run() might be fine
- Consider using `asyncio.to_thread()` with proper timeout handling
""",
    priority="HIGH"
)
```

### Example 2: Feature Addition

```python
task_create(
    title="Feature: Add Streaming Output Support to MCP Tools",
    objective="""
# Problem Statement
MCP tools currently return complete results only after execution finishes. 
For long-running operations (tests, linting), users need real-time feedback.

# Context
- Files: `src/ybis/services/mcp_tools/test_tools.py`, `src/ybis/services/mcp_server.py`
- Related: MCP protocol supports streaming via Server-Sent Events (SSE)

# Requirements
1. Implement streaming output for `run_tests`, `run_linter`, `check_test_coverage`
2. Use SSE or chunked responses for real-time output
3. Maintain backward compatibility (non-streaming mode)
4. Add configuration option to enable/disable streaming
5. Update MCP server to support streaming responses

# Success Criteria
- [ ] Streaming output works for test execution
- [ ] Streaming output works for linting
- [ ] Backward compatibility maintained
- [ ] Configuration option added
- [ ] Documentation updated

# Dependencies
- MCP server SSE support (already exists)

# Risks
- Risk: Breaking existing MCP clients
  Mitigation: Make streaming opt-in, maintain non-streaming mode
- Risk: Performance overhead
  Mitigation: Benchmark and optimize

# Implementation Notes
- MCP protocol supports streaming via `TextContent` chunks
- FastMCP may need updates for streaming support
- Consider using `asyncio.Queue` for output buffering
""",
    priority="MEDIUM"
)
```

### Example 3: Integration Task

```python
task_create(
    title="Integration: Complete EvoAgentX Real Evolution Implementation",
    objective="""
# Problem Statement
EvoAgentX adapter currently has placeholder implementation. Need to complete 
real evolution using TextGradOptimizer and full YBIS↔EvoAgentX conversion.

# Context
- Files: `src/ybis/adapters/evoagentx.py`, `vendors/EvoAgentX/`
- Related: EvoAgentX integration status, missing dependencies

# Requirements
1. Install missing dependencies (dashscope, etc.)
2. Implement real evolution using TextGradOptimizer
3. Complete YBIS workflow spec ↔ EvoAgentX format conversion
4. Test end-to-end evolution workflow
5. Add error handling and logging
6. Update documentation

# Success Criteria
- [ ] All dependencies installed
- [ ] Real evolution works with TextGradOptimizer
- [ ] YBIS↔EvoAgentX conversion complete
- [ ] End-to-end test passes
- [ ] Documentation updated

# Dependencies
- EvoAgentX dependencies installation
- YBIS workflow spec format understanding

# Risks
- Risk: EvoAgentX API changes
  Mitigation: Pin versions, test thoroughly
- Risk: Performance issues
  Mitigation: Benchmark, add timeouts

# Implementation Notes
- EvoAgentX uses TextGrad, AFlow, MIPRO, SEW optimizers
- Need to convert YBIS workflow specs to EvoAgentX format
- Consider caching evolution results
""",
    priority="HIGH"
)
```

---

## Task Workflow

### Step 1: Create Task
```python
task = await task_create(title, objective, priority)
task_id = task["task_id"]
```

### Step 2: Run Workflow
```python
await task_run(task_id, workflow_name="self_develop")
```

### Step 3: Monitor Progress
```python
while True:
    status = await task_status(task_id)
    if status["status"] == "completed":
        break
    await asyncio.sleep(5)
```

### Step 4: Review Artifacts
```python
spec = await artifact_read(task_id, "spec.md")
plan = await artifact_read(task_id, "plan.json")
verifier_report = await artifact_read(task_id, "verifier_report.json")
gate_report = await artifact_read(task_id, "gate_report.json")
```

### Step 5: Approve (if needed)
```python
if gate_report["decision"] == "BLOCK":
    await approval_write(task_id, run_id, approver="user", reason="Changes look good")
```

---

## Quality Checklist

Before creating a task, ensure:
- [ ] Title is specific and descriptive
- [ ] Objective includes problem statement
- [ ] Objective includes context (files, modules)
- [ ] Objective includes requirements (numbered list)
- [ ] Objective includes success criteria (checkboxes)
- [ ] Objective includes dependencies
- [ ] Objective includes risks and mitigations
- [ ] Priority is appropriate
- [ ] Workflow is selected (`self_develop` recommended)

---

## Anti-Patterns (What NOT to Do)

### ❌ Shallow Task
```
Title: "Fix bug"
Objective: "Fix the bug"
Priority: "HIGH"
```

### ❌ Vague Task
```
Title: "Improve performance"
Objective: "Make it faster"
Priority: "MEDIUM"
```

### ❌ Too Broad Task
```
Title: "Refactor everything"
Objective: "Refactor all code"
Priority: "HIGH"
```

### ❌ Missing Context
```
Title: "Add feature"
Objective: "Add the new feature"
Priority: "MEDIUM"
```

---

## Best Practices

1. **Be Specific:** Use exact file names, function names, line numbers
2. **Be Comprehensive:** Include all context, requirements, success criteria
3. **Be Realistic:** Don't create tasks that are too large (break them down)
4. **Be Evidence-First:** Every task should produce artifacts (spec, plan, reports)
5. **Be Traceable:** Link to related tasks, issues, discussions

---

## Conclusion

**From now on, all tasks will be:**
- ✅ Created in YBIS native task system
- ✅ Comprehensive, not shallow
- ✅ Evidence-first (spec + plan + execute + verify + gate)
- ✅ Using `self_develop` workflow
- ✅ Following this standard

**No more shallow tasks!** 🚀

