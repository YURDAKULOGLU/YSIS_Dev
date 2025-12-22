import os

class FileOpsTool:
    def read_file(self, file_path: str) -> str:
        """Read content of a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file (creates directories if needed)"""
        try:
            dirname = os.path.dirname(file_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"

    def list_dir(self, dir_path: str = ".") -> str:
        """List files in a directory"""
        try:
            files = os.listdir(dir_path)
            return "\n".join(files)
        except Exception as e:
            return f"Error listing directory: {e}"

file_ops = FileOpsTool()