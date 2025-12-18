# AI Agent Protocols

**Purpose:** Defines the mandatory and optional context loading protocols for all YBIS_Dev agents.
**System:** Tiered Context Loading (Tier 1 Baseline -> Tier 2 Task-Specific)

---

## 1. Context Loading Protocol

All agents MUST follow this two-phase loading process to ensure alignment with the "Single Source of Truth".

### Phase 1: Baseline Context (MANDATORY)
*Load these files immediately upon activation. Do not ask for permission.*

| Document | Path | Purpose |
| :--- | :--- | :--- |
| **Constitution** | `docs/YBIS_PROJE_ANAYASASI.md` | Core architectural principles, quality gates, forbidden patterns. |
| **Decisions** | `docs/DEVELOPMENT_LOG.md` | Historical architecture decisions (AD-XXX) and current system state. |
| **Project Structure** | `docs/package-structure.md` | Overview of the monorepo structure and package responsibilities. |
| **Taxonomy** | `.YBIS_Dev/Veriler/documentation-taxonomy.md` | Map of all documentation to understand where to find things. |

### Phase 2: Task-Specific Context (DYNAMIC)
*Propose loading these files based on the task type. Wait for user confirmation.*

#### Mode: ARCHITECTURE (Agent: Architect)
*Use when designing new features, refactoring systems, or planning migrations.*
- `docs/tech-stack.md`: Current technology versions and constraints.
- `docs/service-integration-strategy.md`: Patterns for service communication.
- `docs/prd/PRODUCT_REQUIREMENTS.md`: Business requirements and user needs.
- `docs/vision/PROJECT_VISION.md`: Long-term project goals.

#### Mode: DEVELOPMENT (Agent: Developer)
*Use when writing code, fixing bugs, or implementing features.*
- `docs/DEVELOPMENT_GUIDELINES.md`: Coding standards, patterns, and error solutions.
- `docs/tech-stack.md`: Library versions to avoid compatibility issues.
- `docs/tasks.md`: Current task list and status.
- `shared/YBIS_STANDARDS_CHEATSHEET.md`: Quick reference for code style.

#### Mode: QA & TESTING (Agent: QA)
*Use when writing tests, validating features, or auditing code.*
- `docs/quality-standards.md`: Definitions of "Done", testing requirements.
- `docs/testing/TEST_STRATEGY.md` (if exists): Testing methodologies.
- `docs/prd/PRODUCT_REQUIREMENTS.md`: Acceptance criteria.

#### Mode: STRATEGY (Agent: Product Owner)
*Use for roadmap planning, market analysis, and feature prioritization.*
- `docs/roadmap/PRODUCT_ROADMAP.md`: Timeline and milestones.
- `docs/strategy/MARKET_RESEARCH.md`: Competitor and market analysis.
- `docs/strategy/COMPETITIVE_STRATEGY.md`: Positioning and differentiation.

---

## 2. Operational Rules

1.  **Read-Only Baseline:** Agents must treat Phase 1 documents as READ-ONLY unless explicitly tasked with updating them.
2.  **Source of Truth:** If a conflict exists between documents, Phase 1 documents (Tier 0) always take precedence over Phase 2 documents.
3.  **Missing Files:** If a required document is missing, report it immediately and fall back to `README.md`.
4.  **Update Protocol:** When generating new artifacts (code or docs), always cross-reference `documentation-architecture.md` to ensure correct placement and ownership.

---

## 3. Command Execution Protocol

When executing commands defined in agent profiles (e.g., `*create-doc`):

1.  **Resolve Dependency:** Locate the template or script in `.YBIS_Dev/Veriler/{type}/{name}`.
2.  **Load Context:** Ensure relevant Phase 2 context is loaded.
3.  **Execute:** Run the command.
4.  **Validate:** Check output against `YBIS_PROJE_ANAYASASI.md` constraints.
