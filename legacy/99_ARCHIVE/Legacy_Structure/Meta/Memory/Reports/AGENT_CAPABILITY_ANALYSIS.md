# Revize Edilmiş Kapsamlı Ajan ve Model Kabiliyet Analizi
**Tarih:** 29 Kasım 2025 (Rev. 2)
**Hazırlayan:** @MainAgent (Gemini)
**Amaç:** Bu doküman, kullanıcının sağladığı spesifik ve güncel bilgiler ışığında tamamen revize edilmiştir. Amacı, projedeki AI ajanlarının ve bu ajanlara güç veren **sınır (frontier)** dil modellerinin en güncel yeteneklerini, güçlü ve zayıf yönlerini derinlemesine analiz ederek, görev dağılımı stratejisini en üst seviyeye çıkarmaktır.

---

## BÖLÜM 1: SINIR (FRONTIER) DİL MODELLERİNİN YETENEK PROFİLLERİ

Ajanların gerçek gücü, kullandıkları modellerin yeteneklerinden gelir. Bu bölümde, belirttiğiniz en yeni model profillerini ve onların stratejik anlamlarını inceliyoruz.

### 1.1. "Pragmatik Güç Merkezi" Profili (Anthropic Frontier: Claude 4.5 Opus & 3.5 Sonnet)
- **Genel Bakış:** Bu profil, saf kodlama performansı, hız ve pratik geliştirici araçları arasındaki mükemmel dengeyi temsil eder. Anthropic'in en yeni modelleri, özellikle yazılım mühendisliği benchmark'larında (SWE-bench gibi) lider konumdadır.
- **Güçlü Yönleri:**
    - **Benchmark Lideri Kodlama:** Claude 4.5 Opus, gerçek dünya yazılım mühendisliği görevlerinde GPT serisi de dahil olmak üzere rakiplerini geride bırakarak, en yüksek başarı oranlarına ulaşmıştır. Bu, onu özellikle **karmaşık bug fix'ler, refactoring ve yeni özellik implementasyonu** için en güvenilir seçenek yapar.
    - **Hız ve Verimlilik:** Claude 3.5 Sonnet, Opus'a yakın bir performans sunarken ondan çok daha hızlı ve uygun maliyetlidir. Bu, onu interaktif, diyalog bazlı kodlama seansları için ideal kılar.
    - **Devrimsel "Artifacts" Özelliği (Sonnet 3.5):** Bir UI bileşeni veya web sayfası istendiğinde, kodu üretmekle kalmaz, aynı zamanda yan tarafta **canlı bir önizleme penceresi** oluşturur. Bu, frontend ve UI geliştirme döngüsünü inanılmaz hızlandıran, oyunun kurallarını değiştiren bir özelliktir.
- **Zayıf Yönleri:**
    - **Niş Akıl Yürütme:** Felsefe veya çok soyut yaratıcılık gerektiren alanlarda, OpenAI'nin en tepe modellerinin "düşünce derinliğine" henüz tam olarak erişemeyebilir. Ancak bu fark, kodlama ve mühendislik gibi pratik alanlarda önemsizdir.
- **Stratejik Anlamı:** "Claude Code" personamız, bu çift model stratejisini kullanmalıdır. **Karmaşık arka-uç ve algoritma görevleri için Claude 4.5 Opus**, **hızlı, interaktif ve özellikle görsel (UI/frontend) görevler için Claude 3.5 Sonnet** kullanılmalıdır.

