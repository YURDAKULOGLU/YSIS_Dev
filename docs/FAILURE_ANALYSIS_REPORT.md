# Self-Improve Failure Analysis Report

**Tarih**: 2026-01-11  
**Amaç**: Başarısız run'ların nedenlerini analiz etmek

---

## 📊 GENEL DURUM

**5 workspace analiz edildi:**
- Tümünde **lint fail** (Ruff deprecated settings)
- Çoğunda **test fail** (lint fail olduğu için)
- Implementation **başarılı** (files changed var)

---

## 🔴 ANA SORUNLAR

### 1. **pyproject.toml Deprecated Settings (KRİTİK)**

**Hata**: 
```
Ruff check failed: warning: The top-level linter settings are deprecated 
in favour of their counterparts in the `lint` section.
```

**Neden**:
- `pyproject.toml`'de `[tool.ruff]` altında `select` ve `ignore` var
- Ama `[tool.ruff.lint]` section'ı yok
- Ruff yeni format istiyor: `[tool.ruff.lint]` altında olmalı

**Etki**:
- Her test'te lint fail oluyor
- Repair node düzeltmeye çalışıyor ama başarısız
- Loop devam ediyor

**Çözüm Durumu**:
- ✅ `_fix_pyproject_toml_deprecated_settings` fonksiyonu var
- ❌ Worktree'de çalışmıyor (PROJECT_ROOT'ta çalışıyor)
- ❌ Repair plan validation'da `pyproject.toml` filtreleniyordu (düzeltildi)

---

### 2. **Plan Scope Çok Dar**

**Gözlem**:
- Plan'da sadece **1 dosya**: `src/ybis/orchestrator/graph.py`
- Steps: 3 (çok az)
- Objective genel ama dosya spesifik değil

**Neden**:
- RAG context yetersiz olabilir
- Planner çok konservatif plan üretiyor
- Reflection'dan yeterli context çıkmıyor

**Etki**:
- Küçük değişiklikler yapılıyor
- Büyük sorunlar çözülmüyor
- Test fail'ler devam ediyor

---

### 3. **Pytest Boş Error**

**Gözlem**:
```
Pytest failed: 
(boş error mesajı)
```

**Neden**:
- Lint fail olduğu için pytest hiç çalışmıyor olabilir
- Veya pytest çalışıyor ama error capture edilmiyor

**Etki**:
- Test sonuçları net değil
- Gerçek test hataları görünmüyor

---

### 4. **Repair Loop Etkisiz**

**Gözlem**:
- Repair attempt 1/3: "Failed to fix deprecated settings"
- Repair plan validation failed - no valid files found
- Loop devam ediyor ama hiçbir şey düzelmiyor

**Neden**:
- `pyproject.toml` protected file olarak filtreleniyordu (düzeltildi)
- Worktree'de fix çalışmıyordu (düzeltildi)
- LLM'e yeterli context verilmiyordu (düzeltildi)

---

## 📈 BAŞARILI OLANLAR

### ✅ Implementation
- Files changed: 5 dosya
- Success: True
- Executor çalışıyor

### ✅ Reflection
- Issues identified: 2
- Opportunities: 2
- Error patterns: 106

### ✅ Plan Generation
- Plan oluşturuluyor
- Files belirleniyor
- Steps tanımlanıyor

---

## 🔧 ÖNERİLEN DÜZELTMELER

### 1. **pyproject.toml Fix - Worktree Support** ✅ (YAPILDI)
- `_fix_pyproject_toml_deprecated_settings` worktree path alıyor
- Repair node worktree'de çalışıyor

### 2. **Repair Plan Validation - Protected Files İzin** ✅ (YAPILDI)
- Repair için protected files'a izin verildi
- `pyproject.toml` repair plan'da olabilir

### 3. **LLM Context Zenginleştirme** ✅ (YAPILDI)
- Repair objective'ine files, errors, warnings, instructions eklendi

### 4. **Pytest Error Capture** (YAPILMALI)
- Pytest error'ları düzgün capture edilmeli
- Lint fail olsa bile pytest çalışmalı (ayrı ayrı test)

### 5. **Plan Scope Genişletme** (YAPILMALI)
- RAG context artırılmalı
- Reflection'dan daha fazla context çıkarılmalı
- Planner'a daha fazla dosya önerilmeli

### 6. **Verifier İyileştirme** (YAPILMALI)
- Lint ve test ayrı ayrı çalışmalı
- Lint fail olsa bile test çalışmalı
- Error mesajları daha detaylı olmalı

---

## 🎯 ÖNCELİK SIRASI

1. **KRİTİK**: pyproject.toml fix worktree'de çalışsın ✅
2. **KRİTİK**: Repair plan validation protected files'a izin versin ✅
3. **YÜKSEK**: Pytest error capture düzeltilsin
4. **YÜKSEK**: Verifier lint/test ayrı çalışsın
5. **ORTA**: Plan scope genişletilsin (RAG context artırılsın)

---

## 📝 SONUÇ

**Ana Sorun**: `pyproject.toml` deprecated settings hatası sürekli tekrarlanıyor ve repair düzeltemiyor.

**Çözüm Durumu**: 
- ✅ Repair worktree support eklendi
- ✅ Protected files izin verildi
- ✅ LLM context zenginleştirildi
- ⏳ Pytest error capture düzeltilmeli
- ⏳ Verifier iyileştirilmeli

**Beklenen İyileşme**: Bir sonraki run'da `pyproject.toml` hatası düzeltilmeli ve test pass olmalı.

