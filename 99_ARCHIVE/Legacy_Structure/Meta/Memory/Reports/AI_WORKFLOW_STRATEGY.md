# Kişisel AI Destekli Geliştirme İş Akışı Stratejisi

**Amaç:** Gemini, Claude, Copilot gibi farklı LLM'ler ile Cursor, CLI gibi geliştirme araçlarını entegre ederek kişisel yazılım geliştirme verimliliğini en üst düzeye çıkarmak.

**Felsefe:** Hiçbir araç her işte en iyi değildir. Bu strateji, her bir aracın güçlü yönlerini birleştirerek ve zayıf yönlerini diğerleriyle telafi ederek, görev odaklı bir "uzmanlar sistemi" kurmayı hedefler.

---

## 1. LLM Entegrasyon Stratejileri: "Doğru Göreve Doğru Uzman"

### 1.1. Görev Ayrıştırma (Task Specialization)

Aşağıdaki tablo, farklı geliştirme senaryoları için hangi LLM'in "Birincil" ve "İkincil" uzman olarak kullanılabileceğini özetler.

| Görev | Birincil Uzman | İkincil Uzman | Gerekçe ve Kullanım Senaryosu |
| :--- | :--- | :--- | :--- |
| **Yeni Kod Yazma (Sıfırdan)** | **Gemini** | Copilot | **Gemini:** Karmaşık mantık, algoritma ve tam fonksiyon/class taslakları oluşturmada güçlüdür. "Bana X işini yapan bir React hook'u yaz" gibi talepler için idealdir. |
| **Kod Tamamlama (Anlık)** | **Copilot** | Gemini | **Copilot:** Satır içi, anlık kod tamamlama ve küçük bloklar önermede en hızlı ve en entegre olanıdır. Hız ve akıcılık için vazgeçilmezdir. |
| **Mevcut Kodu Anlama/Özetleme** | **Claude** | Gemini | **Claude:** Geniş context penceresi sayesinde uzun kod dosyalarını veya tüm bir modülü analiz edip özetlemede, "Bu kod ne işe yarıyor?" sorusuna cevap vermede çok başarılıdır. |
| **Dokümantasyon ve Yorum Yazma** | **Claude** | Gemini | **Claude:** Teknik metinleri akıcı ve anlaşılır bir dilde yazma, `README.md` veya kod içi yorumlar oluşturma konusunda genellikle daha iyidir. |
| **Refactoring ve Kod Kalitesi** | **Gemini** | Copilot | **Gemini:** Mevcut bir kod bloğunu alıp daha temiz, daha performanslı veya modern pratiklere uygun hale getirme konusunda derinlemesine analiz ve öneriler sunar. |
| **Test Senaryoları Yazma** | **Gemini** | Claude | **Gemini:** Bir fonksiyon veya bileşenin kodunu analiz ederek kapsamlı unit ve entegrasyon testleri (örn: Jest, Vitest) oluşturmada çok yeteneklidir. |
| **Karmaşık Hata Ayıklama (Debugging)**| **Gemini** | Claude | **Gemini:** Hata mesajlarını ve ilgili kod bloklarını analiz ederek olası kök nedenleri ve çözüm önerilerini bulmada güçlü bir mantıksal çıkarım yeteneğine sahiptir. |

### 1.2. API Orkestrasyonu: "Komut Zincirleri"

Farklı LLM'leri bir boru hattı (`|`) gibi kullanarak birleşik iş akışları oluşturun. Bu, özellikle CLI araçları üzerinden çok güçlü hale gelir.

**Örnek İş Akışı: Yeni Bir Özellik İçin Test Yazma**

1.  Önce, özelliğin kodunu **Claude**'a vererek ne yaptığını özetletin.
2.  Sonra, bu özeti ve orijinal kodu **Gemini**'ye vererek birim testleri yazmasını isteyin.

**Örnek Shell Script (`test_generator.sh`):**
```bash
#!/bin/bash
# Kullanım: ./test_generator.sh <dosya_adi.tsx>

# 1. Adım: Claude CLI ile kodu özetle
SUMMARY=$(claude-cli --file "$1" "Bu React bileşeninin ana işlevselliğini ve proplarını özetle.")

# 2. Adım: Gemini CLI ile özeti ve orijinal kodu kullanarak test oluştur
gemini-cli --file "$1" --context "İşlevselliği şu şekilde özetlenen bileşen için Jest ve React Testing Library kullanarak birim testleri yaz: $SUMMARY" > "${1%.tsx}.test.tsx"

echo "Test dosyası oluşturuldu: ${1%.tsx}.test.tsx"
```

### 1.3. Veri Akışı Yönetimi
- **Prompt Chaining:** Bir LLM'in çıktısını, bir sonraki LLM için girdi (veya context) olarak kullanın. Yukarıdaki script buna bir örnektir.
- **Yapısal Çıktılar:** LLM'lerden `JSON` formatında çıktı isteyin. Bu, script'ler aracılığıyla veriyi işlemenizi kolaylaştırır. Örnek: "Bu kodun karmaşıklığını {cyclomaticComplexity: number, lineCount: number} formatında JSON olarak analiz et."

---

## 2. Araç Entegrasyon Stratejileri: "İş Akışını Fiziğe Dökmek"

