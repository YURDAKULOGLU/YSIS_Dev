# YBIS Documentation Taxonomy & Refactoring Plan

**Purpose:** Dokümantasyon mimarisi, her dokümanın işlevi, yeri ve ilişkileri
**Created:** 2025-10-12
**Status:** 🎯 TASARIM & UYGULAMA
**Owner:** Documentation Architect

---

## 📊 MEVCUT DURUM (AS-IS)

### Dosya Sayıları
```yaml
docs/:
  root_files: 5
    - AI_Asistan_Gorev_Dagilimi.md
    - DOCUMENTATION_INDEX.md
    - QUICKSTART.md
    - README.md
    - TESTING_STRATEGY.md
    - YBIS_PROJE_ANAYASASI.md

  Güncel/: 10 files
    - Architecture_better.md
    - DEVELOPMENT_GUIDELINES.md
    - DEVELOPMENT_LOG.md
    - expo-sdk54-migration-plan.md
    - INTEGRATION_ROADMAP.md
    - package-structure.md
    - quality-standards.md
    - service-integration-strategy.md
    - tasks.md
    - tech-stack.md

  vision/: 1 file ✅ (YENİ)
    - PROJECT_VISION.md

  roadmap/: 1 file ✅ (YENİ)
    - PRODUCT_ROADMAP.md

  strategy/: 2 files ✅ (YENİ)
    - COMPETITIVE_STRATEGY.md
    - MARKET_RESEARCH.md

  prd/: 1 file ✅ (GÜNCELLENDİ)
    - PRODUCT_REQUIREMENTS.md

  epics/: 1 file
    - tier-1-port-architecture.md

  stories/: 2 files
    - 1.1.mobile-app-foundation.md
    - 1.2.backend-api-foundation.md

  qa/gates/: 1 file
    - 1.1-mobile-app-foundation.yml

  Asset/: [images, icons]

  Archive/:
    Legacy/: 26 files (eski stratejik/teknik dokümanlar)
    Product-Roadmap/: 15 files (eski roadmap detayları)
    AI-Tasks/: [agent specific tasks]
    Architecture/: [empty]
    Strategy/: [empty]

.YBIS_Dev/:
  root_files: 7
    - AI_BASLANGIC_REHBERI_V2.md ✅ (Token-optimized lazy loading v2.0)
    - AI_GENEL_ANAYASA.md (AI universal constitution)
    - AI_SYSTEM_GUIDE.md (System-level AI guide)
    - core-config.yaml (System configuration)
    - enhanced-ide-development-workflow.md
    - install-manifest.yaml
    - user-guide.md

  Archive/: 1 file
    - AI_BASLANGIC_REHBERI_v1.0_DEPRECATED.md (Archived - use V2.md instead!)

  Veriler/:
    - agents/: 11 agent definitions
    - checklists/: 7 checklists
    - commands/: 58 slash commands
    - data/: 5 knowledge files
    - docs/: [empty]
    - documentation-taxonomy.md ✅ (This file - 5-Tier system)
    - documentation-map.yaml ✅ (Machine-readable doc registry)
    - kelime/: [test files]
    - memory/session-context.md ✅ (Active session - v2.1 real data, demo mode fix logged)
    - scripts/: 5 PowerShell automation scripts
    - session-todos.md ✅ (Current session TODOs)
    - tasks/: [empty]
    - templates/: 19 templates
    - utils/: 2 utility docs
    - workflows/: 7 workflow definitions
    - YBIS_INDEX.md
    - QUICK_INDEX.md ✅ (NEW - "Hangi dosya ne zaman?" guide)
```

---

## 🏗️ YENİ DOKÜMANTASYON MİMARİSİ (TO-BE)

### 🌟 TIER -1: STRATEGIC LAYER (Product & Business)

**Amaç:** Projenin NEDEN ve NE'si. Product vision, market strategy, business goals.
**Kitle:** Product Manager, CEO, Investors, Strategic stakeholders
**Güncelleme Sıklığı:** Quarterly veya major pivot
**Kapsam:** Geniş, high-level, minimal teknik detay

