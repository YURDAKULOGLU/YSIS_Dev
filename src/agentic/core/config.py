import os
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event

# Detect PROJECT_ROOT dynamically
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Define constants for directories and paths
CONSTITUTION_PATH = PROJECT_ROOT / "docs" / "governance" / "00_GENESIS" / "YBIS_CONSTITUTION.md"
DATA_DIR = PROJECT_ROOT / "Knowledge" / "LocalDB"
TASKS_DB_PATH = DATA_DIR / "tasks.db"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

from src.agentic.core.constants import (
    USE_LITELLM_DEFAULT,
    LITELLM_PROVIDER_DEFAULT,
    LITELLM_QUALITY_DEFAULT,
    ENABLE_PROMPT_CACHING_DEFAULT,
    ENABLE_STRUCTURED_OUTPUT_DEFAULT,
    ENABLE_EXTENDED_THINKING_DEFAULT,
    ENABLE_METRICS_DEFAULT,
    USE_ACI_DEFAULT,
    ALLOWLIST_MODE_DEFAULT,
    SANDBOX_MODE_DEFAULT,
    ENABLE_VALIDATION_DEFAULT,
    REQUIRE_TESTS_DEFAULT,
    AIDER_VENV_PATH_DEFAULT,
    AIDER_BIN_DEFAULT,
    AIDER_ENCODING_DEFAULT,
    AIDER_CHAT_LANGUAGE_DEFAULT,
    USE_SPEC_FIRST_DEFAULT,
    REQUIRE_SPEC_DEFAULT,
    AUTO_GENERATE_SPEC_DEFAULT,
    VALIDATE_PLAN_DEFAULT,
    VALIDATE_IMPLEMENTATION_DEFAULT,
    MIN_PLAN_SCORE_DEFAULT,
    MIN_IMPL_SCORE_DEFAULT,
    RAG_RELEVANCE_THRESHOLD_DEFAULT,
    RAG_MAX_RESULTS_DEFAULT,
    RAG_WHITELIST_PATTERNS_DEFAULT,
    RAG_BLACKLIST_PATTERNS_DEFAULT
)

# NOTE: constants.py holds defaults only. config.py is the single source of truth
# for runtime configuration and environment overrides.

def _env_bool(key: str, default: bool) -> bool:
    return os.getenv(key, str(default)).lower() == "true"

def _env_int(key: str, default: int) -> int:
    return int(os.getenv(key, str(default)))

def _env_float(key: str, default: float) -> float:
    return float(os.getenv(key, str(default)))

def _env_list(key: str, default: list[str]) -> list[str]:
    raw = os.getenv(key)
    if not raw:
        return list(default)
    return [item.strip() for item in raw.split(",") if item.strip()]

def get_secret(key: str, default: str = None) -> str:
    """Retrieve secret from environment variables."""
    return os.getenv(key, default)

# ============================================================================
# LiteLLM / Optimization Trinity Feature Flags
# ============================================================================

# Enable LiteLLM Universal Provider (default: false for safety)
USE_LITELLM = _env_bool("YBIS_USE_LITELLM", USE_LITELLM_DEFAULT)

# Provider selection (auto, claude, openai, gemini, deepseek, ollama)
LITELLM_PROVIDER = os.getenv("YBIS_LITELLM_PROVIDER", LITELLM_PROVIDER_DEFAULT)

# Quality level (high, medium, low) - affects model selection
LITELLM_QUALITY = os.getenv("YBIS_LITELLM_QUALITY", LITELLM_QUALITY_DEFAULT)

# Optimization Trinity Features
ENABLE_PROMPT_CACHING = _env_bool("YBIS_ENABLE_CACHING", ENABLE_PROMPT_CACHING_DEFAULT)
ENABLE_STRUCTURED_OUTPUT = _env_bool("YBIS_ENABLE_STRUCTURED", ENABLE_STRUCTURED_OUTPUT_DEFAULT)
ENABLE_EXTENDED_THINKING = _env_bool("YBIS_ENABLE_THINKING", ENABLE_EXTENDED_THINKING_DEFAULT)

# Metrics and observability
ENABLE_METRICS = _env_bool("YBIS_ENABLE_METRICS", ENABLE_METRICS_DEFAULT)

# ============================================================================
# Agent-Computer Interface (ACI) Feature Flags
# ============================================================================

# Enable ACI constrained execution (default: false for safety)
USE_ACI = _env_bool("YBIS_USE_ACI", USE_ACI_DEFAULT)

# Allowlist mode (strict, permissive, off)
ALLOWLIST_MODE = os.getenv("YBIS_ALLOWLIST_MODE", ALLOWLIST_MODE_DEFAULT)

# Sandbox mode (strict, permissive, off)
SANDBOX_MODE = os.getenv("YBIS_SANDBOX_MODE", SANDBOX_MODE_DEFAULT)

# Enable validation/guardrails
ENABLE_VALIDATION = _env_bool("YBIS_ENABLE_VALIDATION", ENABLE_VALIDATION_DEFAULT)

# Require at least one test update for code changes
REQUIRE_TESTS = _env_bool("YBIS_REQUIRE_TESTS", REQUIRE_TESTS_DEFAULT)

