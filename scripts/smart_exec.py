import sys
import subprocess
from pathlib import Path
from src.agentic.core.logger import log

def run_command(command: str):
    """
    Executes a shell command efficiently.
    - Success: Prints minimal summary (1 line).
    - Failure: Prints error details (Last 10 lines).
    - Logs: Saves EVERYTHING to system.log (Invisible to LLM context).
    """
    log.info(f"Executing: {command}")
    
    try:
        # Capture output, but don't print it yet
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        stdout_lines = []
        for line in process.stdout:
            stdout_lines.append(line)
            # Log to file in real-time (debug level), but NOT to console
            log.debug(f"[CMD] {line.strip()}")

        process.wait()
        
        if process.returncode == 0:
            log.success(f"Command completed successfully.")
        else:
            log.error(f"Command failed with exit code {process.returncode}")
            log.error("--- Error Preview ---")
            # Show last 10 lines to the agent
            for line in stdout_lines[-10:]:
                print(f"    {line.strip()}", file=sys.stderr)
            
    except Exception as e:
        log.critical(f"Execution infrastructure failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log.warning("Usage: python smart_exec.py <command>")
        sys.exit(1)
    
    cmd = " ".join(sys.argv[1:])
    run_command(cmd)