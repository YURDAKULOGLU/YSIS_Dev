# Task ID: T-054

- **Source Document:** Closed Beta Sprint - Nexus Delegation
- **Title:** Vitest Config Parsing Error Fix
- **Description:**
  Vitest configuration'da parsing hatası var. Test infrastructure düzeltilmeli.

  **Mevcut Hata:**
  - Vitest config parse edilemiyor
  - Test runner çalışmıyor
  - CI blocked

  **Olası Nedenler:**
  - ESM/CJS module conflict
  - TypeScript config issue
  - Monorepo workspace resolution

  **Yapılacaklar:**
  1. `vitest.config.ts` veya `vite.config.ts` kontrol et
  2. Error log'larını analiz et
  3. Module resolution fix
  4. Test run verify

  **Teknik Notlar:**
  - pnpm workspace kullanılıyor
  - Node 20 LTS
  - TypeScript strict mode

  **Acceptance Criteria:**
  - [ ] `pnpm test` hatasız çalışıyor
  - [ ] Mevcut testler pass ediyor
  - [ ] CI pipeline green

- **Priority:** P3 (Technical Debt)
- **Assigned To:** @Delegate (Çırak)
- **Complexity:** Medium (Investigation required)
- **Estimated Effort:** 1-2 hours
- **Dependencies:** None
