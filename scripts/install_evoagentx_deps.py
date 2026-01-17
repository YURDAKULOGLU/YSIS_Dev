#!/usr/bin/env python3
"""Install EvoAgentX dependencies."""

import subprocess
import sys

def install_deps():
    """Install EvoAgentX core dependencies."""
    deps = [
        "overdue",
        "sympy",
        "scipy>=1.9.0",
        "networkx>=3.3",
        "nltk>=3.9.1",
        "numpy>=1.26.4",
        "tenacity",
        "tree_sitter",
        "tree_sitter_python",
        "antlr4-python3-runtime==4.11",
    ]
    
    print("Installing EvoAgentX dependencies...")
    for dep in deps:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "--quiet"])
            print(f"[OK] {dep}")
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Failed to install {dep}: {e}")

if __name__ == "__main__":
    install_deps()

