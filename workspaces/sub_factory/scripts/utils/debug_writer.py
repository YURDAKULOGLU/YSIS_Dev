from crewai_tools import FileWriterTool
import os

try:
    print("Initializing writer tool...")
    writer = FileWriterTool()

    target_file = os.path.abspath("debug_output.txt")
    print(f"Target file: {target_file}")

    print("Writing content...")
    result = writer._run(filename=target_file, content="Debug content from FileWriterTool direct usage.")

    print(f"Tool operation result: {result}")

    if os.path.exists(target_file):
        print(f"File exists. Size: {os.path.getsize(target_file)} bytes")
        with open(target_file, 'r') as f:
            print(f"Content: {f.read()}")
    else:
        print("File does NOT exist.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
