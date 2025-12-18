# /YBIS:add-summary-header <file_path>

**Amaç:** Belirtilen Markdown dosyasına, AI tarafından hızlıca taranabilir ve token-verimli bir YAML "Özet Başlığı" ekler. Bu başlık, dokümanın ana içeriğini özetler ve durumunu (`status`) belirtir.

**Kullanım:** `/YBIS:add-summary-header C:\path\to\your\document.md`

**Parametreler:**
*   `<file_path>`: Özet başlığı eklenecek Markdown dosyasının mutlak yolu.

**İş Akışı:**
1.  **Dosyayı Oku:** Belirtilen `<file_path>` adresindeki Markdown dosyasının içeriğini okur.
2.  **Özet Çıkar:** Dosya içeriğinden otomatik olarak aşağıdaki bilgileri çıkarır:
    *   `title`: Dosyanın içeriğine uygun, kısa ve açıklayıcı bir başlık.
    *   `status`: Dokümanın mevcut durumu (`draft`, `idea`, `proposal`, `active`, `rejected`, `archived` vb. uygun olan seçilir).
    *   `owner`: Dokümanın sahibi veya sorumlusu (varsa).
    *   `created_date`: Dosyanın oluşturulma veya son güncellenme tarihi.
    *   `summary`: Dokümanın ana fikrini veya amacını özetleyen 1-2 cümlelik kısa bir açıklama.
    *   `key_takeaways`: Dokümanın en önemli 3-5 ana çıkarımını veya kararını listeleyen maddeler.
3.  **YAML Frontmatter Oluştur:** Çıkarılan bilgilerle bir YAML frontmatter bloğu oluşturur.
4.  **Dosyayı Güncelle:** Oluşturulan YAML frontmatter bloğunu, orijinal dosya içeriğinin en başına ekler ve dosyayı günceller.

**Örnek Çıktı Formatı:**
```markdown
---
title: "Doküman Başlığı"
status: "draft"
owner: "AI Agent"
created_date: "2025-10-21"
summary: "Bu doküman, ana fikri özetleyen kısa bir açıklamadır."
key_takeaways:
  - "Ana çıkarım 1"
  - "Ana çıkarım 2"
  - "Ana çıkarım 3"
---

# Orijinal Doküman İçeriği
...
```
