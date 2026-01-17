#!/usr/bin/env python3
"""
Index Codebase for RAG - Index src/ybis/**/*.py for semantic search.

This populates the "codebase" collection in VectorStore so the planner
can retrieve relevant code context when generating plans.

Usage:
    python scripts/index_codebase.py
"""

import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.data_plane.vector_store import VectorStore
from src.ybis.constants import PROJECT_ROOT


def chunk_code(content: str, file_path: str, chunk_size: int = 200) -> list[tuple[str, dict]]:
    """
    Chunk code file into semantic chunks.
    
    Tries to chunk by functions/classes, falls back to line-based chunking.
    
    Args:
        content: File content
        file_path: Relative file path
        chunk_size: Target chunk size in lines
        
    Returns:
        List of (chunk_text, metadata) tuples
    """
    chunks = []
    lines = content.split("\n")
    
    # Try to chunk by function/class boundaries
    current_chunk = []
    current_start = 0
    
    for i, line in enumerate(lines):
        current_chunk.append(line)
        
        # Check if we hit a function/class definition
        is_boundary = (
            line.strip().startswith("def ") or
            line.strip().startswith("class ") or
            line.strip().startswith("@")
        )
        
        # If we have enough lines or hit a boundary, save chunk
        if len(current_chunk) >= chunk_size or (is_boundary and len(current_chunk) > 50):
            chunk_text = "\n".join(current_chunk)
            if chunk_text.strip():
                chunks.append((
                    chunk_text,
                    {
                        "file": file_path,
                        "start_line": current_start,
                        "end_line": i,
                        "type": "code",
                    }
                ))
            current_chunk = []
            current_start = i + 1
    
    # Add remaining lines
    if current_chunk:
        chunk_text = "\n".join(current_chunk)
        if chunk_text.strip():
            chunks.append((
                chunk_text,
                {
                    "file": file_path,
                    "start_line": current_start,
                    "end_line": len(lines),
                    "type": "code",
                }
            ))
    
    # Fallback: if no chunks created, create one
    if not chunks:
        chunks.append((
            content,
            {
                "file": file_path,
                "start_line": 0,
                "end_line": len(lines),
                "type": "code",
            }
        ))
    
    return chunks


def index_codebase():
    """Index src/ybis for semantic search."""
    print("=" * 60)
    print("Indexing Codebase for RAG")
    print("=" * 60)
    print()
    
    try:
        vs = VectorStore()
        print("[OK] VectorStore initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize VectorStore: {e}")
        print("  Make sure ChromaDB is installed: pip install chromadb")
        print("  Or use alternative: pip install --upgrade chromadb opentelemetry-api")
        return
    
    docs = []
    metadata = []
    total_files = 0
    total_chunks = 0
    
    # Index src/ybis/**/*.py
    codebase_path = PROJECT_ROOT / "src" / "ybis"
    if not codebase_path.exists():
        print(f"✗ Codebase path not found: {codebase_path}")
        return
    
    print(f"Scanning: {codebase_path}")
    print()
    
    for py_file in sorted(codebase_path.rglob("*.py")):
        # Skip __pycache__ and test files for now
        if "__pycache__" in str(py_file) or "test_" in py_file.name:
            continue
        
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            rel_path = str(py_file.relative_to(PROJECT_ROOT))
            
            # Chunk the file
            file_chunks = chunk_code(content, rel_path)
            
            for chunk_text, chunk_metadata in file_chunks:
                docs.append(chunk_text)
                metadata.append(chunk_metadata)
                total_chunks += 1
            
            total_files += 1
            
            # Batch insert every 50 chunks
            if len(docs) >= 50:
                try:
                    vs.add_documents("codebase", docs, metadata)
                    print(f"  Indexed {len(docs)} chunks from {total_files} files...")
                    docs, metadata = [], []
                except Exception as e:
                    print(f"  [WARNING] Failed to index batch: {e}")
                    docs, metadata = [], []
        
        except Exception as e:
            print(f"  [WARNING] Failed to process {py_file}: {e}")
            continue
    
    # Insert remaining chunks
    if docs:
        try:
            vs.add_documents("codebase", docs, metadata)
            print(f"  Indexed final {len(docs)} chunks...")
        except Exception as e:
            print(f"  [WARNING] Failed to index final batch: {e}")
    
    print()
    print("=" * 60)
    print(f"[SUCCESS] Indexing complete!")
    print(f"  Files processed: {total_files}")
    print(f"  Total chunks: {total_chunks}")
    print("=" * 60)


if __name__ == "__main__":
    index_codebase()

