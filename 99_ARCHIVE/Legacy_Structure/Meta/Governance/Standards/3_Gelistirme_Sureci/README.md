# Bölüm 3: Geliştirme Süreci

**Amaç:** Bu modül, YBIS projesinde kod geliştirirken izlenmesi gereken standart iş akışını, branch yönetimini ve kod entegrasyon süreçlerini tanımlar.

---

## 1. Genel Bakış

Geliştirme sürecimiz, `main` branch'ini her zaman stabil ve üretime hazır tutma prensibine dayanır. Tüm geliştirmeler, özellik (feature), hata düzeltme (fix) veya bakım (chore) branch'lerinde yapılır ve yalnızca kalite kontrol kapılarından geçtikten sonra Pull Request (PR) ile `main` branch'ine entegre edilir.

Bu modül aşağıdaki iki ana bölümden oluşur:

- **[Branch Stratejisi](./BRANCH_STRATEGY.md):** Branch oluşturma, isimlendirme kuralları ve commit mesajı standartları gibi konuları detaylandırır.

- **[Pull Request Süreci](./PULL_REQUEST_SURECI.md):** Bir Pull Request'in yaşam döngüsünü, zorunlu CI/CD kontrollerini ve kod gözden geçirme gereksinimlerini açıklar.

---

## 2. Bitti Tanımı (Definition of Done - DoD)

Bir görevin veya özelliğin "bitti" olarak kabul edilebilmesi için aşağıdaki tüm kriterleri karşılaması zorunludur:

- ✅ Kod, `BRANCH_STRATEGY.md`'ye uygun bir branch'te geliştirilmiştir.
- ✅ Kod, `2_Kalite_Ve_Standartlar` dokümanında belirtilen tüm kalite ve stil kurallarına uymaktadır.
- ✅ Yeni eklenen kod için testler yazılmış ve projenin genel test kapsamı (coverage) düşmemiştir.
- ✅ Kod, `PULL_REQUEST_SURECI.md`'de belirtilen tüm otomatik ve manuel kontrollerden geçerek `main` branch'ine başarıyla merge edilmiştir.
- ✅ İlgili branch, merge sonrası silinmiştir.
- ✅ Eğer yapılan değişiklik mevcut dokümantasyonu etkiliyorsa, ilgili dokümanlar güncellenmiştir.
