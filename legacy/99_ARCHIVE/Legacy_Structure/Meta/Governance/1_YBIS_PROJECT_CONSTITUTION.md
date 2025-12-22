# Constitution 1: YBIS Project Architecture

**Scope:** Main YBIS project (apps/*, packages/*)
**Enforcement:** Zero tolerance - violations block PR merge
**Version:** 1.0
**Last Updated:** 2025-12-15

---

## 🚨 ENFORCEMENT NOTICE

```
╔═══════════════════════════════════════════════════════════════╗
║                    ZERO TOLERANCE CONSTITUTION                  ║
║                                                               ║
║  EVERY RULE in this constitution is MANDATORY.                ║
║  Violation = PR BLOCKED = Code cannot merge to main.          ║
║                                                               ║
║  NO EXCEPTIONS. NO "this time we'll let it slide".           ║
║  NO "we'll fix it later". FIX NOW or DON'T MERGE.            ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Article 1: Port Architecture (Port-by-Port Architecture)

### 1.1 Rule
Only **changeable external dependencies** require a "Port" abstraction.

### 1.2 Criteria for Ports
A dependency MUST be behind a Port if it has **at least one** of:
- External service (Supabase, OpenAI, etc.)
- Potential to be replaced in future
- Multiple alternatives exist
- Makes network requests
- Contains native code

### 1.3 Examples

**USE Port:**
- `DatabasePort` (Supabase → Cloud SQL)
- `LLMPort` (OpenAI → Anthropic)
- `AuthPort` (OAuth providers)
- `StoragePort` (S3 → Cloudflare R2)

**DON'T USE Port:**
- Internal application logic
- Framework parts (React, Expo Router)
- Single, stable implementations (Zustand, i18next)
- Pure functions

### 1.4 Enforcement
- CI checks for direct imports of external services in `apps/*`
- All ports MUST live in `packages/core/src/ports/`
- All adapters MUST live in `packages/*/src/adapters/`

---

## Article 2: UI Isolation

### 2.1 Rule
ALL UI components MUST be used via `@ybis/ui` package. Direct imports from `tamagui` or other UI libraries in `apps/*` are **forbidden**.

### 2.2 Principle
The `@ybis/ui` package MUST explicitly export approved design system components (`Button`, `YStack`, `Text`, etc.).

**Forbidden:** `export * from 'tamagui'`
**Required:** Individual, explicit exports

### 2.3 Rationale
- Design system consistency
- UI library replacement without app changes
- Single source of truth for components

### 2.4 Enforcement
- ESLint rule: No `tamagui` imports in `apps/*`
- CI validation of `@ybis/ui` exports

---

## Article 3: Build for Scale, Ship Minimal

### 3.1 Rule
Infrastructure MUST be designed to support future expansions (multi-theme, multi-provider), but ship with ONLY minimal features initially.

### 3.2 Examples

**Good:**
```typescript
// Infrastructure supports N themes
interface ThemeProvider {
  register(theme: Theme): void;
  activate(themeId: string): void;
}

// But ship with only 2
const themes = [lightTheme, darkTheme];
```

**Bad:**
```typescript
// Hardcoded to 2 themes
const theme = isDark ? darkTheme : lightTheme;
```

### 3.3 Goal
Adding a new feature (theme, LLM provider, etc.) should NOT require core code changes.

---

## Article 4: Fix the Abstraction

### 4.1 Rule
When architectural mismatch is detected between a low-level technology and a high-level abstraction (like a Port interface), the problem MUST be solved by **redesigning the abstraction**, NOT by adding workarounds or adapter layers.

### 4.2 Principle
Fix the root cause (abstraction layer), not the symptom (implementation).

### 4.3 Example

**Bad (Patching):**
```typescript
// Port doesn't match reality, so we add adapter hacks
class SupabaseAdapter implements DatabasePort {
  async query() {
    // Tons of translation logic
    // Workarounds for impedance mismatch
  }
}
```

**Good (Fix Abstraction):**
```typescript
// Redesign DatabasePort to match how databases actually work
interface DatabasePort {
  // Methods that align with real database capabilities
  rawQuery(sql: string): Promise<Result>;
  transaction<T>(fn: () => T): Promise<T>;
}
```

---

## Article 5: Clean Execution Principle

### 5.1 Rule
The project MUST NOT have multiple libraries, tools, or patterns doing the same job. For any given task, define **one canonical way** and all development follows that path.

### 5.2 Goal
- Reduce technical debt
- Prevent confusion
- Ensure architectural integrity

### 5.3 Implementation
If a duplicate is detected from legacy code, fixing it becomes a **priority tech debt task**.

### 5.4 Examples

**Violations:**
- Two state management libraries (Zustand + Redux)
- Two HTTP clients (fetch + axios)
- Two date libraries (date-fns + moment)

**Resolution:** Choose one, migrate, remove the other.

---

## Article 6: Offline-First & Optimistic UI

### 6.1 Rule
All user actions MUST provide immediate feedback. Network operations MUST be non-blocking.

### 6.2 Patterns

**Optimistic UI:**
```typescript
// Update UI immediately
updateLocalState(newValue);

// Sync in background
syncToServer(newValue).catch(() => {
  // Rollback on failure
  revertLocalState();
  showError();
});
```

**Offline Queue:**
- Failed requests → Queue
- Retry when online
- User sees pending state

### 6.3 Enforcement
- All mutations MUST update local state first
- All network calls MUST have error handlers
- All async operations MUST show loading/error states

---

## Article 7: Zero Tolerance Quality Gates

### 7.1 Forbidden Code Patterns

**Absolutely forbidden** in production code:
- `any` type (TypeScript)
- `@ts-ignore` or `@ts-expect-error`
- `console.log` (use logger)
- Empty `catch` blocks
- Magic numbers (use constants)
- Direct database queries in UI code
- **Emoji in code or output** (breaks Windows console, use `[OK]`, `[X]`, `[WARN]` instead)

### 7.2 CI Checks
- TypeScript strict mode
- ESLint with zero warnings
- 80%+ test coverage
- No security vulnerabilities (npm audit)

### 7.3 Consequences
PR blocked until fixed. No exceptions.

---

## Article 8: Monorepo Boundaries

### 8.1 Package Dependencies

**Allowed:**
```
apps/mobile → packages/ui
apps/mobile → packages/core
packages/ui → packages/core
```

**Forbidden:**
```
packages/core → apps/mobile  ❌
packages/ui → apps/backend    ❌
```

### 8.2 Rule
Core packages MUST NOT depend on apps. Dependencies flow one direction only.

---

## Article 9: Testing Requirements

### 9.1 Coverage Minimums

| Package | Min Coverage |
|---------|--------------|
| `core` | 90% |
| `database` | 85% |
| `auth` | 90% |
| `ui` | 70% |
| `mobile` | 60% |

### 9.2 Test Types Required

**Unit Tests:** All business logic
**Integration Tests:** All port/adapter combinations
**E2E Tests:** Critical user flows

### 9.3 Test Quality
- Tests MUST be deterministic
- Tests MUST be isolated (no shared state)
- Tests MUST clean up after themselves

---

## Article 10: Documentation Standards

### 10.1 Required Documentation

Every feature MUST include:
- **ADR** (Architecture Decision Record) for significant changes
- **README** in package root
- **API docs** for all public interfaces
- **Examples** for complex APIs

### 10.2 Code Comments

**Use comments for:**
- WHY (not WHAT)
- Complex algorithms
- Workarounds (with ticket reference)

**Don't comment:**
- Obvious code
- What the code does (self-documenting names instead)

---

## Article 11: Amendment Process

### 11.1 Proposing Changes
1. Create issue with proposed change
2. Discuss with team
3. Update constitution if approved
4. Bump version number

### 11.2 Authority
Only **project owner** can approve constitutional amendments.

---

## Ratification

**Effective Date:** 2025-12-15
**Approved By:** Project Owner
**Review Schedule:** Quarterly

---

*This constitution governs the YBIS main project. For YBIS_Dev governance, see Constitution 3 (Development Governance).*
