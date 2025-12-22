from src.agentic.core.plugin_system.protocol import ToolProtocol
import subprocess

class GitOps(ToolProtocol):
    def execute(self, operation, *args):
        if operation == "status":
            result = subprocess.run(["git", "status"], capture_output=True, text=True)
            return result.stdout
        else:
            raise ValueError(f"Unsupported operation: {operation}")
