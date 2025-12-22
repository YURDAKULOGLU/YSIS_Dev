import shutil
import os
import glob

class SandboxManager:
    def __init__(self, sandbox_root=".YBIS_Dev/.sandbox"):
        # Ensure path is relative to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        self.sandbox_path = os.path.join(project_root, sandbox_root)
        self.project_root = project_root

    def setup(self):
        """Creates a clean sandbox environment mirroring essential project files."""
        if os.path.exists(self.sandbox_path):
            try:
                shutil.rmtree(self.sandbox_path)
            except Exception as e:
                return f"Error cleaning sandbox: {e}"
        
        os.makedirs(self.sandbox_path)
        
        # Copy config files
        configs = ["package.json", "tsconfig.json", ".eslintrc.js"]
        for cfg in configs:
            src = os.path.join(self.project_root, cfg)
            if os.path.exists(src):
                shutil.copy(src, self.sandbox_path)
                
        # We don't copy the whole src to avoid slowness, 
        # agents will write specific files they need or we mock dependencies.
        return f"Sandbox initialized at {self.sandbox_path}"

    def get_path(self, relative_path: str) -> str:
        """Returns absolute path inside sandbox."""
        return os.path.join(self.sandbox_path, relative_path)

    def cleanup(self):
        """Removes the sandbox."""
        if os.path.exists(self.sandbox_path):
            shutil.rmtree(self.sandbox_path)

sandbox = SandboxManager()
