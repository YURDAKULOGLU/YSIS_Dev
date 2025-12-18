import sys
import os
import asyncio

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Agentic.Agents.doc_writer import doc_writer
from Agentic.Tools.file_ops import file_ops

async def main():
    target_file = ".YBIS_Dev/Agentic/Tools/git_ops.py"
    output_file = "docs/technical/git_ops_manual.md"
    
    print(f"Reading {target_file}...")
    code = file_ops.read_file(target_file)
    
    print("Generating documentation...")
    doc = await doc_writer.document_file('git_ops.py', code)
    
    print(f"Writing to {output_file}...")
    file_ops.write_file(output_file, doc)
    
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