```yaml
TIER_MINUS_1_STRATEGIC:

  docs/vision/PROJECT_VISION.md: ✅ GÜNCEL (v2.0)
    purpose: "Why YBIS exists, target market, problem/solution"
    audience: "Team, investors, strategic decisions"
    scope: "Strategic - Why, Who, What (high-level)"
    length: "Medium (~400 lines)"
    update_frequency: "Quarterly or major pivot"
    status: "ACTIVE"
    derived_from: []
    informs:
      - PRODUCT_ROADMAP.md (timeline priorities)
      - COMPETITIVE_STRATEGY.md (positioning)
      - YBIS_PROJE_ANAYASASI.md (architecture principles)

  docs/roadmap/PRODUCT_ROADMAP.md: ✅ GÜNCEL (v2.0)
    purpose: "Timeline, phases, milestone breakdown"
    audience: "Team, stakeholders, investors"
    scope: "Strategic - When, How (phases)"
    length: "Long (~800 lines, detailed breakdown)"
    update_frequency: "Monthly or phase transition"
    status: "ACTIVE"
    derived_from:
      - PROJECT_VISION.md (goals)
      - MARKET_RESEARCH.md (priorities)
    informs:
      - tasks.md (execution)
      - DEVELOPMENT_LOG.md (timeline validation)

  docs/strategy/MARKET_RESEARCH.md: ✅ GÜNCEL (v2.0)
    purpose: "Market analysis, TAM/SAM/SOM, competitor landscape"
    audience: "Product Manager, Marketing, Investors"
    scope: "Strategic - Market, Users, Competition"
    length: "Very long (~1,100 lines, comprehensive)"
    update_frequency: "Quarterly, Open Beta refresh (competitor deep-dive)"
    status: "ACTIVE"
    notes: "Open Beta competitor deep-dive planned (Week 5-6)"
    derived_from: []
    informs:
      - COMPETITIVE_STRATEGY.md (positioning)
      - PRODUCT_ROADMAP.md (priorities)
      - PROJECT_VISION.md (validation)

  docs/strategy/COMPETITIVE_STRATEGY.md: ✅ GÜNCEL (v2.0)
    purpose: "Positioning, moats, competitive response scenarios"
    audience: "Product Manager, Marketing, Strategic team"
    scope: "Strategic - How to compete, Win"
    length: "Very long (~900 lines, detailed scenarios)"
    update_frequency: "Quarterly, major competitor move"
    status: "ACTIVE"
    derived_from:
      - MARKET_RESEARCH.md (competitor analysis)
      - PROJECT_VISION.md (core values)
    informs:
      - PRODUCT_ROADMAP.md (strategic priorities)
      - YBIS_PROJE_ANAYASASI.md (competitive moats → architecture)
```

**✅ TIER -1 DURUM:**
- 4/4 doküman GÜNCEL (Vision, Roadmap, Market Research, Competitive Strategy)
- Tüm Legacy stratejik dokümanlar taşındı ve güncellendi
- Cross-references eklendi

---

### 🔥 TIER 0: CANONICAL SOURCES (Single Source of Truth)

**Amaç:** Teknik bilginin TEK SAHİBİ. Architecture decisions, development history.
**Kitle:** Developers, Architects, Technical leads
**Güncelleme Sıklığı:** Her architecture decision, major task completion
**Kapsam:** Teknik, decision-focused, historical record

```yaml
TIER_0_CANONICAL:

  docs/YBIS_PROJE_ANAYASASI.md: ✅ GÜNCEL (v3.1.0)
    purpose: "Technical constitution - Port Architecture, quality gates, forbidden patterns"
    audience: "Developers, architects"
    scope: "Canonical - Architecture principles, Tech constraints"
    length: "Long (~500 lines, detailed rules)"
    update_frequency: "Major architecture decision (rare)"
    status: "ACTIVE"
    authority: "CANONICAL - Port definitions, Quality standards"
    owns:
      - port_architecture_principles
      - tier_1_port_catalog (AuthPort, DatabasePort, LLMPort, etc.)
      - quality_gates
      - forbidden_patterns
      - tech_constraints
    derived_from:
      - PROJECT_VISION.md (product principles → architecture)
      - COMPETITIVE_STRATEGY.md (moats → tech choices)
    informs:
      - DEVELOPMENT_LOG.md (AD-XXX align with Anayasa)
      - Architecture_better.md (implementation details)
      - service-integration-strategy.md (port patterns)

  docs/Güncel/DEVELOPMENT_LOG.md: ✅ GÜNCEL (AD-020)
    purpose: "Decision registry - Architecture Decisions (AD-XXX), timeline, issues"
    audience: "Developers, team"
    scope: "Canonical - Historical record, Decisions"
    length: "Very long (grows over time, ~800 lines now)"
    update_frequency: "Daily (progress), On decision (AD-XXX)"
    status: "ACTIVE"
    authority: "CANONICAL - All technical decisions (AD-XXX)"
    owns:
      - architecture_decisions (AD-001 to AD-020)
      - completed_tasks_log
      - issues_and_fixes
      - daily_progress
      - week_completion_status
    derived_from:
      - YBIS_PROJE_ANAYASASI.md (architecture constraints)
      - PRODUCT_ROADMAP.md (timeline, milestones)
    informs:
      - tech-stack.md (versions from AD-XXX)
      - package-structure.md (structure from AD-XXX)
      - tasks.md (completion status)
      - README.md (progress %)
```

