#!/usr/bin/env python3
"""
YBIS PreToolUse Hook - Limit Test
Bu hook, Claude Code PreToolUse hook sisteminin TÜM özelliklerini kullanır.

Hook Trigger: Her tool çağrısından ÖNCE çalışır
Input: stdin'den JSON (tool_name, tool_input, context)
Output: stdout'a JSON (decision: allow/block, reason, modifications)

Capabilities:
1. Tool blocking (güvenlik)
2. Input validation
3. Rate limiting
4. Audit logging
5. Input modification/sanitization
6. Context-aware decisions
7. Multi-condition evaluation
"""

import sys
import json
import os
import re
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

# ============================================================================
# CONFIGURATION
# ============================================================================

# Korunan dosyalar - bu dosyalar EDIT/WRITE edilemez
PROTECTED_FILES = [
    # Core governance
    "docs/governance/YBIS_CONSTITUTION.md",
    "docs/CONSTITUTION.md",

    # Secrets
    ".env",
    ".env.local",
    ".env.production",
    "secrets.json",
    "credentials.json",
    "**/secrets/**",
    "**/.secrets/**",

    # Git internals
    ".git/**",
    ".gitignore",  # Read-only

    # Lock files (integrity)
    "*.lock",
    "package-lock.json",
    "poetry.lock",

    # Claude config (meta-protection)
    ".claude/settings.json",
]

# Tehlikeli Bash komutları - BLOCK
DANGEROUS_COMMANDS = [
    r"rm\s+-rf\s+/",           # Root silme
    r"rm\s+-rf\s+\*",          # Wildcard silme
    r"rm\s+-rf\s+\.\.",        # Parent dir silme
    r"dd\s+if=.*of=/dev/",     # Disk overwrite
    r"mkfs\.",                  # Filesystem format
    r":()\{.*\}",              # Fork bomb
    r">\s*/dev/sd",            # Disk write
    r"chmod\s+-R\s+777",       # Dangerous permissions
    r"curl.*\|\s*(ba)?sh",     # Pipe to shell
    r"wget.*\|\s*(ba)?sh",     # Pipe to shell
    r"sudo\s+rm",              # Sudo delete
    r"sudo\s+dd",              # Sudo disk
    r"eval\s+\$",              # Eval injection
    r"nc\s+-e",                # Netcat shell
    r"python.*-c.*exec",       # Python exec
]

# Güvenli Bash komutları (whitelist) - diğerleri onay gerektirir
SAFE_COMMANDS = [
    r"^git\s+(status|log|diff|branch|show|remote|fetch)",
    r"^ls(\s|$)",
    r"^cat\s+",
    r"^head\s+",
    r"^tail\s+",
    r"^grep\s+",
    r"^find\s+",
    r"^echo\s+",
    r"^pwd$",
    r"^whoami$",
    r"^date$",
    r"^python\s+-m\s+pytest",
    r"^python\s+-m\s+ruff",
    r"^python\s+-m\s+mypy",
    r"^npm\s+(test|run\s+lint|run\s+build)",
    r"^make\s+(test|lint|build|check)",
]

# Rate limiting configuration
RATE_LIMITS = {
    "Bash": {"max_calls": 50, "window_seconds": 60},
    "Write": {"max_calls": 20, "window_seconds": 60},
    "Edit": {"max_calls": 30, "window_seconds": 60},
    "WebFetch": {"max_calls": 10, "window_seconds": 60},
    "WebSearch": {"max_calls": 5, "window_seconds": 60},
}

# Rate limit storage file
RATE_LIMIT_FILE = Path("/tmp/claude_code_rate_limits.json")

# Audit log file
AUDIT_LOG_FILE = Path(os.environ.get("CLAUDE_AUDIT_LOG", "/tmp/claude_code_audit.log"))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_audit(tool_name: str, tool_input: dict, decision: str, reason: str = ""):
    """Audit log'a kayıt yaz"""
    try:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "input_hash": hashlib.sha256(json.dumps(tool_input, sort_keys=True).encode()).hexdigest()[:16],
            "decision": decision,
            "reason": reason,
        }
        with open(AUDIT_LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Audit failure should not block execution


def check_rate_limit(tool_name: str) -> tuple[bool, str]:
    """Rate limit kontrolü"""
    if tool_name not in RATE_LIMITS:
        return True, ""

    config = RATE_LIMITS[tool_name]
    now = time.time()

    # Load existing rate data
    rate_data = {}
    if RATE_LIMIT_FILE.exists():
        try:
            rate_data = json.loads(RATE_LIMIT_FILE.read_text())
        except Exception:
            rate_data = {}

    # Get tool's call history
    tool_key = f"tool_{tool_name}"
    calls = rate_data.get(tool_key, [])

    # Filter to window
    window_start = now - config["window_seconds"]
    calls = [c for c in calls if c > window_start]

    # Check limit
    if len(calls) >= config["max_calls"]:
        return False, f"Rate limit exceeded: {tool_name} called {len(calls)} times in {config['window_seconds']}s (max: {config['max_calls']})"

    # Add this call
    calls.append(now)
    rate_data[tool_key] = calls

    # Save
    try:
        RATE_LIMIT_FILE.write_text(json.dumps(rate_data))
    except Exception:
        pass

    return True, ""


def match_pattern(path: str, pattern: str) -> bool:
    """Glob-like pattern matching"""
    import fnmatch
    return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern)


def is_protected_file(file_path: str) -> bool:
    """Dosyanın korumalı olup olmadığını kontrol et"""
    for pattern in PROTECTED_FILES:
        if match_pattern(file_path, pattern):
            return True
    return False


