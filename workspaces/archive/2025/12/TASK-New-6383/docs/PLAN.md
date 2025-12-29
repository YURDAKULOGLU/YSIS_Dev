---
id: TASK-New-6383
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-28T23:19:10.300871
updated_at: 2025-12-28T23:50:00
target_files:
  - src/agentic/core/execution/aci.py
  - src/agentic/core/execution/command_allowlist.py
  - src/agentic/core/execution/sandbox.py
  - src/agentic/core/plugins/aider_executor_enhanced.py
---

# Task: SWE-agent ACI Pattern Implementation

## Objective

**Goal:** Implement Agent-Computer Interface (ACI) pattern from SWE-agent to constrain and secure agent execution with allowlisted commands, guardrails, and sandboxing.

**Context:**
- Current YBIS uses raw Aider execution (unrestricted shell access)
- SWE-agent showed constrained interface improves reliability & security
- Need to prevent dangerous commands, validate edits, isolate execution

**Success Definition:**
- Constrained command interface (limited action set)
- Command allowlist (only safe operations)
- Execution guardrails (linting, validation)
- Sandbox isolation (protected execution)
- Zero security regressions
- Backward compatible (feature-flagged)

---

## Research Summary

**Sources:**
- [SWE-agent Paper (arXiv)](https://arxiv.org/pdf/2405.15793)
- [SWE-agent ACI Docs](https://swe-agent.com/background/aci/)
- [SWE-Agent Frameworks](https://www.emergentmind.com/topics/swe-agent-frameworks)

**Key Design Principles:**
1. **Simple & Clear Actions:** Straightforward commands, not complex with many options
2. **Compact & Efficient:** Consolidate operations (navigation, editing, etc.)
3. **Guardrails:** Linters validate before edits go through
4. **Constrained Set:** File navigation, viewing, structured editing only
5. **Context Management:** Structured, condensed feedback

**SWE-agent Command Examples:**
```python
# File navigation
find_file(name)          # Find file by name
search_file(pattern)     # Search within file
search_dir(pattern, dir) # Search in directory

# File viewing
open(file, line_start, line_end)  # Open file with line range
scroll_up/scroll_down              # Navigation

# Structured editing (with guardrails)
edit(file, start_line, end_line, replacement)  # Replace lines
# → Runs linter BEFORE allowing edit

# Context management
summary()  # Summarize what's been done
```

---

## Approach

### Strategy: Layered Security Architecture

```
┌─────────────────────────────────────┐
│  Agent Request (Aider/Executor)     │
└──────────────┬──────────────────────┘
               │
        ┌──────▼───────┐
        │  ACI Layer   │  ← Translate to safe commands
        └──────┬───────┘
               │
        ┌──────▼──────────┐
        │  Allowlist Check │  ← Verify command is allowed
        └──────┬───────────┘
               │
        ┌──────▼──────────┐
        │  Guardrails      │  ← Lint/validate before exec
        └──────┬───────────┘
               │
        ┌──────▼──────────┐
        │  Sandbox         │  ← Isolated execution
        └──────┬───────────┘
               │
        ┌──────▼──────────┐
        │  OS/Filesystem   │
        └──────────────────┘
```

**Benefits:**
- Security: Multiple layers of protection
- Reliability: Validation before execution
- Debuggability: Clear logging at each layer
- Flexibility: Can disable layers via flags

---

## Steps

### **Phase 1: Core ACI Interface (3-4 hours)**

**1.1 Create ACI Base Class**

File: `src/agentic/core/execution/aci.py`

```python
class AgentComputerInterface:
    """
    Constrained interface for agent-computer interactions.
    Inspired by SWE-agent's ACI pattern.
    """

    # File Navigation
    async def find_file(self, name: str, dir: str = ".") -> List[str]:
        """Find files matching name pattern"""

    async def search_file(self, file: str, pattern: str) -> List[Tuple[int, str]]:
        """Search within a file, return (line_num, content)"""

    async def search_dir(self, pattern: str, dir: str = ".") -> Dict[str, List[int]]:
        """Search pattern in directory, return {file: [line_nums]}"""

    # File Viewing
    async def open_file(self, file: str, start_line: int = 1, end_line: int = None) -> str:
        """Open file and return content (line range)"""

    async def scroll_down(self, file: str, lines: int = 10) -> str:
        """Scroll down in open file"""

    async def scroll_up(self, file: str, lines: int = 10) -> str:
        """Scroll up in open file"""

    # Structured Editing (with Guardrails)
    async def edit_file(
        self,
        file: str,
        start_line: int,
        end_line: int,
        replacement: str,
        validate: bool = True
    ) -> EditResult:
        """
        Edit file (replace lines).
        Runs linter BEFORE applying if validate=True.
        """

    # Execution (Constrained)
    async def run_command(self, command: str, timeout: int = 30) -> CommandResult:
        """
        Run command (if allowlisted).
        Returns: stdout, stderr, exit_code
        """

    # Context Management
    async def get_context(self) -> Dict[str, Any]:
        """Get current context (files opened, edits made, etc.)"""

    async def summarize(self) -> str:
        """Summarize what's been done so far"""
```

**1.2 Action Results (Data Classes)**

```python
@dataclass
class EditResult:
    success: bool
    file: str
    lines_changed: int
    validation_passed: bool
    validation_errors: List[str] = field(default_factory=list)
    diff: Optional[str] = None

@dataclass
class CommandResult:
    success: bool
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    sandbox_violation: bool = False
```

**Expected Output:**
- `src/agentic/core/execution/aci.py` (~300 lines)
- Clean async API
- Type-safe results

---

### **Phase 2: Command Allowlist (2-3 hours)**

**2.1 Create Allowlist System**

File: `src/agentic/core/execution/command_allowlist.py`

```python
class CommandAllowlist:
    """
    Allowlist of safe commands for agent execution.
    Blocks dangerous operations (rm -rf, sudo, etc.)
    """

    SAFE_COMMANDS = {
        # File operations (read-only)
        "cat", "head", "tail", "less", "grep", "find", "ls", "tree",
        # Code tools
        "git", "pytest", "python", "node", "npm", "pip",
        # Build tools
        "make", "cmake", "cargo", "go",
        # Linters
        "ruff", "pylint", "eslint", "black", "isort",
    }

    DANGEROUS_PATTERNS = [
        r"rm\s+-rf",        # Recursive delete
        r"sudo",            # Privilege escalation
        r"chmod\s+777",     # Dangerous permissions
        r">\s*/dev/",       # Writing to device files
        r"curl.*\|\s*sh",   # Piping to shell
        r"wget.*\|\s*sh",
    ]

    def is_allowed(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Check if command is allowed.
        Returns: (allowed, reason_if_blocked)
        """

    def suggest_alternative(self, command: str) -> Optional[str]:
        """Suggest safe alternative if command is blocked"""
```

**2.2 Configuration**

```python
# Config flags
ENABLE_COMMAND_ALLOWLIST = os.getenv("YBIS_ENABLE_ALLOWLIST", "true").lower() == "true"
ALLOWLIST_MODE = os.getenv("YBIS_ALLOWLIST_MODE", "strict")  # strict|permissive|off
```

**Expected Output:**
- `command_allowlist.py` (~200 lines)
- Configurable allowlist
- Clear error messages

---

### **Phase 3: Execution Guardrails (2-3 hours)**

**3.1 Pre-Edit Validation**

File: `src/agentic/core/execution/guardrails.py`

```python
class ExecutionGuardrails:
    """
    Validation and guardrails for agent actions.
    Prevents syntax errors, dangerous edits, etc.
    """

    async def validate_edit(
        self,
        file: str,
        new_content: str
    ) -> ValidationResult:
        """
        Validate edit before applying.
        - Syntax check (ruff for Python)
        - Import check (no broken imports)
        - Type check (mypy if enabled)
        """

    async def validate_command(
        self,
        command: str
    ) -> ValidationResult:
        """
        Validate command before execution.
        - Allowlist check
        - Resource limit check (timeout, memory)
        - Dangerous pattern check
        """

    async def check_file_safety(self, file: str) -> bool:
        """Check if file is safe to edit (not system file, etc.)"""
```

**3.2 Linting Integration**

```python
class PythonLinter:
    """Lint Python code using ruff"""

    async def lint(self, file: str) -> LintResult:
        """
        Run ruff on file.
        Returns: errors, warnings, suggestions
        """

    async def can_apply_edit(self, file: str, new_content: str) -> bool:
        """
        Check if edit would pass linting.
        Temporarily writes to temp file, lints, then discards.
        """
```

**Expected Output:**
- `guardrails.py` (~250 lines)
- Python linting (ruff)
- Pre-edit validation

---

### **Phase 4: Sandboxing (3-4 hours)**

**4.1 Execution Sandbox**

File: `src/agentic/core/execution/sandbox.py`

```python
class ExecutionSandbox:
    """
    Sandbox for isolating command execution.
    Limits resources, restricts access.
    """

    def __init__(
        self,
        timeout_seconds: int = 30,
        max_memory_mb: int = 512,
        allowed_dirs: List[str] = None,
        network_access: bool = False
    ):
        self.timeout = timeout_seconds
        self.max_memory = max_memory_mb
        self.allowed_dirs = allowed_dirs or [os.getcwd()]
        self.network_access = network_access

    async def run_isolated(
        self,
        command: str,
        cwd: str = None
    ) -> CommandResult:
        """
        Run command in isolated environment.
        - Timeout enforcement
        - Memory limits
        - Directory restrictions
        - Network isolation (optional)
        """

    def _check_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed directories"""

    def _enforce_limits(self, process) -> None:
        """Enforce resource limits on process"""
```

**4.2 Sandbox Modes**

```python
SANDBOX_MODE = os.getenv("YBIS_SANDBOX_MODE", "strict")  # strict|permissive|off

SANDBOX_CONFIGS = {
    "strict": {
        "timeout": 30,
        "max_memory_mb": 512,
        "network_access": False,
        "allowed_dirs": [os.getcwd()],
    },
    "permissive": {
        "timeout": 120,
        "max_memory_mb": 2048,
        "network_access": True,
        "allowed_dirs": [os.getcwd(), "/tmp"],
    },
    "off": None  # No sandboxing
}
```

**Expected Output:**
- `sandbox.py` (~300 lines)
- Resource limits
- Path restrictions

---

### **Phase 5: Integration with Aider (2 hours)**

**5.1 Update AiderExecutorEnhanced**

File: `src/agentic/core/plugins/aider_executor_enhanced.py`

```python
class AiderExecutorEnhanced:
    """Enhanced Aider executor with ACI pattern"""

    def __init__(self):
        self.aci = AgentComputerInterface()  # NEW
        self.use_aci = os.getenv("YBIS_USE_ACI", "true").lower() == "true"

    async def execute(self, plan, artifacts_path, ...):
        if self.use_aci:
            # Use constrained ACI interface
            return await self._execute_with_aci(plan, artifacts_path)
        else:
            # Fallback to old direct execution
            return await self._execute_direct(plan, artifacts_path)

    async def _execute_with_aci(self, plan, artifacts_path):
        """Execute using ACI (constrained, validated, sandboxed)"""

        # Translate plan to ACI actions
        actions = self._plan_to_aci_actions(plan)

        # Execute each action through ACI
        for action in actions:
            result = await self.aci.execute_action(action)

            # Log result
            # Handle errors
            # Update context

    async def _execute_direct(self, plan, artifacts_path):
        """Fallback: direct execution (old method)"""
        # Original implementation
```

**5.2 Feature Flag**

```python
# In config.py
USE_ACI = os.getenv("YBIS_USE_ACI", "false").lower() == "true"  # Off by default (safe)
```

**Expected Output:**
- Updated `aider_executor_enhanced.py` (+100 lines)
- Feature-flagged integration
- Backward compatible

---

### **Phase 6: Testing (2-3 hours)**

**6.1 Test Suite**

File: `workspaces/active/TASK-New-6383/tests/test_aci.py`

```python
class TestACI:
    """Test Agent-Computer Interface"""

    @pytest.mark.asyncio
    async def test_find_file(self):
        """Test file finding"""

    @pytest.mark.asyncio
    async def test_search_file(self):
        """Test file search"""

    @pytest.mark.asyncio
    async def test_edit_with_validation(self):
        """Test edit with linting validation"""

    @pytest.mark.asyncio
    async def test_dangerous_command_blocked(self):
        """Test dangerous commands are blocked"""
```

File: `workspaces/active/TASK-New-6383/tests/test_allowlist.py`

```python
class TestAllowlist:
    """Test command allowlist"""

    def test_safe_commands_allowed(self):
        """Test safe commands pass"""

    def test_dangerous_commands_blocked(self):
        """Test dangerous commands blocked"""

    def test_alternative_suggestions(self):
        """Test alternative command suggestions"""
```

File: `workspaces/active/TASK-New-6383/tests/test_sandbox.py`

```python
class TestSandbox:
    """Test execution sandbox"""

    @pytest.mark.asyncio
    async def test_timeout_enforcement(self):
        """Test command timeout works"""

    @pytest.mark.asyncio
    async def test_path_restrictions(self):
        """Test can't access restricted paths"""

    @pytest.mark.asyncio
    async def test_resource_limits(self):
        """Test resource limits enforced"""
```

**Expected Output:**
- 20+ comprehensive tests
- >90% code coverage
- All tests passing

---

### **Phase 7: Documentation (1 hour)**

**7.1 Documentation Files**
- RUNBOOK.md (execution log)
- RESULT.md (outcomes)
- ACI_GUIDE.md (usage guide)

**7.2 Configuration Guide**

```bash
# Enable ACI pattern
export YBIS_USE_ACI=true

# Allowlist mode
export YBIS_ALLOWLIST_MODE=strict  # strict|permissive|off

# Sandbox mode
export YBIS_SANDBOX_MODE=strict    # strict|permissive|off
```

---

## Risks & Mitigations

### Risk 1: Performance Overhead
**Impact:** MEDIUM
**Mitigation:**
- Caching for repeated operations
- Async execution (no blocking)
- Lazy validation (only when needed)
- Benchmark before/after

### Risk 2: Breaking Aider Workflow
**Impact:** HIGH
**Mitigation:**
- Feature flag (default OFF)
- Fallback to direct execution
- Gradual rollout
- Extensive testing

### Risk 3: False Positives (Blocking Safe Commands)
**Impact:** MEDIUM
**Mitigation:**
- Configurable allowlist
- Alternative suggestions
- Override mechanism (with logging)
- Permissive mode for testing

### Risk 4: Sandbox Escape
**Impact:** LOW
**Mitigation:**
- Multiple layers (allowlist + guardrails + sandbox)
- Regular security reviews
- Leverage OS-level isolation (chroot, containers)

---

## Success Criteria

### Must-Have:
- ✅ ACI interface implemented
- ✅ Command allowlist operational
- ✅ Execution guardrails (linting)
- ✅ Sandbox isolation working
- ✅ Feature-flagged integration
- ✅ Zero security regressions
- ✅ Backward compatible
- ✅ Tests passing (>90% coverage)
- ✅ Documentation complete

### Metrics:
- **Security:** 0 dangerous commands executed
- **Reliability:** <5% false positives (blocked safe commands)
- **Performance:** <100ms overhead per command
- **Usability:** Clear error messages, alternatives suggested

---

## Timeline

**Total Estimated Time:** 15-20 hours (2-3 days)

- Phase 1 (ACI Interface): 3-4 hours
- Phase 2 (Allowlist): 2-3 hours
- Phase 3 (Guardrails): 2-3 hours
- Phase 4 (Sandboxing): 3-4 hours
- Phase 5 (Integration): 2 hours
- Phase 6 (Testing): 2-3 hours
- Phase 7 (Docs): 1 hour

---

## Dependencies

### Completed:
- ✅ TASK-New-9134 (Optimization Trinity)
- ✅ SimplePlannerV2 operational
- ✅ Metrics system in place

### Parallel Work:
- Codex: TASK-New-4130 (Provider abstraction)
- Gemini: TASK-New-7553 (Langfuse observability)

### Blockers:
- None currently

---

**Status:** Ready to begin implementation
**Next Step:** Phase 1 - Create ACI Interface
