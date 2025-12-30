import sys
import threading
from pathlib import Path

from loguru import logger

# Config
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 1. Clear default handler (which is verbose)
logger.remove()

# 2. Console Sink (The "Token Saver")
# Only shows INFO and above.
# Format is clean, no timestamp clutter for the LLM context.
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>➤</green> <level>{message}</level>",
    colorize=True,
    backtrace=False,
    diagnose=False
)

# 3. File Sink (The "Black Box")
# Rotates every 10 MB, keeps logs for 1 week.
# Stores FULL detail including variable values (diagnose=True).
logger.add(
    LOG_DIR / "system.log",
    rotation="10 MB",
    retention="1 week",
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    backtrace=True,
    diagnose=True
)

# 4. JSON Sink (For Machine Analysis / RAG)
# Perfect for when agents need to "investigate" logs programmatically.
json_lock = threading.Lock()

def json_serializer(record):
    with json_lock:
        return {
            "time": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "level": record["level"].name,
            "task_id": record["extra"].get("task_id", ""),
            "message": record["message"]
        }

logger.add(
    LOG_DIR / "system.json.log",
    rotation="10 MB",
    serialize=json_serializer,
    level="DEBUG"
)

# Export usable logger
log = logger

def bind_context(task_id: str):
    """Create a context-aware logger for specific tasks."""
    return log.bind(task_id=task_id)
