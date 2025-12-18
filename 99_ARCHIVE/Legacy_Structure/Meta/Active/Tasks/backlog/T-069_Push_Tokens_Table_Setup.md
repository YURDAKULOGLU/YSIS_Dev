# T-069: Push Tokens Table & Implementation

**Priority:** P3 (Deferred)
**Status:** Deferred
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** Runtime Error - "push_tokens table not found"

---

## Description

Create push_tokens table in Supabase and restore push token saving logic.

## Tasks

### Database

- [ ] Run SQL to create push_tokens table
- [ ] Verify RLS policies work

```sql
CREATE TABLE IF NOT EXISTS public.push_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    device_id TEXT NOT NULL,
    token TEXT NOT NULL,
    platform TEXT NOT NULL CHECK (platform IN ('ios', 'android', 'web')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, device_id)
);

ALTER TABLE public.push_tokens ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own push tokens"
    ON public.push_tokens FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own push tokens"
    ON public.push_tokens FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own push tokens"
    ON public.push_tokens FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own push tokens"
    ON public.push_tokens FOR DELETE USING (auth.uid() = user_id);

CREATE INDEX idx_push_tokens_user_id ON public.push_tokens(user_id);
```

### Code

- [ ] Restore push token saving in useAuth.ts
- [ ] Handle table operations correctly
- [ ] Test token saving on login

## Acceptance Criteria

- No "table not found" errors
- Push tokens saved to database
- Tokens can be used for push notifications

