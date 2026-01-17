# Documentation Style Guide

Purpose:
Keep docs consistent, skimmable, and cross-linkable for agents and humans.

## 1) File Naming
- UPPER_SNAKE_CASE for top-level canonical docs: CONSTITUTION.md, BOOTSTRAP_PLAN.md
- lower_snake_case is allowed for long optional docs, but be consistent.
- Avoid metaphors in filenames.

## 2) Headings
- Use `#` for title, then `##`, `###` progressively.
- Avoid deep nesting beyond `###` unless needed.

## 3) Cross-links
- Prefer relative links: `CONSTITUTION.md`, `AGENTS.md`
- Every doc must include a `References:` section near the top linking to relevant canonical docs.
- Use frontmatter `references:` list for machine-parsable links when helpful.

## 4) Micro-Notes & Doc Graph
- Keep rules in the canonical doc; use short micro-notes elsewhere with links back.
- Avoid duplicating normative statements across multiple docs.
- Run `python scripts/build_doc_graph.py` to generate `docs/reports/doc_graph.md` and `docs/reports/doc_graph.json`.

## 5) Definitions
- When introducing a term (e.g., "syscall", "gate", "lease"), define it once in:
  - INTERFACES.md or ARCHITECTURE.md
- Other docs should link back rather than re-defining differently.

## 6) Normative Language
Use strict language consistently:
- MUST / MUST NOT = non-negotiable
- SHOULD / SHOULD NOT = strong recommendation
- MAY = optional

## 7) Checklists
- Use checkboxes for audits and release steps.
- Ensure checklists have clear pass/fail criteria.

## 8) Examples
- Keep examples minimal and accurate.
- Prefer filesystem paths and artifact names that match ARCHITECTURE.md.        

## 9) Compatibility Notes
If a doc changes a contract or artifact:
- update MIGRATIONS.md
- add a short "Compatibility" section describing impact

## 10) Agent Friendliness
- Put critical rules near top.
- Keep sections short (5–12 lines each).
- Avoid huge prose blocks.

