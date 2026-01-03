# Task ID: T-053

- **Source Document:** Closed Beta Sprint - Nexus Delegation
- **Title:** Schedule Executor için Test Yaz
- **Description:**
  useScheduleExecutor hook'u ve cron parser için unit testler yaz.

  **Test Edilecekler:**
  - `parseCronSchedule()` - cron string parsing
  - `shouldRunToday()` - day matching logic
  - `getScheduledTimeToday()` - time calculation
  - `shouldFlowRun()` - full check logic
  - `getNextRunTime()` - next run calculation

  **Yapılacaklar:**
  1. Test dosyası: `apps/mobile/src/features/flows/hooks/__tests__/useScheduleExecutor.test.ts`
  2. Cron parser testleri (various formats)
  3. Day matching testleri (weekday, monthly)
  4. Time comparison testleri
  5. AsyncStorage mock for last run tracking

  **Test Cases:**
  ```
  - "0 9 * * *" → 09:00 daily
  - "0 9 * * 1" → 09:00 Monday only
  - "0 18 15 * *" → 18:00 on 15th of month
  - Invalid cron → null
  ```

  **Acceptance Criteria:**
  - [ ] Cron parser tüm formatları handle ediyor
  - [ ] Day matching doğru çalışıyor
  - [ ] Time comparison edge cases covered
  - [ ] Testler pass ediyor

- **Priority:** P2 (Quality)
- **Assigned To:** @Delegate (Çırak)
- **Complexity:** Easy
- **Estimated Effort:** 1-2 hours
- **Dependencies:**
  - useScheduleExecutor (✅ ready)