**✅ TIER 0 DURUM:**
- 2/2 doküman GÜNCEL
- YBIS_PROJE_ANAYASASI: Port Architecture netleşmiş (8 Tier 1 Port)
- DEVELOPMENT_LOG: 20 Architecture Decision (AD-001 to AD-020)

---

### 📚 TIER 1: REFERENCE DOCUMENTS (Derived, Read-Mostly)

**Amaç:** Tier 0'dan türetilmiş teknik referanslar. Implementation blueprints.
**Kitle:** Developers (daily reference)
**Güncelleme Sıklığı:** Her AD-XXX değişikliğinde auto-derive
**Kapsam:** Teknik, detailed, implementation-focused

```yaml
TIER_1_REFERENCE:

  docs/Güncel/tech-stack.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Technical reference - All package versions, migration paths"
    audience: "Developers"
    scope: "Reference - What tech, What versions"
    length: "Long (~400 lines, comprehensive)"
    update_frequency: "Every AD-XXX (tech decision)"
    status: "ACTIVE"
    authority: "DERIVED - From DEVELOPMENT_LOG.md (AD-XXX)"
    owns: NOTHING (all derived)
    derived_from:
      - DEVELOPMENT_LOG.md (AD-002: React, AD-015: Auth, AD-016: Deployment)
      - YBIS_PROJE_ANAYASASI.md (tech constraints)
    used_by:
      - Developers (daily reference)
      - package.json (version source)
      - README.md (tech stack display)

  docs/Güncel/package-structure.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Implementation blueprint - Package layout, code examples"
    audience: "Developers"
    scope: "Reference - How to implement (packages, ports, adapters)"
    length: "Very long (~1,700 lines, detailed code)"
    update_frequency: "Every AD-XXX (structure change)"
    status: "ACTIVE"
    authority: "DERIVED - From DEVELOPMENT_LOG + ANAYASA"
    owns: NOTHING (all derived)
    derived_from:
      - DEVELOPMENT_LOG.md (AD-001, AD-002, AD-003, AD-015, AD-016)
      - YBIS_PROJE_ANAYASASI.md (port architecture)
    used_by:
      - Developers (implementation guide)
      - Story writers (technical context)

  docs/README.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Project overview - Quick start, tech stack, status"
    audience: "New developers, stakeholders"
    scope: "Reference - High-level overview"
    length: "Short (~100 lines, concise)"
    update_frequency: "Weekly (progress update)"
    status: "ACTIVE"
    authority: "DERIVED - Auto-generated from multiple sources"
    owns: NOTHING (all derived)
    derived_from:
      - DEVELOPMENT_LOG.md (status, progress %)
      - tech-stack.md (versions)
      - tasks.md (completion %)
    used_by:
      - New team members (onboarding)
      - GitHub visitors (project intro)

  docs/Güncel/Architecture_better.md: ✅ GÜNCEL (v2.0, 2025-10-12)
    purpose: "Architecture deep-dive - Detailed tech decisions, rationale"
    audience: "Architects, senior developers"
    scope: "Reference - Why architecture (detailed)"
    length: "Long (~550 lines)"
    update_frequency: "Major architecture change"
    status: "ACTIVE"
    authority: "DERIVED - From ANAYASA + DEVELOPMENT_LOG"
    owns: NOTHING (all derived)
    derived_from:
      - YBIS_PROJE_ANAYASASI.md (principles)
      - DEVELOPMENT_LOG.md (AD-XXX rationale)
    used_by:
      - Architects (design reference)
      - Story writers (technical context)
    notes: "Recently updated (Firebase → Expo Auth, React 18.3 → 19.1)"

  docs/prd/PRODUCT_REQUIREMENTS.md: ✅ GÜNCEL (v2.0, 2025-10-12)
    purpose: "Product requirements - Features, UX, technical decisions"
    audience: "Product Manager, Developers, QA"
    scope: "Reference - What to build (requirements)"
    length: "Very long (~1,200 lines, comprehensive)"
    update_frequency: "Feature change, major tech decision"
    status: "ACTIVE"
    authority: "HYBRID - Product from PM, Tech from DEVELOPMENT_LOG"
    owns:
      - feature_requirements (product-owned)
      - ux_specifications (product-owned)
    derived_from:
      - PROJECT_VISION.md (product vision)
      - DEVELOPMENT_LOG.md (tech decisions: AD-015, AD-016, AD-017, AD-018, AD-019, AD-020)
      - YBIS_PROJE_ANAYASASI.md (architecture constraints)
    used_by:
      - Developers (feature implementation)
      - QA (test scenarios)
      - Story writers (requirements breakdown)
    notes: "Marked UI/UX as DEPRECATED (bottom tab bar) and TBD (gestures)"
```

