"""
Open Interpreter Bridge
Enables secure code execution via Open Interpreter.
Designed to run commands inside a Docker sandbox.
"""

import os
import subprocess
from typing import Dict, Any, List

class InterpreterBridge:
    def __init__(self, sandbox_image: str = "ybis-interpreter-sandbox"):
        self.sandbox_image = sandbox_image

    def execute(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code using Open Interpreter logic (simulated via Docker for security)"""
        print(f"[INFO] Executing {language} code in sandbox...")

        try:
            # We wrap the code in a shell command for the docker container
            # This is a simplified version of what Open Interpreter does
            cmd = [
                "docker", "run", "--rm",
                self.sandbox_image,
                "python3", "-c", code
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "exit_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"success": False, "output": "", "error": "Execution timed out", "exit_code": -1}
        except Exception as e:
            return {"success": False, "output": "", "error": str(e), "exit_code": -1}

    def chat(self, message: str) -> str:
        """Pass message to Open Interpreter (if running in full mode)"""
        # Note: requires OPENAI_API_KEY or similar
        return "Chat mode not fully implemented. Use execute() for specific tasks."
