# Constitution 2: Universal Code Standards

**Scope:** All code (YBIS project + YBIS_Dev meta-system)
**Enforcement:** CI + Code review
**Version:** 1.0
**Last Updated:** 2025-12-15

---

## Purpose

This constitution defines **universal engineering principles** that apply to ALL code we write, regardless of project. These are timeless software engineering standards.

---

## Article 1: SOLID Principles

### 1.1 Single Responsibility Principle (SRP)
**Rule:** A class/module should have ONE reason to change.

**Example:**
```typescript
// Bad - multiple responsibilities
class User {
  save() { /* DB logic */ }
  sendEmail() { /* Email logic */ }
  validateInput() { /* Validation logic */ }
}

// Good - separated concerns
class User { /* Data model only */ }
class UserRepository { save(user) }
class UserMailer { sendWelcomeEmail(user) }
class UserValidator { validate(user) }
```

### 1.2 Open/Closed Principle (OCP)
**Rule:** Open for extension, closed for modification.

**Example:**
```typescript
// Bad - need to modify for each new type
function processPayment(type: string) {
  if (type === 'credit') { /* ... */ }
  if (type === 'paypal') { /* ... */ }
}

// Good - extend without modifying
interface PaymentProcessor {
  process(amount: number): Promise<void>;
}

class CreditCardProcessor implements PaymentProcessor { }
class PayPalProcessor implements PaymentProcessor { }
```

### 1.3 Liskov Substitution Principle (LSP)
**Rule:** Subtypes must be substitutable for their base types.

**Example:**
```typescript
// Bad - breaks LSP
class Bird { fly() { } }
class Penguin extends Bird {
  fly() { throw new Error("Can't fly!"); } // ❌
}

// Good - proper abstraction
interface Animal { eat() }
interface FlyingAnimal extends Animal { fly() }

class Bird implements Animal { }
class Eagle implements FlyingAnimal { }
class Penguin implements Animal { } // ✅
```

### 1.4 Interface Segregation Principle (ISP)
**Rule:** Don't force clients to depend on interfaces they don't use.

**Example:**
```typescript
// Bad - fat interface
interface Worker {
  code(): void;
  design(): void;
  test(): void;
  deploy(): void;
}

// Good - segregated interfaces
interface Coder { code(): void; }
interface Designer { design(): void; }
interface Tester { test(): void; }
interface DevOps { deploy(): void; }

class FullStackDev implements Coder, Tester { }
class FrontendDev implements Coder, Designer { }
```

### 1.5 Dependency Inversion Principle (DIP)
**Rule:** Depend on abstractions, not concretions.

**Example:**
```typescript
// Bad - depends on concrete class
class UserService {
  constructor(private db: MySQLDatabase) { } // ❌
}

// Good - depends on interface
class UserService {
  constructor(private db: DatabasePort) { } // ✅
}
```

---

## Article 2: Clean Code Principles

### 2.1 Meaningful Names

**Rules:**
- Use intention-revealing names
- Avoid mental mapping
- Use pronounceable names
- Use searchable names

**Examples:**
```typescript
// Bad
const d = 86400; // what is this?
const yyyymmdd = "20250115";

// Good
const SECONDS_PER_DAY = 86400;
const releaseDate = "2025-01-15";
```

### 2.2 Functions

**Rules:**
- Small (< 20 lines ideal)
- Do ONE thing
- One level of abstraction
- Descriptive names
- Minimal arguments (< 3 ideal)

**Examples:**
```typescript
// Bad - does too much
function processUserAndSendEmail(data) {
  const user = validateUser(data);
  saveToDatabase(user);
  sendWelcomeEmail(user.email);
  logActivity(user.id);
  return user;
}

// Good - separated
function createUser(data: UserData): User {
  const user = validateUser(data);
  return saveUser(user);
}

function onUserCreated(user: User): void {
  sendWelcomeEmail(user.email);
  logUserActivity(user.id, 'created');
}
```

### 2.3 Comments

**Use comments for:**
- WHY (not WHAT)
- Warnings of consequences
- TODO/FIXME with ticket references
- Complex algorithms explanation

**DON'T comment:**
- Obvious code
- What code does (use better names instead)
- Commented-out code (delete it)

```typescript
// Bad
// Loop through users and send them emails
users.forEach(u => sendEmail(u)); // ❌

// Good
// Send renewal reminder 7 days before expiration (TICKET-123)
users
  .filter(u => u.expiresInDays(7))
  .forEach(u => sendRenewalReminder(u)); // ✅
```

### 2.4 Error Handling

