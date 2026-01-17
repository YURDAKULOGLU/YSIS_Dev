# Scraper Comparison & Integration

## Mevcut Scraper'lar

### 1. `scripts/fetch_framework_docs.py`
**Amaç:** Basit dokümantasyon scraper  
**Özellikler:**
- ✅ Tek URL scrape eder
- ✅ HTML → Markdown dönüşümü
- ❌ Sadece manuel URL listesi
- ❌ PyPI metadata yok
- ❌ Otomatik URL bulma yok

**Kullanım:**
```python
fetch_docs("https://docs.example.com", "platform_data/knowledge/Frameworks/Example")
```

### 2. `scripts/install_framework.py`
**Amaç:** Framework installer + scraper  
**Özellikler:**
- ✅ Framework kurulumu (pip install)
- ✅ Framework-specific URL mapping
- ✅ GitHub repo mapping
- ✅ Recursive GitHub docs download
- ✅ RAG ingestion
- ❌ Sadece tek framework için
- ❌ requirements.txt parse yok
- ❌ PyPI metadata yok

**Kullanım:**
```bash
python scripts/install_framework.py crewai
```

### 3. `scripts/auto_scrape_package_docs.py` (YENİ)
**Amaç:** Tüm paketler için otomatik scraper  
**Özellikler:**
- ✅ requirements.txt parse
- ✅ PyPI metadata çekme
- ✅ Otomatik URL bulma
- ✅ Framework-specific mappings (install_framework.py'den)
- ✅ GitHub recursive download (install_framework.py'den)
- ✅ Batch processing (tüm paketler)
- ✅ Metadata kaydetme
- ✅ Skip existing
- ⚠️ RAG ingestion ayrı script (ingest_framework_docs_to_rag.py)

**Kullanım:**
```bash
# Tüm paketleri scrape et
python scripts/auto_scrape_package_docs.py

# Tek paket
python scripts/auto_scrape_package_docs.py --package llama-index

# RAG'a ingest et
python scripts/ingest_framework_docs_to_rag.py
```

## Entegrasyon

Yeni scraper (`auto_scrape_package_docs.py`) mevcut scraper'ların en iyi özelliklerini birleştirdi:

1. **Framework Mappings**: `install_framework.py`'deki `FRAMEWORK_DOCS` ve `repo_mappings` eklendi
2. **GitHub Recursive**: `install_framework.py`'deki `_download_github_docs_recursive` metodu eklendi
3. **RAG Ingestion**: Ayrı script olarak `ingest_framework_docs_to_rag.py` oluşturuldu

## Kullanım Senaryoları

### Senaryo 1: Yeni Framework Ekle
```bash
# 1. Framework'ü kur ve dokümanları scrape et
python scripts/install_framework.py new-framework

# VEYA

# 2. requirements.txt'e ekle, sonra tüm paketleri scrape et
python scripts/auto_scrape_package_docs.py
```

### Senaryo 2: Tüm Paketlerin Dokümanlarını Güncelle
```bash
# Tüm paketleri yeniden scrape et
python scripts/auto_scrape_package_docs.py --no-skip

# RAG'a ingest et
python scripts/ingest_framework_docs_to_rag.py
```

### Senaryo 3: Belirli Bir Paket
```bash
# Tek paket scrape
python scripts/auto_scrape_package_docs.py --package llama-index
```

## Önerilen Workflow

1. **İlk Kurulum:**
   ```bash
   # Tüm paketleri scrape et
   python scripts/auto_scrape_package_docs.py
   
   # RAG'a ingest et
   python scripts/ingest_framework_docs_to_rag.py
   ```

2. **Yeni Paket Eklendiğinde:**
   ```bash
   # Sadece yeni paketler scrape edilir (skip_existing=True)
   python scripts/auto_scrape_package_docs.py
   
   # RAG'a ingest et
   python scripts/ingest_framework_docs_to_rag.py
   ```

3. **Manuel Framework Ekleme:**
   ```bash
   # Framework-specific installer kullan
   python scripts/install_framework.py framework-name
   ```

## Karşılaştırma Tablosu

| Özellik | fetch_framework_docs.py | install_framework.py | auto_scrape_package_docs.py |
|---------|------------------------|---------------------|----------------------------|
| requirements.txt parse | ❌ | ❌ | ✅ |
| PyPI metadata | ❌ | ❌ | ✅ |
| Otomatik URL bulma | ❌ | ⚠️ (mapping var) | ✅ |
| Framework kurulumu | ❌ | ✅ | ❌ |
| Batch processing | ❌ | ❌ | ✅ |
| GitHub recursive | ❌ | ✅ | ✅ |
| RAG ingestion | ❌ | ✅ | ⚠️ (ayrı script) |
| Skip existing | ❌ | ❌ | ✅ |
| Metadata kaydetme | ❌ | ❌ | ✅ |

## Sonuç

**Yeni scraper (`auto_scrape_package_docs.py`) en kapsamlı çözüm:**
- ✅ Mevcut scraper'ların tüm özelliklerini içeriyor
- ✅ requirements.txt'teki TÜM paketleri otomatik scrape ediyor
- ✅ PyPI metadata ile akıllı URL bulma
- ✅ Framework-specific mappings korunuyor
- ✅ RAG ingestion ayrı script (daha modüler)

**Öneri:** `auto_scrape_package_docs.py`'yi ana scraper olarak kullan, `install_framework.py`'yi sadece framework kurulumu için kullan.


