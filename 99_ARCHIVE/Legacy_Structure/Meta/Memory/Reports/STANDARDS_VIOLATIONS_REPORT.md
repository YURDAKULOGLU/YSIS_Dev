# YBIS Standartları İhlal Raporu

**Tarih:** 2025-01-XX  
**Durum:** 🔴 Kritik İhlaller Tespit Edildi

---

## 🚨 KRİTİK İHLALLER (PR Engelleme Sebebi)

### 1. **UI İzolasyonu İhlali** ❌

**Kural:** `apps/*` içinde `tamagui` doğrudan import edilemez, `@ybis/ui` kullanılmalı.

**İhlaller:**
- `apps/mobile/app/_layout.tsx:9` - `import config from '../tamagui.config'`
  - **Çözüm:** Config'i `@ybis/ui` paketine taşı veya `@ybis/theme` üzerinden eriş

**Test Dosyaları (Kabul Edilebilir):**
- `apps/mobile/app/(auth)/__tests__/login.test.tsx` - Test dosyası, kabul edilebilir
- `apps/mobile/app/(auth)/__tests__/signup.test.tsx` - Test dosyası, kabul edilebilir

---

### 2. **Vendor SDK Doğrudan İmport İhlali** ❌

**Kural:** `apps/*` içinde vendor SDK'lar (`@supabase/supabase-js`, `expo-auth-session`) doğrudan import edilemez, Port mimarisi kullanılmalı.

**İhlaller:**

#### Backend:
- `apps/backend/src/middleware/auth.ts:2` - `import { createClient } from '@supabase/supabase-js'`
  - **Sorun:** Auth middleware'de Supabase client doğrudan oluşturuluyor
  - **Çözüm:** `DatabasePort` veya `AuthPort` üzerinden JWT doğrulama yapılmalı
  - **Etki:** Port mimarisi prensibi ihlal ediliyor

#### Mobile:
- `apps/mobile/src/contexts/useAuth.ts:11` - `import * as AuthSession from 'expo-auth-session'`
  - **Sorun:** OAuth callback işlemleri için doğrudan expo-auth-session kullanılıyor
  - **Çözüm:** `@ybis/auth` paketindeki adapter'ı kullanmalı veya adapter'a bu özellik eklenmeli

**Kabul Edilebilir:**
- `apps/backend/src/middleware/ports.ts:11` - Type import (`import type { User }`), kabul edilebilir

---

### 3. **TypeScript Strict Mod Eksikliği** ⚠️

**Kural:** Backend'de TypeScript strict mod aktif olmalı (Faz 2 hedefi, şu an teknik borç).

