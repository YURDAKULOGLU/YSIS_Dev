# Vendor Framework'ler Analizi: Sandbox & Worktree

**Date:** 2026-01-08  
**Keşif:** Vendor klasöründe zaten hazır sandbox framework'leri var!

---

## 🎯 Bulunan Hazır Çözümler

### 1. **E2B Sandbox** ⭐⭐⭐ EN İYİ SEÇENEK

**Location:** `vendors/opendevin/third_party/runtime/impl/e2b/`  
**Status:** ✅ Open-source, production-ready  
**GitHub:** https://github.com/e2b-dev/e2b  
**PyPI:** `e2b` ve `e2b-code-interpreter`

**Özellikler:**
- ✅ **Secure cloud environment** - AI-generated code için tasarlanmış
- ✅ **Python SDK** - `e2b` package ile kolay entegrasyon
- ✅ **OpenDevin/OpenHands kullanıyor** - Zaten vendor'da var ve test edilmiş
- ✅ **Isolated filesystem** - Her sandbox kendi filesystem'i
- ✅ **Network isolation** - Güvenli network kontrolü
- ✅ **Resource limits** - CPU, memory limits
- ✅ **Custom Dockerfile** - Özel sandbox image'leri

**Kullanım:**
```python
from e2b_code_interpreter import Sandbox

# Create sandbox
sandbox = Sandbox.create()

# Execute command
result = sandbox.commands.run("python test.py")

# Access filesystem
sandbox.files.write("/workspace/test.py", content)

# Cleanup
sandbox.close()
```

**OpenDevin'deki Implementasyon:**
```python
# vendors/opendevin/third_party/runtime/impl/e2b/sandbox.py
class E2BBox:
    def __init__(self, config: SandboxConfig):
        self.sandbox = Sandbox.create()
    
    def execute(self, cmd: str, timeout: int | None = None):
        result = self.sandbox.commands.run(cmd)
        return result.exit_code, result.stdout
```

**Avantajlar:**
- ✅ Zaten vendor'da var
- ✅ OpenDevin/OpenHands tarafından kullanılıyor (test edilmiş)
- ✅ Open-source
- ✅ Production-ready
- ✅ AI agents için optimize edilmiş

---

### 2. **OpenDevin Runtime Implementations**

**Location:** `vendors/opendevin/third_party/runtime/impl/`

**Mevcut Runtime'lar:**
1. **E2B Runtime** - `e2b/` ⭐ (En iyi)
2. **Modal Runtime** - `modal/` (Cloud-based)
3. **Daytona Runtime** - `daytona/` (Dev environment)
4. **Runloop Runtime** - `runloop/` (Local execution)

**Kullanım:**
```python
# OpenDevin'in runtime interface'i
from openhands.runtime.impl.e2b.e2b_runtime import E2BRuntime

runtime = E2BRuntime(
    config=config,
    event_stream=event_stream,
    llm_registry=llm_registry,
)
```

**Avantajlar:**
- ✅ Zaten vendor'da var
- ✅ Production-ready
- ✅ Event-based architecture
- ✅ Plugin support

**Dezavantajlar:**
- ⚠️ OpenDevin'e bağımlı (heavy dependency)
- ⚠️ Sadece E2B'yi kullanmak için tüm OpenDevin'i yüklemek gerekir

---

### 3. **Git Worktree - OpenDevin'de Yok**

**Durum:** ❌ OpenDevin'de direkt git worktree yönetimi yok

**Alternatifler:**
1. **GitPython** - Pure Python, worktree support
2. **Git Worktree MCP Server** - MCP tool olarak kullanılabilir

---

## 🏆 Önerilen Çözüm: E2B Sandbox (Direkt)

### Neden E2B?

1. **Zaten Vendor'da Var** - `vendors/opendevin/third_party/runtime/impl/e2b/`
2. **Open-Source** - https://github.com/e2b-dev/e2b
3. **Production-Ready** - OpenDevin/OpenHands kullanıyor
4. **AI-Optimized** - AI-generated code için tasarlanmış
5. **Lightweight** - Sadece E2B SDK'sını kullan, OpenDevin'e bağımlı değil

### Implementation Plan

#### Step 1: E2B SDK'yı Kullan (OpenDevin'den Bağımsız)

```python
# pyproject.toml
dependencies = [
    "e2b>=1.0.0",  # E2B Python SDK
    "e2b-code-interpreter>=1.0.0",  # Code interpreter sandbox
]
```

#### Step 2: E2B Adapter Oluştur

