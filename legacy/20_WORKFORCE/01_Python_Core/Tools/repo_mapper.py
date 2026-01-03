"""Repo Mapper - Project structure"""
from pathlib import Path

class RepoMapperTool:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.ignore_dirs = {'node_modules', '.git', 'dist', '__pycache__', '.venv'}

    def get_tree(self, max_depth: int = 2) -> str:
        """Get project tree"""
        lines = []

        def walk(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            try:
                items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
                items = [i for i in items if i.name not in self.ignore_dirs]

                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    connector = "+-- " if is_last else "|-- "
                    lines.append(f"{prefix}{connector}{item.name}")
                    if item.is_dir():
                        extension = "    " if is_last else "|   "
                        walk(item, prefix + extension, depth + 1)
            except:
                pass

        walk(self.project_root)
        return "\n".join(lines)

repo_mapper = RepoMapperTool()
