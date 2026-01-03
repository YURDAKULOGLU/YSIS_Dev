# Session End Command

**Purpose:** Bir geliştirme oturumunu, başarıları özetleyerek, proje sağlığını doğrulayarak ve bir sonraki oturuma hazırlanarak düzgün bir şekilde sonlandırmak.
**Category:** Raporlama ve Bakım
**Agent:** Tümü

## Bu Komut Ne Yapar

Projenin temiz, kararlı ve iyi belgelenmiş bir durumda bırakıldığından emin olmak için bir dizi kontrol ve özetleme işlemi gerçekleştirir.

## Adımlar

1.  **Oturum Başarılarını Özetle:**
    *   [ ] Üzerinde çalışılan birincil story'leri veya görevleri listele (örneğin, "CB-1.3: DatabasePort Uygulaması").
    *   [ ] Ana sonuçları ve story hedeflerine ulaşılıp ulaşılmadığını kısaca açıkla.

2.  **Git Durumunu Doğrula:**
    *   [ ] Commit edilmemiş değişiklikleri veya izlenmeyen dosyaları kontrol etmek için `run_shell_command("git status")` çalıştır.
    *   [ ] Commit edilmemiş değişiklikler varsa, kullanıcıya bunların commit edilip edilmemesi gerektiğini sor.
    *   [ ] Bir commit istenirse, değişiklikleri gözden geçirmek ve bir commit mesajı önermek için `run_shell_command("git diff --staged")` çalıştır.

3.  **Son Kalite Kontrollerini Çalıştır:**
    *   [ ] Linting hatalarını kontrol etmek için `run_shell_command("pnpm -r run lint")` çalıştır.
    *   [ ] TypeScript hatalarını kontrol etmek için `run_shell_command("pnpm -r run type-check")` çalıştır.
    *   [ ] Tüm testlerin geçtiğinden emin olmak için `run_shell_command("pnpm -r run test")` çalıştır.
    *   **KRİTİK:** Bu kontrollerden herhangi biri başarısız olursa, oturum "temiz" bir şekilde sonlandırılmadan önce düzeltilmelidir.

4.  **Takip Eylemlerini ve Engelleyicileri Belirle:**
    *   [ ] Oluşan yeni teknik borçları not al.
    *   [ ] Listele herhangi bir açık soruyu veya bir sonraki oturumda ele alınması gereken kararları.
    *   [ ] Önerilen "Sonraki Story" veya görevi belirle.

5.  **Oturum Özeti Oluştur:**
    *   [ ] Oturumun kısa bir özetini Markdown formatında oluştur. Şunları içermelidir:
        *   **Tarih:** Bugünün tarihi.
        *   **Tamamlanan Görevler:** Tamamlanan story/uygulama dosyasına bağlantı.
        *   **Anahtar Kararlar:** Yeni AD-XXX numaralarını veya önemli mimari seçimleri listele.
        *   **Son Proje Durumu:** "Tüm kontroller geçiyor" veya "Şu tarafından engellendi...".
    *   [ ] Bu özeti, `docs/sessions/SESSION_LOG.md` gibi merkezi bir log dosyasına eklemeyi öner.

6.  **Hazır Durum:**
    *   [ ] Tüm kontrollerin tamamlandığını ve özetin oluşturulduğunu onayla.
    *   [ ] Son durumu kullanıcıya raporla.
    *   [ ] Oturumu sonlandır.

## Başarı Kriterleri

-   ✅ Oturum başarıları özetlendi.
-   ✅ Git durumu temiz (veya değişiklikler kasıtlı olarak kullanıcıya bırakıldı).
-   ✅ Tüm kalite kontrolleri (lint, type-check, test) geçiyor.
-   ✅ Bir oturum özeti oluşturuldu.
-   ✅ Proje, bir sonraki geliştirici/ajan için kararlı bir durumda.
