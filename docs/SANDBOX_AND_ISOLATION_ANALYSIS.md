# Sandbox & Isolation Analysis

**Date:** 2026-01-08  
**Objective:** Analyze current sandbox, worktree, and task execution capabilities

---

## 🔍 Current State

### ✅ What EXISTS

#### 1. **Task Execution (Gerçek Task Yapabiliyor)**
- ✅ **LocalCoder** - LLM-based code generation
- ✅ **File Modification** - `write_file` syscall ile gerçek dosya değişiklikleri
- ✅ **Syscall Protection** - Protected paths kontrolü
- ✅ **Journaling** - Tüm değişiklikler loglanıyor

**Location:** `src/ybis/adapters/local_coder.py`
```python
# Gerçekten dosya değiştiriyor:
write_file(file_path, new_content, ctx)  # PROJECT_ROOT altında direkt yazıyor
```

#### 2. **Basic Security Controls**
- ✅ **Command Allowlist** - `configs/profiles/default.yaml` içinde
- ✅ **Protected Paths** - Core dosyalar korunuyor
- ✅ **Policy Enforcement** - PolicyProvider ile dinamik kontrol

**Location:** `src/ybis/syscalls/exec.py`, `src/ybis/syscalls/fs.py`

#### 3. **Workspace Isolation (Partial)**
- ✅ **Run Isolation** - Her run için ayrı klasör: `workspaces/<task_id>/runs/<run_id>/`
- ✅ **Immutable Runs** - Her run yeni bir klasörde
- ✅ **Artifacts Separation** - Her run'ın kendi artifacts klasörü var

**Location:** `src/ybis/data_plane/workspace.py`

---

## ❌ What's MISSING

### 1. **Real Sandbox Isolation**

**Problem:** Sistem direkt main codebase'i değiştiriyor, sandbox isolation yok.

**Current State:**
- Policy'de `sandbox.enabled: true` var ama implementasyon yok
- `src/ybis/syscalls/exec.py` sadece allowlist kontrolü yapıyor
- Eski yapıda `ExecutionSandbox` ve `DockerSandbox` var ama kullanılmıyor

**Risk:**
- Bir hata olursa main codebase bozulabilir
- Test edilmemiş kod direkt production'a yazılıyor
- Rollback mekanizması yok

**What We Need:**
```python
# İdeal: Sandbox içinde çalıştır, sonra apply et
sandbox = ExecutionSandbox(timeout=30, max_memory_mb=512)
result = await sandbox.run_isolated("python test.py", cwd=workspace_path)
if result.success:
    apply_changes_to_main_codebase()
```

---

### 2. **Git Worktree Isolation**

**Problem:** Git worktree yok, her run için ayrı git branch/worktree oluşturulmuyor.

**Current State:**
- Sadece klasör oluşturuluyor: `workspaces/<task_id>/runs/<run_id>/`
- Git worktree yok
- Her run için ayrı git branch yok

**Risk:**
- Git history'de hangi değişikliklerin hangi task'tan geldiği belirsiz
- Rollback zor
- Merge conflict'ler manuel çözülmeli

**What We Need:**
```python
# İdeal: Her run için ayrı git worktree
git worktree add workspaces/T-123/runs/R-456 T-123-R-456
# Run executes in worktree
# After success: merge to main branch
# After failure: delete worktree
```

---

### 3. **Patch Application System**

**Problem:** `apply_patch` syscall yok, direkt `write_file` kullanılıyor.

**Current State:**
- `write_file` direkt dosyayı overwrite ediyor
- Diff oluşturulmuyor (patch.diff var mı kontrol et)
- Incremental changes yok

**What We Need:**
```python
# İdeal: Patch-based changes
patch = generate_patch(old_content, new_content)
apply_patch(patch, ctx)  # Atomic, reversible
```

---

## 📊 Comparison: Current vs Ideal

| Feature | Current | Ideal | Risk Level |
|---------|---------|-------|------------|
| **File Modification** | ✅ Direct write | ✅ Direct write | 🟡 Medium |
| **Sandbox Isolation** | ❌ None | ✅ Docker/Process isolation | 🔴 High |
| **Git Worktree** | ❌ None | ✅ Per-run worktree | 🟡 Medium |
| **Patch System** | ❌ Direct write | ✅ Patch-based | 🟢 Low |
| **Rollback** | ❌ Manual | ✅ Automatic | 🔴 High |
| **Testing Before Apply** | ❌ No | ✅ Yes | 🔴 High |

---

## 🚨 Critical Risks

### Risk 1: Main Codebase Corruption
**Scenario:** LocalCoder yanlış kod üretir, direkt main codebase'e yazar.

**Impact:** 🔴 HIGH - Production code bozulabilir

