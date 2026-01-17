# YBIS Dependency System

## Overview

The YBIS Dependency System analyzes code and documentation dependencies across the entire project. It tracks:
- Python imports
- Markdown references
- Frontmatter declarations
- Test relationships
- Configuration dependencies

## Quick Start

### 1. Scan Project

```bash
python scripts/dependency_cli.py scan
```

This scans the project and builds a dependency graph saved to `platform_data/dependency_graph.json`.

### 2. Analyze Impact

```bash
python scripts/dependency_cli.py impact src/ybis/constants.py
```

Shows what files are affected if you change a specific file.

### 3. Find Stale Files

```bash
python scripts/dependency_cli.py stale HEAD~10
```

Finds files that may be outdated due to recent changes.

### 4. List Dependencies

```bash
python scripts/dependency_cli.py list src/ybis/orchestrator/graph.py
```

Lists what a file depends on and what depends on it.

## MCP Tools

The dependency system is also available via MCP tools:

- `dependency_scan()` - Scan project and build graph
- `dependency_impact(file_path)` - Analyze impact of changes
- `dependency_stale(since)` - Find stale files
- `dependency_list(file_path)` - List dependencies

## Frontmatter Syntax

You can declare dependencies in file headers using YAML frontmatter. This is especially useful for non-code dependencies that can't be auto-detected.

### Basic Syntax

```markdown
---
depends_on:
  - file: "docs/API.md"
    type: "references"
    critical: true
  - file: "src/ybis/contracts.py"
    type: "uses_schema"
implements:
  - "docs/specs/TASK-123.md"
tests:
  - "tests/test_module.py"
---
```

### Full Example

```markdown
---
depends_on:
  - file: "docs/API.md"
    type: "references"
    critical: true
  - file: "src/ybis/contracts.py"
    type: "uses_schema"
    critical: false
  - file: "configs/profiles/default.yaml"
    type: "configures"
implements:
  - "docs/specs/TASK-123.md"
  - "docs/specs/FEATURE-X.md"
tests:
  - "tests/test_module.py"
  - "tests/integration/test_module.py"
---
```

### Dependency Types

- `imports` - Python/JS imports (auto-detected from code)
- `references` - Document references (links in markdown)
- `implements` - Implements a spec/requirement
- `tests` - Test files for this code
- `configures` - Configuration files
- `extends` - Base class/interface
- `uses_schema` - Uses a schema/contract
- `documents` - Documentation for this code

### Critical Dependencies

Mark dependencies as `critical: true` if changes to the target file require immediate updates to this file. The system will flag these in impact analysis.

Example:
```yaml
depends_on:
  - file: "src/ybis/constants.py"
    type: "imports"
    critical: true  # If constants.py changes, this file MUST be updated
```

### When to Use Frontmatter

Use frontmatter for:
- Non-code dependencies (docs referencing other docs)
- Implicit dependencies (config files, schemas)
- Test relationships (which tests cover which code)
- Spec implementations (which code implements which spec)

Code imports are automatically detected - you don't need to declare them in frontmatter.

## Examples

See `examples/dependency_example.py` for code examples.

## Graph Storage

The dependency graph is stored in `platform_data/dependency_graph.json`. You can:
- Delete it to force a rescan
- Inspect it manually (JSON format)
- Use it programmatically via `DependencyGraph` class

## Troubleshooting

**Graph not found:**
- Run `python scripts/dependency_cli.py scan` first

**Broken paths:**
- Delete `platform_data/dependency_graph.json` and rescan
- Check that relative imports are properly resolved

**Missing dependencies:**
- Ensure files use proper import syntax
- Add frontmatter declarations for non-code dependencies

