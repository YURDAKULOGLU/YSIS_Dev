"""
Agent-Computer Interface (ACI) - Constrained interface for agent execution.

Inspired by SWE-agent's ACI pattern:
- Simple & clear actions (not complex commands)
- Compact & efficient operations
- Guardrails (validation before execution)
- Constrained command set
- Context management

References:
- https://arxiv.org/pdf/2405.15793
- https://swe-agent.com/background/aci/
"""

import os
import re
import asyncio
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class EditResult:
    """Result of a file edit operation"""
    success: bool
    file: str
    lines_changed: int
    validation_passed: bool
    validation_errors: List[str] = field(default_factory=list)
    diff: Optional[str] = None
    message: str = ""


@dataclass
class CommandResult:
    """Result of a command execution"""
    success: bool
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    sandbox_violation: bool = False
    message: str = ""


@dataclass
class SearchResult:
    """Result of a search operation"""
    file: str
    line_number: int
    line_content: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)


# ============================================================================
# Agent-Computer Interface
# ============================================================================

class AgentComputerInterface:
    """
    Constrained interface for agent-computer interactions.

    Provides safe, validated operations for:
    - File navigation (find, search)
    - File viewing (open, scroll)
    - Structured editing (with validation)
    - Command execution (if allowlisted)
    - Context tracking

    Features:
    - Constrained action set (no arbitrary shell access)
    - Pre-execution validation
    - Context awareness
    - Detailed error reporting
    """

    def __init__(
        self,
        base_dir: str = None,
        enable_validation: bool = True,
        enable_allowlist: bool = True,
        enable_sandbox: bool = True
    ):
        """
        Initialize ACI.

        Args:
            base_dir: Base directory for file operations (defaults to cwd)
            enable_validation: Enable pre-edit validation (guardrails)
            enable_allowlist: Enable command allowlist checking
            enable_sandbox: Enable execution sandboxing
        """
        self.base_dir = Path(base_dir) if base_dir else Path.getcwd()
        self.enable_validation = enable_validation
        self.enable_allowlist = enable_allowlist
        self.enable_sandbox = enable_sandbox

        # Context tracking
        self.opened_files: Dict[str, int] = {}  # file -> current_line
        self.edited_files: List[str] = []
        self.executed_commands: List[str] = []
        self.context_history: List[str] = []

        # Lazy-load dependencies
        self._allowlist = None
        self._guardrails = None
        self._sandbox = None

    # ========================================================================
    # File Navigation
    # ========================================================================

    async def find_file(self, name: str, dir: str = ".") -> List[str]:
        """
        Find files matching name pattern.

        Args:
            name: File name or pattern (supports wildcards)
            dir: Directory to search in (relative to base_dir)

        Returns:
            List of matching file paths

        Example:
            >>> files = await aci.find_file("*.py", "src")
            >>> # Returns: ['src/main.py', 'src/utils.py']
        """
        search_dir = self.base_dir / dir
        if not search_dir.exists():
            return []

        try:
            # Use glob for pattern matching
            pattern = name if "*" in name or "?" in name else f"**/*{name}*"
            matches = list(search_dir.glob(pattern))

            # Convert to relative paths
            results = [str(f.relative_to(self.base_dir)) for f in matches if f.is_file()]

            self.context_history.append(f"find_file({name}, {dir}) -> {len(results)} matches")
            return sorted(results)

        except Exception as e:
            self.context_history.append(f"find_file({name}, {dir}) -> ERROR: {e}")
            return []

    async def search_file(
        self,
        file: str,
        pattern: str,
        context_lines: int = 0
    ) -> List[SearchResult]:
        """
        Search within a file for pattern.

        Args:
            file: File path (relative to base_dir)
            pattern: Regex pattern to search for
            context_lines: Number of context lines before/after match

        Returns:
            List of SearchResult objects with matches

        Example:
            >>> results = await aci.search_file("main.py", "def.*test")
            >>> for r in results:
            >>>     print(f"{r.line_number}: {r.line_content}")
        """
        file_path = self.base_dir / file
        if not file_path.exists():
            return []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            results = []
            regex = re.compile(pattern)

            for i, line in enumerate(lines):
                if regex.search(line):
                    # Get context lines
                    start_ctx = max(0, i - context_lines)
                    end_ctx = min(len(lines), i + context_lines + 1)

                    results.append(SearchResult(
                        file=file,
                        line_number=i + 1,
                        line_content=line.rstrip(),
                        context_before=lines[start_ctx:i],
                        context_after=lines[i+1:end_ctx]
                    ))

            self.context_history.append(f"search_file({file}, {pattern}) -> {len(results)} matches")
            return results

        except Exception as e:
            self.context_history.append(f"search_file({file}, {pattern}) -> ERROR: {e}")
            return []

    async def search_dir(
        self,
        pattern: str,
        dir: str = ".",
        file_pattern: str = "*.py"
    ) -> Dict[str, List[int]]:
        """
        Search pattern in directory.

        Args:
            pattern: Regex pattern to search for
            dir: Directory to search in
            file_pattern: File pattern to match (e.g., "*.py")

        Returns:
            Dict mapping {file: [line_numbers]}

        Example:
            >>> matches = await aci.search_dir("TODO", "src", "*.py")
            >>> # Returns: {'src/main.py': [10, 45], 'src/utils.py': [23]}
        """
        search_dir = self.base_dir / dir
        if not search_dir.exists():
            return {}

        results = {}

        try:
            # Find all matching files
            files = search_dir.glob(f"**/{file_pattern}")

            for file_path in files:
                if file_path.is_file():
                    relative_path = str(file_path.relative_to(self.base_dir))
                    matches = await self.search_file(relative_path, pattern, context_lines=0)

                    if matches:
                        results[relative_path] = [m.line_number for m in matches]

            self.context_history.append(
                f"search_dir({pattern}, {dir}) -> {len(results)} files with matches"
            )
            return results

        except Exception as e:
            self.context_history.append(f"search_dir({pattern}, {dir}) -> ERROR: {e}")
            return {}

    # ========================================================================
    # File Viewing
    # ========================================================================

    async def open_file(
        self,
        file: str,
        start_line: int = 1,
        end_line: Optional[int] = None
    ) -> str:
        """
        Open file and return content (optionally with line range).

        Args:
            file: File path (relative to base_dir)
            start_line: Starting line number (1-indexed)
            end_line: Ending line number (None = end of file)

        Returns:
            File content with line numbers

        Example:
            >>> content = await aci.open_file("main.py", 1, 50)
            >>> print(content)
        """
        file_path = self.base_dir / file
        if not file_path.exists():
            return f"ERROR: File not found: {file}"

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Track opened file
            self.opened_files[file] = start_line

            # Apply line range
            start_idx = max(0, start_line - 1)
            end_idx = end_line if end_line else len(lines)
            selected_lines = lines[start_idx:end_idx]

            # Format with line numbers
            formatted = []
            for i, line in enumerate(selected_lines, start=start_line):
                formatted.append(f"{i:4d} | {line.rstrip()}")

            result = "\n".join(formatted)

            self.context_history.append(
                f"open_file({file}, {start_line}, {end_line}) -> {len(selected_lines)} lines"
            )

            return result

        except Exception as e:
            self.context_history.append(f"open_file({file}) -> ERROR: {e}")
            return f"ERROR: {e}"

    async def scroll_down(self, file: str, lines: int = 10) -> str:
        """
        Scroll down in open file.

        Args:
            file: File path
            lines: Number of lines to scroll

        Returns:
            File content after scrolling
        """
        if file not in self.opened_files:
            return f"ERROR: File not opened: {file}. Use open_file() first."

        current_line = self.opened_files[file]
        new_line = current_line + lines

        return await self.open_file(file, new_line, new_line + lines)

    async def scroll_up(self, file: str, lines: int = 10) -> str:
        """
        Scroll up in open file.

        Args:
            file: File path
            lines: Number of lines to scroll

        Returns:
            File content after scrolling
        """
        if file not in self.opened_files:
            return f"ERROR: File not opened: {file}. Use open_file() first."

        current_line = self.opened_files[file]
        new_line = max(1, current_line - lines)

        return await self.open_file(file, new_line, new_line + lines)

    # ========================================================================
    # Structured Editing
    # ========================================================================

    async def edit_file(
        self,
        file: str,
        start_line: int,
        end_line: int,
        replacement: str,
        validate: bool = True
    ) -> EditResult:
        """
        Edit file by replacing line range with new content.

        This is a STRUCTURED edit with validation:
        - Checks syntax (if validate=True)
        - Creates diff
        - Only applies if validation passes

        Args:
            file: File path
            start_line: Starting line to replace (1-indexed)
            end_line: Ending line to replace (inclusive)
            replacement: New content to insert
            validate: Run validation before applying (default: True)

        Returns:
            EditResult with success status and details

        Example:
            >>> result = await aci.edit_file(
            >>>     "main.py", 10, 15,
            >>>     "def new_function():\\n    pass"
            >>> )
            >>> if result.success:
            >>>     print("Edit successful!")
        """
        file_path = self.base_dir / file
        if not file_path.exists():
            return EditResult(
                success=False,
                file=file,
                lines_changed=0,
                validation_passed=False,
                message=f"File not found: {file}"
            )

        try:
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Validate line range
            if start_line < 1 or end_line > len(lines) or start_line > end_line:
                return EditResult(
                    success=False,
                    file=file,
                    lines_changed=0,
                    validation_passed=False,
                    message=f"Invalid line range: {start_line}-{end_line} (file has {len(lines)} lines)"
                )

            # Prepare new content
            replacement_lines = replacement.split('\n')
            if not replacement.endswith('\n'):
                replacement_lines = [l + '\n' for l in replacement_lines[:-1]] + [replacement_lines[-1]]
            else:
                replacement_lines = [l + '\n' for l in replacement_lines]

            new_lines = (
                lines[:start_line-1] +
                replacement_lines +
                lines[end_line:]
            )

            # Validation (if enabled)
            validation_passed = True
            validation_errors = []

            if validate and self.enable_validation:
                # Lazy-load guardrails
                if self._guardrails is None:
                    from src.agentic.core.execution.guardrails import ExecutionGuardrails
                    self._guardrails = ExecutionGuardrails()

                new_content = ''.join(new_lines)
                validation_result = await self._guardrails.validate_edit(file, new_content)

                validation_passed = validation_result.success
                validation_errors = validation_result.errors

                if not validation_passed:
                    return EditResult(
                        success=False,
                        file=file,
                        lines_changed=0,
                        validation_passed=False,
                        validation_errors=validation_errors,
                        message="Validation failed - edit not applied"
                    )

            # Apply edit
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            # Track edit
            if file not in self.edited_files:
                self.edited_files.append(file)

            lines_changed = abs(len(replacement_lines) - (end_line - start_line + 1))

            self.context_history.append(
                f"edit_file({file}, {start_line}-{end_line}) -> {lines_changed} lines changed"
            )

            return EditResult(
                success=True,
                file=file,
                lines_changed=lines_changed,
                validation_passed=validation_passed,
                validation_errors=[],
                message=f"Successfully edited {lines_changed} lines"
            )

        except Exception as e:
            self.context_history.append(f"edit_file({file}) -> ERROR: {e}")
            return EditResult(
                success=False,
                file=file,
                lines_changed=0,
                validation_passed=False,
                message=f"Error: {e}"
            )

    # ========================================================================
    # Command Execution
    # ========================================================================

    async def run_command(
        self,
        command: str,
        timeout: int = 30,
        cwd: str = None
    ) -> CommandResult:
        """
        Run command (if allowlisted and sandboxed).

        Security layers:
        1. Allowlist check (blocks dangerous commands)
        2. Sandbox execution (resource limits, path restrictions)

        Args:
            command: Command to execute
            timeout: Timeout in seconds
            cwd: Working directory (relative to base_dir)

        Returns:
            CommandResult with stdout, stderr, exit code

        Example:
            >>> result = await aci.run_command("pytest tests/")
            >>> if result.success:
            >>>     print(result.stdout)
        """
        import time

        # Allowlist check
        if self.enable_allowlist:
            if self._allowlist is None:
                from src.agentic.core.execution.command_allowlist import CommandAllowlist
                self._allowlist = CommandAllowlist()

            allowed, reason = self._allowlist.is_allowed(command)
            if not allowed:
                alternative = self._allowlist.suggest_alternative(command)
                msg = f"Command blocked: {reason}"
                if alternative:
                    msg += f" (Try: {alternative})"

                return CommandResult(
                    success=False,
                    command=command,
                    stdout="",
                    stderr=msg,
                    exit_code=-1,
                    duration_ms=0.0,
                    sandbox_violation=True,
                    message=msg
                )

        # Execute with sandbox (if enabled)
        start_time = time.time()

        try:
            if self.enable_sandbox:
                # Lazy-load sandbox
                if self._sandbox is None:
                    from src.agentic.core.execution.sandbox import ExecutionSandbox
                    self._sandbox = ExecutionSandbox(
                        timeout_seconds=timeout,
                        allowed_dirs=[str(self.base_dir)]
                    )

                result = await self._sandbox.run_isolated(
                    command,
                    cwd=str(self.base_dir / cwd) if cwd else str(self.base_dir)
                )

                duration_ms = (time.time() - start_time) * 1000

                self.executed_commands.append(command)
                self.context_history.append(f"run_command({command[:50]}...) -> exit={result.exit_code}")

                return result

            else:
                # Direct execution (no sandbox)
                work_dir = self.base_dir / cwd if cwd else self.base_dir

                proc = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(work_dir)
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        proc.communicate(),
                        timeout=timeout
                    )

                    duration_ms = (time.time() - start_time) * 1000

                    result = CommandResult(
                        success=(proc.returncode == 0),
                        command=command,
                        stdout=stdout.decode('utf-8', errors='ignore'),
                        stderr=stderr.decode('utf-8', errors='ignore'),
                        exit_code=proc.returncode,
                        duration_ms=duration_ms,
                        sandbox_violation=False,
                        message="Success" if proc.returncode == 0 else "Command failed"
                    )

                    self.executed_commands.append(command)
                    self.context_history.append(
                        f"run_command({command[:50]}...) -> exit={proc.returncode}"
                    )

                    return result

                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()

                    return CommandResult(
                        success=False,
                        command=command,
                        stdout="",
                        stderr=f"Command timed out after {timeout}s",
                        exit_code=-1,
                        duration_ms=(time.time() - start_time) * 1000,
                        message="Timeout"
                    )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            self.context_history.append(f"run_command({command[:50]}...) -> ERROR: {e}")

            return CommandResult(
                success=False,
                command=command,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=duration_ms,
                message=f"Error: {e}"
            )

    # ========================================================================
    # Context Management
    # ========================================================================

    async def get_context(self) -> Dict[str, Any]:
        """
        Get current context (files opened, edits made, commands run).

        Returns:
            Dict with context information

        Example:
            >>> ctx = await aci.get_context()
            >>> print(f"Opened: {ctx['opened_files']}")
            >>> print(f"Edited: {ctx['edited_files']}")
        """
        return {
            "base_dir": str(self.base_dir),
            "opened_files": list(self.opened_files.keys()),
            "edited_files": self.edited_files.copy(),
            "executed_commands": self.executed_commands.copy(),
            "total_actions": len(self.context_history),
            "history": self.context_history[-10:]  # Last 10 actions
        }

    async def summarize(self) -> str:
        """
        Summarize what's been done so far.

        Returns:
            Human-readable summary

        Example:
            >>> summary = await aci.summarize()
            >>> print(summary)
        """
        ctx = await self.get_context()

        summary_lines = [
            "=== ACI Session Summary ===",
            f"Base Directory: {ctx['base_dir']}",
            f"Total Actions: {ctx['total_actions']}",
            "",
            f"Files Opened: {len(ctx['opened_files'])}",
        ]

        if ctx['opened_files']:
            for f in ctx['opened_files'][:5]:
                summary_lines.append(f"  - {f}")
            if len(ctx['opened_files']) > 5:
                summary_lines.append(f"  ... and {len(ctx['opened_files']) - 5} more")

        summary_lines.append(f"\nFiles Edited: {len(ctx['edited_files'])}")
        if ctx['edited_files']:
            for f in ctx['edited_files'][:5]:
                summary_lines.append(f"  - {f}")
            if len(ctx['edited_files']) > 5:
                summary_lines.append(f"  ... and {len(ctx['edited_files']) - 5} more")

        summary_lines.append(f"\nCommands Executed: {len(ctx['executed_commands'])}")
        if ctx['executed_commands']:
            for cmd in ctx['executed_commands'][:5]:
                summary_lines.append(f"  - {cmd[:60]}...")
            if len(ctx['executed_commands']) > 5:
                summary_lines.append(f"  ... and {len(ctx['executed_commands']) - 5} more")

        summary_lines.append("\nRecent History:")
        for action in ctx['history']:
            summary_lines.append(f"  - {action}")

        return "\n".join(summary_lines)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "AgentComputerInterface",
    "EditResult",
    "CommandResult",
    "SearchResult"
]
