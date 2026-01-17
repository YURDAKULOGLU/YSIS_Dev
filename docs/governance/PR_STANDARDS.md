# PULL REQUEST STANDARDS

> Her PR bu standartlara uymalıdır.
> Agent'lar için: commit = mini-PR gibi düşünün.

**References:**
- COMMIT_STANDARDS.md
- CODE_REVIEW_CHECKLIST.md
- DISCIPLINE.md

---

## 1. PR Title Format

```
<type>(<scope>): <description> [TASK-XXX]
```

**Examples:**
```
feat(planner): add RAG context injection [TASK-123]
fix(executor): prevent empty file writes [TASK-124]
refactor(graph): extract routing logic [TASK-125]
```

---

## 2. PR Description Template

```markdown
## Summary
[1-3 sentences describing what this PR does]

## Changes
- [Bullet list of main changes]
- [Be specific about what was added/modified/removed]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated (if applicable)
- [ ] Manual testing performed

### Test Evidence
[Paste test output or screenshot]

## Risk Assessment
- **Risk Level:** [Low/Medium/High]
- **Protected Paths:** [List any protected paths modified]
- **Breaking Changes:** [Yes/No - if yes, describe]

## Checklist
- [ ] Code follows project standards
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new lint errors

## Related
- Task: TASK-XXX
- Related PRs: #YYY (if any)
- Docs: [Link to relevant docs]
```

---

## 3. PR Size Guidelines

### 3.1 Size Categories

| Size | Files | Lines | Review Time |
|------|-------|-------|-------------|
| XS | 1-2 | < 50 | 5-10 min |
| S | 3-5 | 50-150 | 15-30 min |
| M | 5-10 | 150-400 | 30-60 min |
| L | 10-20 | 400-1000 | 1-2 hours |
| XL | > 20 | > 1000 | **SPLIT** |

### 3.2 Splitting Large PRs

**XL PR'lar ZORUNLU split edilmeli:**

1. **By Layer:**
   - PR1: Data models
   - PR2: Business logic
   - PR3: API/Interface
   - PR4: Tests

2. **By Feature:**
   - PR1: Core functionality
   - PR2: Edge cases
   - PR3: Error handling
   - PR4: Documentation

3. **By Component:**
   - PR1: Planner changes
   - PR2: Executor changes
   - PR3: Verifier changes

---

## 4. PR Quality Gates

### 4.1 Automated Gates (CI)

```yaml
# Required to pass before merge
- lint (ruff)
- type-check (mypy)
- unit-tests (pytest tests/unit)
- golden-tests (pytest -m golden)
- security-scan (bandit)
```

### 4.2 Manual Gates

| Gate | Required For |
|------|--------------|
| Code Review | All PRs |
| Human Approval | Protected paths |
| Architecture Review | New modules |
| Security Review | Auth/crypto changes |

---

## 5. Review Process

### 5.1 Review Timeline

| PR Size | Expected Review Time |
|---------|---------------------|
| XS/S | Same day |
| M | 1 business day |
| L | 2 business days |
| XL | Don't submit - split first |

### 5.2 Reviewer Assignment

- **Auto-assign:** Based on CODEOWNERS
- **Manual request:** For specific expertise
- **Minimum:** 1 approval for non-protected
- **Protected paths:** 2 approvals required

### 5.3 Review Comments

**Comment Prefixes:**
- `[BLOCKER]` - Must fix before merge
- `[QUESTION]` - Need clarification
- `[SUGGESTION]` - Nice to have
- `[NIT]` - Minor style issue

---

## 6. PR Lifecycle

### 6.1 States

```
Draft -> Ready for Review -> Changes Requested -> Approved -> Merged
                   |                    |
                   +--------------------+
                   (iterate until approved)
```

### 6.2 Draft PRs

Use drafts for:
- WIP that needs early feedback
- Dependency on another PR
- Blocking on external decision

### 6.3 Stale PRs

- No activity > 7 days = reminder
- No activity > 14 days = close candidate
- No activity > 30 days = auto-close

---

## 7. Merge Strategy

### 7.1 Merge Types

| Strategy | When to Use |
|----------|-------------|
| Squash | Feature branches (default) |
| Merge commit | Release branches |
| Rebase | Never (history rewrite) |

### 7.2 Post-Merge

1. Delete source branch
2. Verify CI passes on target
3. Update related issues/tasks
4. Notify stakeholders (if needed)

---

## 8. Hotfix Process

### 8.1 When to Hotfix

- Production bug (P0/P1)
- Security vulnerability
- Data corruption risk

### 8.2 Hotfix Flow

```
1. Branch from main: hotfix/TASK-XXX
2. Minimal fix only
3. Expedited review (1 approval OK)
4. Merge to main
5. Cherry-pick to develop
6. Post-mortem
```

### 8.3 Hotfix Restrictions

- NO new features
- NO refactoring
- NO "while I'm here" changes
- MINIMAL scope

---

## 9. Special Cases

### 9.1 Documentation-Only PRs

```markdown
## Summary
Documentation update for [topic].

## Changes
- Updated docs/X.md
- Added examples for Y

## Checklist
- [ ] Links verified
- [ ] Examples tested
- [ ] No broken references
```

### 9.2 Dependency Update PRs

```markdown
## Summary
Update [package] from X.Y.Z to A.B.C

## Changes
- Updated pyproject.toml
- Updated requirements.txt (if applicable)

## Changelog
[Link to package changelog]

## Testing
- [ ] All tests pass
- [ ] No API changes affecting our code
- [ ] No new vulnerabilities introduced

## Risk Assessment
- Breaking changes: [Yes/No]
- Security fixes: [Yes/No]
```

### 9.3 Revert PRs

```markdown
## Summary
Revert "[original PR title]"

This reverts commit [SHA].

## Reason
[Why reverting]

## Impact
[What will happen after revert]

## Follow-up
[Plan to fix the underlying issue]
```

---

## 10. PR Etiquette

### 10.1 For Authors

- Keep PRs small and focused
- Respond to reviews within 24h
- Don't force-push during review
- Say "done" when addressing comments

### 10.2 For Reviewers

- Review within timeline
- Be constructive, not critical
- Explain "why" not just "what"
- Approve when concerns addressed

---

## Agent-Specific Rules

### Self-Submitted PRs

Agent'lar PR submit ettiğinde:

1. **Self-review zorunlu** (CODE_REVIEW_CHECKLIST)
2. **Evidence required** (test output, journal)
3. **Human approval required** for protected paths
4. **Auto-merge disabled** by default

### PR Content

Agent PR'ları şunları içermeli:
- Clear description of changes
- Test evidence
- Journal event summary
- Risk assessment

### Merge Authority

| Change Type | Agent Can Merge |
|-------------|-----------------|
| Tests only | Yes |
| Docs only | Yes |
| Bug fix (non-protected) | Yes |
| New feature | No |
| Protected paths | No |
| Config changes | No |

---

## Checklist Summary

Before creating PR:
- [ ] All tests pass locally
- [ ] Self-review completed
- [ ] PR size is reasonable (< L)
- [ ] Title follows format
- [ ] Description complete

Before requesting review:
- [ ] CI passes
- [ ] No merge conflicts
- [ ] Related docs updated

Before merging:
- [ ] Required approvals obtained
- [ ] All comments addressed
- [ ] Final CI pass confirmed