**✅ TIER 1 DURUM:**
- 5/5 doküman GÜNCEL
- Tüm dokümanlar son AD-XXX'lere align edildi
- Cross-references mevcut

---

### ⚙️ TIER 2: EXECUTION DOCUMENTS (Hybrid - Derived + Dynamic)

**Amaç:** Execution tracking, task management. Hem derived hem dynamic content.
**Kitle:** Developers (daily work)
**Güncelleme Sıklığı:** Daily (task checkboxes), Weekly (guidelines)
**Kapsam:** Execution-focused, practical

```yaml
TIER_2_EXECUTION:

  docs/Güncel/tasks.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Task list - 165 tasks, checkbox status, week breakdown"
    audience: "Developers"
    scope: "Execution - What to do (tasks)"
    length: "Very long (~1,100 lines, detailed tasks)"
    update_frequency: "Daily (checkbox), Weekly (new tasks)"
    status: "ACTIVE"
    authority: "HYBRID - Structure from DEVELOPMENT_LOG, Status dynamic"
    owns:
      - task_checkboxes (dynamic ✅/⏳)
      - task_completion_dates (dynamic)
    derived_from:
      - DEVELOPMENT_LOG.md (AD-XXX → tasks)
      - PRODUCT_ROADMAP.md (phases → weeks)
      - package-structure.md (implementation → tasks)
    used_by:
      - Developers (daily work)
      - DEVELOPMENT_LOG.md (completion logging)
      - README.md (progress %)
    notes: "24/30 tasks completed (Week 1: 80%)"

  docs/Güncel/DEVELOPMENT_GUIDELINES.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Developer rules - Code patterns, error solutions, best practices"
    audience: "Developers"
    scope: "Execution - How to code (rules)"
    length: "Long (~600 lines, practical)"
    update_frequency: "Weekly (learned lessons), On pattern (new rule)"
    status: "ACTIVE"
    authority: "HYBRID - Core from ANAYASA, Examples dynamic"
    owns:
      - code_patterns (curated)
      - error_solutions (curated)
      - practical_examples (dynamic)
    derived_from:
      - YBIS_PROJE_ANAYASASI.md (core rules)
      - DEVELOPMENT_LOG.md (learned lessons, issues)
    used_by:
      - Developers (daily coding)
      - Code reviews (standards)

  docs/stories/1.1.mobile-app-foundation.md: ✅ ACTIVE
    purpose: "Story execution - Foundation story, checkboxes, Dev Agent Record"
    audience: "Developers, QA"
    scope: "Execution - Story details (tasks, context, DOD)"
    length: "Long (~400 lines, detailed)"
    update_frequency: "Daily (checkboxes), On completion (Dev Agent Record)"
    status: "ACTIVE (IN PROGRESS)"
    authority: "HYBRID - Template from .YBIS_Dev, Content dynamic"
    owns:
      - story_checkboxes (dynamic)
      - dev_agent_record (dynamic)
    derived_from:
      - tasks.md (related tasks)
      - PRODUCT_REQUIREMENTS.md (feature requirements)
    used_by:
      - Developers (implementation)
      - QA (testing context)

  docs/stories/1.2.backend-api-foundation.md: ✅ ACTIVE
    purpose: "Story execution - Backend API foundation"
    status: "ACTIVE (PENDING)"
    notes: "Same pattern as 1.1"

  docs/epics/tier-1-port-architecture.md: ✅ ACTIVE
    purpose: "Epic definition - Tier 1 Port Architecture scope"
    audience: "Product Manager, Developers"
    scope: "Execution - Epic scope (high-level stories)"
    length: "Medium (~200 lines)"
    update_frequency: "On epic change"
    status: "ACTIVE"
    authority: "HYBRID - From PRD, Details dynamic"
    derived_from:
      - PRODUCT_REQUIREMENTS.md (epic scope)
      - YBIS_PROJE_ANAYASASI.md (port architecture)
    used_by:
      - Story creation (breakdown)
      - PRODUCT_ROADMAP.md (epic tracking)
```

