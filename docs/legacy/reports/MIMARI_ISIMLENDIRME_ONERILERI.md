# 🏗️ Mimari İsimlendirme ve Dosya Yolu Önerileri

**Soru:** `src/agentic/core/syscalls/` çok derin, neden `agentic` içinde?  
**Cevap:** Haklısın. İşte pratik alternatifler ve karşılaştırma.

---

## 🎯 HANGİ YAPININ NERESİ GÜZEL?

### ✅ Yeni Yapının Güzel Yanları

1. **Minimal Core Felsefesi**
   - Core = sadece enforcement + coordination
   - Vendor/adapters ayrımı net
   - "OS-first" yaklaşım

2. **Deterministic Gates**
   - Policy snapshot + evidence = karar
   - Golden test'lerle garantili
   - Gate report JSON (audit için mükemmel)

3. **Evidence-First**
   - DB source of truth değil, artifacts
   - Immutable runs
   - Migration discipline (schema_version)

4. **Syscall Pattern**
   - Tek enforcement point
   - Journal events otomatik
   - Protected paths kontrolü

### ✅ Mevcut Yapının Güzel Yanları

1. **Çalışıyor ve Test Edilmiş**
   - ACI pratik çözüm
   - Sentinel çalışıyor
   - Workspace layout basit

2. **Pragmatik Yaklaşım**
   - "Organ-first" = hızlı iterasyon
   - Aider direkt entegre
   - Markdown artifacts (okunabilir)

3. **Mevcut Ekosistem**
   - MCP server çalışıyor
   - Dashboard var
   - SQLite task management stabil

---

## 📁 İSİMLENDİRME ALTERNATİFLERİ

### Seçenek 1: `platform` (Önerilen Yapı)

```
src/platform/
  contracts/
  syscalls/
  control_plane/
  data_plane/
  orchestrator/
  adapters/
  services/
```

**Artıları:**
- ✅ "Platform" = OS benzeri, net
- ✅ Generic değil, spesifik
- ✅ 3 seviye derinlik (iyi)

**Eksileri:**
- ⚠️ Python'da `platform` modülü var (çakışma riski)
- ⚠️ Mevcut `src/agentic/` ile uyumsuz

**Import:**
```python
from src.platform.syscalls import fs
from src.platform.contracts import Task
```

### Seçenek 2: `ybis` (Proje-Spesifik)

```
src/ybis/
  contracts/
  syscalls/
  control_plane/
  data_plane/
  orchestrator/
  adapters/
  services/
```

**Artıları:**
- ✅ Proje-spesifik, çakışma yok
- ✅ 3 seviye derinlik (iyi)
- ✅ Kısa ve net

**Eksileri:**
- ⚠️ Proje adına bağlı (generic değil)

**Import:**
```python
from src.ybis.syscalls import fs
from src.ybis.contracts import Task
```

### Seçenek 3: `agentic` (Mevcut - Optimize Edilmiş)

```
src/agentic/
  contracts/        # core/protocols.py → contracts/
  syscalls/         # YENİ (core/execution/aci.py → syscalls/)
  control_plane/    # infrastructure/db.py → control_plane/
  data_plane/       # YENİ (workspace management)
  orchestrator/     # core/graphs/ → orchestrator/
  adapters/         # bridges/ → adapters/
  services/         # mcp_server.py → services/
```

**Artıları:**
- ✅ Mevcut import'lar minimal değişir
- ✅ Backward compatibility kolay

**Eksileri:**
- ⚠️ "agentic" generic (her projede olabilir)
- ⚠️ Hala 3 seviye ama `core/` kaldırılırsa 2 seviye olur

**Import (optimize edilmiş):**
```python
from src.agentic.syscalls import fs  # core/ kaldırıldı
from src.agentic.contracts import Task
```

### Seçenek 4: `runtime` (Alternatif)

