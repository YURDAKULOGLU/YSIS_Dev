#!/usr/bin/env python3
"""
Code Graph Ingestion Script
Runs the CodeGraphIngestor to populate Neo4j with AST data.
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agentic.skills.code_graph import CodeGraphIngestor

def main():
    try:
        ingestor = CodeGraphIngestor()
        root_dir = os.getcwd()
        ingestor.ingest_directory(root_dir)
    except ImportError as e:
        print(f"[ERROR] Dependency missing: {e}")
        print("Run: pip install tree-sitter-languages")
    except Exception as e:
        print(f"[FATAL] {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
