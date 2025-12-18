# Bölüm 1: YBIS Proje Anayasası

---

## 🚨 UYGULAMA BİLDİRİMİ (ENFORCEMENT NOTICE)

```
╔═══════════════════════════════════════════════════════════════╗
║                    SIFIR TOLERANS ANAYASASI                     ║
║                                                               ║
║  Bu anayasadaki HER BİR KURAL ZORUNLUDUR.                      ║
║  İhlal = PR ENGELLENDİ = Kod `main` branch'ine merge edilemez.  ║
║                                                               ║
║  NO EXCEPTIONS. NO "bu sefer geçirelim".                     ║
║  NO "sonra düzeltiriz". ŞİMDİ DÜZELT veya MERGE ETME.          ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 1. Amaç ve Kapsam

Bu anayasa, YBIS projesi için **uyulması zorunlu** temel mimari prensipleri, ürün geliştirme felsefesini ve yönetişim kurallarını tanımlar. Bu doküman, projedeki tüm diğer standartların ve rehberlerin üzerinde yer alır.

---

## 2. Temel Mimari Prensipleri

### 2.1. Port Mimarisi (Port-by-Port Architecture)
- **Kural:** Sadece değiştirilebilir harici bağımlılıklar (external dependencies) için "Port" soyutlaması kullanılır.
- **Kriterler:** Bir bağımlılığın Port arkasına alınması için şu özelliklerden en az birini taşımalıdır: Harici bir servis olması (Supabase, OpenAI), ileride değiştirilme potansiyeli olması, birden fazla alternatifinin bulunması, ağ isteği yapması veya native kod içermesi.
- **Örnekler (Port Kullan):** `DatabasePort` (Supabase → Cloud SQL), `LLMPort` (OpenAI → Anthropic), `AuthPort` (OAuth sağlayıcıları).
- **Örnekler (Port Kullanma):** Dahili uygulama mantığı, framework parçaları (React, Expo Router), tek ve stabil implementasyonlar (Zustand, i18next).

### 2.2. UI İzolasyonu (UI Isolation)
- **Kural:** Tüm UI bileşenleri, `@ybis/ui` paketi üzerinden kullanılmalıdır. Uygulama kodunda (`apps/*`) doğrudan `tamagui` veya başka bir UI kütüphanesinden bileşen import etmek yasaktır.
- **Prensip:** `@ybis/ui` paketi, projenin tasarım sistemi için onaylanmış olan bileşenleri (`Button`, `YStack`, `Text` vb.) tek tek ve açıkça (`explicitly`) export etmelidir. `export * from 'tamagui'` gibi genel ifadeler kullanılamaz.

### 2.3. "Ölçekli İnşa Et, Minimal Başla" (Build for Scale, Ship Minimal)
- **Kural:** Altyapı, gelecekteki genişlemeleri (çoklu tema, çoklu sağlayıcı) destekleyecek şekilde tasarlanmalı, ancak ilk aşamada sadece minimal özellikler (örneğin, açık/koyu tema, tek LLM sağlayıcı) ile başlanmalıdır.
- **Amaç:** Yeni bir özellik (örneğin yeni bir tema veya LLM sağlayıcı) eklemek, çekirdek kodda değişiklik gerektirmemelidir.

### 2.4. "Soyutlamayı Düzelt" (Fix the Abstraction)
- **Kural:** Bir alt seviye teknoloji ile üst seviye bir soyutlama (Port arayüzü gibi) arasında mimari bir uyumsuzluk tespit edildiğinde, sorun ara katmanlar veya geçici çözümler ile "yamalanmamalıdır". Bunun yerine, soyutlamanın kendisi, altta yatan teknolojinin gerçekliğini doğru bir şekilde modelleyecek şekilde yeniden tasarlanmalıdır.
- **Amaç:** Belirtiyi implementasyonda değil, kök nedeni soyutlama katmanında çözmek.

### 2.5. Net Yürütme (Clean Execution) Prensibi
- **Kural:** Projede, aynı işi yapan birden fazla kütüphane, araç veya desenin bir arada bulunması yasaktır. Belirli bir görev için projenin "temeli" olarak kabul edilmiş **tek bir yol** tanımlanmalı ve tüm geliştirmeler bu yolu takip etmelidir.
- **Amaç:** Teknik borcu azaltmak, kafa karışıklığını önlemek ve projenin mimari bütünlüğünü sağlamak.
- **Uygulama:** Eğer projede geçmişten gelen bir ikilik tespit edilirse, bu durumu çözmek öncelikli bir teknik borç görevi olarak ele alınmalıdır.

### 2.6. "Yama Yok, Geçici Çözüm Yok" (No Patch, No Workaround) Prensibi
- **Kural:** Bir sorunun belirtisiyle değil, kök nedeni ile ilgilenilmelidir. Bir kütüphanede hata veya bir soyutlamada kusur bulunduğunda, etrafından dolaşan geçici kodlar yazmak yasaktır. Ya altta yatan sorun çözülmeli (kütüphaneye katkıda bulunarak veya soyutlamayı düzelterek) ya da daha iyi bir araç/soyutlama seçilmelidir.
- **Amaç:** Teknik borcun "çözülmüş" gibi görünmesini engelleyerek, sistemin temelden sağlığını korumak.

---

## 3. Ürün ve Kullanıcı Deneyimi Prensipleri

- **3.1. Veri Odaklı İterasyon:** Kullanıcıların yaptığı her anlamlı etkileşim, kişisel verileri ifşa etmeyecek şekilde analiz edilerek ürün kararlarına yön vermelidir.
- **3.2. "Önce Çevrimdışı" (Offline-First):** Uygulama, internet bağlantısı olmadığında bile temel işlevlerini yerine getirebilmelidir.
- **3.3. "Kullanıcıyı Asla Bekletme" (Optimistic UI):** Zaman alabilecek işlemler (API istekleri vb.) arayüzü kilitlememeli, işlem başarılı olacakmış gibi arayüz anında güncellenmelidir.
- **3.4. "Geri Alınabilir Eylemler" (Reversible Actions):** Kritik ve veri kaybına yol açabilecek eylemler (örn: silme), kullanıcıya kısa bir süre için "Geri Al" imkanı sunmalıdır.
- **3.5. "Düşünceli Kullanıcı Deneyimi" (Thoughtful UX):** Uygulama, her duruma (boş liste, yüklenme, hata) karşı hazırlıklı olmalı ve kullanıcıya net geri bildirimler sunmalıdır.

---

## 4. Yönetişim ve Evrim

### 4.1. Standartların Evrimi
- **Prensip:** Bu anayasa ve bağlı standartlar, yaşayan dokümanlardır. Proje geliştikçe ve yeni dersler öğrenildikçe güncellenmelidirler.
- **Süreç:** Değişiklikler, yinelemeli (iterative) ve geri bildirime dayalı bir süreçle yapılır. Bir standartta değişiklik önerisi, bir görev olarak ele alınır, tartışılır ve onaylandıktan sonra dokümana işlenir. Bu süreç, projenin meta-analiz desenlerinden biridir ve sistemin kendi kendini iyileştirmesini sağlar.

---

## 5. Kalite ve Sürdürülebilirlik Prensipleri

### 5.1. Performans Bütçeleri Prensibi
- **Prensip:** Proje, kullanıcı deneyimini doğrudan etkileyen performans metrikleri (bundle boyutu, yeniden çizim oranları vb.) için tanımlanmış bütçelere uymalıdır.
- **Detaylar:** Bu bütçeler, uygulama fazları ve teknik detaylar `2_Kalite_Ve_Standartlar` dokümanında belirtilmiştir.

### 5.2. Veri Bütünlüğü Prensibi
- **Prensip:** Uygulama, harici kaynaklardan (API'lar vb.) gelen verilerin bütünlüğünü ve doğruluğunu, sisteme dahil edilmeden önce garanti altına almalıdır.
- **Detaylar:** Veri doğrulama stratejisi ve uygulama fazı `2_Kalite_Ve_Standartlar` dokümanında belirtilmiştir.

### 5.3. Test Kalitesi Prensibi
- **Prensip:** Proje, kod kalitesini ve stabilitesini sağlamak için tanımlanmış, ölçülebilir test kapsamı hedeflerine uymalıdır.
- **Detaylar:** Test kapsamı hedefleri, türleri ve uygulama fazı `4_Test_Stratejisi` dokümanında belirtilmiştir.

### 5.4. İzci Kuralı (The Boy Scout Rule)
- **Prensip:** Bir kod dosyasını, bulduğunuzdan daha temiz bırakın. Bir dosyada çalışırken, kodun okunabilirliğini artıran küçük bir iyileştirme (değişken adını netleştirme, yorum ekleme, küçük bir kod tekrarını düzeltme) yapmak teşvik edilir.
- **Amaç:** Projenin kalitesini zamanla, sürekli ve organik olarak artırmak.

### 5.5. En Az Şaşırtma Prensibi (Principle of Least Astonishment - POLA)
- **Prensip:** Kod, bir geliştiricinin beklediği gibi davranmalıdır. Fonksiyonlar ve bileşenler, isimlerinin ima ettiği işi yapmalı ve sürpriz yan etkilerden kaçınmalıdır.
- **Amaç:** Kodun öngörülebilirliğini ve okunabilirliğini artırarak, hata yapma olasılığını azaltmak.

### 5.6. Kendini Tekrar Etme (Don't Repeat Yourself - DRY) Prensibi
- **Prensip:** Bir bilginin veya mantığın her bir parçası, sistem içinde tek, kesin ve yetkili bir temsile sahip olmalıdır. Kod tekrarından kaçınılmalı, ortak mantık yeniden kullanılabilir fonksiyonlara, bileşenlere veya modüllere soyutlanmalıdır.
- **Amaç:** Bakımı kolaylaştırmak ve bir mantık değiştiğinde birden çok yeri güncelleme ihtiyacını ortadan kaldırmak.

### 5.7. "Ona İhtiyacın Olmayacak" (You Ain't Gonna Need It - YAGNI) Prensibi
- **Prensip:** Gerçekten ihtiyaç duyulana kadar bir işlevsellik eklenmemelidir. Gelecekte "belki gerekir" düşüncesiyle kod yazmaktan kaçınılmalıdır.
- **Amaç:** Projeyi gereksiz karmaşıklıktan korumak ve mevcut ihtiyaçlara odaklanmak.
