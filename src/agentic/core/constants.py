import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CONSTITUTION_PATH = PROJECT_ROOT / "docs" / "governance" / "00_GENESIS" / "YBIS_CONSTITUTION.md"
DATA_DIR = PROJECT_ROOT / "Knowledge" / "LocalDB"
TASKS_DB_PATH = DATA_DIR / "tasks.db"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

# LiteLLM / Optimization Trinity Feature Flags
USE_LITELLM = os.getenv("YBIS_USE_LITELLM", "false").lower() == "true"
LITELLM_PROVIDER = os.getenv("YBIS_LITELLM_PROVIDER", "auto")
LITELLM_QUALITY = os.getenv("YBIS_LITELLM_QUALITY", "high")

# Optimization Trinity Features
ENABLE_PROMPT_CACHING = os.getenv("YBIS_ENABLE_CACHING", "true").lower() == "true"
ENABLE_STRUCTURED_OUTPUT = os.getenv("YBIS_ENABLE_STRUCTURED", "true").lower() == "true"
ENABLE_EXTENDED_THINKING = os.getenv("YBIS_ENABLE_THINKING", "false").lower() == "true"

# Metrics and observability
ENABLE_METRICS = os.getenv("YBIS_ENABLE_METRICS", "true").lower() == "true"

# Agent-Computer Interface (ACI) Feature Flags
USE_ACI = os.getenv("YBIS_USE_ACI", "false").lower() == "true"
ALLOWLIST_MODE = os.getenv("YBIS_ALLOWLIST_MODE", "strict")
SANDBOX_MODE = os.getenv("YBIS_SANDBOX_MODE", "strict")

# Enable validation/guardrails
ENABLE_VALIDATION = os.getenv("YBIS_ENABLE_VALIDATION", "true").lower() == "true"

# Aider Isolation (Dedicated Virtual Environment)
AIDER_VENV_PATH = os.getenv(
    "YBIS_AIDER_VENV",
    str(PROJECT_ROOT / ".venv" / "aider")
)

# Optional explicit Aider binary override
AIDER_BIN = os.getenv("YBIS_AIDER_BIN", "")

# Force Aider encoding to prevent mojibake
AIDER_ENCODING = os.getenv("YBIS_AIDER_ENCODING", "utf-8")

# Force chat language for Aider output (default: en)
AIDER_CHAT_LANGUAGE = os.getenv("YBIS_AIDER_CHAT_LANGUAGE", "en")

# Spec-Driven Development (SDD) Feature Flags
USE_SPEC_FIRST = os.getenv("YBIS_USE_SPEC_FIRST", "false").lower() == "true"
REQUIRE_SPEC = os.getenv("YBIS_REQUIRE_SPEC", "false").lower() == "true"
AUTO_GENERATE_SPEC = os.getenv("YBIS_AUTO_GENERATE_SPEC", "true").lower() == "true"

# Validate plan against spec (default: true when feature enabled)
VALIDATE_PLAN = os.getenv("YBIS_VALIDATE_PLAN", "true").lower() == "true"

# Validate implementation against spec (default: true when feature enabled)
VALIDATE_IMPLEMENTATION = os.getenv("YBIS_VALIDATE_IMPL", "true").lower() == "true"

# Minimum compliance scores (0.0-1.0)
MIN_PLAN_SCORE = float(os.getenv("YBIS_MIN_PLAN_SCORE", "0.7"))
MIN_IMPL_SCORE = float(os.getenv("YBIS_MIN_IMPL_SCORE", "0.7"))

# Other constants can be added here
