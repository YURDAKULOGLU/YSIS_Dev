import subprocess
import os
import tempfile
import uuid

class CodeExecutionTool:
    def __init__(self, work_dir: str = "."):
        self.work_dir = os.path.abspath(work_dir)

    def run_python(self, code: str) -> str:
        """Executes Python code and returns output/error."""
        # Create temp file
        filename = f"temp_exec_{uuid.uuid4()}.py"
        filepath = os.path.join(self.work_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Execute with timeout
            result = subprocess.run(
                ["python", filename],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=10 # 10 seconds limit
            )
            
            output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            return output
            
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out (10s limit)."
        except Exception as e:
            return f"Error executing code: {e}"
        finally:
            # Cleanup
            if os.path.exists(filepath):
                os.remove(filepath)

    def run_shell(self, command: str) -> str:
        """Executes a shell command (Safe Mode)."""
        # Forbidden commands (Basic safety)
        forbidden = ["rm -rf", "format", "mkfs", ":(){ :|:& };:"]
        if any(f in command for f in forbidden):
            return "Error: Command blocked by safety policy."

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            return f"EXIT CODE: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        except Exception as e:
            return f"Error executing shell command: {e}"

code_exec = CodeExecutionTool()
