# Bölüm 2: Kalite ve Standartlar

**Amaç:** Bu doküman, YBIS projesindeki kodun tutarlı, okunabilir, sürdürülebilir ve yüksek kalitede olmasını sağlamak için uyulması zorunlu olan teknik standartları tanımlar.

---

## 1. Kod Kalitesi Standartları

### 1.1. TypeScript Strict Modu

- **Hedef:** TypeScript `strict` modunun aktif olması hedeflenmektedir.
- **Mevcut Durum:** Bu kural şu anda `tsconfig.json`'da aktif değildir ve Faz 2'de ele alınması gereken en öncelikli teknik borçtur.
- **Yasaklar (Strict Mod Aktif Olduğunda):**
    - `any` türü kullanmak kesinlikle yasaktır. Bunun yerine `unknown` ve tür koruyucuları (type guards) kullanılmalıdır.
    - `@ts-ignore` veya `@ts-expect-error` yorumları yasaktır. Kök neden çözülmelidir.
- **İstisna (`skipLibCheck`):** `tsconfig.json` dosyasında `skipLibCheck: true` ayarının kullanılması, React Native ve üçüncü parti kütüphanelerin (örn: Tamagui) neden olduğu tip çakışmalarını önlemek için zorunludur ve bir istisnadır.
- **Zorunluluklar (Strict Mod Aktif Olduğunda):**
    - Tüm fonksiyonlar için dönüş tipleri açıkça belirtilmelidir (`explicit return types`).
    - `type` importları kullanılmalıdır: `import type { Foo } from 'bar'`.

### 1.2. ESLint Kuralları

- **Kural:** `.eslintrc.js` dosyasındaki tüm kurallara uyulması zorunludur.
- **Sıfır Uyarı Politikası:** CI/CD sürecinde uyarılar (warnings) hata olarak kabul edilir. Hiçbir uyarı içeren kod `main` branch'ine merge edilemez.
- **Önemli Kurallar:**
    - `no-console`: `console.log()` yerine projenin kendi `Logger` portu kullanılmalıdır. Uyarılara ve hatalara (`warn`, `error`) izin verilir.
    - `no-debugger`: Kodda `debugger` ifadesi bırakılamaz.
    - `prefer-const`: Değeri yeniden atanmayan değişkenler için `const` kullanılmalıdır.

### 1.3. Kod Formatlama (Prettier)

- **Kural:** Projedeki tüm dosyalar, `.prettierrc` dosyasında tanımlanan kurallara göre formatlanmalıdır.
- **Otomasyon:** Bu kural, VS Code'da "Format on Save" ayarı ve pre-commit hook'ları ile otomatik olarak uygulanır.

---

## 2. İsimlendirme ve Dosya Yapısı

### 2.1. İsimlendirme Kuralları

| Tür | Kural | Örnek |
|---|---|---|
| **Componentler** | `PascalCase` | `TaskList`, `ChatContainer` |
| **Hook'lar** | `camelCase`, `use` ön-eki | `useAuth`, `useTasks` |
| **Tipler/Arayüzler** | `PascalCase` | `Task`, `User`, `AuthPort` |
| **Fonksiyonlar/Değişkenler** | `camelCase` | `createTask`, `currentUser` |
| **Sabitler (Constants)** | `UPPER_SNAKE_CASE` | `API_URL`, `MAX_RETRIES` |
| **Dosyalar (Component)** | `PascalCase.tsx` | `TaskList.tsx` |
| **Dosyalar (Diğer)** | `kebab-case.ts` | `validation-schemas.ts` |
| **Klasörler** | `kebab-case` | `task-management`, `auth-service` |

### 2.2. Dosya Organizasyonu (Componentler)

- **Kural:** Component'e ait `props` arayüzü, stiller ve diğer mantıksal birimler aynı dosyada (co-location) bulunmalıdır.

```tsx
// TaskItem.tsx

// 1. Importlar
import React from 'react';
import { Text, YStack } from '@ybis/ui';
import type { Task } from '@ybis/core';

// 2. Props Arayüzü
interface TaskItemProps {
  task: Task;
}

// 3. Component Tanımı
export const TaskItem: React.FC<TaskItemProps> = ({ task }) => {
  return (
    <YStack>
      <Text>{task.title}</Text>
    </YStack>
  );
};

// 4. Stiller (isteğe bağlı)
// const styles = ...
```

### 2.3. Paket Dokümantasyonu (Package Documentation)

- **Kural:** `packages/` altındaki her bir paket, kendi kök dizininde amacını, public API'ını ve temel kullanımını açıklayan bir `README.md` dosyası içermek zorundadır.
- **Amaç:** Her paketin kendi kendini dokümante etmesini sağlamak, kodun anlaşılabilirliğini artırmak ve yeni geliştiricilerin sisteme adaptasyonunu hızlandırmak.

---

## 3. Yasaklanmış Desenler (Zero-Tolerance)

Bu desenlerin kullanımı, projenin sağlığını doğrudan tehdit ettiği için kesinlikle yasaktır ve PR'ların engellenme sebebidir.

- **Paket Yönetimi:**
    - `npm install --force`
    - `npm install --legacy-peer-deps`

- **Kod İçinde:**
    - `@ts-ignore` veya `any` kullanımı.
    - Tamagui gibi kütüphanelerde `bg="$blue5"` gibi kısa kod (shorthand) kullanımı. Her zaman tam ismi (`backgroundColor`) kullanılmalıdır. Bu, TypeScript uyumluluğu için zorunludur.
    - Uygulama kodunda (`apps/*`) `tamagui`, `expo-auth-session`, `@supabase/supabase-js` gibi kütüphanelerin doğrudan import edilmesi. Her zaman projenin kendi soyutlama portları (`@ybis/ui`, `@ybis/auth`, `@ybis/database`) kullanılmalıdır.

---

## 4. İleri Seviye Kalite Kapıları (Gelecek Fazlar)

Aşağıdaki kurallar, projenin uzun vadeli kalitesini garanti altına almak için tasarlanmıştır. Uygulamaları, Kapalı Beta fazından sonra, belirtilen fazlarda zorunlu hale gelecektir.

### 4.1. Performans Bütçeleri
- **Kural:** Mobil uygulamanın production "bundle" boyutu, belirlenen bir tavanı (`10 MB`) aşamaz.
- **Gerekçe:** Büyük bundle boyutları, uygulamanın yavaş açılmasına ve kötü bir kullanıcı deneyimine yol açar.
- **Uygulama Fazı:** **Açık Beta / MVP.**

### 4.2. API Güvenliği ve Veri Doğrulama
- **Kural:** Uygulama katmanları, backend'den gelen veriyi asla "olduğu gibi" kabul edemez. Gelen her veri, **Zod** gibi bir şema doğrulama kütüphanesi kullanılarak doğrulanmalıdır.
- **Gerekçe:** Bu, backend kaynaklı beklenmedik hataların ve çökmelerin önüne geçerek uygulamayı dayanıklı hale getirir.
- **Uygulama Fazı:** **Açık Beta / MVP.**
