# /ybis:end_session

**Amaç:** Aktif geliştirme oturumunu standart bir protokolle sonlandırmak, öğrenimleri kaydetmek ve bir sonraki oturum için temiz bir başlangıç noktası oluşturmak.

**İş Akışı:**

1.  **Oturum Analizi:** AI, mevcut oturumda tamamlanan görevleri, alınan önemli kararları (`AD-XXX` dahil) ve karşılaşılan engelleri özetler.
2.  **`DEVELOPMENT_LOG.md` Güncellemesi:**
    *   AI, oturum özetini `DEVELOPMENT_LOG.md` dosyasına tarih damgasıyla birlikte detaylı bir girdi olarak ekler.
    *   Bu girdi, kalıcı ve değişmez bir kayıt oluşturur.
3.  **`session-context.md` Güncellemesi:**
    *   AI, bir *sonraki* oturumun başlangıç bağlamını hazırlamak için `session-context.md` dosyasını günceller.
    *   **İçerik:**
        *   `Active Focus`: Bir sonraki oturumun ana odağı ne olacak?
        *   `Next Steps (Top 3)`: En önemli 3 aksiyon maddesi.
        *   `Blockers`: Mevcut engeller devam ediyor mu?
    *   Bu dosya, her zaman kısa ve özet halinde kalır (<100 satır).
4.  **Doküman Tutarlılık Kontrolü (En Önemli Adım):**
    *   AI, kullanıcıya şu soruyu sorar: **"Bu oturumda projenin ana mimarisini, teknoloji yığınını (`tech-stack.md`) veya temel prensiplerini (`ANAYASA`) etkileyen bir değişiklik yaptık mı?"**
    *   Eğer cevap "Evet" ise, AI kullanıcıyı bu değişiklikleri kalıcı hale getirmek için `/ybis:log-decision` komutunu çalıştırmaya yönlendirir. Bu, "Canlı Dokümanların" her zaman güncel kalmasını sağlar.

**Kullanım:**
- Geliştirme oturumunun sonunda, tüm önemli işler tamamlandığında çalıştırılır.

**Faydası:**
- "Dual Write" gibi manuel ve hataya açık bir süreci ortadan kaldırır.
- Oturum sonlandırmayı standart bir protokole bağlar.
- Dokümantasyonun güncel kalmasını aktif olarak teşvik eder.
