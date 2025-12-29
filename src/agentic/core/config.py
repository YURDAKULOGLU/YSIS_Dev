import os
from pathlib import Path

# Detect PROJECT_ROOT dynamically
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Define constants for directories and paths
CONSTITUTION_PATH = PROJECT_ROOT / "docs" / "governance" / "00_GENESIS" / "YBIS_CONSTITUTION.md"
DATA_DIR = PROJECT_ROOT / "Knowledge" / "LocalDB"
TASKS_DB_PATH = DATA_DIR / "tasks.db"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

def get_secret(key: str, default: str = None) -> str:
    """Retrieve secret from environment variables."""
    return os.getenv(key, default)

print(f"[Config] Detected PROJECT_ROOT: {PROJECT_ROOT}")

# ============================================================================
# LiteLLM / Optimization Trinity Feature Flags
# ============================================================================

# Enable LiteLLM Universal Provider (default: false for safety)
USE_LITELLM = os.getenv("YBIS_USE_LITELLM", "false").lower() == "true"

# Provider selection (auto, claude, openai, gemini, deepseek, ollama)
LITELLM_PROVIDER = os.getenv("YBIS_LITELLM_PROVIDER", "auto")

# Quality level (high, medium, low) - affects model selection
LITELLM_QUALITY = os.getenv("YBIS_LITELLM_QUALITY", "high")

# Optimization Trinity Features
ENABLE_PROMPT_CACHING = os.getenv("YBIS_ENABLE_CACHING", "true").lower() == "true"
ENABLE_STRUCTURED_OUTPUT = os.getenv("YBIS_ENABLE_STRUCTURED", "true").lower() == "true"
ENABLE_EXTENDED_THINKING = os.getenv("YBIS_ENABLE_THINKING", "false").lower() == "true"

# Metrics and observability
ENABLE_METRICS = os.getenv("YBIS_ENABLE_METRICS", "true").lower() == "true"

# ============================================================================
# Agent-Computer Interface (ACI) Feature Flags
# ============================================================================

# Enable ACI constrained execution (default: false for safety)
USE_ACI = os.getenv("YBIS_USE_ACI", "false").lower() == "true"

# Allowlist mode (strict, permissive, off)
ALLOWLIST_MODE = os.getenv("YBIS_ALLOWLIST_MODE", "strict")

# Sandbox mode (strict, permissive, off)
SANDBOX_MODE = os.getenv("YBIS_SANDBOX_MODE", "strict")

# Enable validation/guardrails
ENABLE_VALIDATION = os.getenv("YBIS_ENABLE_VALIDATION", "true").lower() == "true"

# ============================================================================
# Spec-Driven Development (SDD) Feature Flags
# ============================================================================

# Enable Spec-First workflow (default: false for safety)
USE_SPEC_FIRST = os.getenv("YBIS_USE_SPEC_FIRST", "false").lower() == "true"

# Require SPEC.md before planning (default: false when feature enabled)
REQUIRE_SPEC = os.getenv("YBIS_REQUIRE_SPEC", "false").lower() == "true"

# Auto-generate SPEC.md if missing (default: true when feature enabled)
AUTO_GENERATE_SPEC = os.getenv("YBIS_AUTO_GENERATE_SPEC", "true").lower() == "true"

# Validate plan against spec (default: true when feature enabled)
VALIDATE_PLAN = os.getenv("YBIS_VALIDATE_PLAN", "true").lower() == "true"

# Validate implementation against spec (default: true when feature enabled)
VALIDATE_IMPLEMENTATION = os.getenv("YBIS_VALIDATE_IMPL", "true").lower() == "true"

# Minimum compliance scores (0.0-1.0)
MIN_PLAN_SCORE = float(os.getenv("YBIS_MIN_PLAN_SCORE", "0.7"))
MIN_IMPL_SCORE = float(os.getenv("YBIS_MIN_IMPL_SCORE", "0.7"))

print(f"[Config] Detected PROJECT_ROOT: {PROJECT_ROOT}")
print(f"[Config] Defined CONSTITUTION_PATH: {CONSTITUTION_PATH}")
print(f"[Config] Defined TASKS_DB_PATH: {TASKS_DB_PATH}")
print(f"[Config] Defined CHROMA_DB_PATH: {CHROMA_DB_PATH}")
print(f"[Config] USE_LITELLM: {USE_LITELLM}")
print(f"[Config] LITELLM_PROVIDER: {LITELLM_PROVIDER}")
print(f"[Config] LITELLM_QUALITY: {LITELLM_QUALITY}")
print(f"[Config] USE_ACI: {USE_ACI}")
print(f"[Config] ALLOWLIST_MODE: {ALLOWLIST_MODE}")
print(f"[Config] SANDBOX_MODE: {SANDBOX_MODE}")
print(f"[Config] USE_SPEC_FIRST: {USE_SPEC_FIRST}")
print(f"[Config] REQUIRE_SPEC: {REQUIRE_SPEC}")
print(f"[Config] AUTO_GENERATE_SPEC: {AUTO_GENERATE_SPEC}")
