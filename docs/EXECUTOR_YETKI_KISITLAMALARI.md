# Executor Yetki Kısıtlamaları

**Tarih**: 2026-01-11  
**Sorun**: Executor plan'da olmayan dosyaları değiştiriyor, kritik dosyaları bozuyor

---

## 🚨 SORUN

Executor çok fazla yetkiye sahip:
- Plan'da olmayan dosyaları değiştiriyor (`pyproject.toml`, `constants.py`, etc.)
- LLM kendi başına dosyalar öneriyor
- Kritik config dosyaları bozuluyor (TOML syntax errors)

**Örnek**:
- Plan: `["src/ybis/orchestrator/graph.py", "src/ybis/adapters/registry.py"]`
- Executor değiştirdi: `["graph.py", "registry.py", "constants.py", "local_coder.py", "pyproject.toml"]` ❌
- Sonuç: `pyproject.toml` TOML syntax hatası ile bozuldu

---

## ✅ ÇÖZÜM

### 1. Protected Files Koruması

**Dosya**: `src/ybis/adapters/local_coder.py`

```python
PROTECTED_FILES = {
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    ".gitignore",
    ".env",
    ".env.example",
    "docker-compose.yml",
    "Dockerfile",
}
```

**Kural**: Executor bu dosyaları **ASLA** değiştiremez, plan'da olsa bile.

### 2. Invalid Patterns Filtreleme

**Dosya**: `src/ybis/adapters/local_coder.py`

```python
INVALID_PATTERNS = [
    "all", "of", "the", "existing", "code",
    "tests",  # Directory, not a file
    "*.rst",  # Glob pattern
    "pytest.ini",  # Config file
]
```

**Kural**: Bu pattern'ler otomatik olarak filtrelenir.

### 3. LLM Prompt Sıkılaştırması

**Dosya**: `src/ybis/adapters/local_coder.py` - `_generate_file_content()`

**Önceki Prompt**:
```
You are a code editor. Apply the following changes to the file.
```

**Yeni Prompt**:
```
CRITICAL RULES:
- ONLY modify the file: {file_path.name}
- Do NOT create, modify, or reference any other files
- Do NOT change file structure or add new files
- Do NOT modify configuration files unless explicitly requested
- Return ONLY the complete content of {file_path.name} after changes
```

### 4. Plan Validation Sıkılaştırması

**Dosya**: `src/ybis/orchestrator/self_improve.py` - `_validate_improvement_plan()`

- Protected files plan'dan filtreleniyor
- Invalid patterns filtreleniyor
- Sadece gerçek dosyalar plan'a ekleniyor

---

## 📊 KORUNAN DOSYALAR

| Dosya | Neden Korunuyor |
|-------|----------------|
| `pyproject.toml` | Config dosyası, TOML syntax kritik |
| `requirements.txt` | Dependency listesi |
| `setup.py` | Package setup |
| `.gitignore` | Git config |
| `.env` | Environment variables |
| `docker-compose.yml` | Docker config |
| `Dockerfile` | Docker config |

**Kural**: Bu dosyalar executor tarafından **ASLA** değiştirilemez.

---

## 🔒 YETKİ SEVİYELERİ

### Seviye 1: Plan Validation (Plan Node)
- Invalid patterns filtreleniyor
- Protected files filtreleniyor
- Sadece gerçek dosyalar plan'a ekleniyor

### Seviye 2: Executor Validation (Executor Node)
- Plan'daki dosyalar tekrar validate ediliyor
- Protected files **BLOKLANIYOR**
- Invalid patterns **BLOKLANIYOR**

### Seviye 3: LLM Prompt (LLM Call)
- LLM'e strict kurallar veriliyor
- "ONLY modify this file" vurgulanıyor
- Başka dosyalara referans yasak

---

## 🎯 SONUÇ

Artık executor:
- ✅ Sadece plan'daki dosyaları değiştirebilir
- ✅ Protected files'ı değiştiremez
- ✅ Invalid patterns'ı değiştiremez
- ✅ LLM strict kurallarla sınırlandırılmış

**Güvenlik**: Executor artık kritik dosyaları bozamaz!

