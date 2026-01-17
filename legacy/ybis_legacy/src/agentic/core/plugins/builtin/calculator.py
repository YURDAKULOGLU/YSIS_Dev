from src.agentic.core.plugin_system.protocol import ToolProtocol

class Calculator(ToolProtocol):
    def execute(self, operation, *args):
        if operation == "add":
            return sum(args)
        elif operation == "subtract":
            return args[0] - sum(args[1:])
        elif operation == "multiply":
            result = 1
            for arg in args:
                result *= arg
            return result
        elif operation == "divide":
            if len(args) < 2:
                raise ValueError("At least two arguments required for division")
            result = args[0]
            for arg in args[1:]:
                if arg == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result /= arg
            return result
        else:
            raise ValueError(f"Unsupported operation: {operation}")
