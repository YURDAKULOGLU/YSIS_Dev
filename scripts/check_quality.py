import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✅ {command.split()[0]} Passed")
    except subprocess.CalledProcessError:
        print(f"❌ {command.split()[0]} Failed")
        return False
    return True

def main():
    print("🛡️  Running Quality Gates...")
    
    # 1. Ruff (Linting)
    if not run_command("ruff check ."):
        sys.exit(1)
        
    # 2. MyPy (Type Checking)
    if not run_command("mypy src"):
        sys.exit(1)
        
    # 3. Pytest (Unit Tests)
    if not run_command("pytest"):
        sys.exit(1)

    print("🎉 All Quality Gates Passed!")

if __name__ == "__main__":
    main()