```python
# src/ybis/adapters/e2b_sandbox.py
from e2b_code_interpreter import Sandbox
from ..contracts import RunContext

class E2BSandboxAdapter:
    """E2B sandbox adapter for YBIS."""
    
    def __init__(self):
        self.sandbox = None
    
    def create_sandbox(self, ctx: RunContext) -> Sandbox:
        """Create isolated E2B sandbox for run."""
        self.sandbox = Sandbox.create()
        return self.sandbox
    
    def execute_command(self, cmd: str, timeout: int = 30) -> dict:
        """Execute command in sandbox."""
        result = self.sandbox.commands.run(cmd, timeout=timeout)
        return {
            "success": result.exit_code == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.exit_code,
        }
    
    def write_file(self, path: str, content: str):
        """Write file in sandbox."""
        self.sandbox.files.write(path, content)
    
    def read_file(self, path: str) -> str:
        """Read file from sandbox."""
        return self.sandbox.files.read(path)
    
    def close(self):
        """Close sandbox."""
        if self.sandbox:
            self.sandbox.close()
```

#### Step 3: Git Worktree için GitPython

```python
# pyproject.toml
dependencies = [
    "GitPython>=3.1.40",  # Git worktree support
]
```

```python
# src/ybis/data_plane/git_workspace.py
from git import Repo

def init_git_worktree(task_id: str, run_id: str) -> Path:
    """Create git worktree using GitPython."""
    repo = Repo(PROJECT_ROOT)
    branch_name = f"task-{task_id}-run-{run_id}"
    worktree_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    
    repo.git.worktree("add", str(worktree_path), branch_name)
    return worktree_path
```

---

## 📊 Karşılaştırma

| Çözüm | Source | Dependency | Complexity | Recommendation |
|-------|--------|------------|-----------|---------------|
| **E2B SDK (Direkt)** | PyPI | `e2b` | 🟢 Low | ⭐⭐⭐ BEST |
| **OpenDevin Runtime** | Vendor | OpenDevin | 🔴 High | ⚠️ Overkill |
| **Docker SDK** | PyPI | `docker` | 🟡 Medium | ⭐⭐ Good |
| **GitPython** | PyPI | `GitPython` | 🟢 Low | ⭐⭐⭐ BEST |

---

## ✅ Final Recommendation

### Sandbox: E2B SDK (Direkt Kullanım)

**Why:**
- ✅ Zaten vendor'da var (referans için)
- ✅ Open-source, production-ready
- ✅ AI-optimized
- ✅ Lightweight (sadece SDK)
- ✅ OpenDevin'den bağımsız

**Implementation:**
```bash
pip install e2b e2b-code-interpreter
```

### Git Worktree: GitPython

**Why:**
- ✅ Pure Python
- ✅ Worktree support
- ✅ Easy to use
- ✅ Well-maintained

**Implementation:**
```bash
pip install GitPython
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install e2b e2b-code-interpreter GitPython
```

### 2. Create E2B Adapter
```python
# src/ybis/adapters/e2b_sandbox.py
# (Yukarıdaki kod)
```

### 3. Create Git Worktree Manager
```python
# src/ybis/data_plane/git_workspace.py
# (Yukarıdaki kod)
```

### 4. Integrate into Workflow
```python
# src/ybis/orchestrator/graph.py
from ..adapters.e2b_sandbox import E2BSandboxAdapter

def execute_node(state):
    # Create sandbox
    sandbox = E2BSandboxAdapter()
    sandbox.create_sandbox(ctx)
    
    # Execute in sandbox
    result = sandbox.execute_command("python test.py")
    
    # If success, apply changes
    if result["success"]:
        apply_changes_from_sandbox()
    
    sandbox.close()
```

---

## 📚 References

- **E2B GitHub:** https://github.com/e2b-dev/e2b
- **E2B Docs:** https://e2b.dev/docs
- **E2B Python SDK:** https://pypi.org/project/e2b/
- **OpenDevin E2B Implementation:** `vendors/opendevin/third_party/runtime/impl/e2b/`
- **GitPython:** https://gitpython.readthedocs.io/

---

## 🎯 Sonuç

**Vendor'da zaten hazır çözümler var!**

1. ✅ **E2B Sandbox** - OpenDevin'de var, direkt SDK kullan
2. ✅ **GitPython** - Git worktree için standart çözüm

**Custom implementation'a gerek yok!** Vendor'daki implementasyonları referans al, ama direkt SDK'ları kullan (daha lightweight).

