import sys
import os
import requests
import asyncio
from pathlib import Path
from typing import Optional

# Setup path
sys.path.insert(0, os.getcwd())
from src.agentic.core.config import PROJECT_ROOT

def fetch_markdown(url: str) -> Optional[str]:
    """
    Fetches clean markdown from a URL using jina.ai reader.
    Industry best practice for agentic context.
    """
    print(f"[KnowledgeFetcher] Harvesting from: {url}")
    jina_url = f"https://r.jina.ai/{url}"

    try:
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[KnowledgeFetcher] Error fetching: {e}")
        return None

async def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/fetch_docs.py <library_name> <url>")
        return

    lib_name = sys.argv[1]
    url = sys.argv[2]

    content = fetch_markdown(url)

    if content:
        target_dir = PROJECT_ROOT / "Knowledge" / "API_References"
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / f"{lib_name}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[KnowledgeFetcher] Successfully saved {lib_name} docs to {file_path}")

        # NEXT: We can automatically trigger RAG ingestion here
        print("[KnowledgeFetcher] Ingestion to Vector DB will follow...")
    else:
        print("[KnowledgeFetcher] Harvest failed.")

if __name__ == "__main__":
    asyncio.run(main())