# ============================================================================
# Aider Isolation (Dedicated Virtual Environment)
# ============================================================================

# Path to the dedicated Aider venv (default: .venv/aider)
AIDER_VENV_PATH = os.getenv(
    "YBIS_AIDER_VENV",
    str(PROJECT_ROOT / AIDER_VENV_PATH_DEFAULT)
)

# Optional explicit Aider binary override
AIDER_BIN = os.getenv("YBIS_AIDER_BIN", AIDER_BIN_DEFAULT)

# Force Aider encoding to prevent mojibake
AIDER_ENCODING = os.getenv("YBIS_AIDER_ENCODING", AIDER_ENCODING_DEFAULT)

# Force chat language for Aider output (default: en)
AIDER_CHAT_LANGUAGE = os.getenv("YBIS_AIDER_CHAT_LANGUAGE", AIDER_CHAT_LANGUAGE_DEFAULT)

# ============================================================================
# Spec-Driven Development (SDD) Feature Flags
# ============================================================================

# Enable Spec-First workflow (default: false for safety)
USE_SPEC_FIRST = _env_bool("YBIS_USE_SPEC_FIRST", USE_SPEC_FIRST_DEFAULT)

# Require SPEC.md before planning (default: false when feature enabled)
REQUIRE_SPEC = _env_bool("YBIS_REQUIRE_SPEC", REQUIRE_SPEC_DEFAULT)

# Auto-generate SPEC.md if missing (default: true when feature enabled)
AUTO_GENERATE_SPEC = _env_bool("YBIS_AUTO_GENERATE_SPEC", AUTO_GENERATE_SPEC_DEFAULT)

# Validate plan against spec (default: true when feature enabled)
VALIDATE_PLAN = _env_bool("YBIS_VALIDATE_PLAN", VALIDATE_PLAN_DEFAULT)

# Validate implementation against spec (default: true when feature enabled)
VALIDATE_IMPLEMENTATION = _env_bool("YBIS_VALIDATE_IMPL", VALIDATE_IMPLEMENTATION_DEFAULT)

# Minimum compliance scores (0.0-1.0)
MIN_PLAN_SCORE = _env_float("YBIS_MIN_PLAN_SCORE", MIN_PLAN_SCORE_DEFAULT)
MIN_IMPL_SCORE = _env_float("YBIS_MIN_IMPL_SCORE", MIN_IMPL_SCORE_DEFAULT)

# ============================================================================
# RAG Context Gating Feature Flags
# ============================================================================

# Minimum relevance threshold (0.0-1.0). Documents below this are filtered out.
RAG_RELEVANCE_THRESHOLD = _env_float("YBIS_RAG_THRESHOLD", RAG_RELEVANCE_THRESHOLD_DEFAULT)

# Maximum RAG results to inject into context
RAG_MAX_RESULTS = _env_int("YBIS_RAG_MAX_RESULTS", RAG_MAX_RESULTS_DEFAULT)

# Whitelist patterns (glob) - only these files are included in RAG results
RAG_WHITELIST_PATTERNS = _env_list("YBIS_RAG_WHITELIST", RAG_WHITELIST_PATTERNS_DEFAULT)

# Blacklist patterns (glob) - these files are always excluded
RAG_BLACKLIST_PATTERNS = _env_list("YBIS_RAG_BLACKLIST", RAG_BLACKLIST_PATTERNS_DEFAULT)

log_event(f"Detected PROJECT_ROOT: {PROJECT_ROOT}", component="config")
log_event(f"Defined CONSTITUTION_PATH: {CONSTITUTION_PATH}", component="config")
log_event(f"Defined TASKS_DB_PATH: {TASKS_DB_PATH}", component="config")
log_event(f"Defined CHROMA_DB_PATH: {CHROMA_DB_PATH}", component="config")
log_event(f"USE_LITELLM: {USE_LITELLM}", component="config")
log_event(f"LITELLM_PROVIDER: {LITELLM_PROVIDER}", component="config")
log_event(f"LITELLM_QUALITY: {LITELLM_QUALITY}", component="config")
log_event(f"USE_ACI: {USE_ACI}", component="config")
log_event(f"ALLOWLIST_MODE: {ALLOWLIST_MODE}", component="config")
log_event(f"SANDBOX_MODE: {SANDBOX_MODE}", component="config")
log_event(f"AIDER_VENV_PATH: {AIDER_VENV_PATH}", component="config")
log_event(f"AIDER_BIN: {AIDER_BIN}", component="config")
log_event(f"AIDER_ENCODING: {AIDER_ENCODING}", component="config")
log_event(f"AIDER_CHAT_LANGUAGE: {AIDER_CHAT_LANGUAGE}", component="config")
log_event(f"USE_SPEC_FIRST: {USE_SPEC_FIRST}", component="config")
log_event(f"REQUIRE_SPEC: {REQUIRE_SPEC}", component="config")
log_event(f"AUTO_GENERATE_SPEC: {AUTO_GENERATE_SPEC}", component="config")
log_event(f"RAG_RELEVANCE_THRESHOLD: {RAG_RELEVANCE_THRESHOLD}", component="config")
log_event(f"RAG_MAX_RESULTS: {RAG_MAX_RESULTS}", component="config")
