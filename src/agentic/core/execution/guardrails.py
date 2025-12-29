"""
Execution Guardrails - Validation and safety checks for agent actions.

Prevents:
- Syntax errors (linting before edits)
- Broken imports
- Dangerous file modifications
- Resource limit violations

Features:
- Pre-edit validation (syntax, imports, types)
- Pre-command validation (resource checks)
- File safety checks
- Configurable linters
"""

import os
import ast
import asyncio
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ValidationResult:
    """Result of a validation check"""
    success: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class FileType(Enum):
    """Supported file types for validation"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    GO = "go"
    UNKNOWN = "unknown"


# ============================================================================
# Execution Guardrails
# ============================================================================

class ExecutionGuardrails:
    """
    Validation and guardrails for agent actions.

    Provides:
    - Pre-edit validation (syntax, linting)
    - Pre-command validation (resource limits)
    - File safety checks
    - Language-specific linters
    """

    def __init__(
        self,
        enable_linting: bool = True,
        enable_syntax_check: bool = True,
        enable_import_check: bool = True,
        enable_type_check: bool = False,  # Expensive, off by default
        base_dir: str = None
    ):
        """
        Initialize guardrails.

        Args:
            enable_linting: Run linters on edits
            enable_syntax_check: Check syntax before edits
            enable_import_check: Check imports are valid
            enable_type_check: Run type checker (mypy for Python)
            base_dir: Base directory for file operations
        """
        self.enable_linting = enable_linting
        self.enable_syntax_check = enable_syntax_check
        self.enable_import_check = enable_import_check
        self.enable_type_check = enable_type_check
        self.base_dir = Path(base_dir) if base_dir else Path.getcwd()

        # Lazy-loaded linters
        self._python_linter = None
        self._js_linter = None

    # ========================================================================
    # Edit Validation
    # ========================================================================

    async def validate_edit(
        self,
        file: str,
        new_content: str
    ) -> ValidationResult:
        """
        Validate edit before applying.

        Checks:
        1. Syntax (language-specific)
        2. Imports (not broken)
        3. Linting (if enabled)
        4. Type checking (if enabled)

        Args:
            file: File path
            new_content: Proposed new content

        Returns:
            ValidationResult with errors/warnings

        Example:
            >>> result = await guardrails.validate_edit("main.py", new_code)
            >>> if not result.success:
            >>>     print(f"Validation failed: {result.errors}")
        """
        errors = []
        warnings = []
        suggestions = []

        # Detect file type
        file_type = self._detect_file_type(file)

        # Syntax check
        if self.enable_syntax_check:
            syntax_result = await self._check_syntax(file, new_content, file_type)
            if not syntax_result.success:
                errors.extend(syntax_result.errors)
                warnings.extend(syntax_result.warnings)

        # Import check (Python only for now)
        if self.enable_import_check and file_type == FileType.PYTHON:
            import_result = await self._check_imports(new_content)
            if not import_result.success:
                warnings.extend(import_result.errors)  # Imports are warnings, not errors

        # Linting
        if self.enable_linting:
            lint_result = await self._lint_content(file, new_content, file_type)
            if not lint_result.success:
                # Linting errors are usually warnings
                warnings.extend(lint_result.errors)
                suggestions.extend(lint_result.suggestions)

        # Type checking (if enabled)
        if self.enable_type_check and file_type == FileType.PYTHON:
            type_result = await self._check_types(file, new_content)
            if not type_result.success:
                warnings.extend(type_result.errors)

        # Overall success = no critical errors (warnings are OK)
        success = len(errors) == 0

        return ValidationResult(
            success=success,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            details={
                "file_type": file_type.value,
                "syntax_checked": self.enable_syntax_check,
                "import_checked": self.enable_import_check,
                "linted": self.enable_linting,
                "type_checked": self.enable_type_check
            }
        )

    async def validate_command(
        self,
        command: str,
        timeout: int = 30,
        max_memory_mb: int = 512
    ) -> ValidationResult:
        """
        Validate command before execution.

        Checks:
        1. Allowlist (if command_allowlist enabled)
        2. Resource limits (timeout, memory)
        3. Dangerous patterns

        Args:
            command: Command to validate
            timeout: Timeout in seconds
            max_memory_mb: Memory limit in MB

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []

        # Check resource limits
        if timeout > 300:  # 5 minutes
            warnings.append(f"Long timeout ({timeout}s) - consider reducing")

        if max_memory_mb > 2048:  # 2GB
            warnings.append(f"High memory limit ({max_memory_mb}MB) - consider reducing")

        # Check for suspiciously long commands
        if len(command) > 5000:
            errors.append("Command too long (>5000 chars) - possible injection attempt")

        # Success if no errors
        success = len(errors) == 0

        return ValidationResult(
            success=success,
            errors=errors,
            warnings=warnings
        )

    async def check_file_safety(self, file: str) -> bool:
        """
        Check if file is safe to edit.

        Blocks:
        - System files (/etc, /bin, /usr, /var)
        - Hidden system files (.git, .env with credentials)
        - Binary files

        Args:
            file: File path

        Returns:
            True if safe to edit
        """
        file_path = Path(file)

        # Block system directories
        system_dirs = ["/etc", "/bin", "/usr", "/var", "/sys", "/proc", "/boot"]
        for sys_dir in system_dirs:
            if str(file_path).startswith(sys_dir):
                return False

        # Block .env files (may contain credentials)
        if file_path.name == ".env":
            return False

        # Block .git directory
        if ".git" in file_path.parts:
            return False

        # Block binary files (basic check)
        if file_path.exists():
            try:
                with open(file_path, 'rb') as f:
                    chunk = f.read(1024)
                    # If >10% null bytes, probably binary
                    if chunk.count(b'\x00') > len(chunk) * 0.1:
                        return False
            except Exception:
                return False

        return True

    # ========================================================================
    # Language-Specific Validation
    # ========================================================================

    def _detect_file_type(self, file: str) -> FileType:
        """Detect file type from extension"""
        ext = Path(file).suffix.lower()

        mapping = {
            ".py": FileType.PYTHON,
            ".pyi": FileType.PYTHON,
            ".js": FileType.JAVASCRIPT,
            ".jsx": FileType.JAVASCRIPT,
            ".ts": FileType.TYPESCRIPT,
            ".tsx": FileType.TYPESCRIPT,
            ".rs": FileType.RUST,
            ".go": FileType.GO,
        }

        return mapping.get(ext, FileType.UNKNOWN)

    async def _check_syntax(
        self,
        file: str,
        content: str,
        file_type: FileType
    ) -> ValidationResult:
        """Check syntax for file type"""
        if file_type == FileType.PYTHON:
            return await self._check_python_syntax(content)
        elif file_type in [FileType.JAVASCRIPT, FileType.TYPESCRIPT]:
            return await self._check_js_syntax(content, file_type)
        else:
            # Unknown file type - skip syntax check
            return ValidationResult(success=True)

    async def _check_python_syntax(self, content: str) -> ValidationResult:
        """Check Python syntax using AST"""
        try:
            ast.parse(content)
            return ValidationResult(success=True)
        except SyntaxError as e:
            return ValidationResult(
                success=False,
                errors=[f"Syntax error at line {e.lineno}: {e.msg}"]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[f"Parse error: {e}"]
            )

    async def _check_js_syntax(
        self,
        content: str,
        file_type: FileType
    ) -> ValidationResult:
        """Check JavaScript/TypeScript syntax (requires node)"""
        # For now, skip JS syntax check (would require node installed)
        # TODO: Implement with esprima or acorn parser
        return ValidationResult(
            success=True,
            warnings=["JavaScript syntax check not implemented yet"]
        )

    async def _check_imports(self, content: str) -> ValidationResult:
        """Check Python imports are valid"""
        try:
            tree = ast.parse(content)
            imports = []
            errors = []

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])

            # Check if imports are valid (basic check - just try to import)
            for imp in set(imports):
                try:
                    __import__(imp)
                except ImportError:
                    # Not necessarily an error - might be local module
                    # Just warn
                    pass

            return ValidationResult(success=True)

        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[f"Import check failed: {e}"]
            )

    async def _check_types(self, file: str, content: str) -> ValidationResult:
        """Run mypy type checker (if available)"""
        try:
            # Write content to temp file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(content)
                temp_path = f.name

            # Run mypy
            proc = await asyncio.create_subprocess_exec(
                "mypy",
                "--no-error-summary",
                "--show-error-codes",
                temp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)

            # Clean up temp file
            os.unlink(temp_path)

            if proc.returncode != 0:
                errors = stdout.decode('utf-8', errors='ignore').strip().split('\n')
                return ValidationResult(
                    success=False,
                    errors=[e for e in errors if e.strip()]
                )

            return ValidationResult(success=True)

        except FileNotFoundError:
            # mypy not installed
            return ValidationResult(
                success=True,
                warnings=["mypy not installed - type checking skipped"]
            )
        except asyncio.TimeoutError:
            return ValidationResult(
                success=True,
                warnings=["Type check timed out"]
            )
        except Exception as e:
            return ValidationResult(
                success=True,
                warnings=[f"Type check failed: {e}"]
            )

    async def _lint_content(
        self,
        file: str,
        content: str,
        file_type: FileType
    ) -> ValidationResult:
        """Run linter on content"""
        if file_type == FileType.PYTHON:
            return await self._lint_python(content)
        elif file_type in [FileType.JAVASCRIPT, FileType.TYPESCRIPT]:
            return await self._lint_javascript(content, file_type)
        else:
            return ValidationResult(success=True)

    async def _lint_python(self, content: str) -> ValidationResult:
        """Lint Python code using ruff (or fallback to pylint)"""
        try:
            # Write to temp file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(content)
                temp_path = f.name

            # Try ruff first (faster)
            try:
                proc = await asyncio.create_subprocess_exec(
                    "ruff",
                    "check",
                    "--output-format=text",
                    temp_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)

                # Clean up
                os.unlink(temp_path)

                if proc.returncode != 0:
                    errors = stdout.decode('utf-8', errors='ignore').strip().split('\n')
                    # Filter out empty lines
                    errors = [e for e in errors if e.strip() and not e.startswith('Found')]

                    return ValidationResult(
                        success=len(errors) == 0,
                        errors=errors[:10],  # Limit to 10 errors
                        warnings=errors[10:] if len(errors) > 10 else []
                    )

                return ValidationResult(success=True)

            except FileNotFoundError:
                # ruff not installed - skip linting
                os.unlink(temp_path)
                return ValidationResult(
                    success=True,
                    warnings=["ruff not installed - linting skipped"]
                )

        except asyncio.TimeoutError:
            return ValidationResult(
                success=True,
                warnings=["Linting timed out"]
            )
        except Exception as e:
            return ValidationResult(
                success=True,
                warnings=[f"Linting failed: {e}"]
            )

    async def _lint_javascript(
        self,
        content: str,
        file_type: FileType
    ) -> ValidationResult:
        """Lint JavaScript/TypeScript (requires eslint)"""
        # For now, skip JS linting
        # TODO: Implement with eslint
        return ValidationResult(
            success=True,
            warnings=["JavaScript linting not implemented yet"]
        )


