# Bölüm 4: Test Stratejisi

**Sürüm:** 2.0.0
**Durum:** Aktif
**Framework:** Vitest

---

## 1. Genel Bakış

Bu doküman, YBIS projesindeki yazılım kalitesini garanti altına almak, hataları erken aşamada yakalamak ve kodun sürdürülebilirliğini sağlamak için izlenen test stratejisini tanımlar. Stratejimiz, test piramidi modeline dayanır.

---

## 2. Test Piramidi

Testlerimizin çoğunluğu hızlı ve ucuz olan birim testlerinden oluşur, bunu entegrasyon testleri takip eder ve en tepede az sayıda E2E testi bulunur.

        /\
       /  \
      / E2E\
     /------\
    /  Entegrasyon  \
   /--------------\
  /    Birim Testi   \
 /------------------\

1.  **Birim Testleri (Unit Tests) (%70):** Tek bir fonksiyonun, component'in veya modülün mantığını, dış bağımlılıkları mock'layarak test eder.
2.  **Entegrasyon Testleri (Integration Tests) (%20):** Birden fazla modülün veya bir modülün harici bir servis (veritabanı, API) ile birlikte doğru çalışıp çalışmadığını test eder.
3.  **Uçtan Uca Testler (E2E Tests) (%10):** Kullanıcının bir senaryoyu baştan sona (UI'dan veritabanına) tamamlayabildiğini test eder.

---

## 3. Test Araçları

- **Test Çatısı (Framework):** `vitest`
- **Mock'lama (Mocking):** `vitest`'in dahili `vi.mock` ve `vi.fn` yetenekleri.
- **Doğrulama (Assertions):** `vitest`'in `expect` API'si.
- **Test Kapsamı (Coverage):** `v8` (vitest ile dahili).

---

## 4. Test Türleri ve Uygulamaları

### 4.1. Birim Testleri

- **Konum:** Test edilen koda en yakın `__tests__` klasörü içinde (`*.test.ts`).
- **Amaç:** Adapter mantığını, veri dönüşümlerini ve hata yönetimini harici servisler olmadan test etmek.
- **Kural:** Birim testleri asla gerçek bir API'ye veya veritabanına istek yapmamalıdır.

### 4.2. Entegrasyon Testleri

- **Konum:** `__tests__/integration/` klasörü içinde (`*.integration.test.ts`).
- **Amaç:** Adapter'ların Gerçek harici servislerle (Test Veritabanı, Test API Anahtarları) doğru iletişim kurduğunu doğrulamak.
- **Kural:** Entegrasyon testleri, CI/CD pipeline'ında varsayılan olarak çalıştırılmaz. Sadece `main` branch'ine merge edilirken veya manuel olarak tetiklendiğinde çalışır. Testler, arkalarında veri bırakmamalıdır (cleanup).

### 4.3. Uçtan Uca (E2E) Testler

- **Konum:** `apps/backend/src/__tests__/e2e/` veya `e2e/` (Detox için).
- **Amaç:** Kritik kullanıcı akışlarını (örn: giriş yapma, görev oluşturma) simüle etmek.
- **Durum:** Phase 1 ve sonrası için planlanmıştır. Phase 0 (Mevcut Faz) için manuel testler yeterlidir.

---

## 5. Test Kapsamı (Coverage) Hedefleri

- **Genel Proje:** `%80`
- **Kritik İş Mantığı (Domain Logic):** `%90`
- **Port Adapter'ları:** `%85`

**Kural:** CI/CD pipeline'ı, bu hedeflerin altına düşen Pull Request'leri otomatik olarak engelleyecektir.
**Uygulama Fazı:** **Açık Beta / MVP.** Kapalı Beta süresince bu hedefler bir rehber olarak kullanılır, ancak PR'ları otomatik olarak engellemez.
