# src/agentic/core/constants.py

# File Operations Constants
FILE_READ_OPERATION = "read"

# Configuration Constants
USE_LITELLM_DEFAULT = False
LITELLM_PROVIDER_DEFAULT = "auto"
LITELLM_QUALITY_DEFAULT = "high"
ENABLE_PROMPT_CACHING_DEFAULT = True
ENABLE_STRUCTURED_OUTPUT_DEFAULT = True
ENABLE_EXTENDED_THINKING_DEFAULT = False
ENABLE_METRICS_DEFAULT = True
USE_ACI_DEFAULT = False
ALLOWLIST_MODE_DEFAULT = "strict"
SANDBOX_MODE_DEFAULT = "strict"
ENABLE_VALIDATION_DEFAULT = True
REQUIRE_TESTS_DEFAULT = True
AIDER_VENV_PATH_DEFAULT = ".venv/aider"
AIDER_BIN_DEFAULT = ""
AIDER_ENCODING_DEFAULT = "utf-8"
AIDER_CHAT_LANGUAGE_DEFAULT = "en"
USE_SPEC_FIRST_DEFAULT = False
REQUIRE_SPEC_DEFAULT = False
AUTO_GENERATE_SPEC_DEFAULT = True
VALIDATE_PLAN_DEFAULT = True
VALIDATE_IMPLEMENTATION_DEFAULT = True
MIN_PLAN_SCORE_DEFAULT = 0.7
MIN_IMPL_SCORE_DEFAULT = 0.7

# RAG Context Gating
RAG_RELEVANCE_THRESHOLD_DEFAULT = 0.4  # Minimum relevance score (1-distance), lower = stricter
RAG_MAX_RESULTS_DEFAULT = 5

RAG_WHITELIST_PATTERNS_DEFAULT = [
    "src/agentic/**/*.py",
    "scripts/**/*.py",
    "docs/**/*.md",
    "*.md"
]
RAG_BLACKLIST_PATTERNS_DEFAULT = [
    "legacy/**",
    ".venv/**",
    "node_modules/**",
    "__pycache__/**",
    "*.pyc",
    "workspaces/archive/**"
]
