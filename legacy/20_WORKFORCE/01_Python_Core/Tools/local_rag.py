import os
from typing import Dict

# Optional dependency - ChromaDB may not be installed
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

class LocalRAGTool:
    def __init__(self, persist_path: str = "./.YBIS_Dev/Knowledge/LocalDB"):
        if not CHROMADB_AVAILABLE:
            print("[RAG] ChromaDB not available, running without local knowledge")
            self.client = None
            self.collection = None
            return

        try:
            # Initialize ChromaDB client (Persistent)
            self.client = chromadb.PersistentClient(path=persist_path)

            # Use Ollama for embeddings (running locally)
            # Note: Requires Ollama to be running with 'nomic-embed-text' or similar
            self.embedding_fn = embedding_functions.OllamaEmbeddingFunction(
                url="http://localhost:11434/v1",
                model_name="nomic-embed-text"
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="ybis_knowledge",
                embedding_function=self.embedding_fn
            )
        except BaseException as e:
            print(f"[RAG] CRITICAL INIT FAILURE: {e} (Disabling RAG)")
            self.client = None
            self.collection = None

    def add_document(self, doc_id: str, text: str, metadata: Dict = None):
        """Add a document to the local knowledge base"""
        if not self.collection:
            print("[RAG] Not available, skipping document add")
            return

        if metadata is None:
            metadata = {}

        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"[RAG] Indexed: {doc_id}")

    def search(self, query: str, limit: int = 5) -> str:
        """Search for relevant context"""
        if not self.collection:
            return "Local RAG not available (chromadb/ollama not configured). Proceeding without knowledge base context."

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )

            if not results['documents'] or not results['documents'][0]:
                return "No relevant local knowledge found."

            formatted_results = "Found local context:\n"
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                source = meta.get('source', 'unknown')
                formatted_results += f"- [{source}] ...{doc[:200]}...\n"

            return formatted_results

        except Exception as e:
            return f"Local RAG Error: {str(e)}"

# Singleton
local_rag = LocalRAGTool()
