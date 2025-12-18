# T-008 - Supabase BaaS validation & RLS check (Closed Beta posture)

## What changed
- Added validation/rate-limit Edge Functions for BaaS-only flow (no Hono gateway required):
  - `supabase/functions/chat-guard/index.ts` – validates `create_conversation`/`create_message` payloads with Zod, rate limits 60 req/min/IP, CORS enabled.
  - `supabase/functions/auth-guard/index.ts` – validates login payload (email/password or access token), rate limits 30 req/min/IP, CORS enabled.
  - Shared limiter in `supabase/functions/_shared/rateLimit.ts` (per-instance memory, protects against bursts).
- RLS sanity check (from `migrations/013`): notes/tasks/conversations/messages all enforce `workspace_id` or `user_id` with `WITH CHECK` using `(select auth.uid())` to avoid per-row re-eval. Policies already present and scoped to owner/workspace.

## How to use
1) Deploy functions (Supabase CLI):
   - `supabase functions deploy chat-guard`
   - `supabase functions deploy auth-guard`
2) Call them instead of raw table REST when you want server-side validation pre-RLS. Payloads:
   - Chat: `{ "action": "create_conversation", "payload": { "title": "...", "workspaceId": "<uuid|null>" } }` or `{ "action": "create_message", "payload": { "conversationId": "<uuid>", "content": "..." } }`
   - Auth: `{ "action": "login", "payload": { email, password } }` or `{ "action": "login", "payload": { accessToken, refreshToken? } }`
3) Clients can still post directly to Supabase REST; these functions are a thin validation/rate-limit layer for beta without running the Node backend.

## RLS quick snapshot (critical tables)
- `notes`: `USING workspace_id IN (SELECT id FROM workspaces WHERE owner_id = auth.uid())` and `WITH CHECK` + `user_id = auth.uid()`.
- `tasks`: same shape as notes (workspace + user check).
- `conversations`: `USING/WITH CHECK user_id = auth.uid()`.
- `messages`: `USING/WITH CHECK user_id = auth.uid()`.
-> Ensure clients always write `workspace_id`/`user_id` from JWT; RLS will reject mismatches.

## Recommended next steps
- Wire mobile/web clients to call `chat-guard` and `auth-guard` (keep REST fallback during beta).
- Add Edge Function logging (POST to `logs` table) if you want observability on validation failures.
- If traffic grows, swap the in-memory limiter with KV/Redis (Supabase supports Deno KV).