- **Kullanıcı Geri Bildirimleri ve Pratik Gözlemler:**
    - **Kod Kalitesi:** Geliştiriciler, Claude 3.5 Sonnet'in genellikle "kutudan çıktığı gibi çalışan", temiz ve daha az bug içeren kod üretme eğiliminde olduğunu belirtiyor. GPT-4o'ya kıyasla daha güvenilir ve daha az "halüsinasyon" gördüğü sıkça dile getirilen bir görüş.
    - **Prompt Hassasiyeti:** Claude'un genellikle daha az karmaşık prompt'larla bile istenen sonuca daha direkt ulaştığı, GPT serisinin ise bazen istenen şeyin etrafında dolanabildiği veya aşırı açıklama yapabildiği raporlanıyor.
    - **Konteks Penceresi:** 200K'lık geniş konteks penceresi teoride olduğu gibi pratikte de övülüyor. Kullanıcılar, büyük dosyalarda veya uzun konuşmalarda Claude'un bağlamı tutarlı bir şekilde hatırlama yeteneğinden memnun.
    - **Hız vs. Limitler:** Modelin hızı genel olarak beğenilse de, en büyük şikayet kullanım limitlerinin (özellikle Pro sürümde) yoğun kullanımda çabuk tükenmesi. Bu durum, geliştiricileri limit dolduğunda daha az yetenekli modellere geçmeye zorlayabiliyor.
    - **Artifacts Faktörü:** "Artifacts" özelliği, özellikle frontend geliştiricileri tarafından ezber bozan bir yenilik olarak görülüyor. Canlı önizleme, iterasyon hızını katlayarak artırıyor ve bu özellik tek başına bile Claude'u UI görevleri için birincil tercih haline getiriyor.

