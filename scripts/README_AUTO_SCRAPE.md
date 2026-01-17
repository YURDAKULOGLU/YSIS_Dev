# Automatic Package Documentation Scraper

## Overview

`auto_scrape_package_docs.py` otomatik olarak `requirements.txt`'teki **TÜM** paketlerin dokümantasyonunu scrape eder ve `platform_data/knowledge/Frameworks/` altına kaydeder.

## Features

✅ **Otomatik Paket Tespiti**: `requirements.txt`'i parse eder, tüm paketleri bulur  
✅ **PyPI Metadata**: Her paket için PyPI'den metadata çeker  
✅ **Akıllı URL Bulma**: Documentation URL'lerini otomatik bulur (PyPI, GitHub, docs sites)  
✅ **Çoklu Kaynak Desteği**: GitHub, ReadTheDocs, generic docs sites  
✅ **Markdown Dönüşümü**: HTML'i markdown'a çevirir  
✅ **Metadata Kaydetme**: Her paket için JSON metadata kaydeder  
✅ **Skip Existing**: Zaten scrape edilmiş paketleri atlar (hız için)  

## Usage

### Tüm Paketleri Scrape Et

```bash
python scripts/auto_scrape_package_docs.py
```

### Belirli Bir Paketi Scrape Et

```bash
python scripts/auto_scrape_package_docs.py --package llama-index
```

### Mevcut Dokümanları Yeniden Scrape Et

```bash
python scripts/auto_scrape_package_docs.py --no-skip
```

### Farklı requirements.txt Kullan

```bash
python scripts/auto_scrape_package_docs.py --requirements path/to/requirements.txt
```

## Output Structure

```
platform_data/knowledge/Frameworks/
├── llama-index/
│   ├── metadata.json          # PyPI metadata
│   ├── README.md              # GitHub README (if available)
│   └── docs/                  # Scraped documentation
│       ├── index.md
│       ├── getting_started.md
│       └── ...
├── langchain/
│   ├── metadata.json
│   └── docs/
│       └── ...
└── scraping_results.json      # Scraping results summary
```

## How It Works

1. **Parse Requirements**: `requirements.txt`'i okuyup paket isimlerini çıkarır
2. **Get PyPI Metadata**: Her paket için PyPI API'den metadata çeker
3. **Find Docs URL**: 
   - PyPI'deki `documentation_url` field'ını kontrol eder
   - GitHub repo varsa `docs/` folder'ını kontrol eder
   - Home page'den docs URL'i infer eder
4. **Scrape Documentation**:
   - **GitHub**: README.md ve `docs/` folder'ındaki markdown dosyalarını indirir
   - **Docs Sites**: Tüm sayfaları scrape eder (max 50 sayfa)
   - **Generic**: Tek sayfa scrape eder
5. **Save**: Markdown olarak `platform_data/knowledge/Frameworks/{package}/` altına kaydeder

## Supported Sources

- ✅ **PyPI**: Package metadata
- ✅ **GitHub**: README.md, docs/ folder
- ✅ **ReadTheDocs**: Full documentation sites
- ✅ **Generic Docs Sites**: docs.*, documentation.* patterns
- ✅ **Home Page**: Inferred documentation URLs

## Examples

### Example 1: Scrape All Packages

```bash
$ python scripts/auto_scrape_package_docs.py

[INFO] Found 85 packages in requirements.txt

[INFO] Processing 85 packages...

[1/85] Processing langgraph...
[SCRAPE] Scraping langgraph from https://langchain-ai.github.io/langgraph/...
  [OK] Scraped index.md (1/50)
  [OK] Scraped getting_started.md (2/50)
  ...

[2/85] Processing llama-index...
[SCRAPE] Scraping llama-index from https://github.com/run-llama/llama_index...
  [OK] Downloaded README.md
  [OK] Downloaded docs/getting_started.md
  ...

============================================================
SUMMARY
============================================================
✅ Success: 72
❌ Failed: 8
⏭️  Skipped: 5
```

### Example 2: Scrape Single Package

```bash
$ python scripts/auto_scrape_package_docs.py --package ragas

[1/1] Processing ragas...
[SCRAPE] Scraping ragas from https://docs.ragas.io/...
  [OK] Scraped index.md (1/50)
  [OK] Scraped getting_started.md (2/50)
  ...
```

## Integration with RAG

Scraped documentation otomatik olarak RAG'a ingest edilebilir:

```python
# After scraping, ingest into RAG
from src.rag.local_rag import ingest_documents

for package_dir in Path("platform_data/knowledge/Frameworks").iterdir():
    if package_dir.is_dir():
        ingest_documents(package_dir)
```

## Limitations

- **Rate Limiting**: Her paket arasında 1 saniye bekleme (server'lara nazik olmak için)
- **Max Pages**: Docs sites için maksimum 50 sayfa (infinite loop önlemek için)
- **GitHub API**: Public repo'lar için çalışır
- **Authentication**: Private repo'lar için GitHub token gerekir (şu an desteklenmiyor)

## Future Enhancements

- [ ] GitHub token support for private repos
- [ ] Parallel scraping (multiple packages at once)
- [ ] Automatic RAG ingestion after scraping
- [ ] Incremental updates (only new/changed pages)
- [ ] Support for npm packages (package.json)
- [ ] Support for Go modules (go.mod)

## Troubleshooting

### "Could not fetch PyPI metadata"
- Paket PyPI'de yok olabilir
- İnternet bağlantısını kontrol et

### "No documentation URL found"
- Paket dokümantasyonu olmayabilir
- Manuel olarak `metadata.json`'a `documentation_url` ekle

### "Failed to scrape"
- URL erişilemiyor olabilir
- Rate limiting olabilir (biraz bekle ve tekrar dene)

## Notes

- Scraping işlemi zaman alabilir (85 paket için ~10-15 dakika)
- İlk çalıştırmada tüm paketler scrape edilir
- Sonraki çalıştırmalarda sadece yeni paketler scrape edilir (skip_existing=True)
- `scraping_results.json` dosyası hangi paketlerin başarılı/başarısız olduğunu gösterir


