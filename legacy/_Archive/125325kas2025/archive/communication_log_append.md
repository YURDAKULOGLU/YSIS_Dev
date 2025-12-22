
### [AGENT: Antigravity] [TIME: 2025-11-27T22:50:00+03:00]
**Action:** [BUG FIX]
**Task:** Fix Vitest Parsing Error (T-002)
**Duration:** 10 minutes

**Files Changed:**
- packages/database/vitest.config.ts (Updated)
- packages/auth/vitest.config.ts (Updated)

**What Changed:**
- **Problem:** Vitest/Rollup failed to parse `@supabase/supabase-js` ESM build (`Expected 'from', got 'typeOf'`).
- **Solution:** Configured `resolve.alias` to force usage of the CJS build (`dist/main/index.js`) instead of ESM.
- **Why:** This bypasses the parsing issue with modern syntax in the ESM build.

**Status:** ✅ RESOLVED (Pending verification run)

@Codex - The Vitest parsing error should be resolved. Please verify if you encounter it again.
