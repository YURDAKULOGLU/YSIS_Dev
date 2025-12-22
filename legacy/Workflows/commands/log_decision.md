# /ybis:log-decision

**Amaç:** Projenin mimarisini, teknoloji yığınını veya temel prensiplerini etkileyen önemli bir kararı, ilgili tüm dokümanlara tutarlı bir şekilde kaydetmek.

**İş Akışı:**

1.  **Karar Bilgilerini Toplama:**
    *   AI, kullanıcıdan alınacak kararın detaylarını ister:
        *   **Karar Başlığı:** Kısa ve açıklayıcı bir başlık.
        *   **Gerekçe (Context):** Bu karar neden alındı? Hangi sorunu çözüyor?
        *   **Karar (Decision):** Alınan net karar nedir?
        *   **Trade-off'lar ve Alternatifler:** Değerlendirilen diğer yollar ve neden seçilmedikleri.
        *   **Etki (Impact):** Bu karar projenin hangi kısımlarını etkileyecek?

2.  **`DEVELOPMENT_LOG.md`'ye Kayıt:**
    *   AI, toplanan bilgileri standart `AD-XXX` formatında `DEVELOPMENT_LOG.md` dosyasına ekler. Bu, kararın "gerçeğin tek kaynağı" olarak kaydedilmesini sağlar.

3.  **"Canlı Doküman" Güncelleme Analizi:**
    *   AI, kararın içeriğini analiz eder ve `documentation-map.yaml` dosyasındaki kurallara göre hangi "Canlı Dokümanların" güncellenmesi gerektiğini belirler.
    *   Kullanıcıya bir güncelleme planı sunar:
        *   "Bu karar, projenin teknoloji yığınını güncellemeyi gerektiriyor. `tech-stack.md` dosyasını düzenliyorum."
        *   "Bu kararın arkasındaki gerekçeler karmaşık olduğu için, `Architecture_better.md` dosyasına yeni bir bölüm ekliyorum."
        *   "Bu karar temel bir prensibi değiştirdiği için, `YBIS_PROJE_ANAYASASI.md` dosyasını güncellememiz gerekiyor. Onaylıyor musunuz?"

4.  **Dokümanları Güncelleme:**
    *   AI, kullanıcının onayıyla ilgili dokümanları `replace` veya `write_file` araçlarını kullanarak günceller.

**Kullanım:**
- `/ybis:end_session` komutunun yönlendirmesiyle.
- Geliştirme sırasında anlık olarak önemli bir mimari karar alındığında.

**Faydası:**
- Kararların sadece `DEVELOPMENT_LOG.md`'de kalmasını engeller.
- İlgili tüm dokümanların **anında ve tutarlı bir şekilde** güncellenmesini sağlar.
- Dokümantasyonun zamanla güncelliğini yitirmesinin önüne geçer.
