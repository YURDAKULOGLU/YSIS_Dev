import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class RAGMemory:
    def __init__(self):
        # Standard Path: ProjectRoot/Knowledge/LocalDB/chroma_db
        self.persist_path = os.path.join(os.getcwd(), "Knowledge", "LocalDB", "chroma_db")
        
        # Ensure parent dir exists
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        
        print(f"[RAGMemory] Initializing at: {self.persist_path}")
        
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client (Persistent)
        # We let it fail if it must. No swallowing errors.
        self.client = chromadb.PersistentClient(path=self.persist_path)
        self.collection = self.client.get_or_create_collection(name="rag_memory")

    def add_text(self, text: str) -> None:
        """Add a text entry to the RAG memory."""
        if not self.collection:
            print("[RAGMemory] Collection not available. Cannot add text.")
            return
        
        embedding = self.embedding_model.encode(text).tolist()
        self.collection.add(
            documents=[text],
            embeddings=[embedding]
        )

    def query(self, query: str, limit: int = 5) -> list:
        """Query the RAG memory for similar texts."""
        if not self.collection:
            print("[RAGMemory] Collection not available. Cannot query.")
            return []
        
        embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit
        )
        return results['documents'][0]
