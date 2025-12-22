# Task ID: T-015

- **Title:** Add basic email/password auth UI and wire to Supabase (mobile)
- **Priority:** P0
- **Assigned To:** @Cursor (UI) + @ClaudeCode (hook integration)
- **Description:** Provide minimal login/signup screens in mobile that call `useAuth` (SupabaseAuthAdapter) so users can create/sign in with email/password. Include loading/error states; no advanced flows needed.

## Acceptance
- Login and signup screens exist and are accessible from the app start.
- `signUpWithEmail` / `signInWithEmail` from `useAuth` are invoked; success results in a stored session and user visible in app state.
- Clear error display and retry.
- Works with existing `SupabaseAdapter` auth token sync (RLS compatible).
