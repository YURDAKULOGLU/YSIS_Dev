# YBIS Çekirdek Mimari Prensipleri

**Amaç:** Bu doküman, YBIS projesinin "Scalable but Ship Minimal" (Ölçeklenebilir İnşa Et, Minimal Başla) felsefesini destekleyen, tüm AI asistanları tarafından okunması zorunlu olan temel ve kalıcı mimari prensipleri tanımlar.

---

## 1. Port Mimarisi (Teknoloji Bağımsızlığı)
- **Prensip:** Projenin dış dünya ile olan tüm iletişimleri (veritabanı, harici API'ler, kimlik doğrulama, LLM sağlayıcıları) soyut "Port" arayüzleri üzerinden yapılır.
- **Minimal Gönderim:** İlk aşamada her port için tek bir "Adaptör" (örn: `SupabaseAdapter`, `OpenAIAdapter`) kullanılır.
- **Ölçeklenebilirlik:** Gelecekte, maliyet veya performans nedenleriyle teknoloji sağlayıcısını (örn: Supabase -> kendi PostgreSQL sunucumuz) değiştirmek istediğimizde, sadece yeni bir adaptör yazılır. Uygulamanın çekirdek mantığı asla değişmez. Bu, vendor lock-in riskini sıfırlar.

## 2. Plugin Sistemi (Modüler Özellik Geliştirme)
- **Prensip:** Yeni özellikler (dikeyler), projenin çekirdeğine dokunmadan, kendi kendine yeten birer "plugin" olarak eklenebilecek bir altyapı üzerine kurulur.
- **Minimal Gönderim:** Sadece temel verimlilik özellikleri (Görev, Not, Takvim) geliştirilir.
- **Ölçeklenebilirlik:** Gelecekte "Finans", "Sağlık" veya "Öğrenci" gibi tamamen farklı dikeyler, mevcut sistemi bozmadan, yeni birer eklenti olarak sisteme dahil edilebilir.

## 3. Evrensel Arayüz Bileşenleri (Platformlar Arası Genişleme)
- **Prensip:** Tüm arayüz bileşenleri, hem mobil hem de web platformlarında çalışabilecek şekilde evrensel bir yapıda (`@ybis/ui` paketi altında) tasarlanır.
- **Minimal Gönderim:** Proje sadece mobil uygulama olarak başlar.
- **Ölçeklenebilirlik:** Open Beta veya sonraki bir fazda bir "Web Dashboard" oluşturulmak istendiğinde, mevcut bileşenler yeniden kullanılarak geliştirme süreci haftalarca kısaltılır.

## 4. Birleşik Veri Modeli (Federated Data Model)
- **Prensip:** Port mimarisi, sadece teknoloji değiştirmek için değil, aynı zamanda birden fazla veri kaynağını tek bir arayüz altında birleştirmek için de kullanılır.
- **Minimal Gönderim:** Uygulama sadece kendi veritabanı (`Supabase`) ile konuşur.
- **Ölçeklenebilirlik:** Gelecekte, kullanıcının mevcut araçlarındaki (örn: Notion, Google Keep) verilerine de erişim sağlanabilir. AI, "tüm notlarımı ara" komutuyla hem YBIS veritabanını hem de kullanıcının Notion hesabını aynı anda arayabilir. Bu, YBIS'i gerçek bir "orkestratör" yapar.

## 5. "Workspace" Odaklı Veri Şeması (Çok Kullanıcılı Gelecek)
- **Prensip:** Veritabanı şeması, en başından itibaren tüm tabloları bir `workspace_id` (çalışma alanı kimliği) ile ilişkilendirerek tasarlanır.
- **Minimal Gönderim:** Her kullanıcı, kendisine ait tek bir "çalışma alanı" içinde çalışır. Sistem tek kişilik gibi davranır.
- **Ölçeklenebilirlik:** Gelecekte "Takım" veya "Aile" özellikleri eklenmek istendiğinde, büyük bir veri migrasyonuna gerek kalmaz. Birden fazla kullanıcıyı aynı `workspace_id` altında birleştirmek ve erişim kurallarını güncellemek yeterli olur.

## 6. Akıllı AI Model Yönlendirme (Maliyet/Performans Optimizasyonu)
- **Prensip:** `LLMPort`, arkasında gelen isteğin türüne göre en uygun AI modelini seçen bir yönlendirici (router) gibi davranır.
- **Minimal Gönderim:** Tüm istekler tek ve genel amaçlı bir modele (örn: GPT-4o-mini) gider.
- **Ölçeklenebilirlik:** Basit sınıflandırma işlemleri için çok ucuz veya lokal bir model, karmaşık analizler için en güçlü model, özetleme için bu konuda uzmanlaşmış bir model otomatik olarak seçilir. Bu, AI maliyetlerini optimize ederken her görev için en iyi sonucu almayı sağlar.

## 7. AppActionPort (AI Kontrolünde Arayüz)
- **Prensip:** AI, sadece veriyi değil, uygulamanın kendisini de yönetebilmelidir.
- **Minimal Gönderim:** AI, temel olarak sohbet ve veri işlemleri yapar.
- **Ölçeklenebilirlik:** `AppActionPort` adında bir port üzerinden AI'a, arayüzü doğrudan kontrol etme yetkisi verilir. Kullanıcı "karanlık moda geç" dediğinde AI, `AppActionPort.setTheme('dark')` komutunu çalıştırır. "Beni görevlerime götür" dediğinde `AppActionPort.navigate('/tasks')` komutunu tetikler. Bu, AI'ı uygulamanın içinde bir yardımcıdan, uygulamanın operatörüne dönüştürür.
