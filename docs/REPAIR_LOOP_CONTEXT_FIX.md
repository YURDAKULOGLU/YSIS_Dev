# Repair Loop Context Fix

**Tarih**: 2026-01-11  
**Sorun**: Repair loop'un neden fail olduğu ve LLM'e yeterli context verilmediği

---

## 🔍 SORUN ANALİZİ

### 1. Test Fail
```
Lint Passed: False
Tests Passed: False
Errors:
  - Ruff check failed: warning: The top-level linter settings are deprecated...
  - Pytest failed
```

### 2. Repair Fail
```
Repair attempt 1/3
Actions: Failed to fix deprecated settings; Repair plan validation failed - no valid files found
```

### 3. Loop Neden Oluştu?
- Test fail → Repair'e gidiyor
- Repair `pyproject.toml`'i düzeltmeye çalışıyor
- Ama repair plan validation'da `pyproject.toml` protected file olarak filtreleniyor
- Repair plan boş kalıyor → implement hiçbir şey yapmıyor
- Test tekrar fail → Loop devam ediyor

---

## ✅ YAPILAN DÜZELTMELER

### 1. Repair Plan Validation - Protected Files İzin

**Sorun**: Repair plan'da `pyproject.toml` olsa bile, validation'da protected files filtreleniyordu.

**Çözüm**: Repair için protected files'a izin ver (repair config dosyalarını düzeltmeli).

**Kod**:
```python
# Validate repair plan files exist
# NOTE: For repair, we allow protected files (like pyproject.toml) 
# since repair needs to fix config issues
validated_repair_files = []
for file_path in repair_plan.files:
    # Skip invalid patterns
    if not file_path or file_path in ["all", "of", "the", "existing", "code"]:
        continue
    
    # For repair, allow protected files (they need to be fixed)
    if full_path.exists():
        validated_repair_files.append(path_attempt)
```

### 2. LLM Context Zenginleştirme

**Sorun**: Repair objective'ine yeterli context verilmiyordu.

**Çözüm**: Repair objective'ine şunları ekle:
- Hangi dosyalar değiştiriliyor
- Tam error mesajları
- Warning'ler
- Düzeltme talimatları

**Kod**:
```python
repair_objective_parts = [
    "Fix test failures in the following files:",
    f"Files being modified: {', '.join(current_files)}",
    "",
    "ERRORS:",
    error_summary,
    "",
    "WARNINGS:",
    warning_summary,
    "",
    "INSTRUCTIONS:",
    "1. Review the errors above",
    "2. Identify which files need to be fixed",
    "3. Make minimal changes to fix the errors",
    "4. Ensure fixes don't break existing functionality",
]
```

### 3. pyproject.toml Fix - Worktree Support

**Sorun**: `_fix_pyproject_toml_deprecated_settings` PROJECT_ROOT'ta çalışıyordu, worktree'de değil.

**Çözüm**: Worktree path'i parametre olarak al, önce worktree'de dene.

**Kod**:
```python
def _fix_pyproject_toml_deprecated_settings(project_root: Path, worktree_path: Path | None = None) -> bool:
    # Prefer worktree path if available (repair should fix worktree, not main project)
    if worktree_path and (worktree_path / "pyproject.toml").exists():
        toml_path = worktree_path / "pyproject.toml"
    else:
        toml_path = project_root / "pyproject.toml"
```

### 4. Ruff Auto-Fix - Worktree Support

**Sorun**: Ruff PROJECT_ROOT'ta çalışıyordu.

**Çözüm**: Worktree path'te çalıştır.

**Kod**:
```python
worktree_path = Path(ctx.run_path) if ctx.run_path else PROJECT_ROOT
src_path = worktree_path / "src" if (worktree_path / "src").exists() else PROJECT_ROOT / "src"

result = subprocess.run(
    ["ruff", "check", "--fix", str(src_path)],
    cwd=worktree_path,
    ...
)
```

---

## 🎯 SONUÇ

Artık repair loop:
- ✅ Protected files'ı repair için değiştirebilir (`pyproject.toml` gibi)
- ✅ LLM'e zengin context veriliyor (hangi dosyalar, hangi hatalar, nasıl düzeltilecek)
- ✅ Worktree'de düzeltmeler yapılıyor (main project'e dokunmuyor)
- ✅ Repair plan validation doğru çalışıyor

**Beklenen Davranış**:
1. Test fail → Repair'e git
2. Repair `pyproject.toml`'i düzeltebilir (protected file ama repair için izin var)
3. Repair plan validation geçer
4. Implement düzeltmeleri uygular
5. Test tekrar çalışır → Pass veya tekrar Repair (max 3 attempt)

