# Task ID: T-052

- **Source Document:** Closed Beta Sprint - Nexus Delegation
- **Title:** Flow Tools için Unit Test Yaz
- **Description:**
  Yeni eklenen flow AI tools için unit testler yaz.

  **Test Edilecek Fonksiyonlar:**
  - `createFlow()` - toolServiceFunctions.ts
  - `editFlow()` - toolServiceFunctions.ts
  - `toggleFlow()` - toolServiceFunctions.ts
  - `searchFlows()` - toolServiceFunctions.ts
  - `deleteFlow()` - toolServiceFunctions.ts
  - `runFlow()` - toolServiceFunctions.ts
  - `queryContext()` - toolServiceFunctions.ts

  **Yapılacaklar:**
  1. Test dosyası oluştur: `apps/mobile/src/services/data/__tests__/flowTools.test.ts`
  2. Mock database setup
  3. Her fonksiyon için:
     - Happy path test
     - Error case test (user not authenticated, etc.)
     - Edge case tests

  **Teknik Notlar:**
  - Jest kullan
  - Database mock için `@ybis/database` mock'la
  - Logger mock'la

  **Acceptance Criteria:**
  - [ ] Tüm flow fonksiyonları test edilmiş
  - [ ] Coverage > 80%
  - [ ] Testler pass ediyor
  - [ ] CI'da çalışıyor

- **Priority:** P2 (Quality)
- **Assigned To:** @Delegate (Çırak)
- **Complexity:** Easy-Medium
- **Estimated Effort:** 2-3 hours
- **Dependencies:**
  - Jest config (✅ ready)
  - Flow functions (✅ ready)