**İhlal:**
- `apps/backend/tsconfig.json` - `strict: true` yok
  - **Durum:** Base config'de var ama backend extend ederken override edilmemiş
  - **Etki:** Type safety zayıf, `any` kullanımı kontrol edilmiyor
  - **Öncelik:** Yüksek (Faz 2'de zorunlu)

**Mevcut Durum:**
- ✅ `tsconfig.base.json` - `strict: true` var
- ✅ `apps/mobile/tsconfig.json` - `strict: true` var
- ❌ `apps/backend/tsconfig.json` - `strict` belirtilmemiş (base'den inherit ediyor ama explicit değil)

---

## ⚠️ ORTA SEVİYE İHLALLER

### 4. **Package Dokümantasyon Eksikliği** ⚠️

**Kural:** Her `packages/*` paketinin kök dizininde `README.md` olmalı.

**Eksik README'ler:**
- ❌ `packages/auth/README.md` - Yok
- ❌ `packages/chat/README.md` - Yok
- ❌ `packages/core/README.md` - Yok
- ❌ `packages/i18n/README.md` - Yok
- ❌ `packages/llm/README.md` - Yok
- ❌ `packages/logging/README.md` - Yok
- ❌ `packages/storage/README.md` - Yok
- ❌ `packages/theme/README.md` - Yok
- ❌ `packages/ui/README.md` - Yok
- ❌ `packages/utils/README.md` - Yok
- ✅ `packages/database/src/__tests__/README.md` - Var (ama yanlış yerde)

**Etki:** Yeni geliştiriciler paketlerin amacını ve API'sini anlamakta zorlanıyor.

---

## ✅ KABUL EDİLEBİLİR DURUMLAR

### Console.log Kullanımı
- `apps/mobile/src/logging/*` - Logging sink'lerde `console.warn` kullanımı **intentional**
  - **Sebep:** Infinite recursion önlemek için (Logger kendisini loglamamalı)
  - **Durum:** ✅ Standartlara uygun (yorumlarda açıklanmış)

### UI Paketi Export Stratejisi
- `packages/ui/src/index.ts` - Explicit export kullanılıyor (✅ Standartlara uygun)
  - `export * from` kullanılmıyor, her component açıkça export ediliyor

---

## 📊 ÖZET

| Kategori | İhlal Sayısı | Kritik | Orta | Düşük |
|----------|--------------|--------|------|-------|
| UI İzolasyonu | 1 | 1 | 0 | 0 |
| Vendor SDK | 2 | 2 | 0 | 0 |
| TypeScript | 1 | 0 | 1 | 0 |
| Dokümantasyon | 10 | 0 | 10 | 0 |
| **TOPLAM** | **14** | **3** | **11** | **0** |

---

## 🎯 ÖNCELİKLENDİRME

### P0 (Hemen Düzelt - PR Engelleme)
1. ✅ Backend `auth.ts` - Supabase doğrudan import → Port kullan
2. ✅ Mobile `useAuth.ts` - expo-auth-session doğrudan import → Adapter kullan
3. ✅ Mobile `_layout.tsx` - tamagui.config doğrudan import → @ybis/ui kullan

### P1 (Faz 2'de Zorunlu)
4. ⚠️ Backend TypeScript strict mod aktif et

### P2 (İyileştirme)
5. 📝 Tüm packages için README.md ekle

---

## 🔧 DÜZELTME ÖNERİLERİ

### 1. Backend Auth Middleware Düzeltmesi

```typescript
// ❌ ŞU AN:
import { createClient } from '@supabase/supabase-js';
const supabase = createClient(supabaseUrl, supabaseAnonKey);

// ✅ OLMALI:
import { PortRegistry } from '../services/PortRegistry';
const db = PortRegistry.getInstance().database;
// JWT doğrulama DatabasePort veya AuthPort üzerinden yapılmalı
```

### 2. Mobile Auth Context Düzeltmesi

```typescript
// ❌ ŞU AN:
import * as AuthSession from 'expo-auth-session';

// ✅ OLMALI:
// SupabaseAuthAdapter içinde OAuth callback işlemleri olmalı
// veya yeni bir OAuth adapter method eklenmeli
```

### 3. Mobile Layout Düzeltmesi

```typescript
// ❌ ŞU AN:
import config from '../tamagui.config';

// ✅ OLMALI:
// Config'i @ybis/ui veya @ybis/theme paketine taşı
import { tamaguiConfig } from '@ybis/ui';
```

---

**Son Güncelleme:** 2025-01-XX  
**Kontrol Eden:** AI Assistant  
**Durum:** ✅ Kritik İhlaller Düzeltildi (P0 Tamamlandı)

---

## ✅ DÜZELTME DURUMU

### Tamamlanan Düzeltmeler (2025-01-XX)

1. ✅ **Backend Auth Middleware** - `@supabase/supabase-js` → `@ybis/auth` utility kullanılıyor
2. ✅ **Mobile useAuth** - `expo-auth-session` → `@ybis/auth` utilities kullanılıyor  
3. ✅ **Mobile _layout** - `tamagui.config` → `@ybis/ui` kullanılıyor
4. ✅ **Backend TypeScript** - `strict: true` eklendi

**Implementation Report:** `.YBIS_Dev/ysis_agentic/agents/coding/T-061_Standards_Violations_Fix_Report.md`

### Kalan İşler (P2 - İyileştirme)

- 📝 Package README'leri (10 paket) - Ayrı task olarak planlanabilir

