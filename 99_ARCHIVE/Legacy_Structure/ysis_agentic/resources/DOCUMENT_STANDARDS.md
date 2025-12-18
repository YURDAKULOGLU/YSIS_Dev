---
title: "YBIS Document Standards"
description: "Defines the mandatory metadata and formatting standards for all key documentation files within the YBIS project."
version: "1.0.0"
status: "active"
owner: "@ybis-master"
last_updated: "2025-10-26"
tags: ["standards", "documentation", "frontmatter", "metadata"]
related_docs:
  - "./AI_GENEL_ANAYASA.md"
---
# YBIS Document Standards

**Version:** 1.0
**Status:** ACTIVE
**Owner:** @ybis-master
**Purpose:** To define the mandatory metadata and formatting standards for all key documentation files within the YBIS project.

---

## 1. Mandatory YAML Frontmatter

To ensure all documents are machine-readable and provide immediate context to AI agents and developers, every key Markdown document (`.md`) in this project MUST begin with a YAML frontmatter block.

This block acts as an "ID card" for the document.

### 1.1 Standard Frontmatter Template

```yaml
---
title: "Clear and Concise Document Title"
description: "A brief, one-sentence summary of the document's purpose and content."
version: 1.0.0 # Use Semantic Versioning (Major.Minor.Patch)
status: "draft | active | deprecated | idea" # Choose one
owner: "@architect | @pm | @ybis-master | etc." # The primary agent/role responsible for this doc
last_updated: "YYYY-MM-DD" # The date of the last significant modification
tags: ["tag1", "tag2", "relevant-keyword"] # Helps with search and categorization
related_docs:
  - "./path/to/related_document.md" # List of directly related documents
---
```

### 1.2 Field Definitions

-   **`title` (Required):** The official title of the document.
-   **`description` (Required):** A short, clear summary. An AI should be able to understand the file's purpose from this alone.
-   **`version` (Required):** The document's version number, following SemVer.
    -   `PATCH` (1.0.x): Typos, formatting fixes.
    -   `MINOR` (1.x.0): Adding content, clarifications that don't change the core meaning.
    -   `MAJOR` (x.0.0): Breaking changes, fundamental shifts in strategy or architecture.
-   **`status` (Required):** The current state of the document.
    -   `draft`: A work-in-progress, not yet official.
    -   `active`: The current, official version to be used.
    -   `deprecated`: Outdated and scheduled for archival. Should not be used.
    -   `idea`: A brainstorming or proposal document, not yet a formal plan.
-   **`owner` (Required):** The agent or role primarily responsible for the content's accuracy and maintenance.
-   **`last_updated` (Required):** The date of the last meaningful change.
-   **`tags` (Recommended):** Keywords that help categorize the document (e.g., "architecture", "protocol", "strategy", "constitution").
-   **`related_docs` (Optional):** A list of paths to other documents that are essential for understanding this one.

## 2. Enforcement

-   **New Documents:** All agent tasks that create documents (e.g., `create-doc`) MUST be updated to use this frontmatter template by default.
-   **Existing Documents:** Key documents will be retrofitted with this frontmatter.
-   **Validation:** The `documentation-maintenance.yaml` workflow will be updated to include a step that validates frontmatter compliance.

This standard is mandatory for all documents in the `docs/`, `.YBIS_Dev/Veriler/`, and other key informational directories.