---
type: bug
priority: high
status: backlog
assignee: @Coding
---

# Fix Settings Logout Button & Text

**Description:**
The logout button in Settings screen has incorrect text ("Exit Demo Mode") and is non-functional (does not log out, does not redirect to login).

**Symptoms:**
- Button text says "Exit Demo Mode" instead of "Logout" (or translated equivalent).
- Clicking the button does nothing.
- User remains authenticated on app restart.

**Root Cause Hypothesis:**
- `DrawerFooter.tsx` has hardcoded text.
- `onLogout` prop might not be connected to `useAuth().signOut` correctly.
- Navigation reset logic might be missing after sign out.

**Acceptance Criteria:**
- [ ] Button text displays correct translation (e.g., "Çıkış Yap").
- [ ] Clicking button logs user out of Supabase.
- [ ] App redirects to Login screen immediately.
- [ ] Navigation stack is reset (cannot go back to Settings).
