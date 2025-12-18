---
type: bug
priority: critical
status: backlog
assignee: @Coding
---

# Fix Flow Execution Stalling & Logging

**Description:**
Flows are triggered (`User triggered flow run` log appears), but they never complete. No step logs are generated, and the execution seems to hang indefinitely.

**Symptoms:**
- Log shows `[USER_ACTION] User triggered flow run`.
- No subsequent `[FLOW_ENGINE]` logs for steps.
- Execution status in DB likely remains 'running' forever (zombie).
- `inspect-flow` tool shows no steps.

**Root Cause Hypothesis:**
- Client-side `FlowEngine` might be failing silently before the first step.
- `db.insert` for execution record might be hanging or failing without throwing to UI.
- `useFlows` hook state update might be blocking the engine.

**Acceptance Criteria:**
- [ ] Flow runs to completion (success/fail).
- [ ] All steps are logged to `flow_execution_steps` table.
- [ ] `inspect-flow` shows full execution trace.
- [ ] UI reflects correct status (not stuck on running).
