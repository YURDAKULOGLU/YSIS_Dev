#!/usr/bin/env python3
"""
Create a dedicated virtual environment for Aider.

Usage:
  python scripts/setup_aider_venv.py
  YBIS_AIDER_VENV=.venv/aider YBIS_AIDER_VERSION=0.86.1 python scripts/setup_aider_venv.py
"""
import os
import subprocess
import sys
from pathlib import Path
from venv import EnvBuilder


def resolve_venv_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    return Path(os.getenv("YBIS_AIDER_VENV", root / ".venv" / "aider"))


def resolve_python(venv_path: Path) -> Path:
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def main() -> int:
    venv_path = resolve_venv_path()
    version = os.getenv("YBIS_AIDER_VERSION", "0.86.1")

    print(f"[AiderVenv] Target: {venv_path}")
    venv_path.mkdir(parents=True, exist_ok=True)
    EnvBuilder(with_pip=True).create(venv_path)

    venv_python = resolve_python(venv_path)
    if not venv_python.exists():
        print("[AiderVenv] Python not found in venv")
        return 1

    subprocess.check_call([str(venv_python), "-m", "pip", "install", f"aider-chat=={version}"])
    subprocess.check_call([str(venv_python), "-m", "pip", "install", "tree-sitter-language-pack"])

    print("[AiderVenv] Done.")
    print(f"[AiderVenv] Set YBIS_AIDER_VENV={venv_path}")
    print("[AiderVenv] You can override binary with YBIS_AIDER_BIN if needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
