---
# YBIS Full Cycle Command - Limit Test
# Bu command, Claude Code custom command sisteminin TÜM özelliklerini kullanır

# Command metadata
description: "YBIS tam döngü: task al, planla, kodla, test et, commit et, raporla"

# Tool restrictions - sadece bu tool'lar kullanılabilir
# Boş bırakılırsa tüm tool'lar kullanılabilir
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TodoWrite
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - mcp__ybis__task_create
  - mcp__ybis__task_status
  - mcp__ybis__get_tasks
  - mcp__ybis__claim_task
  - mcp__ybis__task_run
  - mcp__ybis__task_complete
  - mcp__ybis__artifact_write
  - mcp__ybis__artifact_read

# Model override (optional) - bu command için özel model
# model: opus

# Max turns override (optional)
# max-turns: 50

# Timeout override in ms (optional)
# timeout: 600000
---

# YBIS Full Cycle Command

## Görev
Sen YBIS platformunun tam döngü execution agent'ısın. Bu command ile:
1. Task claim et veya oluştur
2. Codebase'i analiz et
3. Plan yaz
4. Kodu implement et
5. Test et
6. Verify et
7. Commit et
8. Raporla

## Argümanlar
Kullanıcı argümanları: `$ARGUMENTS`

Argüman formatları:
- Task ID: `TASK-123` veya `T-abc12345`
- Yeni task: `"task title" --objective "task objective"`
- Boş: Otomatik olarak pending task claim et

## Execution Protocol

### Faz 1: Task Acquisition
```
IF $ARGUMENTS is task ID:
  - task_status ile task bilgilerini al
  - claim_task ile task'ı claim et
ELIF $ARGUMENTS contains "--objective":
  - task_create ile yeni task oluştur
  - Oluşturulan task'ı claim et
ELSE:
  - get_tasks ile pending task'ları listele
  - İlk uygun task'ı claim et
```

### Faz 2: Analysis
```
1. Task objective'i analiz et
2. Codebase exploration yap:
   - Glob ile ilgili dosyaları bul
   - Grep ile pattern'ları ara
   - Read ile kritik dosyaları oku
3. Task subagent'ı ile derinlemesine analiz yap (gerekirse)
4. TodoWrite ile analiz sonuçlarını kaydet
```

### Faz 3: Planning
```
1. PLAN.md oluştur:
   - Objective summary
   - Affected files listesi
   - Step-by-step implementation plan
   - Risk assessment
   - Test strategy
2. artifact_write ile PLAN.md'yi kaydet
3. AskUserQuestion ile plan onayı al (critical changes için)
```

### Faz 4: Implementation
```
1. TodoWrite ile implementation steps'leri oluştur
2. Her step için:
   a. İlgili dosyayı Read et
   b. Edit veya Write ile değişiklik yap
   c. TodoWrite ile step'i complete işaretle
3. Değişiklikleri incremental olarak yap
4. Her major change sonrası verification yap
```

### Faz 5: Testing
```
1. Test dosyalarını bul (Glob: **/test_*.py, **/*.test.ts)
2. İlgili testleri çalıştır:
   - Python: pytest
   - TypeScript: npm test
   - Genel: make test
3. Test failures varsa:
   a. Hataları analiz et
   b. Fix uygula
   c. Testleri tekrar çalıştır
4. Test coverage raporla
```

### Faz 6: Verification
```
1. Lint kontrolü:
   - Python: ruff check, mypy
   - TypeScript: eslint, tsc
2. Security check:
   - Hardcoded secrets
   - SQL injection
   - XSS vulnerabilities
3. Code quality:
   - Complexity check
   - Duplication check
4. Tüm kontroller PASS olmalı
```

### Faz 7: Commit
```
1. git status ile değişiklikleri kontrol et
2. git diff ile review et
3. Uygun commit message oluştur:
   - Conventional commits format
   - Co-authored-by: Claude
4. git add ve git commit
5. Push YAPMA (user onayı gerekli)
```

### Faz 8: Reporting
```
1. RESULT.md oluştur:
   - Summary of changes
   - Files modified
   - Tests status
   - Verification status
   - Commit hash
2. artifact_write ile RESULT.md'yi kaydet
3. task_complete ile task'ı tamamla
4. Final summary çıktısı ver
```

## Output Format

Her faz sonunda status raporu:
```
[FAZ X: NAME] STATUS
- Action 1: OK/FAILED
- Action 2: OK/FAILED
- Duration: Xs
- Notes: ...
```

Final output:
```
=====================================
YBIS FULL CYCLE COMPLETE
=====================================
Task ID: TASK-XXX
Status: COMPLETED/FAILED
Duration: Xm Xs

Changes:
- file1.py: +10 -5
- file2.ts: +20 -0

Tests: X passed, Y failed
Verification: PASS/FAIL
Commit: abc123

Next Steps:
- [ ] Review changes
- [ ] Push to remote
- [ ] Create PR
=====================================
```

## Error Handling

Her hata durumunda:
1. Hatayı logla
2. Mümkünse recovery dene
3. 3 deneme sonrası fail et
4. Partial RESULT.md oluştur
5. task_complete ile failed status kaydet

## Constraints

- Governance: docs/governance/YBIS_CONSTITUTION.md'ye uy
- Protected files: Değiştirme onayı al
- Max retries: 3
- Timeout: 10 dakika/faz
- Commit message: Max 72 karakter başlık

## Variables Available

- `$ARGUMENTS`: Kullanıcının verdiği argümanlar
- `$CWD`: Current working directory
- `$USER`: Kullanıcı adı
- `$DATE`: Bugünün tarihi
- `$PROJECT_ROOT`: Proje kök dizini

## Examples

```bash
# Belirli task'ı çalıştır
/project:ybis-full-cycle TASK-123

# Yeni task oluştur ve çalıştır
/project:ybis-full-cycle "Fix login bug" --objective "Fix the authentication timeout issue in login flow"

# Otomatik task claim
/project:ybis-full-cycle

# Sadece analysis faz
/project:ybis-full-cycle TASK-123 --phase analysis
```