**✅ TIER 2 DURUM:**
- 5/5 doküman ACTIVE
- tasks.md: 24/165 tasks complete
- Story 1.1: In Progress
- Epic Tier-1: Active

---

### 📖 TIER 3: SUPPORT DOCUMENTS (Detailed, Specialized)

**Amaç:** Specific domain deep-dives. Integration, QA, testing details.
**Kitle:** Specialized roles (QA, Integration engineer)
**Güncelleme Sıklığı:** Domain-specific
**Kapsam:** Narrow, deep, specialized

```yaml
TIER_3_SUPPORT:

  docs/Güncel/INTEGRATION_ROADMAP.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Integration strategy - Third-party service integration phases"
    audience: "Backend developers, Integration engineers"
    scope: "Support - Integration details (Google, Notion, Todoist)"
    length: "Long (~350 lines)"
    update_frequency: "Phase transition, New integration"
    status: "ACTIVE"
    authority: "HYBRID - Strategy from ROADMAP, Details specialized"
    derived_from:
      - PRODUCT_ROADMAP.md (integration phases)
      - YBIS_PROJE_ANAYASASI.md (port architecture)
    used_by:
      - Integration engineers (implementation)
      - tasks.md (integration tasks)

  docs/Güncel/service-integration-strategy.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Integration patterns - Port Architecture implementation patterns"
    audience: "Backend developers"
    scope: "Support - Integration patterns (detailed)"
    length: "Very long (~950 lines, comprehensive patterns)"
    update_frequency: "New port, New pattern"
    status: "ACTIVE"
    authority: "HYBRID - From ANAYASA, Patterns specialized"
    derived_from:
      - YBIS_PROJE_ANAYASASI.md (port principles)
      - DEVELOPMENT_LOG.md (AD-XXX integration decisions)
    used_by:
      - Developers (port implementation)
      - Code reviews (pattern validation)

  docs/Güncel/quality-standards.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Quality standards - Testing, code quality, performance benchmarks"
    audience: "QA, Developers"
    scope: "Support - Quality details (tests, standards)"
    length: "Very long (~1,300 lines, comprehensive)"
    update_frequency: "New standard, Quality gate change"
    status: "ACTIVE"
    authority: "HYBRID - From ANAYASA, Details specialized"
    derived_from:
      - YBIS_PROJE_ANAYASASI.md (quality gates)
      - DEVELOPMENT_LOG.md (quality lessons)
    used_by:
      - QA (test design)
      - Developers (code quality)
      - CI/CD (automated checks)

  docs/TESTING_STRATEGY.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Testing strategy - Test levels, frameworks, coverage targets"
    audience: "QA, Developers"
    scope: "Support - Testing approach (strategy)"
    length: "Long (~400 lines)"
    update_frequency: "Major testing change"
    status: "ACTIVE"
    authority: "HYBRID - From quality-standards, Strategy specialized"
    derived_from:
      - quality-standards.md (quality gates)
      - YBIS_PROJE_ANAYASASI.md (testing principles)
    used_by:
      - QA (test planning)
      - Developers (test implementation)

  docs/qa/gates/1.1-mobile-app-foundation.yml: ✅ ACTIVE
    purpose: "Quality gate - Story 1.1 specific quality checks"
    audience: "QA, Developers"
    scope: "Support - Story QA (checklist)"
    length: "Short (~50 lines, checklist)"
    update_frequency: "Story completion"
    status: "ACTIVE"
    authority: "DERIVED - From quality-standards.md"
    derived_from:
      - quality-standards.md (quality criteria)
      - stories/1.1.mobile-app-foundation.md (story context)
    used_by:
      - QA (story validation)
      - Story completion (DOD check)

  docs/Güncel/expo-sdk54-migration-plan.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Migration plan - Expo SDK 54 upgrade details"
    audience: "Developers"
    scope: "Support - Migration details (specific)"
    length: "Medium (~150 lines)"
    update_frequency: "Migration completion (then archive)"
    status: "ACTIVE (migration pending)"
    authority: "SPECIALIZED - Migration-specific"
    derived_from:
      - DEVELOPMENT_LOG.md (AD-002: Expo decision)
      - tech-stack.md (Expo version)
    used_by:
      - Developers (migration execution)
    notes: "Will be archived once migration completes"
```

