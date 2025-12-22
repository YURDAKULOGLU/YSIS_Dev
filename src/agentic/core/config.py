import os
from pathlib import Path

# Detect PROJECT_ROOT dynamically
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Define constants for directories and paths
CONSTITUTION_PATH = PROJECT_ROOT / "docs" / "governance" / "00_GENESIS" / "YBIS_CONSTITUTION.md"
DATA_DIR = PROJECT_ROOT / "Knowledge" / "LocalDB"
TASKS_DB_PATH = DATA_DIR / "tasks.json"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

print(f"[Config] Detected PROJECT_ROOT: {PROJECT_ROOT}")
print(f"[Config] Defined CONSTITUTION_PATH: {CONSTITUTION_PATH}")
print(f"[Config] Defined TASKS_DB_PATH: {TASKS_DB_PATH}")
print(f"[Config] Defined CHROMA_DB_PATH: {CHROMA_DB_PATH}")