```
src/runtime/
  contracts/
  syscalls/
  control_plane/
  data_plane/
  orchestrator/
  adapters/
  services/
```

**Artıları:**
- ✅ "Runtime" = execution environment, net
- ✅ Generic değil, spesifik
- ✅ 3 seviye derinlik (iyi)

**Eksileri:**
- ⚠️ Biraz teknik terim

**Import:**
```python
from src.runtime.syscalls import fs
from src.runtime.contracts import Task
```

---

## 🔄 DOSYA YOLU DERİNLİK KARŞILAŞTIRMASI

| Yapı | Derinlik | Örnek Import | Değerlendirme |
|------|----------|--------------|--------------|
| `src/agentic/core/syscalls/fs.py` | 4 seviye | `from src.agentic.core.syscalls import fs` | ❌ Çok derin |
| `src/platform/syscalls/fs.py` | 3 seviye | `from src.platform.syscalls import fs` | ✅ İyi |
| `src/ybis/syscalls/fs.py` | 3 seviye | `from src.ybis.syscalls import fs` | ✅ İyi |
| `src/agentic/syscalls/fs.py` | 3 seviye | `from src.agentic.syscalls import fs` | ✅ İyi (core kaldırılırsa) |
| `src/runtime/syscalls/fs.py` | 3 seviye | `from src.runtime.syscalls import fs` | ✅ İyi |

**Kural:** 3 seviye ideal, 4 seviye çok derin.

---

## 💡 ÖNERİM: HİBRİT YAKLAŞIM

### Aşama 1: `core/` Kaldır, Düzleştir

**Şu an:**
```
src/agentic/
  core/
    protocols.py
    execution/
      aci.py
    graphs/
      orchestrator_graph.py
```

**Olacak:**
```
src/agentic/
  contracts/          # core/protocols.py → contracts/
  syscalls/           # core/execution/aci.py → syscalls/
  orchestrator/       # core/graphs/ → orchestrator/
```

**Fayda:**
- ✅ 4 seviye → 3 seviye
- ✅ Import'lar kısalır: `from src.agentic.core.execution.aci` → `from src.agentic.syscalls`
- ✅ Daha anlaşılır

### Aşama 2: İsimlendirme Seçimi

**Benim önerim:** `ybis` (proje-spesifik)

