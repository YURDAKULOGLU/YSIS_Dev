# Pull Request (PR) Süreci

**Sürüm:** 1.0.0
**Durum:** Aktif

---

## 1. Pull Request İş Akışı

1.  **Branch Oluştur:** `BRANCH_STRATEGY.md`'de belirtilen kurallara göre yeni bir branch oluştur.

2.  **Değişiklikleri Yap ve Commit'le:** Geliştirmeyi tamamla ve Conventional Commits standardına uygun commit mesajları ile kaydet.

3.  **Branch'i Yayınla (Push):**
    ```bash
    git push origin feature/my-new-feature
    ```

4.  **Pull Request Oluştur:**
    - GitHub deposuna git.
    - "New Pull Request" butonuna tıkla.
    - Kendi branch'ini seç ve `main` branch'ini hedef al.
    - PR şablonunu (açıklama, test detayları, kontrol listesi) eksiksiz doldur.
    - İlgili kişilerden kod gözden geçirmesi (review) talep et.

5.  **Geri Bildirimleri Adresle:**
    - Gözden geçirme sırasında gelen yorumları ve istenen değişiklikleri yap.
    - Yeni commit'ler ile branch'ini güncelle.

6.  **Birleştir (Merge):**
    - PR, en az bir kişiden onay aldığında ve tüm CI/CD kontrolleri başarıyla geçtiğinde birleştirilebilir.
    - Proje standardı olarak **"Squash and merge"** yöntemi kullanılır. Bu, `main` branch'inin temiz ve okunabilir bir geçmişe sahip olmasını sağlar.
    - Birleştirme sonrası kaynak branch otomatik olarak silinir.

---

## 2. Pull Request Gereksinimleri (ZORUNLU)

Bir PR'ın `main` branch'ine birleştirilebilmesi için aşağıdaki tüm kapılardan (gates) geçmesi zorunludur.

### 2.1. Otomatik Kontroller (CI/CD Pipeline)

- ✅ **Testler:** Tüm testler başarıyla geçmelidir.
- ✅ **Tip Kontrolü (Type-Check):** Sıfır TypeScript hatası olmalıdır.
- ✅ **Lint Kontrolü:** Sıfır ESLint uyarısı veya hatası olmalıdır (Uyarılar hata sayılır).
- ✅ **Test Kapsamı (Coverage):** Kod kapsamı, projenin `YBIS_PROJE_ANAYASASI.md`'de belirlediği minimum oranın (%80) altına düşmemelidir.
- ✅ **Build:** Tüm paketler ve uygulamalar başarıyla build olmalıdır.

### 2.2. Manuel Gözden Geçirme (Code Review)

- ✅ **Onay:** En az bir ekip üyesinden "Approve" alınmalıdır.
- ✅ **Açıklama:** PR açıklaması, yapılan değişikliğin "ne" ve "neden" yapıldığını net bir şekilde açıklamalıdır.
- ✅ **Test Kanıtı:** Yapılan testler (manuel veya otomatik) hakkında bilgi verilmelidir.
- ✅ **Dokümantasyon:** Eğer yapılan değişiklik dokümantasyonu etkiliyorsa, ilgili dokümanların da güncellendiği belirtilmelidir.
- ✅ **Çakışma (Conflict):** `main` branch'i ile herhangi bir merge çakışması olmamalıdır.
