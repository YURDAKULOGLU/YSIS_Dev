import subprocess
import sys
import os
import argparse
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event

# Add project root
sys.path.insert(0, os.getcwd())
from src.agentic.core.config import PROJECT_ROOT
from src.agentic.core.plugins.builtin.open_swe import OpenSWE

def dispatch_task(script_name: str, args: list = None):
    """
    Launches a python script in a DETACHED process (new console window).
    This allows the main CLI (Gemini) to continue immediately without waiting.
    """
    if args is None:
        args = []

    script_path = PROJECT_ROOT / script_name

    if not script_path.exists():
        log_event(f"Script not found: {script_path}", component="auto_dispatcher", level="error")
        return

    # Command to run
    cmd = [sys.executable, str(script_path)] + args

    log_event(f"Dispatching background task: {script_name}", component="auto_dispatcher")
    log_event(f"Command: {' '.join(cmd)}", component="auto_dispatcher")

    try:
        if os.name == 'nt':
            # Windows specific: CREATE_NEW_CONSOLE (0x00000010)
            # This detaches the process from the current terminal
            process = subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                close_fds=True
            )
        else:
            # Linux/Mac: nohup equivalent
            process = subprocess.Popen(
                cmd,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        log_event(f"Task dispatched. PID: {process.pid}", component="auto_dispatcher", level="success")
        log_event("(You can verify status in the Dashboard or Log files)", component="auto_dispatcher")

    except Exception as e:
        log_event(f"Failed to dispatch: {e}", component="auto_dispatcher", level="error")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async Task Dispatcher")
    parser.add_argument("script", help="Python script to run in background")
    parser.add_argument("extra_args", nargs=argparse.REMAINDER, help="Arguments for the script")

    args = parser.parse_args()

    if args.script == "open_swe":
        from src.agentic.core.plugins.builtin.open_swe import OpenSWE
        open_swe_plugin = OpenSWE()
        operation = args.extra_args[0]
        extra_args = args.extra_args[1:]
        result = open_swe_plugin.execute(operation, *extra_args)
        log_event(str(result), component="auto_dispatcher")
    else:
        dispatch_task(args.script, args.extra_args)
