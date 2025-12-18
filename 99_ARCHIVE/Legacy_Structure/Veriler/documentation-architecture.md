# YBIS Documentation Architecture

**Purpose:** Doküman hiyerarşisi, ownership modeli ve bağımlılık yapısı  
**Created:** 2025-10-12  
**Status:** 🎯 TASARIM AŞAMASI

---

## 📊 Mevcut Durum Analizi

### Toplam Doküman Sayısı
- **Ana dizin (docs/):** 5 dosya
- **Güncel (docs/Güncel/):** 10 dosya
- **Arşiv (docs/Archive/):** 46+ dosya
- **Epics/Stories/QA:** 4+ dosya
- **TOPLAM AKTİF:** ~19 dosya

### Tespit Edilen Sorunlar ❌
1. **Çapraz bağımlılıklar tanımsız** - Hangi doküman hangisine bağlı belli değil
2. **Source of Truth belirsiz** - Aynı bilgi birden fazla yerde
3. **Güncelleme cascade yok** - Bir değişiklik diğerlerini tetiklemiyor
4. **Ownership yok** - Her bilginin tek sahibi yok

---

## 🏗️ YENİ DOKÜMANTASYON MİMARİSİ

### Tier -1: STRATEGIC LAYER (Product & Business Vision) 🌟

**Kural:** Projenin NEDEN'i ve NE'si burada. Teknik kararlar buradan türer.

```yaml
TIER_MINUS_1_STRATEGIC:
  
  Product_Requirements_Document:
    file: "docs/prd/PRODUCT_REQUIREMENTS.md"  # Legacy'den taşınacak
    role: "Product Vision"
    authority: "STRATEGIC"
    owns:
      - product_vision
      - user_personas
      - feature_priorities
      - success_metrics
    derived_from: NONE
    status: "NEEDS_UPDATE (from legacy/prd.md)"
  
  Project_Vision:
    file: "docs/vision/PROJECT_VISION.md"  # Legacy'den taşınacak
    role: "Why We Build"
    authority: "STRATEGIC"
    owns:
      - mission_statement
      - target_market
      - problem_statement
      - solution_approach
    derived_from: NONE
    status: "NEEDS_UPDATE (from legacy/project-vision.md)"
  
  Market_Research:
    file: "docs/strategy/MARKET_RESEARCH.md"  # Legacy'den taşınacak
    role: "Market Analysis"
    authority: "STRATEGIC"
    owns:
      - market_size
      - competitor_analysis
      - user_research
      - market_opportunities
    derived_from: NONE
    status: "NEEDS_UPDATE (from legacy/market-research.md)"
  
  Competitive_Strategy:
    file: "docs/strategy/COMPETITIVE_STRATEGY.md"  # Legacy'den taşınacak
    role: "Market Positioning"
    authority: "STRATEGIC"
    owns:
      - positioning
      - differentiation
      - go_to_market
      - competitive_advantages
    derived_from: NONE
    status: "NEEDS_UPDATE (from legacy/competitive-strategy.md)"
  
  Product_Roadmap:
    file: "docs/roadmap/PRODUCT_ROADMAP.md"  # Legacy + Archive'den birleştir
    role: "Timeline & Phases"
    authority: "STRATEGIC"
    owns:
      - release_phases
      - milestone_timeline
      - feature_releases
      - version_planning
    derived_from:
      - Product_Requirements_Document (features)
      - Market_Research (priorities)
    status: "NEEDS_UPDATE (from legacy/development-plan.md + Archive/Product-Roadmap/)"
```

**⚠️ Kritik Nokta:** Tier -1 değişirse → Tier 0 (Anayasa) yeniden değerlendirilir!

---

### Tier 0: CANONICAL SOURCES (Single Source of Truth) 🔥

**Kural:** Bu dokümanlar TEKNIK bilginin TEK SAHİBİDİR. Tier -1'den esinlenir.

```yaml
TIER_0_CANONICAL:
  
  YBIS_PROJE_ANAYASASI:
    role: "Constitution"
    authority: "TECHNICAL_CANONICAL"
    owns:
      - port_architecture_principles
      - quality_gates
      - forbidden_patterns
      - tech_constraints
    derived_from:
      - Product_Requirements_Document (feature priorities inform architecture)
      - Competitive_Strategy (performance targets, differentiation)
    
  DEVELOPMENT_LOG:
    role: "Decision Registry"
    authority: "TECHNICAL_CANONICAL"
    owns:
      - architecture_decisions (AD-XXX)
      - completed_tasks
      - issues_and_fixes
      - timeline
    derived_from:
      - YBIS_PROJE_ANAYASASI (architecture constraints)
      - Product_Roadmap (timeline, milestones)
```

