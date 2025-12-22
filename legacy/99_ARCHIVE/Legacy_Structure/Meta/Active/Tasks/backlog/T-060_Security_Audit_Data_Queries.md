# T-060: Security Audit - Data Queries

**Priority:** P0 (Critical)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 4.2

---

## Description

Audit all database queries to ensure proper user_id filtering. Some queries may bypass RLS by not including proper filters.

## Tasks

- [ ] Audit all `db.select()` calls in the codebase
- [ ] Ensure every query has `user_id` filter where needed
- [ ] Verify workspace_id filtering is correct
- [ ] Check for any direct Supabase usage bypassing DatabasePort
- [ ] Document any RLS gaps found

## Files to Check

- `apps/mobile/src/features/*/hooks/*.ts`
- `apps/mobile/src/services/data/toolServiceFunctions.ts`
- Any file using `getDatabasePort()`

## Acceptance Criteria

- All queries properly filter by user_id
- No data leakage possible between users
- Report generated with findings