**Neden?**
1. Çakışma riski yok (Python'da `ybis` modülü yok)
2. Proje adına uygun
3. Kısa ve net
4. Generic değil (her projede "agentic" olabilir ama "ybis" sadece burada)

**Alternatif:** Eğer generic platform istiyorsan → `platform` (ama Python'da `platform` modülü var, dikkat)

---

## 🚀 MİGRASYON STRATEJİSİ

### Senaryo 1: `agentic` → `ybis` (Önerilen)

```python
# Eski
from src.agentic.core.execution.aci import AgentComputerInterface

# Yeni
from src.ybis.syscalls import fs, exec, git
```

**Adımlar:**
1. `src/ybis/` oluştur
2. `src/agentic/core/` → `src/ybis/` map et
3. Import alias ekle (backward compatibility):
   ```python
   # src/agentic/__init__.py
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent))
   from ybis import *  # Re-export
   ```
4. Yavaş yavaş import'ları güncelle
5. Test et, çalışıyorsa `src/agentic/` kaldır

### Senaryo 2: `agentic/core/` → `agentic/` (Düzleştir)

```python
# Eski
from src.agentic.core.execution.aci import AgentComputerInterface

# Yeni
from src.agentic.syscalls import fs, exec, git
```

**Adımlar:**
1. `src/agentic/core/` içeriğini `src/agentic/` altına taşı
2. `core/` klasörünü kaldır
3. Import'ları güncelle
4. Test et

**Daha az risk, daha az değişiklik.**

---

## 📋 KARŞILAŞTIRMA TABLOSU

| Kriter | `platform` | `ybis` | `agentic` (düzleştirilmiş) | `runtime` |
|--------|------------|--------|---------------------------|-----------|
| **Derinlik** | 3 seviye ✅ | 3 seviye ✅ | 3 seviye ✅ | 3 seviye ✅ |
| **Çakışma Riski** | ⚠️ Python'da `platform` var | ✅ Yok | ✅ Yok | ✅ Yok |
| **Generic/Spesifik** | Generic | Spesifik | Generic | Generic |
| **Mevcut Uyumluluk** | ❌ Değişiklik gerekir | ❌ Değişiklik gerekir | ✅ Minimal değişiklik | ❌ Değişiklik gerekir |
| **Anlaşılırlık** | ✅ Net | ✅ Net | ⚠️ "agentic" generic | ✅ Net |
| **Öneri** | ⚠️ İyi ama çakışma riski | ✅ **EN İYİ** | ✅ İyi (minimal risk) | ✅ İyi |

---

## 🎯 SONUÇ VE ÖNERİ

### Kısa Vadeli (Hemen)

**Seçenek A: `agentic` düzleştir (EN AZ RİSK)**
```
src/agentic/
  contracts/      # core/protocols.py
  syscalls/       # core/execution/aci.py
  orchestrator/   # core/graphs/
```

**Artıları:**
- ✅ Mevcut import'lar minimal değişir
- ✅ Backward compatibility kolay
- ✅ Risk düşük

**Eksileri:**
- ⚠️ "agentic" generic (her projede olabilir)

### Orta Vadeli (3-6 ay)

**Seçenek B: `ybis`'e migrate et (EN İYİ)**
```
src/ybis/
  contracts/
  syscalls/
  orchestrator/
```

**Artıları:**
- ✅ Proje-spesifik, çakışma yok
- ✅ Kısa ve net
- ✅ 3 seviye derinlik (ideal)

**Eksileri:**
- ⚠️ Tüm import'ları güncellemek gerekir
- ⚠️ Backward compatibility için alias gerekir

### Uzun Vadeli (6+ ay)

**Seçenek C: `platform`'a migrate et (GENERIC PLATFORM)**

Sadece eğer bu projeyi **generic platform** olarak açık kaynak yapacaksan.

---

## 💬 BENİM NET ÖNERİM

**Şimdi:** `agentic/core/` → `agentic/` düzleştir (minimal risk)

**Sonra:** `agentic` → `ybis` migrate et (3-6 ay içinde, aşamalı)

**Neden?**
1. Şimdi risk almadan düzleştir (4 seviye → 3 seviye)
2. Sonra proje-spesifik isimlendirme yap (`ybis`)
3. Her adımda test et, çalışıyorsa devam et

---

## 🔧 PRATİK ADIMLAR

### Adım 1: Düzleştirme (1 hafta)

```bash
# 1. Yeni yapıyı oluştur
mkdir -p src/agentic/{contracts,syscalls,orchestrator,control_plane,data_plane,adapters,services}

# 2. Dosyaları taşı
mv src/agentic/core/protocols.py src/agentic/contracts/
mv src/agentic/core/execution/aci.py src/agentic/syscalls/
mv src/agentic/core/graphs/orchestrator_graph.py src/agentic/orchestrator/

# 3. Import alias ekle (backward compatibility)
# src/agentic/core/__init__.py
from ..contracts import *
from ..syscalls import *
from ..orchestrator import *
```

### Adım 2: Test Et (1 hafta)

- Tüm test'leri çalıştır
- Import'ları kontrol et
- Çalışıyorsa `core/` klasörünü kaldır

### Adım 3: `ybis`'e Migrate (opsiyonel, 1-2 ay)

- `src/ybis/` oluştur
- `src/agentic/` → `src/ybis/` taşı
- Import alias ekle
- Yavaş yavaş güncelle

---

**Hazırlayan:** AI Assistant  
**Tarih:** 2025-01-XX  
**Versiyon:** 1.0

