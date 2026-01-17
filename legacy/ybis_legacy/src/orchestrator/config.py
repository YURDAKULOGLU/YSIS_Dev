"""
Orchestrator Config Module.
Centralizes all environment variables and constants for the factory.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
# Resolve robustly: If we are in src/orchestrator, parent.parent.parent is root.
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
CONSTITUTION_PATH = PROJECT_ROOT / "docs" / "governance" / "YBIS_CONSTITUTION.md"

# Flags
USE_CREWAI = os.getenv("YBIS_USE_CREWAI", "true").lower() == "true"
USE_POETIQ = os.getenv("YBIS_USE_POETIQ", "true").lower() == "true"
USE_OPENHANDS = os.getenv("YBIS_USE_OPENHANDS", "false").lower() == "true"
SANDBOX_MODE = os.getenv("YBIS_SANDBOX_MODE", "true").lower() == "true"

# Legacy Feature Flags (Restored)
USE_SPEC_FIRST = os.getenv("YBIS_USE_SPEC_FIRST", "true").lower() == "true"
REQUIRE_SPEC = os.getenv("YBIS_REQUIRE_SPEC", "false").lower() == "true"
AUTO_GENERATE_SPEC = os.getenv("YBIS_AUTO_GENERATE_SPEC", "true").lower() == "true"
USE_STORY_SHARDING = os.getenv("YBIS_USE_SHARDING", "true").lower() == "true"
USE_HEALTH_CHECK = os.getenv("YBIS_HEALTH_CHECK", "true").lower() == "true"
USE_REVIEW_GATE = os.getenv("YBIS_REVIEW_GATE", "true").lower() == "true"
EXECUTOR_MODE = os.getenv("YBIS_EXECUTOR_MODE", "aider").lower() # Options: aider, patch, openhands

# Thresholds
MAX_RETRIES = 3
MIN_TEST_COVERAGE = 0.7
MIN_PLAN_SCORE = 0.6
MIN_IMPL_SCORE = 0.7

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
