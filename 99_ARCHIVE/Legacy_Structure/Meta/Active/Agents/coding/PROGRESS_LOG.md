## Work Summary (current session)

- **FlowEngine platform refactor**: Made `packages/core/src/services/FlowEngine.ts` platform-agnostic (uses `crypto.randomUUID` with expo-crypto fallback). This enables running the same engine on server-side (Supabase Edge/Hono) as well as client.
- **Flow seeds**: In `apps/mobile/src/features/flows/hooks/useFlows.ts`, if a user has no flows and workspace is ready, seed default templates (Morning Routine, Daily Summary, etc.) once. Guarded with `hasSeededRef` to avoid duplicates.
- **Flow notifications**: `send_notification` step now schedules a local notification via `expo-notifications` (with permission check, optional `trigger_seconds` delay) and falls back to toast if permissions denied. Works when app is backgrounded.
- **Calendar UX fix**: `apps/mobile/app/(tabs)/calendar.tsx` now wraps day strip and event cards in `Pressable` to restore tap/press interactions for date selection and event editing.
- **Tests**: Mobile Jest suite (`pnpm --filter @ybis/mobile test:jest`) passing after changes.
- **Server-side flow runner (Hono)**: Added `/api/flows` route in backend; runs flows server-side using port-injected DB/LLM, with manual run and scheduled run endpoints. Backend tests still pass.
- **Edge Function flow runner (Supabase)**: New function `supabase/functions/flow-runner/index.ts` to run flows server-side via Supabase cron or manual (service key). Basic handlers (queryContext, create_note/task/event, output_note/task/notification) and execution logging to `flow_executions/steps`. AI processing and push delivery are not yet wired.
- **Push tokens schema aligned**: `supabase/migrations/017_create_push_tokens.sql` updated to match expected columns (user_id, device_id, token, platform, is_active) with RLS policies.
- **Mobile push token save**: `apps/mobile/src/hooks/useNotifications.ts` now saves Expo push token to `push_tokens` (via Supabase adapter) with platform/device_id; ignores duplicate key errors.
- **Edge runner push**: `supabase/functions/flow-runner/index.ts` now fetches `push_tokens` and sends Expo push on flow completion (simple message).

## Pending / Next
- Wire Expo push delivery + token table for server-initiated notifications.
- Onboarding flow design (deferred).
- Consider full alignment of Edge Function runner with FlowEngine features (AI processing, multi-output).
