# E2E Test: Sandbox & Git Worktree Verification

**Date:** 2026-01-08  
**Purpose:** Verify sandbox mode and git worktree integration in E2E tests

---

## Pre-Test Setup

### 1. Environment Variables

```bash
# Optional: E2B API key (only needed if sandbox.type is "e2b")
# export E2B_API_KEY=your_e2b_api_key_here
```

### 2. Policy Configuration

```yaml
# configs/profiles/e2e.yaml
sandbox:
  enabled: true
  type: "local"  # Use local subprocess (no cloud)
  network: false
```

Enable the profile for this run:
```bash
export YBIS_PROFILE=e2e
```

### 3. Git Repository

Ensure you're in a git repository:
```bash
git status  # Should show git repository
```

---

## Test Scenarios

### Scenario A: Sandbox Execution Verification

**Objective:** Verify commands execute under the configured sandbox mode.

**Test Steps:**
1. Run the task: `python scripts/e2e_test_runner.py 4`
2. Note the printed `TASK CREATED` and `Run path`.
3. Check journal: `<run_path>/journal/events.jsonl`

**Expected Events (local mode):**
```json
{"event_type": "COMMAND_EXEC", "payload": {"sandbox_used": false}}
```

**Expected Events (E2B mode):**
```json
{"event_type": "SANDBOX_CREATED", "payload": {"sandbox_type": "e2b", "sandbox_id": "..."}}
{"event_type": "SANDBOX_COMMAND_EXEC", "payload": {"command": "python test_sandbox.py", "exit_code": 0}}
{"event_type": "SANDBOX_CLOSED", "payload": {"sandbox_type": "e2b"}}
```

**Verification:**
- ✅ Local mode: `sandbox_used: false` in `COMMAND_EXEC`
- ✅ E2B mode: `SANDBOX_CREATED`/`SANDBOX_COMMAND_EXEC`/`SANDBOX_CLOSED` events exist

---

### Scenario B: Git Worktree Isolation

**Objective:** Verify each run gets its own git worktree.

**Test Steps:**
1. Run the task: `python scripts/e2e_test_runner.py 1`
2. Note the printed `TASK CREATED` and `Run path`.
3. Check git worktrees: `git worktree list`
4. Check journal: `<run_path>/journal/events.jsonl`

**Expected Events:**
```json
{"event_type": "GIT_WORKTREE_CREATED", "payload": {"branch_name": "task-T-XXX-run-R-XXX", "worktree_path": "..."}}
```

**Verification:**
- ✅ `GIT_WORKTREE_CREATED` event exists
- ✅ Git worktree exists: `git worktree list` shows the branch
- ✅ Worktree path matches run path
- ✅ Changes are isolated (not in main branch)

---

### Scenario C: Fallback Behavior

**Objective:** Verify graceful fallback when sandbox or git not available.

**Test Steps:**
1. **Sandbox Fallback:** Set `sandbox.type: "local"`
2. Run a task
3. Check journal for fallback events

**Expected Events:**
```json
{"event_type": "SANDBOX_FALLBACK", "payload": {"reason": "...", "fallback": "local_subprocess"}}
```

**Verification:**
- ✅ `SANDBOX_FALLBACK` event exists when E2B unavailable
- ✅ Commands still execute (using subprocess)
- ✅ No crashes or errors

**Git Fallback:**
1. Run task in non-git directory
2. Check journal for fallback events

**Expected Events:**
```json
{"event_type": "GIT_WORKTREE_SKIPPED", "payload": {"reason": "Not a git repository"}}
```

**Verification:**
- ✅ `GIT_WORKTREE_SKIPPED` event exists
- ✅ Regular directory created (not worktree)
- ✅ Task still executes successfully

---

### Scenario D: Sandbox + Worktree Integration

**Objective:** Verify both sandbox and worktree work together.

**Test Steps:**
1. Set `sandbox.type: "e2b"` in policy and export `YBIS_PROFILE=e2e`
2. Ensure git repository exists
3. Create task: "Create and modify a file"
4. Run task
5. Check both sandbox and worktree events

**Expected Events:**
```json
{"event_type": "GIT_WORKTREE_CREATED", ...}
{"event_type": "SANDBOX_CREATED", ...}
{"event_type": "SANDBOX_COMMAND_EXEC", ...}
{"event_type": "SANDBOX_CLOSED", ...}
```

**Verification:**
- ✅ Both `GIT_WORKTREE_CREATED` and `SANDBOX_CREATED` events exist
- ✅ Commands executed in sandbox
- ✅ Changes isolated in git worktree
- ✅ Both cleanup properly after run

---

## Journal Event Reference

### Sandbox Events

- `SANDBOX_CREATED` - E2B sandbox created
- `SANDBOX_COMMAND_EXEC` - Command executed in sandbox
- `SANDBOX_FILE_WRITE` - File written in sandbox
- `SANDBOX_FILE_READ` - File read from sandbox
- `SANDBOX_CLOSED` - Sandbox closed
- `SANDBOX_CREATE_FAILED` - Sandbox creation failed
- `SANDBOX_COMMAND_ERROR` - Command execution error
- `SANDBOX_FALLBACK` - Fallback to local execution

### Git Worktree Events

- `GIT_WORKTREE_CREATED` - Worktree created
- `GIT_WORKTREE_REUSED` - Existing worktree reused
- `GIT_WORKTREE_SKIPPED` - Worktree skipped (not git repo)
- `GIT_WORKTREE_FAILED` - Worktree creation failed
- `GIT_WORKTREE_REMOVED` - Worktree removed
- `GIT_WORKTREE_REMOVE_FAILED` - Worktree removal failed
- `GIT_WORKTREE_CLEANUP_ERROR` - Cleanup error

---

## Troubleshooting

### E2B Sandbox Not Working

**Symptoms:**
- No `SANDBOX_CREATED` events
- `SANDBOX_CREATE_FAILED` events

**Solutions:**
1. Check `E2B_API_KEY` is set: `echo $E2B_API_KEY`
2. Check policy: `sandbox.type: "e2b"` in `configs/profiles/e2e.yaml`       
3. Check E2B SDK installed: `pip list | grep e2b`
4. Check network connectivity to E2B API

### Git Worktree Not Working

**Symptoms:**
- No `GIT_WORKTREE_CREATED` events
- `GIT_WORKTREE_SKIPPED` events

**Solutions:**
1. Check git repository: `git status`
2. Check GitPython installed: `pip list | grep GitPython`
3. Check git version: `git --version` (needs 2.5+)
4. Check permissions: Can create branches?

---

## Success Criteria

**A test passes if:**
- ✅ All expected events appear in journal
- ✅ No error events (`*_FAILED`, `*_ERROR`)
- ✅ Sandbox isolation works (commands in sandbox)
- ✅ Git isolation works (changes in worktree)
- ✅ Fallback works gracefully (no crashes)

---

## Integration with E2E Stress Test Plan

These verification scenarios should be run **before** the main E2E stress tests:

1. **Pre-Flight Check:** Run Scenario A, B, C to verify setup
2. **Main Tests:** Run E2E_STRESS_TEST_PLAN.md scenarios
3. **Post-Flight Check:** Verify sandbox/worktree events in all runs

---

## References

- **E2B Docs:** https://e2b.dev/docs
- **GitPython Docs:** https://gitpython.readthedocs.io/
- **E2E Stress Test Plan:** `docs/E2E_STRESS_TEST_PLAN.md`
- **Sandbox Integration:** `docs/SANDBOX_INTEGRATION_SUMMARY.md`


