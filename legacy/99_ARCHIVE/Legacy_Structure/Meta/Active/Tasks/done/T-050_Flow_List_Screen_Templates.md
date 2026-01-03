# Task ID: T-050

- **Source Document:** Closed Beta Sprint - Nexus Delegation
- **Title:** Flow List Screen - Template'lerden Flow Oluşturma
- **Description:**
  Flow list ekranına template seçim UI'ı ekle. Kullanıcı mevcut 5 template'den birini seçerek hızlıca flow oluşturabilmeli.

  **Mevcut Durum:**
  - ✅ FLOW_TEMPLATES array'i hazır (`useFlows.ts`)
  - ✅ createFlow fonksiyonu çalışıyor
  - ❌ UI'da template seçimi yok
  - ❌ Flow list screen basit "coming soon" gösteriyor

  **Yapılacaklar:**
  1. `apps/mobile/app/(tabs)/flows.tsx` dosyasını güncelle
  2. Template listesi göster (5 adet)
  3. Template'e tıklayınca flow oluştur
  4. Oluşturulan flow'ları listele
  5. Flow'a tıklayınca run/toggle/delete seçenekleri

  **Teknik Notlar:**
  - `useFlows` hook'unu kullan
  - `FLOW_TEMPLATES` export'unu import et
  - i18n key'leri `flows.*` altında mevcut

  **Acceptance Criteria:**
  - [ ] Template listesi görünür
  - [ ] Template seçince flow oluşur
  - [ ] Flow listesi güncellenir
  - [ ] Flow toggle çalışır (aktif/pasif)
  - [ ] Flow silme çalışır

- **Priority:** P1 (Important for Closed Beta)
- **Assigned To:** @Delegate (Çırak)
- **Complexity:** Easy
- **Estimated Effort:** 1-2 hours
- **Dependencies:**
  - useFlows hook (✅ ready)
  - FLOW_TEMPLATES (✅ ready)
