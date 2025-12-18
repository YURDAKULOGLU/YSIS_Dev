# Summary: Documentation Homogenization Plan

This document outlines a two-phase plan to standardize all YBIS documentation.

## **Goal**
Ensure all documentation is consistent, maintainable, and automatically validated.

---

## **Phase 1: Manual Cleanup**

This phase focuses on bringing existing critical documents up to standard.

- **Task 1.1: Add YAML Frontmatter:** Ensure all key documents have a complete and accurate YAML frontmatter block (title, description, version, status, owner, last_updated, tags, related_docs).
- **Task 1.2: Standardize Formatting:** Enforce consistent use of headings (H1, H2, H3), ISO 8601 date format (`YYYY-MM-DD`), relative link paths, and language tags on code blocks.
- **Task 1.3: Fix Cross-References:** Find and fix all broken internal documentation links.
- **Task 1.4: Update "Last Updated" Dates:** Ensure the `last_updated` field in the frontmatter reflects the date of the last significant content change.

---

## **Phase 2: Automated Enforcement**

This phase focuses on building tools to maintain standards automatically.

- **Task 2.1: Frontmatter Validator (`validate-frontmatter.ts`):** A script to scan all markdown files and validate the presence and format of required YAML frontmatter fields. This will be integrated into the CI/CD pipeline.
- **Task 2.2: Link Checker (`check-doc-links.ts`):** A script to parse all markdown files and report any broken internal links.
- **Task 2.3: Auto-Update "Last Updated" Hook:** A pre-commit hook that automatically updates the `last_updated` field in the frontmatter of any modified markdown files.
- **Task 2.4: Documentation Health Dashboard (`docs-health-check.ts`):** A script that runs all validators and generates a summary report on the overall health and compliance of the project's documentation.

---

## **Status**

The plan's "Phase 1 Planning" is complete and is ready for execution, starting with the manual addition of frontmatter to documents.
