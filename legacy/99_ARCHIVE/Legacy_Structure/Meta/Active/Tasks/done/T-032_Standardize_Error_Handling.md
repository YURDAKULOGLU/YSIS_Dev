# Task ID: T-032

- **Source Document:** `RELEASE_READINESS_ASSESSMENT.md`, `PRODUCTION_CHECKLIST.md`
- **Title:** (P1) Standardize Error Handling - Replace console.error/warn with Logger
- **Description:** 
  Some code still uses `console.error`, `console.warn`, or `console.log` instead of the standardized `Logger` from `@ybis/logging`. This creates inconsistent logging and makes it harder to track errors in production.

  **Current Status:**
  - ✅ Most code uses `Logger` from `@ybis/logging`
  - ⚠️ Some files still use `console.warn` in logging sinks (may be intentional to avoid recursion)
  - ⚠️ Commented-out `console.log` statements exist (low priority)

  **Files with console usage:**
  - `apps/mobile/src/logging/file-sink.ts` - `console.warn` (line 84) - May be intentional (logging sink)
  - `apps/mobile/src/logging/remote-sink.ts` - `console.warn` (line 16) - May be intentional (logging sink)
  - `apps/mobile/src/features/widgets/components/WidgetItemsList.tsx` - Commented `console.log` (line 167) - Low priority
  - `apps/mobile/src/services/database.ts` - Commented `console.warn` (line 68) - Low priority

  **Requirements:**
  1. Review logging sink files - `console.warn` in sinks may be intentional to avoid infinite recursion
  2. Remove or replace commented-out console statements
  3. Ensure all active error/warning logging uses `Logger` instead of `console`
  4. Document any intentional `console` usage (e.g., in logging sinks to prevent recursion)

  **Technical Notes:**
  - Logging sinks (`file-sink.ts`, `remote-sink.ts`, `supabase-sink.ts`) may intentionally use `console.warn` to avoid infinite recursion when Logger itself fails
  - Check comments in these files - they may already explain why console is used
  - Production Checklist requires: "Standardize error responses in Backend (Hono middleware)" - this is about API error responses, not logging

  **Acceptance Criteria:**
  - [ ] Review logging sink files - verify if console usage is intentional
  - [ ] Remove commented-out console statements (or document why they're kept)
  - [ ] Replace any active console.error/warn with Logger (except in logging sinks if intentional)
  - [ ] Document any remaining console usage with explanation
  - [ ] Verify no console statements in production code paths (except logging infrastructure)

- **Priority:** P1 (High - Code quality, but not blocking)
- **Assigned To:** @ClaudeCode
- **Related Tasks:** 
  - Production Checklist: Error Handling standardization
- **Estimated Effort:** 1-2 hours
- **Dependencies:** 
  - Logger infrastructure (✅ exists)
  - Understanding of logging sink architecture


