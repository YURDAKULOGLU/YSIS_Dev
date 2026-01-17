#!/usr/bin/env python3
"""
Verify RAG is working by querying the codebase collection.
"""

import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def verify_rag():
    from src.ybis.data_plane.vector_store import VectorStore

    print("=" * 60)
    print("RAG Verification")
    print("=" * 60)
    print()

    # Check if .chroma exists
    chroma_dir = project_root / ".chroma"
    if not chroma_dir.exists():
        print("[FAIL] .chroma directory not found")
        print("       Run: python scripts/index_codebase.py")
        return False

    print(f"[OK] .chroma directory exists: {chroma_dir}")

    # Try to query
    try:
        vs = VectorStore()
        print("[OK] VectorStore initialized")
        
        # Test query
        query = "dependency graph analysis"
        print(f"\nQuerying: '{query}'")
        results = vs.query("codebase", query, top_k=3)

        if not results:
            print("[FAIL] No results returned - collection may be empty")
            print("       Run: python scripts/index_codebase.py")
            return False

        print(f"[OK] Query returned {len(results)} results")
        print()
        print("Sample results:")
        print("-" * 60)
        for i, result in enumerate(results, 1):
            file_path = result['metadata'].get('file', 'unknown')
            distance = result.get('distance', 0.0)
            doc_preview = result['document'][:300].replace('\n', ' ')
            print(f"\n{i}. File: {file_path}")
            print(f"   Distance: {distance:.4f}")
            print(f"   Preview: {doc_preview}...")
        print("-" * 60)
        print()
        print("[SUCCESS] RAG is working!")
        return True

    except Exception as e:
        print(f"[FAIL] Query failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_rag()
    sys.exit(0 if success else 1)

