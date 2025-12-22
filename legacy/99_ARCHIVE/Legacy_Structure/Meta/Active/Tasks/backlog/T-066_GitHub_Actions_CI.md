# T-066: GitHub Actions CI Setup

**Priority:** P1 (Important)
**Effort:** 1 day
**Assignee:** @Coding / @GitHub
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 12

---

## Description

Set up GitHub Actions for automated testing and linting on pull requests.

## Tasks

- [ ] Create `.github/workflows/ci.yml`
- [ ] Run type checking on PRs
- [ ] Run linting on PRs
- [ ] Run tests on PRs (when tests exist)
- [ ] Add status checks to branch protection
- [ ] Set up EAS preview builds (optional)

## Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  lint-and-type:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm run typecheck
      - run: pnpm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm run test
```

## Acceptance Criteria

- PRs blocked on lint/type failures
- CI runs in < 5 minutes
- Clear error messages on failures