### Tier 1: REFERENCE DOCUMENTS (Derived, Read-Only)

**Kural:** Bu dokümanlar TIER 0'dan türer. Manuel değişiklik YASAK!

```yaml
TIER_1_REFERENCE:
  
  tech-stack.md:
    role: "Technical Reference"
    authority: "DERIVED"
    owns: NOTHING
    derived_from:
      - DEVELOPMENT_LOG (AD-002, AD-015, etc.)
      - YBIS_PROJE_ANAYASASI (tech constraints)
    
  package-structure.md:
    role: "Implementation Blueprint"
    authority: "DERIVED"
    owns: NOTHING
    derived_from:
      - DEVELOPMENT_LOG (AD-001, AD-002, AD-003, AD-015)
      - YBIS_PROJE_ANAYASASI (port architecture)
    
  README.md:
    role: "Project Overview"
    authority: "DERIVED"
    owns: NOTHING
    derived_from:
      - DEVELOPMENT_LOG (status, progress)
      - tech-stack.md (versions)
```

### Tier 2: EXECUTION DOCUMENTS (Partially Derived)

**Kural:** Bu dokümanlar hem türetilmiş hem de dinamik içerik içerir.

```yaml
TIER_2_EXECUTION:
  
  tasks.md:
    role: "Task List"
    authority: "HYBRID"
    owns:
      - task_checkboxes (dynamic)
      - task_completion_status (dynamic)
    derived_from:
      - DEVELOPMENT_LOG (AD-XXX decisions)
      - package-structure.md (implementation details)
    dynamic_content:
      - checkbox_status
      - completion_dates
    
  DEVELOPMENT_GUIDELINES.md:
    role: "Developer Rules"
    authority: "HYBRID"
    owns:
      - code_patterns
      - error_solutions
    derived_from:
      - YBIS_PROJE_ANAYASASI (core rules)
      - DEVELOPMENT_LOG (learned lessons)
```

### Tier 3: NAVIGATION & META (Auto-Generated)

**Kural:** Bu dokümanlar otomatik generate edilir.

```yaml
TIER_3_META:
  
  DOCUMENTATION_INDEX.md:
    role: "Navigation"
    authority: "AUTO_GENERATED"
    owns: NOTHING
    generated_from:
      - all_document_frontmatter
      - file_structure
    
  QUICKSTART.md:
    role: "Getting Started"
    authority: "HYBRID"
    owns:
      - setup_steps (curated)
    derived_from:
      - tasks.md (first tasks)
      - tech-stack.md (versions)
```

---

## 🔗 DEPENDENCY GRAPH

### Bilgi Akışı (Information Flow)

```
TIER -1 (STRATEGIC)
    ↓ shapes
TIER 0 (CANONICAL)
    ↓ derives
TIER 1 (REFERENCE)
    ↓ affects
TIER 2 (EXECUTION)
    ↓ generates
TIER 3 (META)
```

**Örnek Akış:**
```
Market Research (Tier -1)
    → "ADHD users need simple onboarding"
        → PRD (Tier -1): Feature priority
            → Anayasa (Tier 0): Architecture principle "Progressive disclosure"
                → Development Log (Tier 0): AD-XXX decision
                    → tech-stack (Tier 1): Expo Router (simple navigation)
                        → tasks (Tier 2): T007 Configure Expo Router
```

### Örnek: "React Version" Bilgisi

```yaml
react_version:
  
  CANONICAL_SOURCE:
    file: "DEVELOPMENT_LOG.md"
    section: "AD-002"
    value: "19.1.0"
    last_updated: "2025-10-06"
  
  REFERENCES:
    - file: "tech-stack.md"
      locations:
        - line: 15 (Core Framework section)
        - line: 282 (Migration section)
        - line: 338 (Package versions)
    
    - file: "package-structure.md"
      locations:
        - line: 411 (mobile dependencies)
    
    - file: "README.md"
      locations:
        - line: 5 (Tech Stack header)
  
  UPDATE_RULE: |
    IF DEVELOPMENT_LOG.md#AD-002 changes:
      THEN update ALL references automatically
      AND log the cascade update
```

