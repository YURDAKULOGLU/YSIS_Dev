from fastmcp import FastMCP
import inspect

print("Attributes of FastMCP:")
print(dir(FastMCP))

try:
    print("\nSignature of run:")
    print(inspect.signature(FastMCP.run))
except Exception as e:
    print(f"Could not get signature of run: {e}")

try:
    print("\nHelp on run:")
    help(FastMCP.run)
except:
    pass
