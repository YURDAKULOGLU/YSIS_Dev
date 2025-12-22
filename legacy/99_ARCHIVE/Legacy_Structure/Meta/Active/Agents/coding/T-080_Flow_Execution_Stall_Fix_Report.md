# T-080: Flow Execution Stall - Root Cause Analysis & Fix

**Date**: 2025-12-04
**Agent**: @ClaudeCode (Terminal Coder)
**Status**: ✅ Fix Implemented - Awaiting Deployment

---

## 🔍 Root Cause Analysis

### Problem Summary
Flows were triggered but never completed. No step logs were generated, and executions remained in "running" state indefinitely.

### Investigation Process

1. **Analyzed FlowEngine** (`packages/core/src/services/FlowEngine.ts`)
   - ✅ Engine implementation is correct
   - ✅ Callbacks (onStepStart, onStepEnd) are properly awaited
   - ✅ Logging is comprehensive

2. **Investigated useFlows Hook** (`apps/mobile/src/features/flows/hooks/useFlows.ts`)
   - ✅ Flow execution logic is correct
   - ✅ DB insert/update calls are properly structured
   - ⚠️ DB errors in callbacks are caught and logged but not thrown

3. **Checked Database State**
   - ❌ No flow_executions records found in DB
   - ❌ Initial execution record insert was failing silently

4. **Identified RLS Policy Issue**
   - **PRIMARY CAUSE**: `flow_executions` INSERT policy in migration `013_optimize_rls_performance.sql`
   ```sql
   CREATE POLICY "Users can create flow executions" ON flow_executions
     FOR INSERT
     WITH CHECK (
       workspace_id IN (
         SELECT id FROM workspaces WHERE owner_id = (select auth.uid())
       )
       AND user_id = (select auth.uid())
     );
   ```

   **The Bug**: When `workspace_id` is `NULL`, the policy check fails because:
   - `NULL IN (SELECT ...)` returns `NULL` (not `FALSE`)
   - SQL treats `NULL` as unknown, causing the policy to fail
   - Insert is **silently rejected** by RLS without throwing an error

### Why Silent Failure?
- Supabase RLS policy violations don't throw exceptions to client
- They return empty result sets or affect 0 rows
- Code in useFlows (line 1076-1089) wraps insert in try-catch but RLS failures don't trigger catch block
- Result: No execution record created, flow appears to hang

---

## ✅ Solution Implemented

Created migration `016_fix_flow_executions_rls.sql` with fixes:

### 1. Fixed INSERT Policy
```sql
CREATE POLICY "Users can create flow executions" ON flow_executions
  FOR INSERT
  WITH CHECK (
    user_id = (select auth.uid())
    AND (
      workspace_id IS NULL                           -- ✅ Allow NULL workspace_id
      OR workspace_id IN (
        SELECT id FROM workspaces WHERE owner_id = (select auth.uid())
      )
    )
  );
```

### 2. Fixed SELECT Policy
```sql
CREATE POLICY "Users can read flow executions in their workspace" ON flow_executions
  FOR SELECT
  USING (
    user_id = (select auth.uid())                    -- ✅ User can read their own
    OR workspace_id IN (
      SELECT id FROM workspaces WHERE owner_id = (select auth.uid())
    )
  );
```

### 3. Added Missing UPDATE Policy
```sql
CREATE POLICY "Users can update their flow executions" ON flow_executions
  FOR UPDATE
  USING (user_id = (select auth.uid()));
```

### 4. Optimized flow_execution_steps Policies
- Updated to use `(select auth.uid())` instead of `auth.uid()` for performance
- Prevents re-evaluation for every row (Supabase best practice)

---

## 📋 Deployment Steps

**REQUIRED**: Apply migration to production database

```bash
# Option 1: Via Supabase Dashboard
# 1. Open Supabase Dashboard > SQL Editor
# 2. Run the SQL from: supabase/migrations/016_fix_flow_executions_rls.sql

# Option 2: Via CLI (if available)
npx tsx scripts/apply-migration.ts 016_fix_flow_executions_rls.sql
```

---

## ✅ Testing Checklist

After migration is applied:

- [ ] Create a new flow via mobile app
- [ ] Trigger flow execution manually
- [ ] Verify `[FLOW_ENGINE]` logs appear in console
- [ ] Verify flow completes with success/fail status
- [ ] Run `npx tsx scripts/inspect-flow.ts` to verify:
  - Execution record exists in `flow_executions`
  - Steps are logged in `flow_execution_steps`
  - Execution has `completed_at` timestamp
- [ ] Check UI reflects correct execution status

---

## 📊 Expected Results After Fix

1. **Flow executions will be created in DB** (even when workspace_id is null)
2. **Step logs will be recorded** in `flow_execution_steps` table
3. **Executions will complete** with proper status (completed/failed)
4. **UI will show correct status** (not stuck on "running")
5. **inspect-flow tool will show full trace** of execution steps

---

## 🎯 Related Files Modified

- `supabase/migrations/016_fix_flow_executions_rls.sql` (NEW)
- `scripts/apply-migration.ts` (NEW - helper script)

## 🔗 References

- Task: `.YBIS_Dev/ysis_agentic/tasks/in_progress/T-080_Fix_Flow_Execution_Stall.md`
- FlowEngine: `packages/core/src/services/FlowEngine.ts`
- useFlows Hook: `apps/mobile/src/features/flows/hooks/useFlows.ts`
- Inspect Tool: `scripts/inspect-flow.ts`

---

**Next Actions**: Apply migration and test flow execution end-to-end.
