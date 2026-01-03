# META PLANES - Drift-Proof Bootstrap Factory

Bu doküman, YBIS'in "agentic software factory" çekirdeğini **drift'e dayanıklı** şekilde büyütmek için gereken meta-katmanları (planes), zorunlu kapıları (gates), protokolleri (contracts), ve bootstrap çalışma ritüellerini tanımlar.

## 0) Sözlük ve amaç

### Amaç
* **Core sabit** kalsın.
* Framework'ler / ajanlar / modeller **değiştirilebilir** olsun.
* Sistem, **kendi kendini büyütürken** drift üretmesin.
* Her run **kanıtlı** (artifacts) ve **geri alınabilir** (rollback) olsun.
* Sistem **tek modele bağlı** kalmasın; local + API sağlayıcılarla çalışsın.

### Drift tanımı (bu sistemde)
* **Truth drift:** Doküman / config / kod farklı şey söylüyor.
* **Path drift:** Relative path / cwd kayması / duplicate root / ".YBIS_Dev" gibi hardcode.
* **Scope drift:** Agent yanlış alana yazar (legacy/.venv/.git/sandbox).
* **Dependency drift:** Lock yok -> ortam kayar -> "bende çalışıyor".
* **Behavior drift:** Framework eklenince core davranışı değişir.
* **Evidence drift:** Plan/runbook/log/diff yok -> ne olduğu bilinmez.

Bu dokümanın hedefi: drift'in tekrarını **otomatik engellemek**.

---

## 1) Sistem mimarisi: Core + Planes

Sistem iki ana parçadan oluşur:

### 1.1 Core (değişmez)
Core, framework bilmez. Sadece:
* **CoreConfig** (tek truth)
* **OrchestratorBackend** (LangGraph/Temporal/diğer olabilir)
* **Sentinel** (drift + kalite gate)
* **Artifact System** (PLAN/RUNBOOK/EVIDENCE/DIFF)

### 1.2 Planes (meta katmanlar)
Planes, "framework eklemekten" daha üst bir kavramdır: aynı problemi farklı açıdan çözer.

* **Knowledge Plane:** RAG, failure memory, repo map, decision memory
* **Spec Plane:** spec-first, contract-first, golden tasks, ADR
* **Policy Plane:** policy-as-code, izinler, tool erişimi, sandbox rule'ları
* **Verification Plane:** test + semantic verification + risk scanner + replay
* **Evolution Plane:** postmortem -> gate update, model router kalibrasyonu, self-heal

Her plane bir "plugin" değildir; plane = sistemin davranışını stabilize eden meta-mekanizmalar setidir.

---

## 2) Değişmez Invariants (Anayasa)
Bu maddeler "opsiyon" değil. İhlal = fail.

### I-1: Single Source of Truth
* Tüm path/config sadece **CoreConfig** üzerinden türetilir.
* Kod içinde hardcoded root / ".YBIS_Dev" / "../" / "C:\" / "~" yasak.
* Orchestrator çalışırken `cwd` git root'a sabitlenir.

### I-2: Active/Archive ayrımı
* Agent yalnızca **ACTIVE allowlist** alanlara yazar.
* `legacy/`, `.venv/`, `.git/`, `.sandbox*`, `archive/` alanları **write-deny**.

### I-3: Containment (Executor izolasyonu)
* Executor (Aider/SWE agent) yalnız izinli file setini görür.
* İzin kuralları "config/allowlist + ignore file" ile enforce edilir.
* Ignore/settings dosyaları yoksa **hard fail**.

### I-4: Evidence First (Artifacts zorunlu)
Her run (başarılı/başarısız) şu çıktıları üretir:
* `PLAN.md`
* `RUNBOOK.md`
* `EVIDENCE/*`
* `CHANGES/*` (diff, changed_files.json)
* `META.json` (model/router/env hash)

Artifacts yoksa "done" yok.

### I-5: Contract Over Framework
* Core, framework import etmez.
* Framework entegrasyonu yalnızca **adapter + protocol** üzerinden.

