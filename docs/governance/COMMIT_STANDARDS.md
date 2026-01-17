# COMMIT STANDARDS

> Commit'ler hikaye anlatır. Kötü commit = Kötü hikaye.

**References:**
- DISCIPLINE.md
- CODE_STANDARDS.md

---

## 1. Commit Message Format

```
<type>(<scope>): <subject>

[body]

[footer]
```

### 1.1 Type (Zorunlu)

| Type | Description | Semver |
|------|-------------|--------|
| `feat` | New feature for the user | MINOR |
| `fix` | Bug fix for the user | PATCH |
| `perf` | Performance improvement | PATCH |
| `refactor` | Code change (no behavior change) | - |
| `style` | Formatting, whitespace | - |
| `docs` | Documentation only | - |
| `test` | Adding/updating tests | - |
| `chore` | Maintenance (deps, configs) | - |
| `ci` | CI/CD changes | - |
| `revert` | Reverting previous commit | PATCH |

### 1.2 Scope (Opsiyonel)

Etkilenen modül veya alan:

```
feat(planner): add RAG context support
fix(executor): handle empty LLM response
refactor(graph): simplify node transitions
docs(api): update MCP tool documentation
test(verifier): add lint failure cases
chore(deps): update pydantic to 2.6
```

**Allowed Scopes:**
- `planner`, `executor`, `verifier`, `gate` (orchestrator)
- `graph`, `workflow` (core)
- `mcp`, `api`, `cli` (interfaces)
- `adapters`, `services` (infra)
- `deps`, `config`, `ci` (maintenance)

### 1.3 Subject (Zorunlu)

- Lowercase başlar
- Imperative mood ("add" not "added")
- Max 50 karakter
- Period ile bitmez

```
# DOĞRU
feat(planner): add vector store context injection
fix(executor): prevent empty file writes
refactor(graph): extract routing logic to module

# YANLIŞ
feat(planner): Added new feature    # Past tense, starts uppercase
fix: fixed the bug.                  # Vague, ends with period
Update code                          # No type, no scope, too vague
```

### 1.4 Body (Opsiyonel)

- 72 karakter/satır
- Ne değişti ve NEDEN değişti
- Bullet points tercih edilir

```
feat(planner): add vector store context injection

- Query ChromaDB for relevant code snippets
- Include top 5 results in LLM prompt
- Add journal events for RAG queries
- Cache queries for 1 hour

This improves plan quality by providing relevant
codebase context to the LLM, reducing hallucinations.
```

### 1.5 Footer (Opsiyonel)

```
Refs: TASK-123
Closes: #456
Co-Authored-By: Claude <noreply@anthropic.com>
BREAKING CHANGE: API signature changed
```

---

## 2. Commit Granularity

### 2.1 One Commit = One Logical Change

```
# DOĞRU - Her commit tek amaçlı
1. feat(planner): add vector store query
2. test(planner): add vector store tests
3. docs(planner): document RAG integration

# YANLIŞ - Karışık commitler
1. Add planner feature and fix executor bug and update docs
```

### 2.2 Commit Size Guidelines

| Size | Lines Changed | Complexity |
|------|---------------|------------|
| XS | < 20 | Single function change |
| S | 20-50 | Few function changes |
| M | 50-150 | Module-level change |
| L | 150-500 | Multi-module change |
| XL | > 500 | **SPLIT REQUIRED** |

### 2.3 What Goes in Separate Commits

- Formatting changes (should be pre-commit only)
- Refactoring (no behavior change)
- Feature addition (behavior change)
- Test addition
- Documentation

---

## 3. Breaking Changes

### 3.1 Identification

Breaking change = Mevcut kullanıcı kodunu bozan değişiklik

- Function signature change
- Return type change
- Exception type change
- Config key rename
- API endpoint change

### 3.2 Documentation

```
feat(api)!: rename task_status to get_task

BREAKING CHANGE: The `task_status` MCP tool has been renamed
to `get_task` for consistency with other tools.

Migration:
- Before: await mcp.task_status("TASK-123")
- After: await mcp.get_task("TASK-123")
```

**NOT:** `!` suffix type'dan sonra breaking change'i işaretler.

---

## 4. Commit Verification

### 4.1 Pre-Commit Checks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: commit-msg-check
        name: Commit message format
        entry: python scripts/check_commit_msg.py
        language: system
        stages: [commit-msg]
```

### 4.2 Commit Message Validation Script

```python
#!/usr/bin/env python3
"""Validate commit message format."""
import re
import sys

TYPES = ["feat", "fix", "perf", "refactor", "style", "docs", "test", "chore", "ci", "revert"]
PATTERN = re.compile(
    r"^(?P<type>" + "|".join(TYPES) + r")"
    r"(?:\((?P<scope>[a-z_]+)\))?"
    r"(?P<breaking>!)?"
    r": (?P<subject>[a-z].{0,48}[^.])$"
)

def validate(msg: str) -> bool:
    first_line = msg.split("\n")[0]
    if PATTERN.match(first_line):
        return True
    print(f"Invalid commit message: {first_line}")
    print("Expected format: <type>(<scope>): <subject>")
    return False

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        sys.exit(0 if validate(f.read()) else 1)
```

---

## 5. Examples

### 5.1 Feature Commit
```
feat(executor): add content size validation

- Add size ratio check (new/old must be > 0.5)
- Log warning for suspicious size changes
- Add journal event for validation failures

Prevents LLM from destroying file content by
returning much smaller output than input.

Refs: TASK-456
```

### 5.2 Bug Fix Commit
```
fix(planner): handle empty RAG results

Previously, planner crashed when vector store returned
no results. Now it falls back to heuristic planning.

- Check for empty results before processing
- Add fallback plan generation
- Add test for empty RAG scenario

Closes: #123
```

### 5.3 Refactor Commit
```
refactor(graph): extract routing to conditional_routing.py

Move all routing functions to dedicated module for
better organization and testability.

No behavior change - pure structural refactoring.
```

### 5.4 Breaking Change Commit
```
feat(api)!: change plan response format

BREAKING CHANGE: Plan response now uses structured format.

Before:
  {"plan": "text description..."}

After:
  {"files": [...], "steps": [...], "context": "..."}

Migration guide: docs/migrations/v2-plan-format.md
```

---

## 6. Git History Quality

### 6.1 Clean History Goals

- Her commit tek başına mantıklı
- Bisect yapılabilir (her commit çalışır)
- Blame useful (değişiklik nedeni görünür)
- Log readable (hikaye anlatır)

### 6.2 What to Avoid

```
# KÖTÜ - WIP commitler
WIP
WIP 2
fix
stuff
asdf

# KÖTÜ - Mega commitler
Add everything for the new feature including tests docs and configs
```

### 6.3 Squash Before Merge

- Feature branch'te WIP OK
- Develop'a merge öncesi squash
- Clean, atomic commits only in develop/main

---

## 7. Co-Authorship

### 7.1 AI-Assisted Commits

```
feat(planner): add context window optimization

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 7.2 Pair Programming

```
fix(executor): resolve race condition in file writes

Co-Authored-By: Developer1 <dev1@example.com>
Co-Authored-By: Developer2 <dev2@example.com>
```

---

## Checklist

Before committing:
- [ ] Type is correct
- [ ] Scope is appropriate
- [ ] Subject is clear and imperative
- [ ] Body explains WHY (if needed)
- [ ] Breaking changes are marked
- [ ] One logical change per commit
- [ ] Tests pass
- [ ] Lint passes
