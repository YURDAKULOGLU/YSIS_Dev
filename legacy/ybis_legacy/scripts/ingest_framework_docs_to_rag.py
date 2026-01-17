#!/usr/bin/env python3
"""
Ingest scraped framework documentation into RAG.
This script ingests all documentation from Knowledge/Frameworks/ into RAG.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def ingest_to_rag():
    """Ingest all framework docs into RAG (from install_framework.py)."""
    try:
        from src.agentic.tools.local_rag import get_local_rag
        
        rag = get_local_rag()
        if not rag:
            print("[SKIP] RAG not available (get_local_rag returned None)")
            return
        
        if not hasattr(rag, 'is_available') or not rag.is_available():
            print("[SKIP] RAG not available (is_available() returned False)")
            return
        
        docs_base = PROJECT_ROOT / "Knowledge" / "Frameworks"
        if not docs_base.exists():
            print(f"[ERROR] {docs_base} does not exist!")
            return
        
        # Find all markdown files
        md_files = list(docs_base.rglob("*.md"))
        print(f"[INFO] Found {len(md_files)} markdown files to ingest...")
        
        ingested = 0
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Generate doc_id from relative path
                try:
                    rel_path = md_file.relative_to(docs_base)
                    parts = rel_path.parts
                    framework_name = parts[0] if parts else "unknown"
                    doc_id = f"framework:{framework_name}:{str(rel_path).replace('\\', '/')}"
                except:
                    doc_id = f"framework:unknown:{md_file.name}"
                
                # Add to RAG with framework name as metadata
                rag.add_document(
                    doc_id=doc_id,
                    content=content,
                    metadata={
                        "source": f"framework:{framework_name}",
                        "file": md_file.name,
                        "type": "framework_docs",
                        "framework": framework_name
                    }
                )
                ingested += 1
                if ingested % 10 == 0:
                    print(f"  [PROGRESS] Ingested {ingested}/{len(md_files)} files...")
            except Exception as e:
                print(f"  [WARN] Failed to ingest {md_file}: {e}")
        
        print(f"\n[SUCCESS] Ingested {ingested}/{len(md_files)} files into RAG!")
        
    except ImportError:
        print("[ERROR] RAG not available (import failed)")
        print("  Make sure src.agentic.tools.local_rag is available")
    except Exception as e:
        print(f"[ERROR] RAG ingestion failed: {e}")

if __name__ == "__main__":
    ingest_to_rag()

