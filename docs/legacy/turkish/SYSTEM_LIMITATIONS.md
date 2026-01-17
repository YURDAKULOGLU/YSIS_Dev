# Sistem Sınırlamaları

**Date:** 2026-01-09  
**Purpose:** Cursor AI model sınırlamaları ve bunların iş akışına etkileri

## Kritik Sınırlamalar

### 1. **Terminal Çıktılarını Görememe** ⚠️ KRİTİK

**Sınırlama:**
- AI model terminal komutlarını çalıştırabilir (`run_terminal_cmd`)
- Ancak komut çıktılarını (stdout/stderr) göremez
- Sadece exit code bilgisi alınır (0 = başarılı, diğer = hata)

**Etki:**
- Komut başarısız olsa bile model bunu göremez
- Hata mesajları görmezden gelinir
- "Başarılı" varsayımı yapılır, verification yapılamaz

**Örnek Senaryo:**
```powershell
Move-Item -Path "config" -Destination "legacy\config" -Force
# Exit code: 0 (başarılı görünüyor)
# Ama gerçekte: "Cannot find path" hatası olabilir
# Model bunu göremez → "Moved" raporu yazılır
```

**Çözüm Stratejisi:**
1. **Verification-First Approach:**
   - Her komuttan sonra `Test-Path` ile doğrulama yapılmalı
   - Komut çıktısı yerine dosya sistem durumu kontrol edilmeli

2. **Script-Based Operations:**
   - Kritik işlemler için verification script'i yazılmalı
   - Script hem işlemi yapsın hem doğrulasın

3. **Explicit Error Handling:**
   - `-ErrorAction Stop` kullanılmalı
   - Hata durumunda script exit code döndürmeli

**Örnek Doğru Yaklaşım:**
```powershell
# ❌ YANLIŞ (model terminal çıktısını göremez)
Move-Item -Path "config" -Destination "legacy\config" -Force
Write-Host "config/ moved successfully"

# ✅ DOĞRU (verification yapılıyor)
Move-Item -Path "config" -Destination "legacy\config" -Force -ErrorAction Stop
if (Test-Path "config") {
    throw "VERIFICATION FAILED: config/ still exists"
}
if (-not (Test-Path "legacy\config")) {
    throw "VERIFICATION FAILED: legacy\config not created"
}
Write-Host "✅ config/ moved and verified"
```

---

### 2. **Asenkron İşlem Durumunu Görememe**

**Sınırlama:**
- Background işlemler başlatılabilir (`is_background: true`)
- Ancak işlem durumu (çalışıyor mu, bitti mi, hata verdi mi) görülemez

**Etki:**
- Background işlemlerin başarısı doğrulanamaz
- Hata durumları tespit edilemez

**Çözüm:**
- Background işlemler yerine senkron işlemler tercih edilmeli
- Veya işlem sonucu dosya sisteminde bir işaret bırakılmalı (flag file)

---

### 3. **Dosya İçeriği Değişikliklerini Gerçek Zamanlı Görememe**

**Sınırlama:**
- Dosya okunabilir (`read_file`)
- Ancak dosya içeriği değiştiğinde otomatik güncellenmez
- Her okuma için explicit `read_file` çağrısı gerekir

**Etki:**
- Dosya değişiklikleri tespit edilemez
- Cache'lenmiş eski içerik kullanılabilir

**Çözüm:**
- Kritik dosyalar her kullanımda yeniden okunmalı
- Dosya hash'leri karşılaştırılabilir (eğer metadata mevcut)

---

### 4. **Git Durumunu Tam Görememe**

**Sınırlama:**
- Git komutları çalıştırılabilir
- Ancak `git status`, `git diff` çıktıları görülemez
- Sadece exit code bilgisi alınır

**Etki:**
- Dirty repo durumu tespit edilemez
- Commit öncesi değişiklikler görülemez

**Çözüm:**
- Git durumu için explicit verification script'i kullanılmalı
- Örnek: `git status --porcelain` çıktısı bir dosyaya yazılabilir, sonra okunabilir

---

## İş Akışı Etkileri

### Verification-First Principle

**Kural:** Her kritik işlemden sonra verification zorunlu.

**Neden:** Terminal çıktılarını göremediğimiz için, işlem başarısını dosya sistem durumundan doğrulamalıyız.

**Uygulama:**
1. İşlem yap (Move-Item, Copy-Item, etc.)
2. Verification yap (Test-Path, Get-ChildItem, etc.)
3. Rapor yaz (sadece verification başarılıysa)

### Script-Based Critical Operations

**Kural:** Kritik işlemler için verification script'i yazılmalı.

**Neden:** Model terminal çıktısını göremediği için, script hem işlemi yapmalı hem doğrulamalı.

**Örnek:**
```python
# scripts/verify_move.py
import sys
from pathlib import Path

source = Path(sys.argv[1])
dest = Path(sys.argv[2])

# Move operation
# ... (move logic)

# Verification
if source.exists():
    print(f"ERROR: {source} still exists")
    sys.exit(1)
if not dest.exists():
    print(f"ERROR: {dest} not created")
    sys.exit(1)

print(f"SUCCESS: {source} moved to {dest}")
sys.exit(0)
```

---

## Sistem Dokümantasyonu Gereksinimleri

### 1. **Her Kritik İşlem İçin Verification Adımı**

Dokümantasyonda belirtilmeli:
- Hangi işlemler kritik?
- Verification nasıl yapılır?
- Hata durumunda ne yapılır?

### 2. **Script Template'leri**

Verification içeren script template'leri sağlanmalı:
- `scripts/templates/verify_move.ps1`
- `scripts/templates/verify_copy.ps1`
- `scripts/templates/verify_delete.ps1`

### 3. **Error Handling Standartları**

- `-ErrorAction Stop` zorunlu mu?
- Exit code'lar nasıl yorumlanmalı?
- Hata mesajları nereye yazılmalı?

---

## Önerilen İyileştirmeler

### 1. **Verification Helper Functions**

```powershell
function Move-AndVerify {
    param(
        [string]$Source,
        [string]$Destination
    )
    Move-Item -Path $Source -Destination $Destination -Force -ErrorAction Stop
    if (Test-Path $Source) {
        throw "VERIFICATION FAILED: $Source still exists"
    }
    if (-not (Test-Path $Destination)) {
        throw "VERIFICATION FAILED: $Destination not created"
    }
    Write-Host "✅ $Source moved to $Destination"
}
```

### 2. **Verification Script Generator**

Model, kritik işlemler için otomatik verification script'i oluşturabilir.

### 3. **Status File Pattern**

Background işlemler için status file kullanılabilir:
```powershell
# İşlem başlat
Start-Process -FilePath "script.ps1" -ArgumentList @("--status-file", "status.json")

# Status kontrol
$status = Get-Content "status.json" | ConvertFrom-Json
if ($status.status -eq "failed") {
    throw "Operation failed: $($status.error)"
}
```

---

## Sonuç

**Ana Sınırlama:** Terminal çıktılarını görememe → Verification eksikliği

**Çözüm:** Verification-First Principle + Script-Based Operations

**Disiplin Kuralı:** "Moved" demek için gerçekten taşınmış olmalı. Verification olmadan rapor yazılmamalı.

**Not:** Bu sınırlamalar Cursor AI model'in teknik kısıtlamalarıdır. İş akışı bu sınırlamalara göre tasarlanmalıdır.

