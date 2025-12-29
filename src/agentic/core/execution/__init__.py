"""
Execution layer for YBIS agent system.

Provides constrained, secure execution through:
- Agent-Computer Interface (ACI)
- Command allowlist
- Execution guardrails
- Sandboxing
"""

from .aci import (
    AgentComputerInterface,
    EditResult,
    CommandResult,
    SearchResult
)

from .command_allowlist import (
    CommandAllowlist,
    AllowlistMode,
    get_allowlist
)

from .guardrails import (
    ExecutionGuardrails,
    ValidationResult,
    FileType,
    get_guardrails
)

from .sandbox import (
    ExecutionSandbox,
    DockerSandbox,
    SandboxMode,
    get_sandbox
)

__all__ = [
    "AgentComputerInterface",
    "EditResult",
    "CommandResult",
    "SearchResult",
    "CommandAllowlist",
    "AllowlistMode",
    "get_allowlist",
    "ExecutionGuardrails",
    "ValidationResult",
    "FileType",
    "get_guardrails",
    "ExecutionSandbox",
    "DockerSandbox",
    "SandboxMode",
    "get_sandbox"
]
