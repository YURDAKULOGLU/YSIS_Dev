---
type: bug
priority: high
status: done
assignee: @Coding
completed_at: 2025-12-04
---

# Fix Auth Persistence (Session Restoration)

**Description:**
The application does not remember the user's session. Every time the app is opened, it behaves as a fresh install/login, requiring re-authentication or showing "Welcome back" toast inappropriately.

**Symptoms:**
- App opens to Login screen (or behaves like fresh session) on every launch.
- "Welcome back" toast might appear but session state is flaky.

**Root Cause Hypothesis:**
- `SupabaseAuthAdapter` initialization might not be reading from `AsyncStorage` correctly.
- `useAuth` hook might be defaulting to `loading: true` and not checking persisted session fast enough.
- `SecureStore` (if used) might be failing on some devices/simulators.

**Acceptance Criteria:**
- [ ] User remains logged in after closing and reopening the app.
- [ ] App bypasses Login screen if session is valid.
- [ ] Session token is correctly refreshed if expired.
