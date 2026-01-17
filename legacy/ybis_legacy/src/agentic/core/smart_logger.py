import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Config
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

class SmartLogger:
    """
    Token-Efficient Logger for AI Agents.
    - Console: Shows only INFO/ERROR (Low Token)
    - File: Shows DEBUG/TRACE (High Detail)
    """

    @staticmethod
    def get_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Clear existing handlers to prevent duplicate logs
        if logger.hasHandlers():
            logger.handlers.clear()

        # 1. File Handler (The Black Box - Full Detail)
        # Rotates every run or day
        timestamp = datetime.now().strftime("%Y%m%d")
        file_handler = logging.FileHandler(LOG_DIR / f"system_{timestamp}.log", encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # 2. Console Handler (The Agent View - Token Efficient)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        # Minimal format: just the message, maybe a tiny prefix
        console_formatter = logging.Formatter('> %(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

# Helper for scripts
def smart_log(msg: str, level="info"):
    l = SmartLogger.get_logger("YBIS_Core")
    if level == "info": l.info(msg)
    elif level == "error": l.error(msg)
    elif level == "debug": l.debug(msg)
