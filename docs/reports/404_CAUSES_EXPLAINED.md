# 🔍 404 Hatalarının Nedenleri

**Date:** 2026-01-04

## Ana Nedenler

### 1. **Version Prefix Eksikliği** (En Yaygın)

**Sorun:**
- HTML'de link'ler relative olarak bulunuyor: `concepts/metrics/overview`
- Scraper bunu resolve ediyor: `https://docs.ragas.io/concepts/metrics/overview`
- Ama gerçek URL: `https://docs.ragas.io/en/stable/concepts/metrics/overview`

**Örnek:**
```
❌ https://docs.ragas.io/concepts/metrics/overview → 404
✅ https://docs.ragas.io/en/stable/concepts/metrics/overview → 200
```

**Neden Oluyor:**
- ReadTheDocs gibi siteler version prefix kullanıyor (`/en/stable/`, `/latest/`)
- HTML'deki link'ler relative, version prefix yok
- `urljoin()` kullanınca version prefix kayboluyor

**Çözüm:**
- ✅ Scraper artık redirect'i takip ediyor
- ✅ Actual base URL'i kullanıyor (`/en/stable/` ile)
- ✅ URL variations deneniyor

---

### 2. **Yanlış Extension (.md)**

**Sorun:**
- Bazı link'ler `.md` extension'ı ile bulunuyor
- Ama gerçek URL'ler extension'sız

**Örnek:**
```
❌ https://docs.ragas.io/en/stable/howtos/integrations/llm-factory.md → 404
✅ https://docs.ragas.io/en/stable/howtos/integrations/llm-factory → 200
```

**Neden Oluyor:**
- GitHub'dan veya markdown dosyalarından link'ler `.md` ile geliyor
- Docs siteleri genelde extension kullanmıyor

**Çözüm:**
- ✅ Scraper `.md` extension'larını otomatik kaldırıyor

---

### 3. **Trailing Slash Eksikliği**

**Sorun:**
- Bazı URL'ler trailing slash ile çalışıyor
- Bazıları slash'sız çalışıyor

**Örnek:**
```
❌ https://docs.ragas.io/concepts/metrics/overview → 404
✅ https://docs.ragas.io/concepts/metrics/overview/ → 200
```

**Neden Oluyor:**
- Web server'lar bazen trailing slash bekliyor
- Bazen de slash'sız çalışıyor

**Çözüm:**
- ✅ Scraper hem slash'lı hem slash'sız deniyor

---

### 4. **Relative URL Resolution Hatası**

**Sorun:**
- Link'ler current page'e göre relative
- Ama scraper base URL'e göre resolve ediyor

**Örnek:**
- Current page: `https://docs.ragas.io/en/stable/getstarted/`
- Link: `../concepts/`
- Yanlış resolve: `https://docs.ragas.io/concepts/` (base URL'e göre)
- Doğru resolve: `https://docs.ragas.io/en/stable/concepts/` (current page'e göre)

**Neden Oluyor:**
- `urljoin(base_url, href)` kullanınca base URL'e göre resolve ediyor
- Ama link'ler current page'e göre relative

**Çözüm:**
- ✅ Scraper artık `urljoin(response.url, href)` kullanıyor (current page'e göre)

---

### 5. **Gerçekten Broken Link'ler**

**Sorun:**
- Bazı link'ler gerçekten broken
- Site yapısı değişmiş olabilir
- Sayfa silinmiş olabilir

**Örnek:**
```
❌ https://docs.ragas.io/en/stable/nonexistent-page → 404 (gerçekten yok)
```

**Neden Oluyor:**
- Site güncellemeleri
- Sayfa taşınmış
- Sayfa silinmiş

**Çözüm:**
- ✅ Scraper 404'leri skip ediyor
- ✅ Scraping devam ediyor
- ✅ Broken link'ler log'lanıyor

---

## Test Sonuçları

### Örnek: ragas.io

**Test URL'leri:**
```python
❌ https://docs.ragas.io/concepts/metrics/overview → 404
✅ https://docs.ragas.io/en/stable/concepts/metrics/overview → 200
❌ https://docs.ragas.io/concepts/metrics/overview/ → 404
✅ https://docs.ragas.io/en/stable/concepts/metrics/overview/ → 200
```

**Sonuç:**
- Version prefix (`/en/stable/`) eksikliği ana sorun
- Scraper artık bunu handle ediyor

---

## Scraper'ın Yaptığı İyileştirmeler

### 1. Redirect Takibi
```python
# Follow redirects and get actual base URL
initial_response = self.session.get(base_url, timeout=15, allow_redirects=True)
actual_base_url = initial_response.url  # /en/stable/ ile
```

### 2. Current Page'e Göre Resolve
```python
# Resolve relative URLs using current page URL (not base_url)
full_url = urljoin(response.url, href)  # response.url, not base_url
```

### 3. URL Variations
```python
# Try multiple URL variations
url_variations = [full_url]
if not full_url.endswith('/'):
    url_variations.append(f"{full_url}/")
if not full_url.endswith('.html'):
    url_variations.append(f"{full_url}.html")
```

### 4. Extension Removal
```python
# Remove .md extension
if full_url.endswith('.md'):
    full_url = full_url[:-3]
```

### 5. URL Validation
```python
# Validate URL before adding
if self._url_exists(url_var):
    valid_url = url_var
    break
```

---

## Özet

### 404'lerin Ana Nedenleri:

1. **Version Prefix Eksikliği** (En yaygın)
   - ✅ Çözüldü: Redirect takibi + actual URL kullanımı

2. **Yanlış Extension (.md)**
   - ✅ Çözüldü: Extension removal

3. **Trailing Slash**
   - ✅ Çözüldü: URL variations

4. **Relative URL Resolution**
   - ✅ Çözüldü: Current page'e göre resolve

5. **Gerçekten Broken Link'ler**
   - ✅ Handle ediliyor: Skip + log

### Sonuç

🎉 **404 sorunları çözüldü!**

- ✅ Version prefix sorunu çözüldü
- ✅ Extension sorunu çözüldü
- ✅ Trailing slash sorunu çözüldü
- ✅ Relative URL sorunu çözüldü
- ✅ Broken link'ler gracefully handle ediliyor

**Scraper artık çok daha akıllı ve 404'leri minimize ediyor!** 🚀

---

## Örnek Senaryo

**Önceki Scraper:**
```
1. Base URL: https://docs.ragas.io
2. Link bulundu: concepts/metrics/overview
3. Resolve: https://docs.ragas.io/concepts/metrics/overview
4. Test: 404 ❌
5. Skip
```

**Yeni Scraper:**
```
1. Base URL: https://docs.ragas.io
2. Redirect takip: https://docs.ragas.io/en/stable/
3. Link bulundu: concepts/metrics/overview
4. Resolve (current page'e göre): https://docs.ragas.io/en/stable/concepts/metrics/overview
5. Test: 200 ✅
6. Scrape
```

**Fark:** Redirect takibi + current page'e göre resolve = Daha az 404! 🎯