**Mitigation Needed:**
1. Sandbox isolation (test before apply)
2. Git worktree (easy rollback)
3. Approval workflow (human review)

---

### Risk 2: No Rollback Mechanism
**Scenario:** Bir run başarısız olur, dosyalar bozulur.

**Impact:** 🔴 HIGH - Manual recovery gerekir

**Mitigation Needed:**
1. Git worktree (automatic cleanup)
2. Backup before changes
3. Transaction-like commits

---

### Risk 3: Untested Code in Production
**Scenario:** Code generate edilir, test edilmeden main'e yazılır.

**Impact:** 🟡 MEDIUM - Tests might fail later

**Mitigation Needed:**
1. Sandbox testing before apply
2. Verifier must pass before write
3. Staged commits (not direct writes)

---

## 💡 Recommendations

### Priority 1: Add Git Worktree Support
**Why:** Easy rollback, clear history, isolation

**Implementation:**
```python
# src/ybis/data_plane/git_workspace.py
def init_git_worktree(task_id: str, run_id: str) -> Path:
    """Create git worktree for run."""
    branch_name = f"task-{task_id}-run-{run_id}"
    worktree_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    
    # Create worktree
    subprocess.run(["git", "worktree", "add", str(worktree_path), branch_name])
    
    return worktree_path

def cleanup_worktree(worktree_path: Path):
    """Remove worktree after run."""
    subprocess.run(["git", "worktree", "remove", str(worktree_path)])
```

---

### Priority 2: Add Sandbox Testing
**Why:** Test before apply, prevent corruption

**Implementation:**
```python
# src/ybis/syscalls/exec.py
def run_command_sandboxed(cmd, ctx, cwd):
    """Run command in sandbox, test before applying."""
    # 1. Run in sandbox
    sandbox_result = sandbox.run_isolated(cmd, cwd=workspace_path)
    
    # 2. Verify results
    if sandbox_result.success:
        # 3. Apply to main codebase
        apply_changes_from_sandbox(workspace_path)
    else:
        # 4. Report failure
        raise ExecutionError(sandbox_result.stderr)
```

---

### Priority 3: Add Patch System
**Why:** Atomic changes, easy review, reversible

**Implementation:**
```python
# src/ybis/syscalls/fs.py
def apply_patch(patch_content: str, ctx: RunContext) -> PatchApplyReport:
    """Apply patch atomically."""
    # 1. Validate patch
    # 2. Create backup
    # 3. Apply patch
    # 4. Verify (run tests)
    # 5. Commit or rollback
```

---

## 🎯 Action Plan

### Phase 1: Quick Wins (1-2 days)
1. ✅ Add git worktree support to `workspace.py`
2. ✅ Add cleanup mechanism for failed runs
3. ✅ Add backup before file writes

### Phase 2: Sandbox Integration (3-5 days)
1. ✅ Integrate `ExecutionSandbox` from old structure
2. ✅ Add sandbox testing before apply
3. ✅ Add sandbox result validation

### Phase 3: Patch System (5-7 days)
1. ✅ Implement `apply_patch` syscall
2. ✅ Generate patch.diff before writes
3. ✅ Add patch validation and rollback

---

## 📝 Test Plan

### Test 1: Sandbox Isolation
```python
def test_sandbox_isolation():
    """Verify changes don't affect main codebase until approved."""
    # 1. Run task in sandbox
    # 2. Verify main codebase unchanged
    # 3. Approve changes
    # 4. Verify changes applied
```

### Test 2: Git Worktree
```python
def test_git_worktree():
    """Verify each run has isolated git worktree."""
    # 1. Create run
    # 2. Verify worktree created
    # 3. Make changes in worktree
    # 4. Verify main branch unchanged
    # 5. Cleanup worktree
```

### Test 3: Rollback
```python
def test_rollback():
    """Verify failed runs can be rolled back."""
    # 1. Create run with changes
    # 2. Simulate failure
    # 3. Verify rollback works
    # 4. Verify main codebase unchanged
```

---

## ✅ Conclusion

**Current Status:**
- ✅ Gerçek task yapabiliyor (dosya değişiklikleri çalışıyor)
- ❌ Sandbox isolation YOK (riskli)
- ❌ Git worktree YOK (rollback zor)
- ⚠️ Production-ready değil (test edilmemiş kod direkt yazılıyor)

**Recommendation:**
1. **Immediate:** Git worktree ekle (kolay, hızlı)
2. **Short-term:** Sandbox testing ekle (orta zorluk)
3. **Long-term:** Patch system ekle (zor ama ideal)

**Risk Level:** 🟡 MEDIUM-HIGH (şu an için test ortamında kullanılabilir, production için eklemeler gerekli)

