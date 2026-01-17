# SOTA Solutions Research: Sandbox & Git Worktree

**Date:** 2026-01-08  
**Objective:** Find ready-made solutions instead of custom implementation

**UPDATE:** Vendor klasöründe zaten hazır framework'ler bulundu! Detaylar için `docs/VENDOR_FRAMEWORKS_ANALYSIS.md` bak.

---

## 🎯 Requirements

1. **Sandbox Isolation** - Safe code execution with resource limits
2. **Git Worktree Management** - Per-run git isolation
3. **Python Integration** - Easy to integrate with existing codebase
4. **Production Ready** - Battle-tested, maintained

---

## 🔍 Research Results

### Option 1: Docker SDK (docker-py) ⭐ RECOMMENDED

**Library:** `docker` (docker-py)  
**GitHub:** https://github.com/docker/docker-py  
**PyPI:** `docker>=7.0.0`  
**Stars:** 7k+ ⭐  
**Status:** ✅ Actively maintained

**Pros:**
- ✅ Industry standard (Docker)
- ✅ Full isolation (filesystem, network, resources)
- ✅ Easy Python API
- ✅ Production-ready
- ✅ Cross-platform (Linux, Windows, macOS)
- ✅ Resource limits (CPU, memory, disk)
- ✅ Network isolation
- ✅ Clean state per execution

**Cons:**
- ⚠️ Requires Docker daemon
- ⚠️ Slightly heavier than process-based sandbox

**Usage Example:**
```python
import docker

client = docker.from_env()

# Run command in isolated container
container = client.containers.run(
    "python:3.12-slim",
    "python test.py",
    remove=True,  # Auto-remove after execution
    mem_limit="512m",
    network_disabled=True,
    volumes={"/workspace": {"bind": "/workspace", "mode": "ro"}},
    working_dir="/workspace",
)

print(container.decode('utf-8'))
```

**Integration:**
```python
# src/ybis/adapters/docker_sandbox.py
from docker import DockerClient

class DockerSandboxAdapter:
    def run_isolated(self, cmd, cwd, timeout=30):
        client = DockerClient()
        container = client.containers.run(
            "python:3.12-slim",
            cmd,
            remove=True,
            mem_limit="512m",
            network_disabled=True,
            volumes={str(cwd): {"bind": "/workspace", "mode": "rw"}},
        )
        return container.decode('utf-8')
```

---

### Option 2: GitPython ⭐ RECOMMENDED

**Library:** `GitPython`  
**GitHub:** https://github.com/gitpython-developers/GitPython  
**PyPI:** `GitPython>=3.1.40`  
**Stars:** 4k+ ⭐  
**Status:** ✅ Actively maintained

**Pros:**
- ✅ Pure Python Git API
- ✅ Worktree support (Git 2.5+)
- ✅ Easy to use
- ✅ Well-documented
- ✅ Production-ready

**Cons:**
- ⚠️ Requires Git installed
- ⚠️ Worktree support requires Git 2.5+

**Usage Example:**
```python
from git import Repo

repo = Repo(PROJECT_ROOT)

# Create worktree
worktree_path = PROJECT_ROOT / "workspaces" / "T-123" / "runs" / "R-456"
branch_name = "task-T-123-run-R-456"

# Create worktree
repo.git.worktree("add", str(worktree_path), branch_name)

# Work in worktree
worktree_repo = Repo(worktree_path)
worktree_repo.git.checkout(branch_name)

# Make changes...

# Cleanup
repo.git.worktree("remove", str(worktree_path))
```

**Integration:**
```python
# src/ybis/data_plane/git_workspace.py
from git import Repo

def init_git_worktree(task_id: str, run_id: str) -> Path:
    """Create git worktree for isolated execution."""
    repo = Repo(PROJECT_ROOT)
    branch_name = f"task-{task_id}-run-{run_id}"
    worktree_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    
    # Create worktree
    repo.git.worktree("add", str(worktree_path), branch_name)
    
    return worktree_path
```

---

### Option 3: subprocess + resource (Built-in) ⚠️ LIMITED

**Library:** Built-in (`subprocess` + `resource`)  
**Status:** ✅ Always available

**Pros:**
- ✅ No dependencies
- ✅ Lightweight
- ✅ Cross-platform (with limitations)

**Cons:**
- ❌ Limited isolation (process-level only)
- ❌ No filesystem isolation
- ❌ No network isolation (without extra tools)
- ❌ Windows support limited

**Usage Example:**
```python
import subprocess
import resource

# Set resource limits (Unix only)
resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))  # 512MB
resource.setrlimit(resource.RLIMIT_CPU, (30, 30))  # 30 seconds

result = subprocess.run(
    ["python", "test.py"],
    timeout=30,
    cwd=workspace_path,
    capture_output=True,
)
```

