import sys
import os
import glob
from pathlib import Path
import asyncio

# Setup path
sys.path.insert(0, os.getcwd())
from src.agentic.core.plugins.rag_memory import RAGMemory
from src.agentic.core.config import PROJECT_ROOT

async def ingest_all():
    print("[KnowledgeIngester] Starting massive ingestion to Vector DB...")

    rag = RAGMemory()
    knowledge_dir = PROJECT_ROOT / "Knowledge"

    # Supported file types
    extensions = ["*.md", "*.py", "*.json"]
    files_to_index = []

    for ext in extensions:
        files_to_index.extend(glob.glob(str(knowledge_dir / "**" / ext), recursive=True))

    # Also index the current codebase (important for self-awareness)
    files_to_index.extend(glob.glob(str(PROJECT_ROOT / "src" / "**" / "*.py"), recursive=True))

    print(f"[KnowledgeIngester] Found {len(files_to_index)} files to digest.")

    for file_path in files_to_index:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            rel_path = os.path.relpath(file_path, PROJECT_ROOT)

            # Use add_text instead of add
            rag.add_text(f"FILE: {rel_path}\n\nCONTENT:\n{content}", metadata={"path": rel_path})
            print(f"[KnowledgeIngester] Digested: {rel_path}")
        except Exception as e:
            print(f"[KnowledgeIngester] Failed to digest {file_path}: {e}")

    print("[KnowledgeIngester] MASSIVE INGESTION COMPLETE. The factory is now Super-Aware.")

if __name__ == "__main__":
    asyncio.run(ingest_all())
