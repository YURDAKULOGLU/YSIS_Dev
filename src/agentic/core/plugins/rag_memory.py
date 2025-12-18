from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class RAGMemory:
    def __init__(self, persist_path: str = "./.YBIS_Dev/Knowledge/LocalDB"):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            # Initialize ChromaDB client (Persistent)
            self.client = chromadb.PersistentClient(path=persist_path)
            self.collection = self.client.get_or_create_collection(name="rag_memory")
        except Exception as e:
            print(f"[RAGMemory] Error initializing ChromaDB: {e}")
            self.client = None
            self.collection = None

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