**Rules:**
- Use exceptions, not error codes
- Provide context in exceptions
- Don't return null (use Optional/Result pattern)
- Don't ignore caught exceptions

```typescript
// Bad
function getUser(id: string): User | null {
  try {
    return db.findUser(id);
  } catch (e) {
    return null; // ❌ Lost error context
  }
}

// Good
function getUser(id: string): Result<User, Error> {
  try {
    const user = db.findUser(id);
    return Result.ok(user);
  } catch (e) {
    logger.error(`Failed to fetch user ${id}`, e);
    return Result.err(new UserNotFoundError(id));
  }
}
```

### 2.6 Output Formatting

**Rules:**
- **NO EMOJI** in code, console output, or logs (breaks Windows console encoding)
- Use ASCII alternatives: `[OK]`, `[X]`, `[WARN]`, `[INFO]`, `[LAUNCH]`
- All output must be Windows console safe (cp1252/cp1254 compatible)

**Examples:**
```typescript
// Bad - emoji breaks Windows console
console.log("✅ Success");
console.log("❌ Failed");
console.log("⚠️ Warning");

// Good - ASCII safe
console.log("[OK] Success");
console.log("[X] Failed");
console.log("[WARN] Warning");
```

**Rationale:** Windows consoles use cp1252/cp1254 encoding which cannot display Unicode emoji, causing UnicodeEncodeError crashes.

---

## Article 3: Testing Principles

### 3.1 Test Pyramid

**Distribution:**
```
    /\
   /E2E\      10% - End-to-end (critical flows)
  /------\
 /  INT   \   20% - Integration (boundaries)
/----------\
|   UNIT   |  70% - Unit (business logic)
```

### 3.2 FIRST Principles

**F**ast - Tests run quickly (< 1s each)
**I**ndependent - No test depends on another
**R**epeatable - Same result every time
**S**elf-validating - Pass/fail, no manual checking
**T**imely - Written before/with production code (TDD)

### 3.3 Test Structure (AAA Pattern)

```typescript
test('should calculate total with tax', () => {
  // Arrange
  const cart = new ShoppingCart();
  cart.addItem({ price: 100, quantity: 2 });

  // Act
  const total = cart.calculateTotal({ taxRate: 0.1 });

  // Assert
  expect(total).toBe(220); // 200 + 20 tax
});
```

### 3.4 What to Test

**DO test:**
- Business logic
- Edge cases
- Error handling
- Port/adapter boundaries

**DON'T test:**
- Framework code
- Third-party libraries
- Getters/setters
- Trivial code

---

## Article 4: Security Principles (OWASP Top 10)

### 4.1 Input Validation

**Rule:** NEVER trust user input.

```typescript
// Bad
const userId = req.params.id;
const user = await db.query(`SELECT * FROM users WHERE id = ${userId}`); // ❌ SQL injection

// Good
const userId = validateUUID(req.params.id); // Throws if invalid
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]); // ✅ Parameterized
```

### 4.2 Authentication & Authorization

**Rules:**
- Always hash passwords (bcrypt, argon2)
- Use secure session management
- Implement RBAC (Role-Based Access Control)
- Never expose sensitive data in logs/errors

### 4.3 Data Protection

**Rules:**
- Encrypt sensitive data at rest
- Use HTTPS for all network communication
- Implement proper CORS policies
- Sanitize all output (XSS prevention)

### 4.4 Dependencies

**Rules:**
- Keep dependencies updated
- Run `npm audit` / `pnpm audit` regularly
- Review dependency licenses
- Minimize dependency count

---

## Article 5: Performance Principles

### 5.1 Premature Optimization

**Rule:** "Premature optimization is the root of all evil" - Donald Knuth

**Process:**
1. Make it work
2. Make it right (clean)
3. Make it fast (if needed)

### 5.2 Measure First

**Rules:**
- Profile before optimizing
- Use real-world data
- Set performance budgets
- Monitor in production

### 5.3 Common Optimizations

**DO:**
- Cache expensive calculations
- Use pagination for large datasets
- Lazy load non-critical resources
- Debounce/throttle user inputs

**DON'T:**
- Micro-optimize before profiling
- Trade readability for minor gains
- Optimize code that runs once

---

## Article 6: Code Review Principles

### 6.1 Reviewer Responsibilities

**Check for:**
- Correctness (does it work?)
- Tests (are they sufficient?)
- Design (is it maintainable?)
- Style (follows standards?)
- Security (any vulnerabilities?)

### 6.2 Author Responsibilities

**Before submitting:**
- Self-review your code
- Run tests locally
- Update documentation
- Keep PR small (< 400 lines ideal)

### 6.3 Review Etiquette

**DO:**
- Be kind and constructive
- Explain WHY, not just WHAT
- Praise good work
- Ask questions, don't command

**DON'T:**
- Nitpick trivial style issues (use linter)
- Block PR for personal preferences
- Use dismissive language

---

## Article 7: Git Workflow

### 7.1 Commit Messages

**Format:**
```
type(scope): short summary (max 50 chars)

Detailed explanation if needed (wrap at 72 chars)

Fixes: #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change (no behavior change)
- `test`: Adding tests
- `docs`: Documentation only
- `chore`: Build, CI, dependencies

**Examples:**
```
feat(auth): add password reset flow

Implements email-based password reset with token expiration.
Token valid for 1 hour. Sends email via Supabase.

Fixes: #456
```

### 7.2 Branch Strategy

**Branches:**
- `main` - Production-ready code
- `feature/xyz` - New features
- `fix/xyz` - Bug fixes
- `refactor/xyz` - Code improvements

**Rules:**
- Never commit directly to `main`
- Always PR from feature branch
- Squash commits when merging
- Delete branch after merge

### 7.3 Pull Requests

**PR must include:**
- Clear description
- Link to ticket/issue
- Screenshots (for UI changes)
- Test plan
- Updated docs

---

## Article 8: Documentation Standards

### 8.1 Code Documentation

**Use JSDoc/TSDoc for:**
```typescript
/**
 * Calculates the total price including tax and shipping.
 *
 * @param items - Array of cart items
 * @param options - Calculation options
 * @returns Total price in cents
 * @throws {ValidationError} If items array is empty
 *
 * @example
 * ```ts
 * const total = calculateTotal(
 *   [{ price: 100, qty: 2 }],
 *   { taxRate: 0.1, shipping: 500 }
 * );
 * // Returns: 2700 (200 + 20 tax + 500 shipping)
 * ```
 */
function calculateTotal(
  items: CartItem[],
  options: CalculationOptions
): number { }
```

### 8.2 README Standards

Every package/module MUST have:
- **Purpose** - What does this do?
- **Installation** - How to set up?
- **Usage** - Quick examples
- **API** - Public interface
- **Contributing** - How to contribute?

### 8.3 Architecture Decision Records (ADRs)

**When to write:**
- Significant architectural decisions
- Technology choices
- Design pattern adoptions

**Format:**
```markdown
# ADR-001: Use Port/Adapter for External Dependencies

## Status: Accepted

## Context
We need to integrate multiple external services (Supabase, OpenAI)
and want the ability to swap them out in the future.

## Decision
Implement Port/Adapter pattern for all external dependencies.

## Consequences
+ Easy to swap implementations
+ Better testing (mock ports)
- More boilerplate code
- Learning curve for new devs
```

---

## Article 9: Continuous Integration

### 9.1 CI Pipeline Requirements

**All PRs must pass:**
1. Linting (ESLint, Prettier)
2. Type checking (TypeScript strict)
3. Unit tests (min coverage)
4. Integration tests
5. Security audit
6. Build verification

### 9.2 Quality Gates

**Block merge if:**
- Any test fails
- Coverage drops below threshold
- New security vulnerabilities
- Build fails
- Linter errors

---

## Article 10: Dependency Management

### 10.1 Adding Dependencies

**Before adding a new dependency:**
1. Is it actively maintained?
2. What's the bundle size impact?
3. How many transitive dependencies?
4. Is there a lighter alternative?
5. Can we implement it ourselves (if small)?

### 10.2 Dependency Updates

**Schedule:**
- Patch updates: Weekly (automated)
- Minor updates: Monthly (reviewed)
- Major updates: Quarterly (planned)

### 10.3 License Compliance

**Allowed licenses:**
- MIT, Apache 2.0, BSD
- ISC, CC0, Unlicense

**Forbidden licenses:**
- GPL (copyleft - conflicts with proprietary)
- AGPL
- Custom restrictive licenses

---

## Enforcement

### Automated
- CI pipeline checks
- Pre-commit hooks
- IDE plugins (ESLint, Prettier)

### Manual
- Code review
- Pair programming
- Architecture review sessions

---

## Amendment Process

1. Propose change via RFC
2. Team discussion (async or sync)
3. Vote (consensus preferred)
4. Update constitution
5. Update tooling (linters, CI)

---

**Last Updated:** 2025-12-15
**Review Schedule:** Annually

---

*These standards apply to all code. For project-specific rules, see Constitution 1 (YBIS Project). For meta-system governance, see Constitution 3 (Development Governance).*
