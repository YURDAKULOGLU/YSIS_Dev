"""
KNOWLEDGE INGESTOR
Reads markdown files from Knowledge/API_References and embeds them into Mem0.
User ID for docs: "technical_docs"
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.getcwd())

from src.agentic.bridges.mem0_bridge import Mem0Bridge

def ingest_docs():
    print("📚 STARTING KNOWLEDGE INGESTION...")
    
    docs_dir = "Knowledge/API_References"
    if not os.path.exists(docs_dir):
        print(f"❌ Directory not found: {docs_dir}")
        return

    # Initialize Mem0 for Docs
    mem = Mem0Bridge(user_id="technical_docs")
    
    files = [f for f in os.listdir(docs_dir) if f.endswith(".md")]
    
    print(f"found {len(files)} documents.")
    
    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        print(f"   Processing: {filename}...")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Mem0 automatically chunks text, but we can provide metadata
        mem.add(content, metadata={"source": filename, "type": "documentation"})
        print(f"   ✅ Indexed: {filename}")

    print("\n🎉 INGESTION COMPLETE. Mem0 is now a Technical Expert.")

if __name__ == "__main__":
    ingest_docs()