### I-6: Fallback Always
* Plugin/Framework çökerse sistem çalışmaya devam eder:
  * Planner fallback
  * Executor fallback
  * Memory fallback
  * Tools fallback (deny by default)

---

## 3) Plane-1: Knowledge Plane (RAG'in doğru hali)
RAG burada üç şeye hizmet eder: **hata tekrarını azaltmak**, **kararları stabilize etmek**, **repo'yu doğru anlamak**.

### 3.1 Failure-RAG (Hata Hafızası) - en yüksek ROI
**Problem:** Aynı failure pattern'leri tekrar ediyor.
**Çözüm:** Her failure artifacts'ı otomatik indexlenir; planner/verifier'a "benzer olay + çözüm" enjekte edilir.

#### Zorunlu "Error Signature" standardı
Sentinel her fail'e bir signature verir:
* `SENTINEL_FAIL:FORBIDDEN_DIR_WRITE`
* `SENTINEL_FAIL:HARDCODED_PATH`
* `EXECUTOR_FAIL:AIDER_ARTIFACT_CODE_FENCE`
* `MEMORY_FAIL:CHROMA_SQLITE_LOCK`
* `VERIFY_FAIL:TESTS_FAILED`
* `ARTIFACT_FAIL:MISSING_PLAN`

Bu signature:
* `artifacts/<task_id>/META.json` içine yazılır,
* indexer tarafından memory store'a atılır,
* bir sonraki benzer durumda retrieve edilir.

#### Injection kuralı
Planner'a (ve gerekirse executor/verifier'a) şu "minimum" kontekst eklenir:
* Son 5 benzer failure'ın "root cause + fix summary"si
* Bu repo için "yasak alanlar ve doğru path sistemi"
* "Benzer çözümde yapılan yanlışlar" listesi

### 3.2 Decision-RAG (Karar Hafızası / ADR)
**Problem:** Mimari kararlar drift ediyor.
**Çözüm:** ADR (Architecture Decision Record) standardı + index.
* `docs/adr/ADR-YYYYMMDD-<title>.md`
* Her ADR: Context -> Decision -> Consequences -> Alternatives -> Rollback/Exit

Planner plan çıkarırken ilgili ADR'leri görür.

### 3.3 Repo-RAG (Semantic Map)
**Problem:** Agent yanlış dosyayı seçiyor, aynı işi iki yerde yapıyor.
**Çözüm:** Repo'nun "semantic haritası":
* Modül sınırları
* Entry points
* Protocol/adapter listesi
* Forbidden dirs
* Test coverage sinyalleri

Bu map "best-effort" çalışır; çökerse sistem çalışmaya devam eder.

---

## 4) Plane-2: Spec Plane (Spec-first + Contract-first)

### 4.1 Spec-to-Contract-to-Code zinciri
Yeni capability eklemenin tek doğru yolu:
1. **SPEC** (ne istiyoruz, sınırlar, başarı kriteri)
2. **CONTRACT** (protocol, schema, invariants)
3. **CONTRACT TESTS** (golden tasks + plugin contract suite)
4. **ADAPTER** (tek giriş)
5. **IMPLEMENTATION** (framework/agent/code)
6. **RUNBOOK** (kurulum + doğrulama + rollback)
7. **EVIDENCE** (log + diff + meta)

Spec olmadan merge yok. Contract tests olmadan merge yok.

### 4.2 Golden Tasks (Altın görev seti)
Bu sistem "orchestrator değişebilir" diyorsa, tek gerçek sigorta golden tasks'tır.
* Her backend/agent/framework eklemesi golden suite'i koşar.
* Golden tasks: pass/fail net, deterministik, drift'i yakalar.

(Detay: `docs/GOLDEN_TASKS.md`)

---

## 5) Plane-3: Policy Plane (Policy-as-Code + Permissions)
Bu plane drift'in çoğunu "başlamadan" öldürür.

