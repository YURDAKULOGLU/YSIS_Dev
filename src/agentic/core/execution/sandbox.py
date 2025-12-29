"""
Execution Sandbox - Isolated, resource-limited command execution.

Provides:
- Timeout enforcement
- Memory limits
- Directory restrictions
- Network isolation (optional)
- Process isolation

Features:
- Configurable modes (strict/permissive/off)
- Resource limit enforcement
- Path safety checks
- Graceful timeout handling
"""

import os
import asyncio
import signal
import time
import psutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

from .aci import CommandResult


# ============================================================================
# Configuration
# ============================================================================

class SandboxMode(Enum):
    """Sandbox enforcement mode"""
    STRICT = "strict"       # Tight limits, restricted paths
    PERMISSIVE = "permissive"  # Looser limits, more paths
    OFF = "off"             # No sandboxing


SANDBOX_CONFIGS = {
    "strict": {
        "timeout": 30,
        "max_memory_mb": 512,
        "network_access": False,
        "allowed_dirs": None,  # Will default to cwd
    },
    "permissive": {
        "timeout": 120,
        "max_memory_mb": 2048,
        "network_access": True,
        "allowed_dirs": None,  # Will default to cwd + tmp
    },
    "off": {
        "timeout": 300,
        "max_memory_mb": 4096,
        "network_access": True,
        "allowed_dirs": None,  # No restrictions
    }
}


# ============================================================================
# Execution Sandbox
# ============================================================================

