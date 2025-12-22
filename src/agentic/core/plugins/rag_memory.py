import os
import uuid
import datetime
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class RAGMemory:
    """
    Enhanced RAG Memory for YBIS.
    Stores Context, Decisions, and Failures.
    """
    def __init__(self):
        from src.agentic.core.config import CHROMA_DB_PATH

        self.persist_path = CHROMA_DB_PATH
        
        # Ensure parent dir exists
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        
        print(f"[RAGMemory] Initializing at: {self.persist_path}")
        
        # Load lightweight embedding model
        # On RTX 5090 this is instant.
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client (Persistent)
        self.client = chromadb.PersistentClient(path=self.persist_path)
        
        # Collections
        self.general_coll = self.client.get_or_create_collection(name="general_memory")
        self.failure_coll = self.client.get_or_create_collection(name="failure_memory")

    def store_failure(self, task_id: str, error_msg: str, plan_context: str, signature: str = "UNKNOWN"):
        """
        Store a failure event to prevent recurrence.
        """
        text_content = f"FAILURE: {signature}\nERROR: {error_msg}\nCONTEXT: {plan_context}"
        
        embedding = self.embedding_model.encode(text_content).tolist()
        
        self.failure_coll.add(
            ids=[str(uuid.uuid4())],
            documents=[text_content],
            embeddings=[embedding],
            metadatas=[
                {
                    "type": "failure",
                    "task_id": task_id,
                    "signature": signature,
                    "timestamp": datetime.datetime.now().isoformat()
                }
            ]
        )
        print(f"[RAGMemory] 🧠 Stored failure pattern: {signature}")

    def retrieve_relevant_failures(self, current_task: str, n_results: int = 3) -> List[str]:
        """
        Retrieve past failures relevant to the current task.
        Used to warn the Planner.
        """
        if self.failure_coll.count() == 0:
            return []
            
        embedding = self.embedding_model.encode(current_task).tolist()
        
        results = self.failure_coll.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        
        # Flatten results
        return results['documents'][0] if results['documents'] else []

    def add_text(self, text: str, metadata: Dict[str, Any] = None) -> None:
        """Add general context memory."""
        embedding = self.embedding_model.encode(text).tolist()
        meta = metadata or {}
        meta["timestamp"] = datetime.datetime.now().isoformat()
        
        self.general_coll.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
            metadatas=[meta]
        )

    def query(self, query: str, n_results: int = 5) -> List[str]:
        """Query general memory."""
        if self.general_coll.count() == 0:
            return []
            
        embedding = self.embedding_model.encode(query).tolist()
        results = self.general_coll.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []