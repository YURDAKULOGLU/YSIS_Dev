# CODE REVIEW CHECKLIST

> Her kod değişikliği bu checklist ile review edilir.
> Agent self-review için de geçerlidir.

**References:**
- DISCIPLINE.md
- CODE_STANDARDS.md
- SECURITY.md

---

## 1. Correctness

### 1.1 Logic
- [ ] Algorithm doğru mu?
- [ ] Edge cases handle edilmiş mi?
- [ ] Off-by-one errors var mı?
- [ ] Null/None checks var mı?
- [ ] Division by zero koruması var mı?

### 1.2 Error Handling
- [ ] Exception'lar yakalanmış mı?
- [ ] Error recovery var mı?
- [ ] Error messages açıklayıcı mı?
- [ ] Errors log'lanmış mı?
- [ ] User-facing errors sanitize edilmiş mi?

### 1.3 Async/Concurrency
- [ ] Race conditions var mı?
- [ ] Deadlock riski var mı?
- [ ] Proper async/await kullanılmış mı?
- [ ] Blocking I/O async context'te var mı?

---

## 2. Security

### 2.1 Input Validation
- [ ] User input validate edilmiş mi?
- [ ] SQL injection koruması var mı?
- [ ] Path traversal koruması var mı?
- [ ] Command injection koruması var mı?

### 2.2 Data Protection
- [ ] Secrets log'lanmıyor mu?
- [ ] PII mask'lanmış mı?
- [ ] Sensitive data encrypt edilmiş mi?
- [ ] Temporary files temizleniyor mu?

### 2.3 Access Control
- [ ] Authorization check var mı?
- [ ] Protected paths respect ediliyor mu?
- [ ] Sandbox boundaries korunuyor mu?

---

## 3. Performance

### 3.1 Efficiency
- [ ] N+1 query var mı?
- [ ] Unnecessary loops var mı?
- [ ] Memory leak riski var mı?
- [ ] Large data memory'de mi?

### 3.2 Caching
- [ ] Cacheable operations cached mı?
- [ ] Cache invalidation doğru mu?
- [ ] Cache TTL uygun mu?

### 3.3 Resource Usage
- [ ] Connections properly closed mı?
- [ ] File handles closed mı?
- [ ] Timeout var mı?

---

## 4. Code Quality

### 4.1 Readability
- [ ] Variable names descriptive mi?
- [ ] Function names action-oriented mi?
- [ ] Magic numbers constant mı?
- [ ] Complex logic documented mı?

### 4.2 Structure
- [ ] Functions < 50 lines mi?
- [ ] Single responsibility principle?
- [ ] Proper abstraction level?
- [ ] DRY (Don't Repeat Yourself)?

### 4.3 Type Safety
- [ ] Type hints complete mi?
- [ ] mypy pass ediyor mu?
- [ ] Generic types properly constrained mı?

---

## 5. Testing

### 5.1 Coverage
- [ ] New code tested mi?
- [ ] Edge cases tested mi?
- [ ] Error paths tested mi?
- [ ] Integration points tested mi?

### 5.2 Test Quality
- [ ] Tests meaningful mi?
- [ ] Tests independent mi?
- [ ] Mock'lar appropriate mı?
- [ ] Assertion messages clear mi?

---

## 6. Documentation

### 6.1 Code Documentation
- [ ] Public functions docstring var mı?
- [ ] Complex logic comment var mı?
- [ ] TODO'lar ticket'a bağlı mı?

### 6.2 External Documentation
- [ ] API changes documented mı?
- [ ] Config changes documented mı?
- [ ] Breaking changes documented mı?

---

## 7. Maintainability

### 7.1 Dependencies
- [ ] New deps necessary mi?
- [ ] Deps version pinned mi?
- [ ] License compatible mı?

### 7.2 Configuration
- [ ] Hardcoded values yok mu?
- [ ] Config validated mı?
- [ ] Defaults sensible mi?

### 7.3 Compatibility
- [ ] Backward compatible mi?
- [ ] Migration path var mı?
- [ ] Deprecation warning var mı?

---

## 8. Observability

### 8.1 Logging
- [ ] Operations logged mı?
- [ ] Errors logged mı?
- [ ] Log levels appropriate mı?
- [ ] Sensitive data masked mı?

### 8.2 Monitoring
- [ ] Journal events var mı?
- [ ] Metrics tracked mı?
- [ ] Alerting configured mı?

---

## Review Response Format

```markdown
## Review: [PR/Change Title]

### Approved / Changes Requested / Blocked

### Summary
[One paragraph overall assessment]

### Issues Found
1. **[SEVERITY]** [Location] - [Description]
   - Suggestion: [How to fix]

### Questions
- [Clarification questions]

### Positive Notes
- [What was done well]
```

### Issue Severity

| Severity | Description | Action |
|----------|-------------|--------|
| CRITICAL | Security/data loss risk | Must fix before merge |
| HIGH | Bug or major issue | Must fix before merge |
| MEDIUM | Code quality issue | Should fix |
| LOW | Nitpick/suggestion | Optional |

---

## Automated Checks

Bu checklist'in bir kısmı otomatik kontrol edilir:

| Check | Tool | When |
|-------|------|------|
| Lint | ruff | pre-commit |
| Type check | mypy | CI |
| Tests | pytest | CI |
| Security | bandit | CI |
| Coverage | pytest-cov | CI |
| Commit format | custom script | commit-msg hook |
| Doc coverage | interrogate | CI |

---

## Self-Review (Agents)

Agent'lar kendi kodlarını review ederken:

1. Önce kodu yaz
2. 5 saniye "bekle" (context switch)
3. Bu checklist'i uygula
4. Issue varsa düzelt
5. Issue yoksa devam et

**KURAL:** Self-review atlanırsa task incomplete sayılır.