**Verdict:** ⚠️ Not recommended for production - too limited

---

### Option 4: Firejail (External Tool) ⚠️ COMPLEX

**Tool:** `firejail`  
**Status:** ✅ Actively maintained  
**Platform:** Linux only

**Pros:**
- ✅ Strong isolation
- ✅ Lightweight
- ✅ Network isolation

**Cons:**
- ❌ Linux only
- ❌ Requires external binary
- ❌ Complex Python integration
- ❌ Not cross-platform

**Verdict:** ⚠️ Not recommended - platform-specific

---

## 🏆 Recommended Solution Stack

### For Sandbox: Docker SDK
```python
# pyproject.toml
dependencies = [
    "docker>=7.0.0",  # Add this
]
```

**Why:**
- Industry standard
- Full isolation
- Easy integration
- Production-ready

---

### For Git Worktree: GitPython
```python
# pyproject.toml
dependencies = [
    "GitPython>=3.1.40",  # Add this
]
```

**Why:**
- Pure Python
- Worktree support
- Easy to use
- Well-maintained

---

## 📦 Implementation Plan

### Step 1: Add Dependencies
```toml
# pyproject.toml
dependencies = [
    "docker>=7.0.0",
    "GitPython>=3.1.40",
]
```

### Step 2: Create Docker Sandbox Adapter
```python
# src/ybis/adapters/docker_sandbox.py
from docker import DockerClient
from docker.errors import DockerException

class DockerSandboxAdapter:
    """Docker-based sandbox for code execution."""
    
    def __init__(self, image: str = "python:3.12-slim"):
        self.client = DockerClient()
        self.image = image
    
    def run_isolated(self, cmd: list[str], cwd: Path, timeout: int = 30) -> dict:
        """Run command in isolated Docker container."""
        try:
            container = self.client.containers.run(
                self.image,
                cmd,
                remove=True,
                mem_limit="512m",
                network_disabled=True,
                volumes={str(cwd): {"bind": "/workspace", "mode": "rw"}},
                working_dir="/workspace",
                timeout=timeout,
            )
            return {
                "success": True,
                "stdout": container.decode('utf-8'),
                "stderr": "",
            }
        except DockerException as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
            }
```

### Step 3: Create Git Worktree Manager
```python
# src/ybis/data_plane/git_workspace.py
from git import Repo, GitCommandError

def init_git_worktree(task_id: str, run_id: str) -> Path:
    """Create git worktree for isolated execution."""
    repo = Repo(PROJECT_ROOT)
    branch_name = f"task-{task_id}-run-{run_id}"
    worktree_path = PROJECT_ROOT / "workspaces" / task_id / "runs" / run_id
    
    try:
        # Create worktree
        repo.git.worktree("add", str(worktree_path), branch_name)
        return worktree_path
    except GitCommandError as e:
        # Fallback to regular directory if worktree fails
        worktree_path.mkdir(parents=True, exist_ok=True)
        return worktree_path

def cleanup_worktree(worktree_path: Path):
    """Remove git worktree."""
    try:
        repo = Repo(PROJECT_ROOT)
        repo.git.worktree("remove", str(worktree_path))
    except GitCommandError:
        # If worktree removal fails, just delete directory
        import shutil
        shutil.rmtree(worktree_path, ignore_errors=True)
```

---

## 🔄 Migration Strategy

### Phase 1: Add Dependencies (5 min)
```bash
pip install docker GitPython
```

### Phase 2: Create Adapters (1-2 hours)
- Create `docker_sandbox.py` adapter
- Create `git_workspace.py` manager
- Add to `__init__.py`

### Phase 3: Integrate (2-3 hours)
- Update `workspace.py` to use git worktree
- Update `exec.py` to use docker sandbox (optional, can be gradual)
- Add fallback if Docker/Git not available

### Phase 4: Test (1 hour)
- Test git worktree creation/cleanup
- Test docker sandbox execution
- Test fallback mechanisms

**Total Time:** ~4-6 hours

---

## ✅ Benefits

1. **No Custom Code** - Use battle-tested libraries
2. **Production Ready** - Industry standard tools
3. **Easy Maintenance** - Libraries handle updates
4. **Better Isolation** - Docker provides full isolation
5. **Git Integration** - Native git worktree support

---

## 📚 References

- **Docker SDK:** https://docker-py.readthedocs.io/
- **GitPython:** https://gitpython.readthedocs.io/
- **Docker Hub:** https://hub.docker.com/_/python

---

## 🎯 Decision

**Recommended:** Use Docker SDK + GitPython

**Why:**
- ✅ SOTA (State-of-the-Art) solutions
- ✅ Production-ready
- ✅ Well-maintained
- ✅ Easy integration
- ✅ No custom code needed

**Alternative:** If Docker is too heavy, use subprocess + resource (but limited isolation)

