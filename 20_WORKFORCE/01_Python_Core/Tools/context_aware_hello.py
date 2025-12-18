
import os
from pathlib import Path

def get_project_name():
    """Reads project name from README.md"""
    readme_path = Path(__file__).parent.parent.parent.parent / "README.md"
    try:
        content = readme_path.read_text(encoding='utf-8')
        # Simple extraction: First line
        first_line = content.split('\n')[0]
        return first_line.replace('#', '').strip()
    except Exception as e:
        return f"Unknown Project (Error: {e})"

def main():
    project_name = get_project_name()
    print(f"Hello from {project_name}")

if __name__ == "__main__":
    main()
