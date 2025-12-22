# READ THIS FIRST — YBIS Bootstrap Factory Agent Operating Manual

Bu repo “agentic software factory”dir. Sen (CLI agent) bu fabrikanın operatörüsün.
**Hedef:** görevleri drift’siz bitir, kanıt üret, sistemi kendi kendine büyütecek şekilde framework stacking’i güvenli hale getir.

---

## 0) Mutlak Kurallar (ihlal = fail)

1. **Forbidden dirs’e yazma yok:** `legacy/`, `.venv/`, `.git/`, `.sandbox*`, `archive/`, `site-packages/`
2. **Path hardcode yok:** `.YBIS_Dev`, `../` (normalize edilmemiş), `C:\`, `~`
3. **Artifacts zorunlu:** Her run sonunda `PLAN.md`, `RUNBOOK.md`, `EVIDENCE/*`, `CHANGES/*`, `META.json`
4. **Sentinel fail ise “done” deme.**
5. **Framework core’a sızamaz:** her entegrasyon `adapter + contracts + tests_contract + runbook + policy` ile olur.
6. **Tek modele bağlı kalma:** Router/Provider abstraction kullan; gerekirse API/provider switch.

---

## 1) Bu doküman seti nasıl okunacak? (okuma sırası)

Aşağıdaki dosyaları **sırayla** oku; okurken not çıkarma yerine “kısa özet + zorunlu invariants listesi” üret.

1. `docs/META_PLANES.md`
   * Invariants (Anayasa) + Planes + gates
2. `docs/GOLDEN_TASKS.md`
   * regression sigortası; pass/fail signature listesi
3. `docs/EXTERNAL_AGENTS_PIPELINE.md`
   * dış agent kabul + sandbox/policy
4. `docs/PROMPTS_WORKFLOWS.md`
   * planner/executor/verifier/router standardları

**Okuma çıktı formatı (tek sayfa):**
* “Core invariants” (madde madde)
* “Forbidden writes” listesi
* “Artifacts checklist”
* “En acil 5 gap” (repo içindeki mevcut durumla kıyasla)

---

## 2) Başlangıç Sanity Check (çalışmaya başlamadan)

### 2.1 Dosyalar var mı?

* `config/.sandbox_aiderignore` ✅
* `config/aider_model_settings.yml` ✅
* (opsiyonel) `config/.aider.conf.yml` ✅
* `docs/*` dokümanları ✅

Eksikse: **önce oluştur** (bu mesajdaki içerikleri kullan).

### 2.2 Active/Archive ayrımı uygulanıyor mu?

* Active allowlist: `src/ tests/ docs/ config/ templates/ scripts/`
* Forbidden/Archive: `legacy/ archive/ .venv/ .git/ .sandbox*`

Eğer repo hâlâ `legacy/.venv` gibi büyük yükler taşıyorsa:
* “P0” olarak temizlemeden framework stacking başlatma.

---

## 3) İlk görev: “Factory Gates’i aktif et”

Bu repo için ilk sprint görevleri (P0):

### P0-1 — Containment gerçek olsun

* Aider çağrılarında `--aiderignore config/.sandbox_aiderignore`
* Aider model settings: `--model-settings-file config/aider_model_settings.yml`
* Bu dosyalar yoksa **hard fail** (sessiz devam yok)

### P0-2 — Sentinel drift gate’leri

Sentinel şu kontrolleri **hard fail** yapacak:
* forbidden dirs changed?
* hardcoded/relative path var mı?
* artifacts eksik mi?
* code fence / marker / AST parse fail var mı?
* lock/env hash kanıtı var mı? (en az meta’da)

### P0-3 — Artifacts zorunluluğu

Orchestrator her run sonunda artifacts üretmek zorunda.
Artifacts yoksa: `ARTIFACT_FAIL:*` signature.

---

## 4) Çalışma Protokolü (her task’te aynı)

**RUN LOOP (tek doğru akış):**

1. Intake → TaskSpec
2. Plan → `PLAN.md`
3. Execute → ChangeSet (diff)
4. Verify → Sentinel
5. Artifacts write → `RUNBOOK.md`, `EVIDENCE/*`, `CHANGES/*`, `META.json`
6. Decide:
   * PASS → done
   * FAIL → retry (limitli) + postmortem

**Her fail sonrası:** `templates/POSTMORTEM.md` doldur (auto-postmortem).

---

## 5) “Devasa dokümanı append ederek kurma” yöntemi

Bu repo’da canonical dokümanlar `docs/` altındadır.
**Append ile tek mega dosya üretmek** istenirse:
* Hedef dosya: `BOOTSTRAP_FACTORY_FULL.md` (root)
* İçerik sırası:
  1. `AGENT_READ_THIS_FIRST.md`
  2. `docs/META_PLANES.md`
  3. `docs/GOLDEN_TASKS.md`
  4. `docs/EXTERNAL_AGENTS_PIPELINE.md`
  5. `docs/PROMPTS_WORKFLOWS.md`

**Kural:** Mega dosya sadece “derleme çıktısıdır”.
Kaynak dokümanlar değişmeden kalır; mega dosya yeniden üretilir.

---

## 6) Model bağımsızlık standardı

* Plan / Code / Verify çağrıları “provider string” görmez.
* Tüm seçim `ModelRouter` üzerinden olur.
* Router politikası:
  * plan: hızlı/ucuz
  * code: güçlü
  * verify: orta + sentinel test karar verici
  * risk:high → escalate + (policy’ye göre) HITL

---

## 7) İlk çalıştırma önerisi (Aider)

Aider’ı çalıştırırken (manuel kullanım için örnek):

* `--aiderignore config/.sandbox_aiderignore`
* `--model-settings-file config/aider_model_settings.yml`
* `--no-auto-commits`
* `--no-pretty`

(Detaylar opsiyonel `.aider.conf.yml` ile de set edilebilir.)
