import shutil
import subprocess
import sys
import time
import os
import urllib.request
from pathlib import Path

# ANSI Colors for "Emoji-style" output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log(msg, level="info"):
    if level == "info":
        print(f"{Colors.OKCYAN}[INFO]️  {msg}{Colors.ENDC}")
    elif level == "success":
        print(f"{Colors.OKGREEN}[OK] {msg}{Colors.ENDC}")
    elif level == "warning":
        print(f"{Colors.WARNING}[WARN]️  {msg}{Colors.ENDC}")
    elif level == "error":
        print(f"{Colors.FAIL}[FAIL] {msg}{Colors.ENDC}")
    elif level == "wait":
        print(f"{Colors.OKBLUE}⏳ {msg}{Colors.ENDC}")

def is_process_running(process_name):
    # Simple check using tasklist on Windows
    try:
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True).decode()
        return process_name in output
    except:
        return False

def check_ollama():
    log("Checking Ollama Status...", "wait")
    try:
        # Check if port 11434 is responding
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as response:
            if response.status == 200:
                log("Ollama is RUNNING and responding.", "success")
                return True
    except Exception:
        pass

    log("Ollama is NOT running.", "warning")

    # Try to start Ollama
    if shutil.which("ollama"):
        log("Attempting to start Ollama in background...", "wait")
        try:
            subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NEW_CONSOLE)

            # Wait for it to come up
            for _ in range(10):
                time.sleep(2)
                try:
                    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1):
                        log("Ollama started successfully!", "success")
                        return True
                except:
                    continue
        except Exception as e:
            log(f"Failed to auto-start Ollama: {e}", "error")
    else:
        log("Ollama executable not found in PATH.", "error")

    return False

def check_docker():
    log("Checking Docker Status...", "wait")
    try:
        subprocess.check_output("docker ps", shell=True, stderr=subprocess.STDOUT)
        log("Docker is RUNNING.", "success")
        return True
    except subprocess.CalledProcessError:
        log("Docker daemon is NOT running.", "warning")

        # Try to start Docker Desktop on Windows
        docker_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if os.path.exists(docker_path):
            log("Attempting to start Docker Desktop...", "wait")
            try:
                subprocess.Popen([docker_path])
                log("Docker Desktop launch signal sent. Waiting for daemon (this may take a minute)...", "wait")

                # Wait up to 60 seconds for Docker to be ready
                for i in range(12):
                    time.sleep(5)
                    try:
                        subprocess.check_output("docker ps", shell=True, stderr=subprocess.STDOUT)
                        log("Docker started successfully!", "success")
                        return True
                    except:
                        print(".", end="", flush=True)
                print()
            except Exception as e:
                log(f"Failed to launch Docker Desktop: {e}", "error")
        else:
            log(f"Docker Desktop not found at default location: {docker_path}", "warning")

    return False

def main():
    print(f"{Colors.HEADER}[TOOLS]️  YBIS DEPENDENCY AUTO-FIXER [TOOLS]️{Colors.ENDC}")
    print("---------------------------------------")

    ollama_ok = check_ollama()
    print("---------------------------------------")
    docker_ok = check_docker()
    print("---------------------------------------")

    if ollama_ok and docker_ok:
        log("ALL SYSTEMS GO! [LAUNCH]", "success")
        sys.exit(0)
    else:
        log("Some systems failed to start. Manual intervention required.", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
