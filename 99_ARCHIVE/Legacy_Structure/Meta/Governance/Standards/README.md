# YBIS Projesi Ana Kontrol Merkezi

**Sürüm:** 1.1.0
**Durum:** Aktif

Bu doküman, YBIS projesinin tüm standartları, süreçleri, komutları ve dokümantasyon yapısı için **TEK** ana giriş noktasıdır (Single Source of Truth).

---

## 1. Operasyon Standartları El Kitabı (İçindekiler)

Projenin "nasıl yapıldığını" anlatan modüler rehberler.

- **[1. Anayasa](./1_Anayasa/README.md):** Projenin temel, değişmez kuralları. **(Her oturumda okunmalı)**
- **[2. Kalite ve Standartlar](./2_Kalite_Ve_Standartlar/README.md):** Kodlama stili, linting, TypeScript kuralları.
- **[3. Geliştirme Süreci](./3_Gelistirme_Sureci/):** Git akışı, branch ve PR süreçleri.
- **[4. Test Stratejisi](./4_Test_Stratejisi/README.md):** Test felsefesi, türleri ve araçları.
- **[5. Teknoloji Yığını (Tech Stack)](./tech-stack.md):** Projede kullanılan teknolojiler, kütüphaneler ve versiyonlar.

---

## 2. Ajan Farkındalık Haritası (Agent Awareness Map)

Ajanların, görev bazlı olarak hangi dokümanları okuması gerektiğini belirten "lazy-loading" haritası.

| Senaryo/Görev Tipi | Anahtar Kelimeler (Keywords) | Okunacak Dokümanlar (Lazy-Load) |
| --- | --- | --- |
| Yeni UI Component Geliştirme | `component`, `UI`, `view`, `stil`, `tasarım` | `./2_Kalite_Ve_Standartlar/README.md` |
| Git Branch/PR İşlemleri | `branch`, `commit`, `PR`, `merge`, `rebase` | `./3_Gelistirme_Sureci/BRANCH_STRATEGY.md`, `./3_Gelistirme_Sureci/PULL_REQUEST_SURECI.md` |
| Test Yazma veya Düzeltme | `test`, `jest`, `vitest`, `coverage` | `./4_Test_Stratejisi/README.md` |
| Yeni Bir Özellik Ekleme | `yeni özellik`, `planlama`, `epic`, `story` | `./3_Gelistirme_Sureci/README.md` |
| Kod Kalitesini İnceleme | `refactor`, `kod kalitesi`, `lint`, `gözden geçir` | `./2_Kalite_Ve_Standartlar/README.md` |

---

## 3. Ana Komut İndeksi (Master Command Index)

Sık kullanılan ve bilinmesi gereken ana komutlar.

- `/help`: Yardım menüsünü gösterir.
- `/reset`: Mevcut oturumu ve hafızayı sıfırlar.
- `/commit`: Değişiklikleri Git'e commit etme sürecini başlatır.
- `/kusbakisi-analiz`: Projedeki süreçler ve yapılar hakkında kuşbakışı bir analiz yapar.
- `/meta`: Mevcut konuşma üzerinde meta-seviye bir analiz yürüterek süreç, davranış ve yönetişim desenlerini tanımlar ve bu desenlere dayanarak Anayasa değişiklikleri önerir.
- **Not:** Otomatik başlangıç pipeline'ı nedeniyle eski `/session start` komutu kullanımdan kaldırılmıştır.

---

## 4. Genel Dokümantasyon Haritası (Overall Documentation Map)

Projenin diğer önemli dokümantasyon alanlarına hızlı linkler:

- **[Hızlı Başlangıç (Quickstart)](../QUICKSTART.md):** Yeni geliştiriciler için kurulum ve başlangıç rehberi.
- **[Geliştirme Logu (Dev Log)](../Güncel/DEVELOPMENT_LOG.md):** Önemli kararların ve değişikliklerin kaydedildiği proje günlüğü.
- **[AI Agent Görev Dağılımı](../AI_Asistan_Gorev_Dagilimi.md):** Farklı AI ajanlarının görev dağılımları ve iş akışları.
- **[Strateji Dokümanları](../strategy/):** Pazar araştırması, rekabet analizi.
- **[Vizyon ve Ürün](../vision/):** Projenin uzun vadeli vizyonu ve ürün yol haritası.
- **[Raporlar](../reports/):** Geçmiş analizler, denetimler ve toplantı özetleri.
- **[Mimari Kararları](../design/):** Üst seviye mimari tasarım dokümanları.
- **[Arşiv](../Archive/):** Artık aktif olmayan tüm dokümanlar.

---

## 5. Doküman Bağımlılık Haritası (Document Dependency Map)

Bu harita, bir doküman güncellendiğinde hangi diğer dokümanların etkilenebileceğini gösterir. Bir dokümanı değiştirmeden önce, bu haritayı kontrol ederek sistemin homojen kalmasını sağlayın.

- **`1_Anayasa/README.md` (Ana Anayasa)**
    - **Bağımlı Olanlar (Dependents):** TÜM DİĞER DOKÜMANLAR. Anayasadaki bir değişiklik, projenin tüm standartlarını etkileyebilir.

- **`2_Kalite_Ve_Standartlar/README.md` (Kalite Standartları)**
    - **Bağımlı Olanlar:** `3_Gelistirme_Sureci/PULL_REQUEST_SURECI.md`, `4_Test_Stratejisi/README.md`.

- **`tech-stack.md` (Teknoloji Yığını)**
    - **Bağımlı Olanlar:** `2_Kalite_Ve_Standartlar/README.md`, `4_Test_Stratejisi/README.md`.