### 1.2. "Derin Düşünür" Profili (OpenAI Frontier: GPT-5.1 / o-series)
- **Genel Bakış:** Bu profil, ham işlem gücünden ziyade, bir problemi çözmeden önce "düşünme", planlama ve en iyi stratejiyi belirleme yeteneğini temsil eder. OpenAI'nin `o-series` (o1, o3-pro) ve varsayımsal `GPT-5.1`'i bu kategoriye girer.
- **Güçlü Yönleri:**
    - **Zincirleme Düşünce (Chain of Thought):** Bir komutu alır almaz kod yazmak yerine, problemi alt adımlara ayırır, bir plan oluşturur ve bu planı adım adım uygular. Bu, özellikle karmaşık ve daha önce görülmemiş görevlerde başarı oranını ciddi şekilde artırır.
    - **Üst Düzey Mantıksal Akıl Yürütme:** Bilimsel makaleleri anlama, karmaşık matematik problemleri çözme ve çok katmanlı soyut sistemler tasarlama konusunda rakipsizdir.
    - **Agentic Planlama:** Otonom bir ajanın beyni olmak için tasarlanmıştır. "Uygulamayı deploy et" gibi geniş bir hedefi alıp, bunun için gereken tüm adımları (gerekli script'leri yazma, konfigürasyonları kontrol etme, komutları çalıştırma) kendisi planlayabilir.
- **Zayıf Yönleri:**
    - **Hız ve Gereklilik:** Basit bir fonksiyon yazmak gibi görevler için bu "derin düşünme" süreci gereksiz derecede yavaş ve maliyetli olabilir. Her görev için bir stratejiste ihtiyaç yoktur.
- **Stratejik Anlamı:** Bu profil, projenin en karmaşık, stratejik ve mimari kararlarının alınması gereken yerlerde devreye girmelidir. Özellikle **yeni bir sistemin sıfırdan mimarisini tasarlarken veya çok kritik bir güvenlik açığını analiz ederken** bu modelin akıl yürütme gücü hayati önem taşır.

- **Kullanıcı Geri Bildirimleri ve Pratik Gözlemler:**
    - **Akıl Yürütme ve "Kıvrak Zeka":** Kullanıcılar, GPT serisinin hala en "yaratıcı" ve "kıvrak zekalı" model olduğu konusunda hemfikir. Özellikle daha önce karşılaşılmamış, soyut ve yaratıcı çözüm gerektiren problemlerde GPT'nin performansı öne çıkıyor.
    - **Kod Kalitesinde Tutarsızlık ve "Tembellik":** GPT-4o'nun çıkışıyla birlikte, birçok geliştirici kodlama yeteneklerinde bir "gerileme" veya "tembelleşme" olduğunu rapor etti. Modelin bazen kodu tamamlamadığı, placeholder'lar bıraktığı veya bariz hatalar yaptığına dair şikayetler mevcut. Bu durum, "Derin Düşünür" profilinin her zaman en iyi kodu yazacağı anlamına gelmediğini, sadece en iyi planı yapabileceğini gösteriyor.
    - **Prompt Mühendisliği:** GPT'den en iyi sonucu almak, genellikle daha fazla "prompt mühendisliği" gerektiriyor. Kullanıcılar, istedikleri formatı ve sonucu elde etmek için Claude'a göre daha fazla deneme-yanılma yapmak zorunda kaldıklarını belirtiyor.
    - **Hız:** GPT-4o'nun hızı genel olarak beğeniliyor, ancak bu hızın bazen kalite pahasına geldiği düşünülüyor. "Derin Düşünür" modlarının (o-series) ise bu kalite sorununu çözmesi bekleniyor, ancak bu da hızı düşürecektir.

### 1.3. "Orkestratör" Profili (Google Frontier: Gemini 3 Pro)
- **Genel Bakış:** Bu profil, tek bir görevi mükemmel yapmaktan ziyade, çok büyük bir bağlamı anlama ve bu bağlam içindeki farklı parçaları bir araya getirme yeteneğini temsil eder.
- **Güçlü Yönleri:**
    - **Devasa Konteks Penceresi (1M+ token):** Projenin **tüm kod tabanını** tek seferde hafızasına alabilir. Bu, "Bu yaptığımız değişiklik projenin başka hangi noktasını etkiler?" veya "Projedeki tüm testleri analiz et ve eksik alanları raporla" gibi görevler için eşsiz bir yetenektir.
    - **Yerleşik Multimodalite:** Sadece kodu değil, Figma tasarımlarını, akış şemalarını, hatta kullanıcı geri bildirim videolarını aynı anda anlayabilir.
    - **Ekosistem Entegrasyonu:** Google'ın kendi servisleriyle (örn: Vertex AI, Google Cloud) doğal bir entegrasyon potansiyeli vardır.
- **Zayıf Yönleri:**
    - **Saf Kod Üretimi:** Birebir kod üretme veya anlık bug fix benchmark'larında bazen Claude serisinin gerisinde kalabilir. Onun gücü, kodu yazmaktan çok, kodun büyük resimdeki yerini anlamaktır.
- **Stratejik Anlamı:** `@MainAgent` (ben) ve `@Antigravity` gibi orkestrasyon ve sistem geneli analiz rollerinde bu modelin kullanılması en doğrusudur. **Proje genelinde tutarlılığı sağlama, dokümantasyonu kodla senkronize etme ve mimari kararların etkisini analiz etme** gibi görevler için idealdir.

- **Kullanıcı Geri Bildirimleri ve Pratik Gözlemler:**
    - **Devasa Konteksin Pratiği:** Geliştiriciler, Gemini'nin 1 milyon token'lık konteks penceresini "teoride harika, pratikte dikkatli kullanılmalı" olarak yorumluyor. Tüm kod tabanını vermek, modelin bazen ana görevden sapmasına veya alakasız detaylara odaklanmasına neden olabiliyor ("iğne samanlıkta kayboluyor"). En iyi sonucun, görevin gerektirdiği en alakalı dosyaları seçerek konteks oluşturmakla alındığı belirtiliyor.
    - **Kod Üretimi Performansı:** Gemini'nin saf kod üretme yeteneği, genellikle Claude ve GPT'nin en iyi versiyonları arasında bir yerde konumlandırılıyor. Ne Claude kadar direkt hatasız, ne de GPT kadar yaratıcı bulunabiliyor. Ancak Google ekosistemi (Firebase, Google Cloud, Android) ile ilgili kodlarda daha başarılı olduğu gözlemleniyor.
    - **Geliştirici Deneyimi:** Google'ın AI araçları (AI Studio, Vertex AI) henüz diğer platformlar kadar "geliştirici dostu" veya "cilalı" bulunmayabiliyor. API'ların ve araçların olgunlaşması için hala zaman olduğu genel bir kanı. Bu durum, Gemini'yi ham bir motor olarak güçlü kılsa da, son kullanıcı araçlarında deneyimi bir adım geride bırakabiliyor.

---

## BÖLÜM 2: DERİNLEMESİNE AJAN VE ARAÇ ANALİZİ (REV. 2)

### 2.1. Antigravity
- **Temel Fonksiyonu:** Karmaşık, çok adımlı görevleri yürüten ve diğer ajanları/araçları yönetebilen bir üst düzey orkestratör.
- **Underlying Models:** **Gemini 3 Pro**'nun orkestrasyon ve geniş konteks yeteneklerini kullanarak çalışır. Ancak gerektiğinde diğer API'leri (örn: OpenAI, Anthropic) de tetikleyebilir.
- **Anahtar Özellikler:**
    - **Otonom İş Akışı:** "Veritabanı şemasını güncelle, ilgili API route'larını refactor et ve sonucu Slack'e bildir" gibi bir iş akışını baştan sona kendi yönetebilir.
    - **Paralel Görev Yürütme:** Farklı görevleri farklı API'lere veya alt-ajanlara aynı anda atayarak süreci hızlandırabilir.
- **Güçlü Yönleri:**
    - **Meta-Ajan:** Diğer araçların ve API'lerin üzerinde bir yönetici katmanı olarak çalışır.
    - **Altyapı Yönetimi:** CI/CD pipeline'larını tetikleme, bulut ortamlarında script çalıştırma gibi altyapısal görevler için idealdir.
- **Zayıf Yönleri:**
    - **Overkill:** Tek bir dosyada basit bir değişiklik yapmak için Antigravity'yi kullanmak, sineği topla avlamaya benzer.
- **En İyi Kullanım Alanları:**
    - **Sistem Kurulumu ve Dağıtımı (Deployment):** Yeni bir ortam kurma veya uygulamayı production'a deploy etme gibi çok adımlı, karmaşık süreçler.
    - **Periyodik Bakım:** Her gece testleri çalıştırıp, sonuçları analiz edip, hataları `TASK_BOARD.md`'ye otomatik olarak ekleyen bir görev.

- **Kullanıcı Geri Bildirimleri ve Pratik Gözlemler:**
    - **Yüksek Öğrenme Eğrisi:** Antigravity gibi üst düzey orkestrasyon araçları, "tak-çalıştır" kolaylığında değildir. Kullanıcılar, bir iş akışını doğru şekilde tanımlamanın ve ajana doğru yetkileri vermenin zaman aldığını belirtiyor.
    - **"İzleme" Modu Kritikliği:** Ajan otonom çalışırken, ne yaptığını "Manager Surface" gibi bir arayüzden anlık olarak izlemek hayati önem taşıyor. Kullanıcılar, ajanın beklenmedik bir yola sapması durumunda müdahale edebilmenin önemini vurguluyor.
    - **Hata Ayıklama Zorluğu:** Otonom bir ajanın neden başarısız olduğunu anlamak, geleneksel bir koddaki hatayı bulmaktan daha zor olabiliyor. Ajanın "düşünce sürecini" loglayan mekanizmaların ne kadar detaylı olduğu, bu noktada kilit rol oynuyor.

### 2.2. Cursor
- **Temel Fonksiyonu:** AI'ı bir yardımcı olmaktan çıkarıp, geliştirme ortamının merkezine koyan, proje bütününü anlayan akıllı bir kod editörü.
- **Underlying Models:** **Kendi özel "Composer 1" modeline sahiptir.** Ancak ayarlardan GPT-4o, **Claude 4.5 Opus** gibi dış modellere de geçiş yapma imkanı sunar.
- **Anahtar Özellikler ve Stratejik Kullanım:**
    - **Composer 1 Modeli:** Hızlı, editörle derinlemesine entegre ve basit-orta karmaşıklıktaki görevler için optimize edilmiştir. **Hızlı refactoring, boilerplate kod üretimi veya mevcut kod üzerinde değişiklikler yapmak için varsayılan tercih bu olmalıdır.**
    - **Dış Model Kullanımı (Stratejik Seçim):**
        - Görev, **çok karmaşık bir mantık veya daha önce görülmemiş bir algoritma tasarımı** gerektiriyorsa, Cursor içinden **"GPT-5.1" (Derin Düşünür)** profiline sahip modele geçiş yapılmalıdır.
        - Görev, **bir UI bileşeni tasarlamak veya görsel bir şeyi kodlamaksa**, Cursor içinden **"Claude 3.5 Sonnet"** modeline geçiş yapılarak (eğer API destekliyorsa) Artifacts benzeri bir deneyim hedeflenebilir.
    - **Agent Mode:** Terminal komutları çalıştırabilen, kendi yazdığı kodu test edip düzeltebilen en otonom modudur. **"Bu bug'ı düzelt"** gibi daha genel hedefler verildiğinde, çözüm için gerekli adımları (dosya okuma, yazma, test çalıştırma) kendi kendine belirler.
- **Güçlü Yönleri:**
    - **Proje Çapında Farkındalık:** Bir değişiklik yaparken, bunun projenin başka hangi köşesini etkileyeceğini bilmesi, en büyük gücüdür.
    - **Modeller Arası Geçiş:** Tek bir arayüzden, görevin ihtiyacına göre en doğru "beyni" seçme esnekliği sunar.
- **Zayıf Yönleri:**
    - **Kaynak Tüketimi:** Standart bir metin editöründen daha fazla sistem kaynağına ihtiyaç duyar.
- **En İyi Kullanım Alanları:**
    - **Mimari Refactoring:** Projedeki bir temel sınıfın veya arayüzün (interface) değiştirilmesi ve bu değişikliğin 20+ dosyaya hatasız bir şekilde yansıtılması.
    - **Sıfırdan Özellik Geliştirme:** "Agent Mode"da, "Kullanıcının profil resmini güncelleyebileceği bir ayarlar sayfası oluştur. Gerekli component, hook ve API çağrılarını sen yaz." gibi kapsamlı görevler.

- **Kullanıcı Geri Bildirimleri ve Pratik Gözlemler:**
    - **Verimlilik Artışı:** Geliştiriciler arasındaki genel kanı, Cursor'a alıştıktan sonra verimliliğin **2x ila 3x** arttığı yönünde. Özellikle proje çapında değişiklikler için harcanan zamanı dramatik ölçüde azalttığı belirtiliyor.
    - **"Her Zaman Güvenme, Her Zaman Doğrula":** Kullanıcıların üzerinde birleştiği en önemli nokta, Cursor'un ürettiği hiçbir kodun körü körüne kabul edilmemesi gerektiği. Ajanın önerilerini her zaman dikkatle incelemek ve test etmek bir zorunluluk olarak görülüyor.
    - **Buggy ve Dikkat Dağıtıcı Olabilir:** Bazı kullanıcılar, özellikle çok aktifken, sürekli öneri getirmesinin veya bazen hatalı kod üretmesinin dikkat dağıtıcı olabildiğini rapor ediyor.
    - **Composer 1 vs Dış Modeller:**
        - **Composer 1:** "Steroidli otomatik tamamlama" gibi hissettirdiği söyleniyor. İnanılmaz hızlıdır ve basit-orta seviye düzenlemeler için mükemmeldir. Kullanıcılar, hızlı bir geri bildirim döngüsü için bunu tercih ediyor.
        - **Dış Modeller (GPT/Claude):** Daha derin akıl yürütme veya sıfırdan karmaşık bir mantık kurma gerektiğinde, kullanıcılar genellikle daha güçlü dış modellere geçiş yapmanın daha iyi sonuç verdiğini belirtiyor. Composer 1'in hızı, bu durumlarda derinlikten ödün verebiliyor.

### 2.3. Copilot CLI
- **Temel Fonksiyonu:** Geliştiricinin klavyesinin bir uzantısı gibi çalışan, terminal-native, hızlı ve çevik bir AI ajanı.
- **Underlying Models:** `/model` komutu ile **GPT-5.1, Claude 4.5 Opus** dahil olmak üzere mevcut en güçlü modellere anında geçiş yapabilir. Bu, onun en stratejik özelliğidir.
- **Anahtar Özellikler:**
    - **Terminal Kamuflajı:** Geliştirme ortamını terk etmeden, doğrudan komut satırında çalışır.
    - **Dinamik Model Seçimi:** Bir shell script'i yazmak gibi basit bir görev için hızlı bir model (örn: Claude 3.5 Sonnet) kullanırken, bir sonraki komutta karmaşık bir `git` komutu oluşturmak için "Derin Düşünür" (örn: GPT-5.1) profiline geçebilir.
- **Güçlü Yönleri:**
    - **Çeviklik ve Hız:** Hızlı, tek seferlik görevler ve script'ler için en verimli araçtır.
    - **Bağlam Değiştirme Yeteneği:** `/model` komutu, ona adeta bir "İsviçre çakısı" kimliği kazandırır.
- **Zayıf Yönleri:**
    - **Görsel ve Kapsamlı Görevler:** Görsel bir arayüzü yoktur ve Cursor gibi tüm projeyi kapsayan derin mimari değişiklikler için tasarlanmamıştır.
- **En İyi Kullanım Alanları:**
    - **"Yardımcı Pilot" Görevleri:** "Bu projedeki tüm `TODO` yorumlarını bul ve bir markdown listesi oluştur.", "npm paketlerindeki zafiyetleri kontrol eden komutu yaz.", "Bu karmaşık regex'i bana açıkla."
    - **Git ve Altyapı İşlemleri:** "Son 3 commit'i tek bir commit altında toplayan interaktif bir rebase komutu başlat."

- **Kullanıcı Geri Bildirimleri ve Pratik Gözlemler:**
    - **Akış Bozmayan Yardımcı:** Geliştiriciler tarafından en çok övülen yönü, IDE veya başka bir pencereye geçmeden, doğrudan terminalde kalarak hızlıca yardım alabilmek. Bu, "akışı bozmama" (staying in the flow) açısından çok değerli bulunuyor.
    - **Prompt Çabası vs Kodlama Çabası:** Karmaşık bir görev için, mükemmel prompt'u oluşturmaya çalışmanın bazen kodu doğrudan yazmaktan daha uzun sürebildiği yaygın bir geri bildirim. Bu nedenle, genellikle küçük ve net tanımlanmış görevler için daha verimli olduğu düşünülüyor.
    - **IDE'den Bağımsızlık:** Farklı editörler (VS Code, Vim, JetBrains) kullanan takımlarda, Copilot CLI'nin herkes için ortak bir AI yardımcısı standardı oluşturması pratik bir avantaj olarak görülüyor.
    - **Güvenilirlik:** Diğer tüm AI araçları gibi, önerilerinin bazen hatalı veya en iyi pratiklere uygun olmayabileceği, bu yüzden çıktısının her zaman bir geliştirici tarafından doğrulanması gerektiği vurgulanıyor.

---

## BÖLÜM 3: STRATEJİK GÖREV-AJAN EŞLEŞTİRME MATRİSİ (REV. 2)

| Görev Senaryosu | Birincil Ajan | Kullanılacak Model/Mod | Gerekçe | Yedek Ajan |
| :--- | :--- | :--- | :--- | :--- |
| **Yeni bir ekranın UI'ını sıfırdan kodlamak** | Claude Code (Persona) | Claude 3.5 Sonnet | **Artifacts özelliği** ile canlı önizleme yaparak en hızlı geliştirme döngüsünü sunar. | Cursor |
| **Karmaşık bir algoritmayı veya backend servisini sıfırdan yazmak** | Copilot CLI | GPT-5.1 / o-series | **Derin Düşünür** profili, en iyi mantıksal planı ve en hatasız kodu üretir. | Claude Code (Opus 4.5) |
| **Proje genelinde (15+ dosya) bir API'nin kullanım şeklini değiştirmek**| Cursor | Agent Mode + Composer 1 | Proje çapında farkındalığı ve otonom dosya düzenleme yeteneği bu iş için idealdir. | Antigravity |
| **"Build neden patlıyor?" sorununu araştırmak** | Antigravity | Gemini 3 Pro | Logları okuma, komut çalıştırma ve internette arama yapma gibi çok adımlı otonom bir iş akışı gerektirir. | Copilot CLI |
| **Basit bir shell script'i yazmak veya bir `git` komutu oluşturmak** | Copilot CLI | Claude 3.5 Sonnet (Hız için) | En hızlı ve en direkt çözümü sunan terminal-native araçtır. | - |
| **"Yaptığımız son değişiklikler mimariyi bozuyor mu?" diye analiz etmek**| @MainAgent (Gemini) | Gemini 3 Pro (Geniş Konteks) | Tüm kod tabanını hafızasına alıp, yapılan değişikliğin potansiyel yan etkilerini analiz edebilir. | - |
| **Projedeki tüm component'ler için test taslakları oluşturmak** | Antigravity (Orkestratör) | `Codex` Fonksiyonunu Tetikler | Bu bir batch (toplu) iştir ve en iyi şekilde otomatize edilmiş bir script ile yapılır. | Cursor |
