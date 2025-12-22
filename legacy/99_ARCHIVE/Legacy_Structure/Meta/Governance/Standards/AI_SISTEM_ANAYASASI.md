# AI Sistemi Anayasası

**Sürüm:** 1.1.0
**Durum:** Aktif
**Amaç:** Bu anayasa, YBIS projesinde çalışan tüm AI asistanları için geçerli olan evrensel kuralları, protokolleri ve çalışma prensiplerini tek bir merkezi belgede birleştirir.

---

## 1. Temel Prensipler

### 1.1. Araç Yönlendirme Prensibi (Tool Routing Principle)

Her AI aracının (Claude, Gemini, Cursor vb.) kendine özgü güçlü yanları vardır. Bir görev, başka bir aracın uzmanlık alanına daha uygunsa, bu durum kullanıcıya gerekçesiyle birlikte belirtilmeli ve görev yönlendirmesi önerilmelidir. Nihai karar her zaman kullanıcıdadır.

### 1.2. Komut Yönlendirme Prensibi (Command Index Principle)

Bir kullanıcı isteği birden fazla iş akışıyla karşılanabiliyorsa, doğrudan eyleme geçilmez. Bunun yerine, merkezi "Kontrol Merkezi" dokümanına başvurularak kullanıcıya olası iş akışları ve ilgili komutlar seçenek olarak sunulur.

### 1.3. Ajanlar Arası İletişim Protokolü (Inter-Agent Communication)

AI ajanları arası görev ve bilgi aktarımı, `docs/AI/` klasörü altındaki standartlaştırılmış "gelen kutusu" yapısı üzerinden yürütülür. Bir ajan, görevi devretmeden önce çıktısını ilgili ajanın klasörüne kaydeder.

### 1.4. Anayasa Değişiklik Prensibi (Constitution Amendment Principle)

Bu anayasa yaşayan bir belgedir. Bir AI asistanı, mevcut kurallarda bir eksiklik veya iyileştirme potansiyeli tespit ederse, bunu yapılandırılmış bir formatta kullanıcıya "Anayasa Değişiklik Teklifi" olarak sunma ve onay isteme yetkisine sahiptir. Onay alınmadan anayasa dosyaları asla doğrudan değiştirilemez.

### 1.5. İşbirlikçi Zeka Prensibi (Collaborative Intelligence Principle)

Bu prensip, insan ve yapay zeka arasındaki işbirliği modelini tanımlar. Stratejik yönlendirme, nihai karar ve soyut hedefler insan tarafından belirlenir. Detaylı analiz, veri işleme, kod yazma ve otomasyon gibi görevler ise yapay zeka tarafından yürütülür. Ajan, görevleri proaktif olarak anlamak ve uygulamak için "Ajan Farkındalık Haritası" gibi araçları kullanır.

### 1.6. Kod Paylaşım Prensibi (Code Sharing Principle)

- **Kural:** Tüm tekrar eden fonksiyonlar, tipler ve yardımcı işlevler (`utils`) merkezi ve paylaşılan bir `package` altına taşınmalıdır. Aynı mantığın birden fazla uygulama (`apps/*`) veya paket (`packages/*`) dizininde yer alması yasaktır.
- **Amaç:** Kod tekrarını (duplication) önlemek, bakımı kolaylaştırmak ve "Net Yürütme Prensibi"ni proje genelinde uygulamak.
- **Uygulama:** Bu kural, CI/CD sürecinde `duplicate-detector` gibi araçlarla otomatik olarak kontrol edilmelidir.

---

## 2. Başlangıç ve Bağlam Yükleme Protokolü (Startup & Context Loading Protocol)

Bu protokol, her ajanın bir oturuma başlarken minimum token kullanarak maksimum bağlama sahip olmasını sağlar.

### 2.1. Zorunlu Başlangıç Prosedürü

**Kural:** Her yeni AI oturumu, herhangi bir göreve başlamadan önce aşağıdaki adımları tamamlamak zorundadır. "Kullanıcı acil görev verdi" veya "görev basit" gibi mazeretler kabul edilemez.

1.  **Kontrol Merkezi'ni Oku:** Ajan, ilk olarak `docs/YBIS_STANDARDS/README.md` dosyasını okur. Bu dosya, projenin ana haritasıdır.
2.  **Anayasaları Oku:** Ajan, `docs/YBIS_STANDARDS/1_Anayasa/README.md` (Proje Anayasası) ve bu dokümanın kendisini (`AI_SISTEM_ANAYASASI.md`) okur.
3.  **Hazırlık Bildirimi:** Bu üç temel doküman okunduktan sonra, ajan kullanıcıya soru sormadan, "✅ Bağlam yüklendi, hazırım." şeklinde kısa bir bildirimde bulunur.

### 2.2. Görev Bazlı Akıllı Yükleme (Lazy Loading)

- **Kural:** Başlangıçta sadece yukarıdaki üç temel dosya okunur. Diğer tüm standartlar ve rehberler, görevin gerektirdiği anda, "Kontrol Merkezi"ndeki "Ajan Farkındalık Haritası"na başvurularak yüklenir.
- **Örnek:** Kullanıcı "yeni bir test yaz" dediğinde, ajan haritayı kontrol eder ve `4_Test_Stratejisi/README.md` dosyasını okuyarak göreve başlar.
- **Amaç:** Bu yaklaşım, her oturumun hızlı ve düşük maliyetli başlamasını sağlar, gereksiz bilgi yüklemesini önler.

---

## 3. İçerik ve İletişim Kuralları (Content & Communication Conventions)

### 3.1. AI Talimatlarını Ayırma

- **Prensip:** AI tarafından yönetilen veya AI'a yönelik talimatlar içeren metin blokları, dokümanın ana içeriğinden net bir şekilde ayrılmalıdır.
- **Kural:** Tüm AI talimatları, sistem tarafından oluşturulan notlar veya bir insan tarafından okunması gerekmeyen meta-veriler, HTML yorum blokları (`<!-- ... -->`) içine alınmalıdır.

### 3.2. Özel Direktifler

- **Kritik Bilgi:** AI'ın mutlak suretle dikkat etmesi gereken kritik bilgiler, `<!-- IMPORTANT: ... -->` formatında belirtilmelidir.
- **Zorunlu Eylem:** AI'ın bir görevi yerine getirirken yapması gereken belirli eylemler, `<!ACTION!> ... </!ACTION!>` formatında belirtilmelidir.
- **Amaç:** Bu formatlar, AI'ın talimatları doğru bir şekilde önceliklendirmesini ve eyleme dönüştürmesini sağlar, insan odaklı okunabilirliği artırır ve AI'ın yanlışlıkla kendi talimatlarını içerik olarak yorumlamasını engeller.