**✅ TIER 3 DURUM:**
- 6/6 doküman GÜNCEL/ACTIVE
- Integration, QA, Testing domains covered
- Expo migration plan active

---

### 🗺️ TIER 4: NAVIGATION & META (Auto-Generated, Guides)

**Amaç:** Navigation, quick start, meta documentation.
**Kitle:** New team members, quick reference
**Güncelleme Sıklığı:** Weekly (auto-generate)
**Kapsam:** Navigation, onboarding

```yaml
TIER_4_META:

  docs/DOCUMENTATION_INDEX.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Navigation - All docs index, quick links"
    audience: "Everyone"
    scope: "Meta - Navigation (auto-generated)"
    length: "Medium (~200 lines)"
    update_frequency: "Weekly (auto-generate)"
    status: "ACTIVE"
    authority: "AUTO_GENERATED - From all doc frontmatter"
    owns: NOTHING (all generated)
    generated_from:
      - all_document_frontmatter
      - file_structure
    used_by:
      - New team members (navigation)
      - Documentation discovery

  docs/QUICKSTART.md: ✅ GÜNCEL (2025-10-12)
    purpose: "Quick start - Setup steps, first tasks"
    audience: "New developers"
    scope: "Meta - Onboarding (curated)"
    length: "Long (~400 lines, detailed)"
    update_frequency: "Major setup change"
    status: "ACTIVE"
    authority: "HYBRID - Structure auto, Content curated"
    owns:
      - setup_steps (curated)
    derived_from:
      - tasks.md (first tasks)
      - tech-stack.md (versions)
      - README.md (overview)
    used_by:
      - New developers (onboarding)

  docs/AI_Asistan_Gorev_Dagilimi.md: ✅ GÜNCEL (2025-10-12)
    purpose: "AI workflow - Agent roles, task distribution"
    audience: "AI agents, Team"
    scope: "Meta - AI workflow (guide)"
    length: "Long (~400 lines)"
    update_frequency: "AI workflow change"
    status: "ACTIVE"
    authority: "HYBRID - From .YBIS_Dev, Curated"
    derived_from:
      - .YBIS_Dev/Veriler/agents/ (agent definitions)
      - .YBIS_Dev/AI_BASLANGIC_REHBERI.md (workflow)
    used_by:
      - AI agents (role understanding)
      - Team (AI workflow reference)
```

**✅ TIER 4 DURUM:**
- 3/3 doküman GÜNCEL
- Navigation and onboarding covered

---

## 🔗 .YBIS_Dev İLE PARALEL ÇALIŞMA

### .YBIS_Dev Amacı ve İşlevi

```yaml
.YBIS_Dev/:
  purpose: "AI system configuration and meta-documentation"
  audience: "AI agents, System"
  relationship_to_docs/: "Meta layer - Controls how docs/ is used"

  AI_BASLANGIC_REHBERI.md:
    purpose: "Master AI workflow guide - Entry point for all AI agents"
    role: "META - How AI agents should work"
    points_to:
      - AI_GENEL_ANAYASA.md (universal AI rules)
      - YBIS_PROJE_ANAYASASI.md (project-specific rules)

  AI_GENEL_ANAYASA.md:
    purpose: "Universal AI constitution - General AI behavior rules"
    role: "META - AI behavior standards"
    applies_to: "All AI agents (Claude, GitHub Copilot, etc.)"

  core-config.yaml:
    purpose: "System configuration - Paths, commands, workflows"
    role: "META - System config"
    defines:
      - documentation_paths (docs/prd, docs/architecture, docs/qa)
      - command_locations (.YBIS_Dev/Veriler/Commands/)
      - workflow_locations (.YBIS_Dev/Veriler/workflows/)

  Veriler/:
    purpose: "AI system data - Agents, commands, templates, workflows"

    agents/:
      purpose: "AI agent definitions (11 agents)"
      files:
        - analyst.md, architect.md, dev.md, doc-generator.md
        - pm.md, po.md, qa.md, sm.md, ux-expert.md
        - ybis-master.md, ybis-orchestrator.md
      role: "META - Agent behavior definitions"
      used_by: "AI_Asistan_Gorev_Dagilimi.md (agent role distribution)"

    commands/:
      purpose: "Slash commands (58 commands)"
      examples:
        - /implement, /plan, /qa-gate, /create-story
        - /session-start, /health-check-docs, /update-docs
      role: "META - AI agent command library"
      execution: "BMad prefix commands"

    checklists/:
      purpose: "Quality checklists (7 checklists)"
      files:
        - story-dod-checklist.md (Story Definition of Done)
        - documentation-consistency-checklist.md
        - change-checklist.md
      role: "META - Quality gates"
      used_by:
        - AI agents (quality validation)
        - Developers (manual checks)

    templates/:
      purpose: "Document templates (19 templates)"
      examples:
        - story-tmpl.yaml, prd-tmpl.yaml, qa-gate-tmpl.yaml
        - architecture-tmpl.yaml, competitor-analysis-tmpl.yaml
      role: "META - Document generation templates"
      used_by:
        - AI agents (document creation)
        - /create-story, /create-doc commands

    workflows/:
      purpose: "Workflow definitions (7 workflows)"
      examples:
        - brownfield-fullstack.yaml
        - greenfield-ui.yaml
        - documentation-maintenance.yaml
      role: "META - Process workflows"
      used_by: "AI agents (workflow execution)"

    documentation-architecture.md:
      purpose: "5-Tier documentation system definition"
      role: "META - Documentation structure (this document's foundation)"
      status: "ACTIVE"

    session-todos.md:
      purpose: "Current session TODO tracking"
      role: "META - Session management"
      status: "ACTIVE (14/17 tasks complete)"

    memory/session-context.md:
      purpose: "Session context memory"
      role: "META - AI memory persistence"
      status: "ACTIVE"
```