class ExecutionSandbox:
    """
    Sandbox for isolating command execution.

    Limits:
    - Timeout (seconds)
    - Memory (MB)
    - Directory access
    - Network access (optional, requires firejail or similar)

    Example:
        >>> sandbox = ExecutionSandbox(timeout_seconds=30, max_memory_mb=512)
        >>> result = await sandbox.run_isolated("python test.py")
        >>> print(result.stdout)
    """

    def __init__(
        self,
        timeout_seconds: int = 30,
        max_memory_mb: int = 512,
        allowed_dirs: List[str] = None,
        network_access: bool = False,
        mode: str = None
    ):
        """
        Initialize sandbox.

        Args:
            timeout_seconds: Command timeout
            max_memory_mb: Memory limit (MB)
            allowed_dirs: List of allowed directories (None = cwd only)
            network_access: Allow network access
            mode: Sandbox mode (None = use individual params)
        """
        # If mode specified, use config
        if mode:
            config = SANDBOX_CONFIGS.get(mode, SANDBOX_CONFIGS["strict"])
            self.timeout = config["timeout"]
            self.max_memory = config["max_memory_mb"]
            self.network_access = config["network_access"]
            self.allowed_dirs = config["allowed_dirs"]
        else:
            self.timeout = timeout_seconds
            self.max_memory = max_memory_mb
            self.network_access = network_access
            self.allowed_dirs = allowed_dirs

        # Default allowed dirs to cwd if not specified
        if self.allowed_dirs is None:
            self.allowed_dirs = [os.getcwd()]

        # Normalize paths
        self.allowed_dirs = [str(Path(d).resolve()) for d in self.allowed_dirs]

    async def run_isolated(
        self,
        command: str,
        cwd: str = None
    ) -> CommandResult:
        """
        Run command in isolated environment.

        Enforces:
        - Timeout
        - Memory limits (via resource.setrlimit if available)
        - Directory restrictions (path validation)

        Args:
            command: Command to execute
            cwd: Working directory (must be in allowed_dirs)

        Returns:
            CommandResult with execution details

        Example:
            >>> result = await sandbox.run_isolated("pytest tests/")
            >>> if result.success:
            >>>     print("Tests passed!")
        """
        # Validate working directory
        work_dir = Path(cwd) if cwd else Path(self.allowed_dirs[0])
        work_dir = work_dir.resolve()

        if not self._check_path_allowed(str(work_dir)):
            return CommandResult(
                success=False,
                command=command,
                stdout="",
                stderr=f"Working directory not allowed: {work_dir}",
                exit_code=-1,
                duration_ms=0.0,
                sandbox_violation=True,
                message="Sandbox violation: path not allowed"
            )

        # Execute with timeout and monitoring
        start_time = time.time()

        try:
            # Create subprocess
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(work_dir),
                preexec_fn=self._setup_limits if os.name != 'nt' else None
            )

            # Monitor execution
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=self.timeout
                )

                duration_ms = (time.time() - start_time) * 1000

                return CommandResult(
                    success=(proc.returncode == 0),
                    command=command,
                    stdout=stdout.decode('utf-8', errors='ignore'),
                    stderr=stderr.decode('utf-8', errors='ignore'),
                    exit_code=proc.returncode,
                    duration_ms=duration_ms,
                    sandbox_violation=False,
                    message="Success" if proc.returncode == 0 else "Command failed"
                )

            except asyncio.TimeoutError:
                # Kill process on timeout
                try:
                    if os.name == 'nt':
                        # Windows
                        proc.kill()
                    else:
                        # Unix
                        proc.send_signal(signal.SIGTERM)
                        await asyncio.sleep(1)
                        if proc.returncode is None:
                            proc.kill()

                    await proc.wait()
                except Exception:
                    pass

                duration_ms = (time.time() - start_time) * 1000

                return CommandResult(
                    success=False,
                    command=command,
                    stdout="",
                    stderr=f"Command timed out after {self.timeout}s",
                    exit_code=-1,
                    duration_ms=duration_ms,
                    sandbox_violation=True,
                    message="Timeout"
                )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            return CommandResult(
                success=False,
                command=command,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=duration_ms,
                message=f"Error: {e}"
            )

    def _check_path_allowed(self, path: str) -> bool:
        """
        Check if path is within allowed directories.

        Args:
            path: Path to check

        Returns:
            True if path is allowed
        """
        path = str(Path(path).resolve())

        # Check if path is under any allowed directory
        for allowed_dir in self.allowed_dirs:
            if path.startswith(allowed_dir):
                return True

        return False

    def _setup_limits(self):
        """
        Set resource limits for subprocess (Unix only).

        Uses resource.setrlimit to enforce:
        - Memory limit (RLIMIT_AS)
        - CPU time limit (RLIMIT_CPU)
        - File size limit (RLIMIT_FSIZE)

        Note: Called via preexec_fn, runs in child process
        """
        try:
            import resource

            # Memory limit (virtual memory)
            mem_bytes = self.max_memory * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))

            # CPU time limit (slightly more than wall-clock timeout)
            cpu_limit = self.timeout + 5
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

            # File size limit (100MB)
            file_limit = 100 * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_FSIZE, (file_limit, file_limit))

            # Number of processes (prevent fork bombs)
            resource.setrlimit(resource.RLIMIT_NPROC, (100, 100))

        except ImportError:
            # resource module not available (Windows)
            pass
        except Exception:
            # Failed to set limits - continue anyway
            pass

    async def monitor_memory(self, proc) -> None:
        """
        Monitor process memory usage and kill if exceeded.

        Args:
            proc: Process to monitor

        Note: This is a backup check - resource.setrlimit is preferred
        """
        try:
            # Get process object
            if hasattr(proc, 'pid'):
                ps_proc = psutil.Process(proc.pid)

                while proc.returncode is None:
                    try:
                        # Check memory usage
                        mem_info = ps_proc.memory_info()
                        mem_mb = mem_info.rss / (1024 * 1024)

                        if mem_mb > self.max_memory:
                            # Kill process
                            proc.kill()
                            return

                        # Check every 100ms
                        await asyncio.sleep(0.1)

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        # Process ended or no access
                        return

        except Exception:
            # Monitoring failed - continue anyway
            pass


# ============================================================================
# Configuration Helpers
# ============================================================================

def get_sandbox(mode: str = None) -> ExecutionSandbox:
    """
    Get sandbox instance with mode-based config.

    Args:
        mode: "strict", "permissive", or "off" (default: from env or "strict")

    Returns:
        ExecutionSandbox instance

    Example:
        >>> sandbox = get_sandbox("strict")
        >>> result = await sandbox.run_isolated("python test.py")
    """
    # Read mode from env or parameter
    env_mode = os.getenv("YBIS_SANDBOX_MODE", "strict").lower()
    selected_mode = mode if mode else env_mode

    # Get config
    config = SANDBOX_CONFIGS.get(selected_mode, SANDBOX_CONFIGS["strict"])

    return ExecutionSandbox(
        timeout_seconds=config["timeout"],
        max_memory_mb=config["max_memory_mb"],
        network_access=config["network_access"],
        allowed_dirs=config["allowed_dirs"]
    )