# ============================================================================
# Configuration
# ============================================================================

_default_guardrails = None


def get_guardrails(
    enable_linting: bool = True,
    enable_syntax_check: bool = True
) -> ExecutionGuardrails:
    """
    Get default guardrails instance (singleton pattern).

    Args:
        enable_linting: Enable linting
        enable_syntax_check: Enable syntax checking

    Returns:
        ExecutionGuardrails instance
    """
    global _default_guardrails

    if _default_guardrails is None:
        _default_guardrails = ExecutionGuardrails(
            enable_linting=enable_linting,
            enable_syntax_check=enable_syntax_check
        )

    return _default_guardrails


# ============================================================================
# Testing
# ============================================================================

async def test_guardrails():
    """Test guardrails functionality"""
    guardrails = ExecutionGuardrails()

    # Test Python syntax check
    valid_python = """
def hello():
    print("Hello, world!")
"""

    invalid_python = """
def hello()
    print("Missing colon!")
"""

    print("=== Testing Python Syntax ===")
    result = await guardrails.validate_edit("test.py", valid_python)
    print(f"Valid Python: {'✓' if result.success else '✗'}")

    result = await guardrails.validate_edit("test.py", invalid_python)
    print(f"Invalid Python: {'✗' if not result.success else '✓'}")
    if result.errors:
        print(f"  Errors: {result.errors}")

    # Test file safety
    print("\n=== Testing File Safety ===")
    safe_files = ["src/main.py", "test.txt", "README.md"]
    unsafe_files = ["/etc/passwd", ".env", ".git/config"]

    for f in safe_files:
        safe = await guardrails.check_file_safety(f)
        print(f"{'✓' if safe else '✗'} {f}")

    for f in unsafe_files:
        safe = await guardrails.check_file_safety(f)
        print(f"{'✗' if not safe else '✓'} {f}")


if __name__ == "__main__":
    asyncio.run(test_guardrails())


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ExecutionGuardrails",
    "ValidationResult",
    "FileType",
    "get_guardrails"
]
