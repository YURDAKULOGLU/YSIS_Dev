# Sandbox & Isolation Status Report

**Date:** 2026-01-08  
**Question:** Sandbox, worktree var mı ve gerçek task yapabiliyor mu?

---

## ✅ GERÇEK TASK YAPABİLİYOR MU?

### **EVET, Gerçek Task Yapabiliyor!**

**Kanıt:**
1. ✅ **LocalCoder** - LLM ile kod üretiyor
2. ✅ **write_file syscall** - Gerçek dosyaları değiştiriyor
3. ✅ **File Modification** - `PROJECT_ROOT` altında direkt yazıyor
4. ✅ **Journaling** - Tüm değişiklikler loglanıyor

**Örnek:**
```python
# src/ybis/adapters/local_coder.py:72
write_file(file_path, new_content, ctx)  # Gerçekten dosyayı değiştiriyor!
```

**⚠️ AMA:** Sandbox isolation YOK, direkt main codebase'i değiştiriyor!

---

## ❌ SANDBOX VAR MI?

### **HAYIR, Gerçek Sandbox Isolation YOK**

**Mevcut Durum:**
- ❌ **Sandbox Isolation YOK** - Process/Docker isolation yok
- ✅ **Policy Var** - `configs/profiles/default.yaml` içinde `sandbox.enabled: true` var ama kullanılmıyor
- ✅ **Allowlist Var** - Command allowlist kontrolü var
- ❌ **Eski Sandbox Kullanılmıyor** - `src/agentic/core/execution/sandbox.py` var ama yeni yapıda entegre değil

**Risk:**
- 🔴 **Yüksek Risk** - Test edilmemiş kod direkt main codebase'e yazılıyor
- 🔴 **Rollback Yok** - Bir hata olursa manuel düzeltme gerekir
- 🟡 **Production Risk** - Production'da kullanmak için güvenli değil

**Ne Yapıyor Şu An:**
```python
# src/ybis/syscalls/exec.py
def run_command(cmd, ctx, cwd):
    # Sadece allowlist kontrolü
    if not _is_allowed(cmd):
        raise PermissionError()
    
    # Direkt subprocess.run() - sandbox yok!
    result = subprocess.run(cmd, cwd=work_dir, ...)
```

**Ne Olmalı:**
```python
# İdeal: Sandbox içinde çalıştır
sandbox = ExecutionSandbox(timeout=30, max_memory_mb=512)
result = await sandbox.run_isolated(cmd, cwd=workspace_path)
```

---

## ❌ GIT WORKTREE VAR MI?

### **HAYIR, Git Worktree YOK**

**Mevcut Durum:**
- ❌ **Git Worktree YOK** - Her run için ayrı git worktree oluşturulmuyor
- ✅ **Klasör Isolation Var** - `workspaces/<task_id>/runs/<run_id>/` oluşturuluyor
- ❌ **Git Branch YOK** - Her run için ayrı git branch yok
- ❌ **Git Integration YOK** - Git commit/merge mekanizması yok

**Ne Yapıyor Şu An:**
```python
# src/ybis/data_plane/workspace.py
def init_run_structure(task_id, run_id):
    # Sadece klasör oluşturuyor
    run_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    run_path.mkdir(parents=True, exist_ok=True)
    # Git worktree YOK!
```

**Ne Olmalı:**
```python
# İdeal: Git worktree ile isolation
def init_git_worktree(task_id, run_id):
    branch_name = f"task-{task_id}-run-{run_id}"
    worktree_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    
    # Git worktree oluştur
    subprocess.run(["git", "worktree", "add", str(worktree_path), branch_name])
    
    return worktree_path
```

---

## 📊 Özet Tablo

| Özellik | Durum | Risk | Öncelik |
|---------|-------|------|---------|
| **Gerçek Task Execution** | ✅ VAR | 🟢 Düşük | - |
| **File Modification** | ✅ VAR | 🟡 Orta | - |
| **Sandbox Isolation** | ❌ YOK | 🔴 Yüksek | 🔥 Yüksek |
| **Git Worktree** | ❌ YOK | 🟡 Orta | 🔥 Yüksek |
| **Patch System** | ⚠️ Kısmi | 🟡 Orta | 🟡 Orta |
| **Rollback** | ❌ YOK | 🔴 Yüksek | 🔥 Yüksek |

---

## 🚨 Kritik Eksiklikler

### 1. Sandbox Isolation Eksik
**Sorun:** Test edilmemiş kod direkt main codebase'e yazılıyor.

**Çözüm:**
- Eski `ExecutionSandbox`'ı yeni yapıya entegre et
- Veya Docker sandbox kullan
- Test et, sonra apply et

### 2. Git Worktree Eksik
**Sorun:** Rollback zor, git history belirsiz.

**Çözüm:**
- Her run için git worktree oluştur
- Başarılı olursa merge et
- Başarısız olursa sil

### 3. Patch System Eksik
**Sorun:** `apply_patch` syscall INTERFACES.md'de var ama implementasyonu yok.

**Çözüm:**
- `apply_patch` syscall implement et
- Patch.diff oluştur (şu an oluşturulmuyor gibi)
- Atomic apply/rollback

---

## 💡 Hızlı Çözüm Önerileri

### Öncelik 1: Git Worktree Ekle (1-2 saat)
```python
# src/ybis/data_plane/git_workspace.py (YENİ)
def init_git_worktree(task_id: str, run_id: str) -> Path:
    """Create git worktree for isolated execution."""
    branch_name = f"task-{task_id}-run-{run_id}"
    worktree_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    
    # Create worktree
    subprocess.run([
        "git", "worktree", "add", 
        str(worktree_path), 
        branch_name
    ], check=True)
    
    return worktree_path
```

### Öncelik 2: Sandbox Testing Ekle (2-3 saat)
```python
# src/ybis/syscalls/exec.py (GÜNCELLE)
def run_command_sandboxed(cmd, ctx, cwd):
    """Run in sandbox, test before applying."""
    # 1. Run in isolated workspace
    # 2. Run tests
    # 3. If pass, apply to main
    # 4. If fail, report error
```

### Öncelik 3: Patch System Ekle (3-4 saat)
```python
# src/ybis/syscalls/fs.py (YENİ)
def apply_patch(patch_content: str, ctx: RunContext):
    """Apply patch atomically with rollback."""
    # 1. Validate patch
    # 2. Create backup
    # 3. Apply patch
    # 4. Verify
    # 5. Commit or rollback
```

---

## ✅ Sonuç

**Soru:** Sandbox, worktree var mı ve gerçek task yapabiliyor mu?

**Cevap:**
- ✅ **Gerçek task yapabiliyor** - Dosya değişiklikleri çalışıyor
- ❌ **Sandbox YOK** - Isolation yok, riskli
- ❌ **Worktree YOK** - Git worktree yok, rollback zor

**Durum:** 
- 🟡 **Test ortamında kullanılabilir**
- 🔴 **Production için güvenli değil** (sandbox ve worktree gerekli)

**Öneri:** 
1. Git worktree ekle (kolay, hızlı)
2. Sandbox testing ekle (orta zorluk)
3. Sonra production'a geç