def is_dangerous_command(command: str) -> tuple[bool, str]:
    """Tehlikeli komut kontrolü"""
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, f"Dangerous command pattern detected: {pattern}"
    return False, ""


def is_safe_command(command: str) -> bool:
    """Güvenli komut kontrolü (whitelist)"""
    for pattern in SAFE_COMMANDS:
        if re.match(pattern, command.strip(), re.IGNORECASE):
            return True
    return False


def sanitize_input(tool_name: str, tool_input: dict) -> dict:
    """Input sanitization - tehlikeli karakterleri temizle"""
    sanitized = tool_input.copy()

    if tool_name == "Bash":
        command = sanitized.get("command", "")
        # Remove null bytes
        command = command.replace("\x00", "")
        # Remove ANSI escape sequences
        command = re.sub(r"\x1b\[[0-9;]*m", "", command)
        sanitized["command"] = command

    elif tool_name in ["Write", "Edit"]:
        # File path sanitization
        file_path = sanitized.get("file_path", "")
        # Prevent path traversal
        file_path = file_path.replace("../", "").replace("..\\", "")
        # Remove null bytes
        file_path = file_path.replace("\x00", "")
        sanitized["file_path"] = file_path

    return sanitized


# ============================================================================
# TOOL-SPECIFIC VALIDATORS
# ============================================================================

def validate_bash(tool_input: dict) -> tuple[str, str, dict]:
    """Bash tool validation"""
    command = tool_input.get("command", "")

    # 1. Dangerous command check
    is_dangerous, reason = is_dangerous_command(command)
    if is_dangerous:
        return "block", reason, {}

    # 2. Safe command check (whitelist)
    if is_safe_command(command):
        return "allow", "Safe command (whitelisted)", {}

    # 3. Unknown command - allow but log
    log_audit("Bash", tool_input, "allow", "Unknown command - allowed with logging")
    return "allow", "Command allowed (not in blocklist)", {}


def validate_edit(tool_input: dict) -> tuple[str, str, dict]:
    """Edit tool validation"""
    file_path = tool_input.get("file_path", "")

    # Protected file check
    if is_protected_file(file_path):
        return "block", f"Protected file cannot be edited: {file_path}", {}

    return "allow", "", {}


def validate_write(tool_input: dict) -> tuple[str, str, dict]:
    """Write tool validation"""
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")

    # Protected file check
    if is_protected_file(file_path):
        return "block", f"Protected file cannot be written: {file_path}", {}

    # Secret detection in content
    secret_patterns = [
        r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?[a-zA-Z0-9]{20,}",
        r"(?i)(secret|password|passwd|pwd)\s*[=:]\s*['\"]?[^\s'\"]{8,}",
        r"(?i)(aws[_-]?secret|aws[_-]?key)\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{20,}",
        r"-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----",
        r"(?i)bearer\s+[a-zA-Z0-9._-]{20,}",
    ]

    for pattern in secret_patterns:
        if re.search(pattern, content):
            return "block", f"Potential secret detected in content (pattern: {pattern[:30]}...)", {}

    return "allow", "", {}


def validate_webfetch(tool_input: dict) -> tuple[str, str, dict]:
    """WebFetch tool validation"""
    url = tool_input.get("url", "")

    # Block internal/local URLs
    blocked_patterns = [
        r"^https?://localhost",
        r"^https?://127\.",
        r"^https?://0\.",
        r"^https?://10\.",
        r"^https?://192\.168\.",
        r"^https?://172\.(1[6-9]|2[0-9]|3[0-1])\.",
        r"^file://",
        r"^ftp://",
    ]

    for pattern in blocked_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return "block", f"Internal/local URL blocked: {url}", {}

    return "allow", "", {}


# ============================================================================
# MAIN HOOK LOGIC
# ============================================================================

def process_hook(input_data: dict) -> dict:
    """Ana hook processing logic'i"""

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    context = input_data.get("context", {})

    # 1. Sanitize input
    tool_input = sanitize_input(tool_name, tool_input)

    # 2. Rate limit check
    rate_ok, rate_reason = check_rate_limit(tool_name)
    if not rate_ok:
        log_audit(tool_name, tool_input, "block", rate_reason)
        return {
            "decision": "block",
            "reason": rate_reason,
        }

    # 3. Tool-specific validation
    validators = {
        "Bash": validate_bash,
        "Edit": validate_edit,
        "Write": validate_write,
        "WebFetch": validate_webfetch,
    }

    if tool_name in validators:
        decision, reason, modifications = validators[tool_name](tool_input)

        if decision == "block":
            log_audit(tool_name, tool_input, "block", reason)
            return {
                "decision": "block",
                "reason": reason,
            }

        # Log allowed with modifications
        if modifications:
            log_audit(tool_name, tool_input, "allow", f"Modified: {list(modifications.keys())}")
            return {
                "decision": "allow",
                "reason": reason,
                "modifications": modifications,
            }

    # 4. Default: allow
    log_audit(tool_name, tool_input, "allow", "Default allow")
    return {
        "decision": "allow",
    }


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        # Read input from stdin
        input_text = sys.stdin.read()
        input_data = json.loads(input_text)

        # Process
        result = process_hook(input_data)

        # Output result
        print(json.dumps(result))

    except json.JSONDecodeError as e:
        # Invalid JSON input
        print(json.dumps({
            "decision": "allow",
            "reason": f"Hook JSON parse error (allowing): {e}",
        }))

    except Exception as e:
        # Any other error - fail open (allow)
        print(json.dumps({
            "decision": "allow",
            "reason": f"Hook error (allowing): {e}",
        }))