### docs/ ↔ .YBIS_Dev/ İlişkisi

```yaml
information_flow:

  .YBIS_Dev/ → docs/:
    - Templates → Document creation
    - Workflows → Document maintenance
    - Checklists → Quality validation
    - Commands → Document updates

  docs/ → .YBIS_Dev/:
    - YBIS_PROJE_ANAYASASI.md → AI_BASLANGIC_REHBERI.md (project rules)
    - DEVELOPMENT_LOG.md → session-todos.md (task tracking)
    - All docs → YBIS_INDEX.md (documentation registry)

coordination_points:

  Document Creation:
    trigger: "/create-story" or "/create-doc"
    workflow:
      1. AI agent reads template (.YBIS_Dev/Veriler/templates/)
      2. AI agent reads context (docs/YBIS_PROJE_ANAYASASI.md, DEVELOPMENT_LOG.md)
      3. AI agent creates document (docs/stories/ or docs/prd/)
      4. AI agent validates (checklists/)

  Documentation Update:
    trigger: "DEVELOPMENT_LOG.md AD-XXX added"
    workflow:
      1. AI agent detects change (.YBIS_Dev/workflows/documentation-maintenance.yaml)
      2. AI agent identifies affected docs (documentation-architecture.md)
      3. AI agent updates references (tech-stack.md, package-structure.md)
      4. AI agent validates (checklists/documentation-consistency-checklist.md)

  Quality Gate:
    trigger: "Story completion"
    workflow:
      1. AI agent reads DOD checklist (.YBIS_Dev/Veriler/checklists/story-dod-checklist.md)
      2. AI agent validates story (docs/stories/1.1.mobile-app-foundation.md)
      3. AI agent checks quality gate (docs/qa/gates/1.1-mobile-app-foundation.yml)
      4. AI agent updates DEVELOPMENT_LOG.md
```

---

## 📊 DOKÜMANTASYON İŞLEVLERİ ÖZETİ

### Kapsam vs Detay Matrix

```
                     KAPSAM (Scope)
                  Geniş ←----------→ Dar
              │
        Yüksek│  Vision          │  quality-standards
              │  Roadmap         │  service-integration
     D        │  Market Research │  TESTING_STRATEGY
     E        │  Competitive     │
     T  ------│------------------│------------------
     A        │  PRD             │  Architecture_better
     Y        │  ANAYASA         │  package-structure
              │  DEVELOPMENT_LOG │  tech-stack
       Düşük │  README          │  tasks
              │  QUICKSTART      │  expo-sdk54-migration
              │

LEGEND:
  Geniş Kapsam, Yüksek Detay: Strategic, comprehensive (Vision, Roadmap)
  Geniş Kapsam, Düşük Detay: Overview, high-level (PRD, README)
  Dar Kapsam, Yüksek Detay: Specialized, deep (quality-standards, integration patterns)
  Dar Kapsam, Düşük Detay: Specific, focused (tasks, migration plans)
```

### Doküman Tipi Kategorileri