### Örnek: "Auth Strategy" Bilgisi

```yaml
auth_strategy:
  
  CANONICAL_SOURCE:
    file: "DEVELOPMENT_LOG.md"
    section: "AD-015"
    value: "Expo Auth Session (OAuth 2.0 + PKCE)"
    last_updated: "2025-10-11"
  
  REFERENCES:
    - file: "tech-stack.md"
      locations:
        - line: 281 (Auth section)
        - Auth Dependencies section
    
    - file: "package-structure.md"
      locations:
        - line: 22 (Key Decisions)
        - line: 1054 (Auth package structure)
        - line: 1091-1188 (ExpoAuthAdapter code)
        - line: 1674 (Port migration table)
    
    - file: "tasks.md"
      locations:
        - T020-T026 (Auth tasks section)
    
    - file: "YBIS_PROJE_ANAYASASI.md"
      locations:
        - AuthPort definition
  
  UPDATE_RULE: |
    IF DEVELOPMENT_LOG.md#AD-015 changes:
      THEN update ALL references
      AND create Migration Plan
      AND notify ALL agents
```

---

## 📋 OWNERSHIP REGISTRY

### Kimse Neyin Sahibi?

```yaml
ownership_map:
  
  # Architecture Decisions
  architecture_decisions:
    owner: "DEVELOPMENT_LOG.md"
    format: "AD-XXX sections"
    update_frequency: "on_decision"
  
  # Tech Stack Versions
  package_versions:
    owner: "DEVELOPMENT_LOG.md"
    format: "AD-XXX (e.g., AD-002 for React)"
    references:
      - "tech-stack.md" (display)
      - "package-structure.md" (implementation)
  
  # Port Architecture
  port_definitions:
    owner: "YBIS_PROJE_ANAYASASI.md"
    format: "Section 2 (Port Architecture)"
    references:
      - "service-integration-strategy.md" (details)
      - "package-structure.md" (implementation)
  
  # Task Status
  task_completion:
    owner: "tasks.md"
    format: "Checkbox status"
    synced_to:
      - "DEVELOPMENT_LOG.md" (completion notes)
      - "README.md" (progress %)
  
  # Quality Standards
  quality_gates:
    owner: "YBIS_PROJE_ANAYASASI.md"
    format: "Section 3 (Quality Gates)"
    references:
      - "quality-standards.md" (detailed specs)
      - "DEVELOPMENT_GUIDELINES.md" (how to achieve)
  
  # Integration Strategy
  integration_roadmap:
    owner: "INTEGRATION_ROADMAP.md"
    format: "Phase definitions"
    references:
      - "service-integration-strategy.md" (patterns)
      - "tasks.md" (execution)
```

---

## 🔄 UPDATE CASCADE RULES

### Rule 1: Architecture Decision Changes

```yaml
trigger: "DEVELOPMENT_LOG.md AD-XXX modified"

cascade:
  - check: "tech-stack.md references"
  - check: "package-structure.md references"
  - check: "tasks.md affected tasks"
  - check: "YBIS_PROJE_ANAYASASI.md alignment"
  
notification:
  - agents: ["DevAgent", "ArchAgent", "DocAgent"]
  - checklist: "documentation-consistency-checklist.md"
```

### Rule 2: Constitution Changes

```yaml
trigger: "YBIS_PROJE_ANAYASASI.md modified"

cascade:
  - check: "ALL derived documents"
  - check: "service-integration-strategy.md"
  - check: "quality-standards.md"
  
notification:
  - severity: "CRITICAL"
  - agents: ["ALL"]
  - approval_required: true
```

### Rule 3: Task Completion

```yaml
trigger: "tasks.md checkbox checked"

cascade:
  - update: "DEVELOPMENT_LOG.md (add completion note)"
  - update: "README.md (update progress %)"
  
notification:
  - agents: ["DevAgent"]
  - checklist: "story-dod-checklist.md"
```

---

## 🎯 ÖNERİLEN YAPILANDIRMA

### Aşama 1: Canonical Sources Tanımla (Bu dosya) ✅
- [x] Tier 0 dokümanları belirle
- [x] Ownership registry oluştur
- [x] Dependency graph çiz

### Aşama 2: Documentation Map Oluştur (Sonraki)
- [ ] `documentation-map.yaml` yaz
- [ ] Her doküman için metadata
- [ ] Bağımlılık zincirleri

