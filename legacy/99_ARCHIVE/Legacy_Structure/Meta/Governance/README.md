# Governance

**Purpose:** Constitutional framework for YBIS project and YBIS_Dev meta-system.

This folder contains the governing rules, standards, and principles that all code and agents must follow.

---

## Three Constitutions

We maintain **three separate constitutions** for different scopes:

### 1. YBIS Project Constitution
**File:** `1_YBIS_PROJECT_CONSTITUTION.md`
**Scope:** Main YBIS project (apps/*, packages/*)
**Enforcement:** Zero tolerance - PR blocked if violated

**Covers:**
- Port/Adapter architecture
- UI Isolation
- Build for Scale, Ship Minimal
- Quality gates (no `any`, no `@ts-ignore`, etc.)
- Testing requirements
- Monorepo boundaries

**When to reference:** Working on main YBIS codebase

---

### 2. Universal Code Standards
**File:** `2_UNIVERSAL_CODE_STANDARDS.md`
**Scope:** ALL code (YBIS + YBIS_Dev)
**Enforcement:** CI + Code review

**Covers:**
- SOLID principles
- Clean Code (naming, functions, comments)
- Testing principles (test pyramid, FIRST)
- Security (OWASP Top 10)
- Performance principles
- Git workflow
- Documentation standards

**When to reference:** Writing ANY code, regardless of project

---

### 3. Development Governance
**File:** `3_DEVELOPMENT_GOVERNANCE.md`
**Scope:** YBIS_Dev meta-system
**Enforcement:** Agent coordination + tooling

**Covers:**
- Multi-agent coordination (Claude + Gemini)
- Communication protocols (TASK_BOARD, agent_messages.json)
- Conflict resolution
- Resource limits & safety
- Orchestration layers
- Agentic Prime Directives
- Dogfooding principles

**When to reference:** Working on YBIS_Dev itself, agent coordination

---

## Hierarchy

When rules conflict, they override in this order:

1. **User** (can override anything)
2. **Constitution 3** (Development Governance) - for meta-system work
3. **Constitution 1** (YBIS Project) - for project-specific rules
4. **Constitution 2** (Universal Standards) - baseline for all code

---

## Amendment Process

### For Constitutions 1 & 2 (Project + Universal):
1. Create RFC (Request for Comments)
2. Team discussion
3. User approval required
4. Update constitution + tooling

### For Constitution 3 (Development Governance):
1. Agent proposes in `agent_messages.json`
2. Other agents review (2 turns max)
3. If consensus → user approves
4. Constitution updated, version bumped

---

## Current Status

| Constitution | Version | Last Updated | Signed By |
|--------------|---------|--------------|-----------|
| YBIS Project | 1.0 | 2025-12-15 | User |
| Universal Standards | 1.0 | 2025-12-15 | User |
| Development Governance | 3.0 | 2025-12-15 | Claude ✅, Gemini ✅, User (pending) |

---

## Quick Reference

**For YBIS main project work:**
- Primary: Constitution 1 (YBIS Project)
- Supporting: Constitution 2 (Universal Standards)

**For YBIS_Dev meta-system work:**
- Primary: Constitution 3 (Development Governance)
- Supporting: Constitution 2 (Universal Standards)

**For any code review:**
- Check against Constitution 2 (Universal Standards) first
- Then check project-specific rules (Constitution 1 or 3)

---

## Legacy Files

The following files are superseded by the 3-constitution structure:
- `Constitution.md` → Merged into Constitution 1
- `AGENTIC_CONSTITUTION.md` → Merged into Constitution 3
- `MULTI_AGENT_CONSTITUTION.md` → Merged into Constitution 3
- `MULTI_AGENT_CONSTITUTION_V2.md` → Merged into Constitution 3

---

**Last Updated:** 2025-12-15
