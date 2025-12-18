# T-068: Complete Google OAuth Implementation

**Priority:** P1 (Important)
**Effort:** 1 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 4.1

---

## Description

Complete Google OAuth sign-in flow that is currently incomplete.

## Current State

- Google OAuth button exists
- `useAuth.ts` has partial implementation
- Deep link callback not working
- `startAsync` API deprecated

## Tasks

- [ ] Update to new expo-auth-session API
- [ ] Configure Google Cloud OAuth credentials
- [ ] Set up proper redirect URIs
- [ ] Handle OAuth callback
- [ ] Exchange code for Supabase session
- [ ] Test on iOS and Android

## Implementation

```typescript
// New approach using WebBrowser
import * as WebBrowser from 'expo-web-browser';
import { makeRedirectUri } from 'expo-auth-session';

WebBrowser.maybeCompleteAuthSession();

const redirectUri = makeRedirectUri({
  scheme: 'ybis',
  path: 'auth/callback',
});

// Start OAuth flow
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: redirectUri,
  },
});
```

## Configuration

1. Google Cloud Console:
   - Add authorized redirect URIs
   - Enable OAuth consent screen

2. Supabase Dashboard:
   - Configure Google provider
   - Add redirect URLs

3. app.json:
   - Add scheme for deep linking

## Acceptance Criteria

- User can sign in with Google
- Works on both iOS and Android
- Proper error handling
- Session persists correctly