### 2.1. Cursor IDE: "Merkez Komuta"
- **Çoklu LLM Yapılandırması:** Cursor ayarlarından farklı görevler için farklı LLM'leri (API anahtarlarınızla) yapılandırın.
- **`@` Komutları:** Sohbet panelinde `@Gemini` veya `@Claude` gibi komutlarla doğrudan istediğiniz uzmana soru sorun.
- **"Code With..." Özelliği:** Bir kod bloğunu seçip `Ctrl+K` ile açılan menüde, o anki göreve en uygun LLM'i seçerek (örn: "Refactor with Gemini", "Document with Claude") doğrudan düzenleme yapın.

### 2.2. CLI Araçları: "Otomasyonun Gücü"
Bu, verimliliği en çok artıracak alandır. `~/.bashrc`, `~/.zshrc` veya PowerShell profilinize özel fonksiyonlar ve alias'lar ekleyin.

**Örnek Alias ve Fonksiyonlar:**

```bash
# .bashrc veya .zshrc dosyanıza ekleyin

# Bir dosyanın özetini almak için
function summarize() {
  claude-cli --file "$1" "Bu dosyanın amacını, ana fonksiyonlarını ve dışa aktarımlarını 3 maddede özetle."
}

# Bir dosya için test taslağı oluşturmak için
function testgen() {
  gemini-cli --file "$1" "Bu dosyadaki kod için Vitest kullanarak birim testleri yaz. Mocking gereken yerleri belirt." > "${1%.*}.test.ts"
  echo "Test taslağı oluşturuldu: ${1%.*}.test.ts"
}

# Seçili kodun kalitesini analiz etmek için
function quality() {
  gemini-cli --file "$1" "Bu kod parçasındaki olası hataları, performans sorunlarını ve SOLID prensiplerine aykırı durumları analiz et ve raporla."
}
```

### 2.3. Coxex (veya Diğer Özelleşmiş Araçlar)
`Coxex` ismini, projenize veya alanınıza özel, daha niş bir analiz aracı için bir yer tutucu olarak ele alalım.
- **Kullanım Alanı:** Bu tür araçları, genel amaçlı LLM'lerin yetersiz kaldığı çok spesifik görevler için kullanın. Örneğin:
    - Bir C++ projesindeki memory leak'leri analiz etme.
    - Bir veritabanı sorgusunun yürütme planını (execution plan) optimize etme.
    - Özel bir donanım için yazılmış kodun performansını profilleme.
- **Entegrasyon:** Bu aracın çıktılarını (genellikle bir log veya rapor) kopyalayıp, bu çıktıyı yorumlaması ve aksiyon planı oluşturması için **Gemini** veya **Claude**'a girdi olarak verin.

---

## 3. Verimlilik Artırma Metrikleri: "Gelişimi Ölçmek"

| Metrik | Nasıl Ölçülür? | Hedef |
| :--- | :--- | :--- |
| **Geliştirme Süresi Kısalması** | Jira/GitHub gibi araçlarda bir "story" veya "task"in başlangıcından bitişine kadar geçen süreyi (cycle time) takip edin. | Cycle time'da %20 azalma. |
| **Kod Kalitesinde Artış** | Statik analiz araçlarından (ESLint, SonarQube vb.) gelen kritik uyarı sayısını veya kod karmaşıklığı (cyclomatic complexity) skorlarını izleyin. | Kritik uyarı sayısını %30 azaltma. |
| **Hata Oranında Azalma** | CI/CD pipeline'ında başarısız olan build sayısını veya QA sürecinde bulunan bug sayısını takip edin. | Başarısız build oranını %15 düşürme. |
| **Tekrarlayan Görev Otomasyonu**| Haftalık olarak "bunu yine manuel yaptım" dediğiniz görevleri not alın ve ay sonunda kaç tanesini otomatize ettiğinizi (örn: CLI script'i ile) sayın. | Ayda en az 2 manuel görevi otomatize etme. |

---

## 4. Öğrenme ve Optimizasyon: "Sürekli İyileştirme Döngüsü"

Bu strateji statik değildir; yaşayan bir süreç olmalıdır. **İki haftalık kişisel "iyileştirme sprint'leri"** uygulayın.

- **1. Adım: Gözlemle (1 Hafta Boyunca):**
    - Hangi görevlerde en çok zaman harcıyorsunuz?
    - Hangi LLM, hangi tür görevde sizi hayal kırıklığına uğrattı veya şaşırttı?
    - Hangi manuel işlemi en çok tekrarladınız? (örn: log dosyası analizi, yeni bileşen için boilerplate kod yazma)

- **2. Adım: Ayarla ve Otomatize Et (Sprint Sonu):**
    - Gözlemlerinize dayanarak bir CLI script'i yazın.
    - Cursor'daki "prompt library"nize yeni bir prompt ekleyin.
    - Görev ayrıştırma tablonuzda bir değişikliği test etmeye karar verin. (örn: "Bu hafta refactoring için Copilot'u deneyeceğim.")

- **3. Adım: Dene ve Ölç (Sonraki Sprint):**
    - Yaptığınız değişikliğin metriklerinize (örn: bir story'yi tamamlama süreniz) nasıl yansıdığını gözlemleyin.
    - İşe yaradıysa kalıcı hale getirin, yaramadıysa eski sisteme dönün veya yeni bir hipotez geliştirin.

Bu döngü, zamanla size özel, son derece optimize edilmiş ve verimli bir kişisel iş akışı yaratmanızı sağlayacaktır.
