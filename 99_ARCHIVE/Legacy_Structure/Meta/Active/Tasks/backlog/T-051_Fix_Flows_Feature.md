---
type: task
status: backlog
priority: high
assignee: "@ClaudeCode"
proposal: "P-001"
---

# T-051: Fix Flows Feature Architecture & Bugs

**Blocker:** `T-080_Fix_Flow_Execution_Stall.md` (Critical Fix)

## Objective
Refactor the "Flows" feature to use a consistent state management pattern (Zustand) and fix critical bugs preventing flow execution.

## Context
The current implementation has conflicting state logic (`useFlows` vs `useFlowsStore`) and broken data formats (Trigger Object vs Cron). See **Proposal P-001** for details.

## Requirements

### 1. Refactor State Management
- [ ] Update `apps/mobile/src/stores/useFlowsStore.ts`:
    - Add `runFlow` action.
    - Ensure all CRUD operations are robust.
- [ ] Update `apps/mobile/src/features/flows/hooks/useFlows.ts`:
    - Remove internal `useState` logic.
    - Wrap `useFlowsStore`.
    - Register Output Handlers (`output_notification`, `output_note`, `output_task`) in the `FlowEngine` setup.

### 2. Fix FlowBuilder
- [ ] Update `apps/mobile/src/features/flows/components/FlowBuilder.tsx`:
    - Convert Schedule Object to Cron String on save.
    - Add UI for Tool Parameters (when AI is disabled).

### 3. Core Engine Updates
- [ ] Update `packages/core/src/services/FlowEngine.ts`:
    - Implement a mock/stub for AI processing to prevent crashes.

### 4. Fix RLS Policies
- [x] Update `supabase/migrations/003_create_flows_table.sql` (or create new migration):
    - **DONE:** Created `supabase/migrations/014_fix_flows_rls.sql`.
    - **VERIFIED:** Checked against live schema. `profiles` table links users to workspaces, so the policy is correct.
    - Modify "Users can create flows in their workspace" policy.
    - Allow creation if user is a *member* of the workspace, not just the *owner*.
    - Check `workspace_members` table (if exists) or adjust logic.

## Acceptance Criteria
- [ ] User can create a Scheduled Flow (saved as Cron).
- [ ] User can run a Flow manually.
- [ ] Output actions (e.g., Notification) actually trigger.
