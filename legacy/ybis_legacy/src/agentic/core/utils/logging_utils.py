from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional


def _resolve_root() -> Path:
    env_root = os.getenv("YBIS_CODE_ROOT") or os.getenv("PROJECT_ROOT")
    root = Path(env_root) if env_root else Path(".")
    return root.resolve()


def get_log_path(component: str) -> Path:
    safe = component.replace(" ", "_").lower()
    return _resolve_root() / "Knowledge" / "Logs" / f"{safe}.log"


def log_event(
    message: str,
    component: str = "system",
    level: str = "info",
    log_path: Optional[Path] = None,
) -> None:
    level_map = {
        "info": "INFO",
        "warning": "WARN",
        "error": "ERROR",
        "success": "SUCCESS",
    }
    tag = level_map.get(level, "INFO")
    line = f"[{tag}] [{component}] {message}"
    print(line)

    logger = logging.getLogger(component)
    logger.propagate = False

    path = log_path or get_log_path(component)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except Exception:
        # Avoid breaking runtime if logging fails.
        pass