### Aşama 3: Validation Script (Sonraki)
- [ ] Python script: `check-doc-consistency.py`
- [ ] Otomatik tutarsızlık tespiti
- [ ] Cascade update detector

### Aşama 4: Automation (Gelecek)
- [ ] Pre-commit hook
- [ ] Interactive checklist
- [ ] Auto-sync system

---

## 🚨 KRİTİK KURALLAR

### ✅ DO's
1. **DEVELOPMENT_LOG.md** değiştiğinde → Tüm references kontrol et
2. **YBIS_PROJE_ANAYASASI.md** değiştiğinde → Approval iste
3. **tasks.md** checkbox işaretlendiğinde → DEVELOPMENT_LOG'a not ekle
4. Her AD-XXX için → Affected documents listele

### ❌ DON'Ts
1. **tech-stack.md'yi direkt değiştirme** → DEVELOPMENT_LOG'dan türet
2. **package-structure.md'yi manuel güncelleme** → AD-XXX'den al
3. **README.md version'unu elle yaz** → Auto-generate et
4. **Aynı bilgiyi 2 yerde canonical yapma** → Tek source seç

---

## 📊 MEVCUT DURUM → HEDEFİ

### Öncesi (Şu an) ❌
```
Legacy docs (unutulmuş) ──┐
DEVELOPMENT_LOG ──────────┤
tech-stack ────────────────┼──→ Hepsi birbirinden bağımsız
package-structure ─────────┤     Değişiklik manuel yayılıyor
tasks ─────────────────────┤     Tutarsızlık garantili
README ────────────────────┘     Strategy → Tech bağlantısı YOK
```

### Sonrası (Hedef) ✅
```
TIER -1 (STRATEGIC)
  ├── PRD (product vision)
  ├── Project Vision (why)
  ├── Market Research (user needs)
  ├── Competitive Strategy (positioning)
  └── Product Roadmap (timeline)
         ↓ shapes
TIER 0 (CANONICAL)
  ├── YBIS_PROJE_ANAYASASI (tech constitution)
  └── DEVELOPMENT_LOG (decisions)
         ↓ auto-cascade
TIER 1 (REFERENCE)
  ├── tech-stack (derived)
  ├── package-structure (derived)
  └── README (derived)
         ↓ affects
TIER 2 (EXECUTION)
  ├── tasks (hybrid)
  └── DEVELOPMENT_GUIDELINES (hybrid)
         ↓ generates
TIER 3 (META)
  ├── DOCUMENTATION_INDEX (auto)
  └── QUICKSTART (auto)
```

---

## 📦 LEGACY MIGRATION PLAN

### Aşama 1: Strategic Docs Güncelleme (Öncelikli)

**Hedef:** Legacy'deki stratejik dokümanları güncelleyip aktif hale getir

```yaml
migration_tasks:
  
  TASK_1_PRD_UPDATE:
    source: "docs/Archive/Legacy/prd.md"
    target: "docs/prd/PRODUCT_REQUIREMENTS.md"
    status: "PENDING"
    actions:
      - Extract: User personas (still valid?)
      - Extract: Feature priorities (align with current tasks)
      - Extract: Success metrics (update for Closed Beta)
      - Remove: Outdated tech references (Firebase, etc.)
      - Add: Current tech stack alignment
      - Add: Tier 1 Port Architecture impact
    estimated_time: "2 hours"
  
  TASK_2_VISION_UPDATE:
    source: "docs/Archive/Legacy/project-vision.md"
    target: "docs/vision/PROJECT_VISION.md"
    status: "PENDING"
    actions:
      - Verify: Mission statement still accurate?
      - Update: Target market (ADHD focus?)
      - Update: Problem statement (current market)
      - Update: Solution approach (Expo + Port Architecture)
    estimated_time: "1 hour"
  
  TASK_3_ROADMAP_CONSOLIDATION:
    sources:
      - "docs/Archive/Legacy/development-plan.md"
      - "docs/Archive/Product-Roadmap/closed-beta-scope.md"
      - "docs/Archive/Product-Roadmap/open-beta-scope.md"
      - "docs/Archive/Product-Roadmap/mvp-release-scope.md"
    target: "docs/roadmap/PRODUCT_ROADMAP.md"
    status: "PENDING"
    actions:
      - Merge: All roadmap versions
      - Align: With current tasks.md
      - Update: Expo Auth Session (not Firebase)
      - Update: React 19.1.0 (not 19.2.0)
      - Add: Week-by-week breakdown
      - Cross-reference: tasks.md checkboxes
    estimated_time: "3 hours"
  
  TASK_4_MARKET_RESEARCH_UPDATE:
    source: "docs/Archive/Legacy/market-research.md"
    target: "docs/strategy/MARKET_RESEARCH.md"
    status: "PENDING"
    actions:
      - Update: Competitor analysis (2025 landscape)
      - Verify: User research (still valid?)
      - Add: Recent market trends
      - Update: ADHD app market insights
    estimated_time: "2 hours"
  
  TASK_5_COMPETITIVE_STRATEGY_UPDATE:
    source: "docs/Archive/Legacy/competitive-strategy.md"
    target: "docs/strategy/COMPETITIVE_STRATEGY.md"
    status: "PENDING"
    actions:
      - Update: Positioning vs competitors
      - Verify: Differentiation strategy
      - Update: Go-to-market plan
      - Align: With current Port Architecture advantage
    estimated_time: "1.5 hours"
```

