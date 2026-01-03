# Framework Intake Checklist

> Mandatory for all new Tier 1 & Tier 2 frameworks.
> File this document in docs/frameworks/<name>/INTAKE.md before adoption.

---

## 1. STRATEGIC FIT
- [ ] Problem: What specific problem does this solve?
- [ ] Redundancy: Does this overlap with existing tools?
- [ ] Sponsor: Which agent is the primary owner?

## 2. ARCHITECTURAL WIRING
- [ ] Single Entry Point: Does it support run_orchestrator.py?
- [ ] Provider Agnostic: Does it use BaseProvider?
- [ ] Statelessness: Does it use SQLite tasks.db?

## 3. OBSERVABILITY & SECURITY
- [ ] Tracing: Does it provide hooks for Langfuse?
- [ ] Logging: Does it use loguru?
- [ ] Secrets: Does it use Config.get_secret()?

## 4. MAINTAINABILITY
- [ ] License: Is it Open Source compatible?
- [ ] Rollback: How is it removed if it fails?
