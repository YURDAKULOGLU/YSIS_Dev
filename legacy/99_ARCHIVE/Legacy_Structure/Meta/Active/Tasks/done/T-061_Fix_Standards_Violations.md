# T-061: Fix YBIS Standards Violations

**Agent:** @Composer (Cursor IDE Agent)  
**Priority:** P0 (Critical - Blocks PR)  
**Status:** ✅ Completed  
**Created:** 2025-01-XX  
**Completed:** 2025-12-04

---

## Problem

YBIS_STANDARDS kontrolünde 14 ihlal tespit edildi. Bunların 3'ü kritik (PR engelleme sebebi):

1. **UI İzolasyonu İhlali:** `apps/mobile/app/_layout.tsx` - tamagui.config doğrudan import
2. **Vendor SDK İhlali (Backend):** `apps/backend/src/middleware/auth.ts` - @supabase/supabase-js doğrudan import
3. **Vendor SDK İhlali (Mobile):** `apps/mobile/src/contexts/useAuth.ts` - expo-auth-session doğrudan import

## Requirements

### P0 (Critical - Must Fix Now)
- [x] Backend auth middleware: @supabase/supabase-js → @ybis/auth utility kullan ✅
- [x] Mobile useAuth: expo-auth-session → @ybis/auth adapter kullan ✅
- [x] Mobile _layout: tamagui.config → @ybis/ui veya @ybis/theme kullan ✅

### P1 (Phase 2 - High Priority)
- [x] Backend TypeScript strict mod aktif et ✅

### P2 (Improvement)
- [ ] Tüm packages için README.md ekle (10 paket) → T-076'ya taşındı

## Acceptance Criteria

- [x] Tüm kritik ihlaller düzeltildi ✅
- [x] Kod standartlara uygun ✅
- [x] Linter hataları yok ✅
- [x] Testler geçiyor ✅
- [x] Implementation report oluşturuldu ✅

## Completion Summary

**Completed by:** @Composer (Cursor IDE Agent)  
**Date:** 2025-12-04  
**Report:** `.YBIS_Dev/ysis_agentic/agents/coding/T-061_Standards_Violations_Fix_Report.md`

### Fixed Issues:
1. ✅ Backend auth middleware - Port Architecture compliance
2. ✅ Mobile useAuth - Port Architecture compliance  
3. ✅ Mobile _layout - UI Isolation compliance
4. ✅ Backend TypeScript strict mode enabled

**Files Changed:** 11 files  
**New Files Created:** 3 utility files  
**Linter Errors:** 0

## Technical Notes

- Port mimarisi prensibine uygun olmalı
- Vendor SDK kullanımı sadece packages seviyesinde olmalı
- UI izolasyonu: apps/* içinde sadece @ybis/ui kullanılmalı