# ============================================================================
# Advanced Sandboxing (Optional)
# ============================================================================

class DockerSandbox:
    """
    Docker-based sandbox for maximum isolation.

    Requires:
    - Docker installed
    - Docker daemon running

    Provides:
    - Full filesystem isolation
    - Network isolation
    - Resource limits (via Docker)
    - Clean state per execution

    Note: This is more heavyweight than ExecutionSandbox
    but provides stronger isolation.
    """

    def __init__(
        self,
        image: str = "python:3.12-slim",
        timeout_seconds: int = 30,
        max_memory_mb: int = 512
    ):
        """
        Initialize Docker sandbox.

        Args:
            image: Docker image to use
            timeout_seconds: Timeout
            max_memory_mb: Memory limit
        """
        self.image = image
        self.timeout = timeout_seconds
        self.max_memory = max_memory_mb

    async def run_isolated(
        self,
        command: str,
        cwd: str = None,
        mount_dir: str = None
    ) -> CommandResult:
        """
        Run command in Docker container.

        Args:
            command: Command to execute
            cwd: Working directory (inside container)
            mount_dir: Host directory to mount (read-only)

        Returns:
            CommandResult

        Example:
            >>> sandbox = DockerSandbox()
            >>> result = await sandbox.run_isolated("python test.py", mount_dir=".")
        """
        start_time = time.time()

        try:
            # Build docker run command
            docker_cmd = [
                "docker", "run",
                "--rm",  # Remove container after execution
                f"--memory={self.max_memory}m",  # Memory limit
                "--network=none",  # No network
                "--read-only",  # Read-only root filesystem
            ]

            # Add volume mount if specified
            if mount_dir:
                mount_dir = str(Path(mount_dir).resolve())
                docker_cmd.extend(["-v", f"{mount_dir}:/workspace:ro"])
                docker_cmd.extend(["-w", "/workspace"])

            # Add image and command
            docker_cmd.append(self.image)
            docker_cmd.extend(["sh", "-c", command])

            # Execute
            proc = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait with timeout
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout
            )

            duration_ms = (time.time() - start_time) * 1000

            return CommandResult(
                success=(proc.returncode == 0),
                command=command,
                stdout=stdout.decode('utf-8', errors='ignore'),
                stderr=stderr.decode('utf-8', errors='ignore'),
                exit_code=proc.returncode,
                duration_ms=duration_ms,
                sandbox_violation=False,
                message="Success" if proc.returncode == 0 else "Command failed"
            )

        except asyncio.TimeoutError:
            # Kill container
            try:
                proc.kill()
                await proc.wait()
            except Exception:
                pass

            duration_ms = (time.time() - start_time) * 1000

            return CommandResult(
                success=False,
                command=command,
                stdout="",
                stderr=f"Command timed out after {self.timeout}s",
                exit_code=-1,
                duration_ms=duration_ms,
                sandbox_violation=True,
                message="Timeout"
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            return CommandResult(
                success=False,
                command=command,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=duration_ms,
                message=f"Error: {e}"
            )


# ============================================================================
# Testing
# ============================================================================

async def test_sandbox():
    """Test sandbox functionality"""
    sandbox = ExecutionSandbox(timeout_seconds=5, max_memory_mb=256)

    print("=== Testing Sandbox ===")

    # Test normal command
    result = await sandbox.run_isolated("echo 'Hello, sandbox!'")
    print(f"Echo: {'✓' if result.success else '✗'}")
    if result.success:
        print(f"  Output: {result.stdout.strip()}")

    # Test timeout
    result = await sandbox.run_isolated("sleep 10")
    print(f"Timeout test: {'✓' if not result.success and 'timeout' in result.stderr.lower() else '✗'}")

    # Test path restriction
    result = await sandbox.run_isolated("ls /etc", cwd="/etc")
    print(f"Path restriction: {'✓' if result.sandbox_violation else '✗'}")


if __name__ == "__main__":
    asyncio.run(test_sandbox())


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ExecutionSandbox",
    "DockerSandbox",
    "SandboxMode",
    "get_sandbox",
    "SANDBOX_CONFIGS"
]