**Toplam tahmini süre:** ~9.5 saat

---

### Aşama 2: Cross-Link Strategic → Technical

**Hedef:** Tier -1 → Tier 0 bağlantıları kur

```yaml
cross_linking:
  
  PRD_to_ANAYASA:
    - PRD'deki feature priorities → Anayasa'da architecture principles
    - Örnek: "Fast onboarding" → "Progressive disclosure pattern"
  
  VISION_to_DEVELOPMENT_LOG:
    - Vision'daki target users → AD-XXX decisions
    - Örnek: "ADHD users" → AD-015 (simple auth flow = Expo Auth)
  
  ROADMAP_to_TASKS:
    - Roadmap phases → tasks.md weeks
    - Closed Beta scope → Phase 0.1-0.4 tasks
    - Open Beta scope → Phase 1.0 tasks (future)
  
  COMPETITIVE_to_TECH_STACK:
    - Performance targets → tech choices
    - Örnek: "Faster than Notion" → React 19.1 + Tamagui
```

---

### Aşama 3: Legacy Archive Cleanup

**Ne yapılacak Legacy dosyalarla?**

```yaml
legacy_file_disposition:
  
  KEEP_AS_ARCHIVE:
    - architecture.md (historical tech decisions)
    - Chat ürün architecture.md (initial product design)
    - modernization-session-22-sep-2025.md (transformation journey)
    reason: "Historical reference, shows evolution"
  
  MERGE_AND_DELETE:
    - prd.md → docs/prd/PRODUCT_REQUIREMENTS.md
    - project-vision.md → docs/vision/PROJECT_VISION.md
    - development-plan.md → docs/roadmap/PRODUCT_ROADMAP.md
    - market-research.md → docs/strategy/MARKET_RESEARCH.md
    - competitive-strategy.md → docs/strategy/COMPETITIVE_STRATEGY.md
    reason: "Güncellendi, aktif hale getirildi"
  
  DELETE_OBSOLETE:
    - tech-stack-decisions.md (tech-stack.md'de var)
    - nodejs-version-analysis-report.md (irrelevant)
    - nodejs-version-correction.md (fixed)
    reason: "Artık gereksiz veya duplicate"
```

---

## ⏭️ SONRAKI ADIM

### Seçenek A: Legacy Migration First (Öncelikli) 🎯
1. ✅ PRD güncellemesi (2 saat)
2. ✅ Roadmap birleştirme (3 saat)
3. ✅ Cross-linking (1 saat)
4. → Sonra `documentation-map.yaml`

**Avantaj:** Strategy → Tech bağlantısı kurulur, proje felsefesi netleşir

### Seçenek B: Map First, Migrate Later
1. ✅ `documentation-map.yaml` (mevcut durum için)
2. ✅ Legacy migration
3. → Map güncelleme

**Avantaj:** Önce teknik sistem oturur, sonra strategic layer eklenir

---

**Hangisini öneriyorsun?**

Ben **Seçenek A**'yı öneriyorum çünkü:
- PRD güncel olmalı → Roadmap tutarlı olmalı
- Roadmap tutarlı olmalı → tasks.md align olmalı
- Strategy → Tech bağlantısı kurulmalı → Sonra map anlamlı olur

**Hangisiyle başlayalım? 🚀**

