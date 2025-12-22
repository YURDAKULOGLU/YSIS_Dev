# YBIS Branch Stratejisi

**Sürüm:** 2.0.0
**Durum:** Aktif

---

## 1. Ana Branch'ler

- **`main`**: Her zaman canlıya çıkmaya hazır, stabil ve test edilmiş kodu içerir.
  - Bu branch'e doğrudan commit atmak yasaktır.
  - Tüm değişiklikler Pull Request (PR) ile ve onay alındıktan sonra merge edilir.

---

## 2. Geliştirme Branch'leri

### 2.1. Branch İsimlendirme Kuralı

Tüm branch'ler aşağıdaki formatta isimlendirilmelidir:

```
<tip>/<kısa-açıklama>
```

- **`feature/`**: Yeni bir özellik geliştirilirken kullanılır.
  - *Örnek:* `feature/calendar-integration`

- **`fix/`**: Bir hatayı düzeltirken kullanılır.
  - *Örnek:* `fix/keyboard-animation-glitch`

- **`chore/`**: Bakım, bağımlılık güncelleme, konfigürasyon gibi görevler için kullanılır.
  - *Örnek:* `chore/update-expo-sdk`

- **`docs/`**: Sadece dokümantasyon güncellemeleri için kullanılır.
  - *Örnek:* `docs/add-testing-strategy`

- **`refactor/`**: Davranışı değiştirmeyen kod yeniden yapılandırmaları için kullanılır.
  - *Örnek:* `refactor/extract-auth-port`

### 2.2. Branch Yaşam Döngüsü

1.  **Oluştur:** Her zaman `main` branch'inden yeni bir branch oluşturulur.
    ```bash
    git checkout main
    git pull origin main
    git checkout -b feature/my-new-feature
    ```
2.  **Geliştir:** Değişiklikler yapılır ve anlamlı commit mesajları ile kaydedilir.
3.  **Yayınla (Push):** Branch, uzak sunucuya push edilir.
4.  **Pull Request (PR):** GitHub üzerinden `main` branch'ine bir PR açılır.
5.  **Gözden Geçir ve Onayla:** PR, kod gözden geçirmesinden ve otomatik CI kontrollerinden geçer.
6.  **Birleştir (Merge):** Onaylanan PR, "Squash and merge" yöntemiyle `main` branch'ine birleştirilir.
7.  **Sil:** Birleştirilen branch, otomatik olarak silinir.

---

## 3. Commit Mesajı Standardı

Proje, [Conventional Commits](https://www.conventionalcommits.org/) standardını takip eder.

```
<tip>: <açıklama>
```

- **`feat`**: Yeni bir özellik.
- **`fix`**: Bir hata düzeltmesi.
- **`chore`**: Bakım veya araçlarla ilgili değişiklikler.
- **`docs`**: Dokümantasyon değişiklikleri.
- **`refactor`**: Kodun yeniden yapılandırılması.
- **`test`**: Test ekleme veya düzeltme.
- **`ci`**: CI/CD pipeline değişiklikleri.

**Örnek:**
`feat: Add user authentication with OAuth`
`fix: Resolve tab bar overflow on mobile`
