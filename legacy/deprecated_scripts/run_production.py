"""Deprecated wrapper for the unified orchestrator entrypoint (loop mode)."""
import sys

from run_orchestrator import main


if __name__ == "__main__":
    sys.exit(main(["--loop"]))
