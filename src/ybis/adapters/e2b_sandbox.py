"""
E2B Sandbox Adapter - Isolated code execution using E2B.

Implements sandbox isolation following the Port Architecture:
- Core never imports E2B directly
- All E2B usage goes through this adapter
- Policy-controlled (can fallback to local execution)
"""

import os

from ..contracts import RunContext
from ..syscalls.journal import append_event


class E2BSandboxAdapter:
    """
    E2B Sandbox Adapter - Wraps E2B SDK for isolated execution.

    Follows Port Architecture: Core uses adapter, not E2B directly.
    """

    def __init__(self, ctx: RunContext | None = None):
        """
        Initialize E2B sandbox adapter.

        Args:
            ctx: Optional run context for journaling (can be None for testing)
        """
        self.ctx = ctx
        self.sandbox = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of E2B sandbox."""
        if self._initialized:
            return

        try:
            from e2b_code_interpreter import Sandbox

            # Check for API key
            e2b_api_key = os.getenv("E2B_API_KEY")
            if not e2b_api_key:
                raise ValueError(
                    "E2B_API_KEY environment variable required for E2B sandbox"
                )

            # Create sandbox
            self.sandbox = Sandbox.create()
            self._initialized = True

            # Journal event (if ctx provided)
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_CREATED",
                    {
                        "sandbox_type": "e2b",
                        "sandbox_id": getattr(self.sandbox, "sandbox_id", "unknown"),
                    },
                )

        except ImportError:
            raise ImportError(
                "E2B SDK not installed. Install with: pip install e2b e2b-code-interpreter"
            )
        except Exception as e:
            # Journal failure (if ctx provided)
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_CREATE_FAILED",
                    {
                        "sandbox_type": "e2b",
                        "error": str(e),
                    },
                )
            raise

    def execute_command(
        self, cmd: list[str], timeout: int | None = None, cwd: str | None = None
    ) -> dict:
        """
        Execute command in E2B sandbox.

        Args:
            cmd: Command as list of strings
            timeout: Timeout in seconds
            cwd: Working directory (inside sandbox)

        Returns:
            Dict with success, stdout, stderr, exit_code
        """
        self._ensure_initialized()

        # Convert command to string
        cmd_str = " ".join(cmd)

        try:
            # Execute in sandbox
            result = self.sandbox.commands.run(cmd_str, timeout=timeout or 30)

            # Extract output
            stdout = getattr(result, "stdout", "") or ""
            stderr = getattr(result, "stderr", "") or ""
            exit_code = getattr(result, "exit_code", 0)

            # Journal event (if ctx provided)
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_COMMAND_EXEC",
                    {
                        "command": cmd_str,
                        "exit_code": exit_code,
                        "stdout_length": len(stdout),
                        "stderr_length": len(stderr),
                    },
                )

            return {
                "success": exit_code == 0,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
            }

        except Exception as e:
            # Journal error (if ctx provided)
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_COMMAND_ERROR",
                    {
                        "command": cmd_str,
                        "error": str(e),
                    },
                )

            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
            }

    def write_file(self, path: str, content: str) -> None:
        """
        Write file in sandbox.

        Args:
            path: File path (inside sandbox)
            content: File content
        """
        self._ensure_initialized()

        try:
            # E2B uses files.write() or filesystem.write()
            filesystem = getattr(self.sandbox, "files", None) or getattr(
                self.sandbox, "filesystem", None
            )
            if filesystem:
                filesystem.write(path, content)

            # Journal event (if ctx provided)
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_FILE_WRITE",
                    {
                        "path": path,
                        "content_length": len(content),
                    },
                )

        except Exception as e:
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_FILE_WRITE_ERROR",
                    {
                        "path": path,
                        "error": str(e),
                    },
                )
            raise

    def read_file(self, path: str) -> str:
        """
        Read file from sandbox.

        Args:
            path: File path (inside sandbox)

        Returns:
            File content
        """
        self._ensure_initialized()

        try:
            filesystem = getattr(self.sandbox, "files", None) or getattr(
                self.sandbox, "filesystem", None
            )
            if filesystem:
                return filesystem.read(path)
            return ""

        except Exception as e:
            if self.ctx:
                append_event(
                    self.ctx.run_path,
                    "SANDBOX_FILE_READ_ERROR",
                    {
                        "path": path,
                        "error": str(e),
                    },
                )
            raise

    def close(self) -> None:
        """Close sandbox and cleanup."""
        if self.sandbox:
            try:
                self.sandbox.close()
                if self.ctx:
                    append_event(
                        self.ctx.run_path,
                        "SANDBOX_CLOSED",
                        {
                            "sandbox_type": "e2b",
                        },
                    )
            except Exception as e:
                if self.ctx:
                    append_event(
                        self.ctx.run_path,
                        "SANDBOX_CLOSE_ERROR",
                        {
                            "sandbox_type": "e2b",
                            "error": str(e),
                        },
                    )
            finally:
                self.sandbox = None
                self._initialized = False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def is_available(self) -> bool:
        """
        Check if E2B sandbox is available.
        
        Returns:
            True if E2B SDK is installed and API key is configured
        """
        try:
            import os

            from e2b_code_interpreter import Sandbox
            
            # Check for API key
            e2b_api_key = os.getenv("E2B_API_KEY")
            if not e2b_api_key:
                return False
            
            # Try to import (if import fails, not available)
            return True
        except ImportError:
            return False
        except Exception:
            return False

    def execute(self, cmd: list[str], timeout: int | None = None, cwd: str | None = None) -> dict:
        """
        Execute command in E2B sandbox (alias for execute_command).
        
        Args:
            cmd: Command as list of strings
            timeout: Timeout in seconds
            cwd: Working directory (inside sandbox)
            
        Returns:
            Dict with success, stdout, stderr, exit_code
        """
        return self.execute_command(cmd, timeout, cwd)

    def create(self) -> "E2BSandboxAdapter":
        """
        Create and initialize E2B sandbox (alias for _ensure_initialized).
        
        Returns:
            Self for method chaining
        """
        self._ensure_initialized()
        return self


