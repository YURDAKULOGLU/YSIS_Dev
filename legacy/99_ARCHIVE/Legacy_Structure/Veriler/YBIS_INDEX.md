# YBIS AI Sistemi Komut İndeksi

Bu doküman, belirli bir hedefe ulaşmak için hangi komutun veya iş akışının kullanılacağını gösteren bir rehberdir. Bir görevin nasıl yapılacağından emin olmadığında, doğru aracı bulmak için bu indeksi kullan.

---

## Görev: Yeni Bir Özellik Geliştirme

### Senaryo 1: Hızlı ve Doğrusal Geliştirme (İyi tanımlanmış, küçük özellikler için)

Bu iş akışı, fikirden göreve hızlıca geçmek için tasarlanmıştır.

1.  **Spesifikasyon Oluştur:** `/spec:specify "Özellik açıklaması"`
2.  **Teknik Plan Yap:** `/spec:plan`
3.  **Görevleri Listele:** `/spec:tasks`
4.  **Uygulamayı Yap:** `@dev *develop-story <story_dosyası>`

### Senaryo 2: Kapsamlı ve Ajan-Bazlı Geliştirme (Büyük, karmaşık özellikler için)

Bu iş akışı, BMad metodolojisini kullanarak, farklı uzmanlıklara sahip AI ajanları ile derinlemesine bir geliştirme süreci sunar.

1.  **Gereksinimleri Oluştur (PM):** `@bmad:pm *create-prd`
2.  **Mimariyi Tasarla (Architect):** `@bmad:architect *create-architecture`
3.  **Hikayeleri Oluştur (SM):** `@bmad:sm *draft`
4.  **Hikayeyi Uygula (Dev):** `@bmad:dev *develop-story <story_dosyası>`

---

## Görev: Mevcut Kodu İyileştirme veya Yeniden Düzenleme (Refactoring)

*   **Komut:** `/refactor <dosya_veya_klasör_yolu>`
*   **Açıklama:** Belirtilen dosya veya klasördeki kodu analiz eder ve iyileştirme önerileri sunar.

---

## Görev: Proje Hakkında Genel Bilgi Alma

*   **Komut:** `@ybis-orchestrator *status`
*   **Açıklama:** Projenin mevcut durumu, aktif ajanlar ve ilerleme hakkında bilgi verir.

---

## Görev: Kendi Komutunu Ekleme

*Bu bölüm, kendi özel komutlarınızı ekledikçe genişletilecektir.*

1.  **Özel Komut 1:** `/ybis:sindir <parametreler>`
    *   **Açıklama:** [Sizin tarafınızdan eklenecek açıklama]
