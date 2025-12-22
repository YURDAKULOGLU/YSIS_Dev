from src.agentic.core.plugin_system.protocol import ToolProtocol

class FileOps(ToolProtocol):
    def execute(self, operation, *args):
        if operation == "read":
            if len(args) < 1:
                raise ValueError("File path required for read operation")
            file_path = args[0]
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError(f"Unsupported operation: {operation}")