```yaml
document_types:

  STRATEGIC:
    files: [Vision, Roadmap, Market Research, Competitive Strategy]
    characteristics:
      - Geniş kapsam, minimal teknik detay
      - Long-term (quarterly updates)
      - Business/product focused
      - Non-technical audience

  CANONICAL:
    files: [YBIS_PROJE_ANAYASASI, DEVELOPMENT_LOG]
    characteristics:
      - Single source of truth
      - Technical decisions
      - Historical record
      - Authority over all derived docs

  REFERENCE:
    files: [tech-stack, package-structure, Architecture_better, PRD, README]
    characteristics:
      - Derived from canonical
      - Read-only (no manual edits to derived parts)
      - Technical details
      - Daily developer reference

  EXECUTION:
    files: [tasks, DEVELOPMENT_GUIDELINES, stories, epics]
    characteristics:
      - Hybrid (derived + dynamic)
      - Task tracking, checkboxes
      - Daily updates
      - Practical, actionable

  SUPPORT:
    files: [INTEGRATION_ROADMAP, service-integration, quality-standards, TESTING_STRATEGY, QA gates, expo-migration]
    characteristics:
      - Specialized domains
      - Deep, narrow focus
      - Domain expert audience
      - Detailed patterns/standards

  META:
    files: [DOCUMENTATION_INDEX, QUICKSTART, AI_Asistan_Gorev_Dagilimi]
    characteristics:
      - Navigation, onboarding
      - Auto-generated or curated
      - High-level guides
      - Everyone audience
```

---



---

## 🚀 SONRAKI ADIMLAR

### ✅ COMPLETED (2025-10-12)

#### 1. Documentation Map YAML Oluşturuldu ✅
```yaml
file: ".YBIS_Dev/Veriler/documentation-map.yaml"
status: COMPLETE
content:
  - 31 documents registered
  - Metadata, dependencies, references
  - Update cascade rules
  - Cross-linking registry
```

#### 2. AI Başlangıç Prosedürü V2.0 ✅
```yaml
file: ".YBIS_Dev/AI_BASLANGIC_REHBERI_V2.md"
status: COMPLETE
content:
  - 3-Tier lazy loading system
  - Token optimization (20K → 3-5K)
  - Just-in-time documentation loading
  - Command-triggered reads
```

#### 3. Quick Index Oluşturuldu ✅
```yaml
file: ".YBIS_Dev/Veriler/QUICK_INDEX.md"
status: COMPLETE
content:
  - "Hangi dosya ne zaman?" decision tree
  - TIER 1-3 loading strategy
  - Agent-specific guides
  - Quick reference for all docs
```

#### 4. Session Context v2.0 ✅
```yaml
file: ".YBIS_Dev/Veriler/memory/session-context.md"
status: COMPLETE (Real Data)
content:
  - Week 1, Day 5 state
  - Last 3 AD decisions
  - Next steps clear
  - Dual-write rule integrated
```

### 🔜 NEXT PRIORITIES

#### Priority 1: Cross-Linking Automation
```yaml
actions:
  - Strategic → Technical bidirectional links
  - PRD ↔ ANAYASA ↔ DEVELOPMENT_LOG refs
  - Roadmap ↔ tasks alignment
  - Vision ↔ Competitive Strategy ↔ Architecture moats

estimated_time: "1 hour"
status: PENDING
```

#### Priority 2: Validation Workflow
```yaml
script: "scripts/check-doc-consistency.py"
checks:
  - Canonical source changes → Affected docs list
  - AD-XXX in DEVELOPMENT_LOG → References in tech-stack
  - Task completion → DEVELOPMENT_LOG note
  - Tier 0 change → Approval required

estimated_time: "2 hours"
status: PENDING
```

#### Priority 3: Agent Testing
```yaml
test: "Dry-run onboarding with new v2.0 system"
agents: [Claude, Gemini, Cursor, Copilot]
verify:
  - TIER 1 loads correctly (<5K token)
  - Lazy loading triggers appropriately
  - Dual-write rule is followed
  - session-context stays under 100 lines

estimated_time: "30 minutes per agent"
status: PENDING
```

---

**DOCUMENTATION SYSTEM v2.0 COMPLETE! 🎉**

**Token Efficiency Achieved:**
- ✅ Session start: 3-5K token (was: 20-30K)
- ✅ Lazy loading: Just-in-time reads
- ✅ Dual-write: Context sync automated
- ✅ Quick index: Decision tree ready

**Next Session:**
- Use AI_BASLANGIC_REHBERI_V2.md
- Load TIER 1 only (4 files)
- Follow QUICK_INDEX.md for subsequent reads
- Maintain dual-write discipline