### 5.1 Policy-as-Code (basit kural motoru)
Policy bir doküman değil, **çalışan kural seti** olmalı.
Minimum policy maddeleri:
* Forbidden dirs'e yazma: deny
* Hardcoded path: deny
* Tool izinleri: allowlist
* Network: default deny (external agent'larda)
* Artifact zorunluluğu: enforce
* Risk bazlı HITL: risk yüksekse onay checkpoint

### 5.2 Capability Permissions (step-scoped permissions)
Her step, sadece gereken izinleri alır:
* `cap:plan`
* `cap:code`
* `cap:verify`
* `cap:tool:web`
* `cap:tool:github`
* `cap:memory:read`
* `cap:memory:write`

External agent'lar için default minimum = `cap:plan` bile olmayabilir; görevine göre verilir.

### 5.3 Tool Registry + Audit
Tool çağrıları:
* argümanlarıyla birlikte loglanır
* result summary kaydedilir
* rate limit uygulanır
* policy check'ten geçer

---

## 6) Plane-4: Verification Plane (Test + Semantik + Replay)

### 6.1 Sentinel: kalite + drift gate
Sentinel "unit test runner" değil, "factory gate"tir.
Zorunlu gate kategorileri:
* Repo hygiene gate (forbidden dirs touched?)
* Path drift gate (hardcoded/relative/duplicate root?)
* Artifact integrity gate (plan/runbook/evidence/diff var mı?)
* Executor artifact gate (code fence/markers/AST parse?)
* Contract gate (schema/invariants)
* Dependency drift gate (lock + env hash)

### 6.2 Risk Scanner (değişiklik sınıflandırma)
ChangeSet risk flag'leri:
* `risk:high` -> auth/infra/config/core touched
* `risk:medium` -> new dependency, broad refactor
* `risk:low` -> docs/tests only

Risk yüksekse:
* daha sıkı verification
* daha güçlü modele route
* opsiyonel HITL checkpoint

### 6.3 Replay Harness (Repro)
Her artifact run, yeniden yürütülebilir olmalı:
* aynı task spec
* aynı scope
* aynı env hash (veya container digest)
* aynı verification komutları

Replay komutu:
* `ybis replay <task_id>`

---

## 7) Plane-5: Evolution Plane (Self-Improvement)
Bu plane "koltuğa oturma"nın gerçek motoru.

### 7.1 Auto-Postmortem -> Gate Update
Her fail sonrası sistem:
* postmortem çıkarır (template)
* root cause kategoriler
* kalıcı önlem önerir:
  * policy rule
  * sentinel check
  * prompt update
  * golden task ekleme

Kural: "Aynı root cause 2 kez olduysa" -> otomatik "kalıcı önlem PR" önerisi.

### 7.2 Model Router Calibration (tek modele bağlı kalmama)
Sistem periyodik kalibrasyon suite'i koşar:
* 20-50 mini görev
* provider/model denemeleri
* latency/başarı/cost skorları
* router policy güncelleme önerisi

Routing örneği:
* Plan: hızlı/ucuz
* Code patch: güçlü
* Verify reasoning: orta (ama karar sentinel test)
* Risk high: escalate

---

## 8) External Agents Pipeline (dış ajan kabul sistemi)

### 8.1 Agent Package Standard
External agent şu dosyalarla gelir:
* `agent.yaml`
* `adapter.py`
* `tests_contract.py`
* `runbook.md`
* `policy_requirements.md`

Core asla direct import yapmaz; registry -> adapter.

### 8.2 Sandbox + Permissions
External agent:
* sandbox içinde koşar
* file allowlist (task scope)
* tool allowlist (manifest)
* network default deny

### 8.3 Acceptance Gate
Merge için:
* manifest valid
* contract tests pass
* drift scan pass
* artifacts pass
* replay pass (toleranslı)

---

## 9) Operasyonel workflow (Agent çalışma ritüeli)

### 9.1 Her task için "Definition of Done"
* artifacts var
* sentinel pass
* rollback var
* contract suite pass (gerekliyse)
* scope rules ihlal edilmedi

### 9.2 Her framework ekleme için "Definition of Done"
* adapter + contracts + tests_contract + runbook + policy_requirements
* fallback tanımlı
* golden tasks + plugin contract suite pass
