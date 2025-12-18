# Task ID: T-057

- **Source Document:** Test Infra Gap
- **Title:** React Native UI Testleri için Jest Kurulumu
- **Description:**
  Vitest, React Native/Testing Library paketlerini parse edemiyor (Flow tipi `typeof import` hatalar). Auth ekranlar ve RN UI testleri i‡in Jest tabanl runner kur.

  **Yaplacaklar:**
  1. `apps/mobile/jest.config.js` i‡in jest-expo preset ve transformIgnorePatterns ayarla
  2. Jest setup dosyas (jest.setup.js) ve gerekli Expo/Router mock'lar ekle
  3. `@testing-library/jest-native` entegrasyonu
  4. Auth login/signup testlerini Jest ile ‡alŸacak ‡evir
  5. `pnpm test:jest` script'ini CI'ya ekle ve localde koŸ

  **Acceptance Criteria:**
  - [ ] Jest runner RN UI testlerini ‡alŸtryor (auth login/signup)
  - [ ] `pnpm test:jest` localde geiyor
  - [ ] Vitest pipeline etkilenmiyor (mantk testleri ayn)

- **Priority:** P2 (Test Infrastructure)
- **Assigned To:** @Delegate (Çırak)
- **Complexity:** Medium
- **Estimated Effort:** 2 hours
- **Dependencies:** jest-expo, @testing-library/react-native, babel-jest
