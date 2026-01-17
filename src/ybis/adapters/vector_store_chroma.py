"""
ChromaDB Vector Store Adapter.

Adapter for ChromaDB vector database integration.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..syscalls.journal import append_event


class VectorStoreAdapter(ABC):
    """Base interface for vector store adapters."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if adapter is available."""
        ...

    @abstractmethod
    def add_documents(
        self, collection: str, documents: list[str], metadata: list[dict[str, Any]] | None = None
    ) -> None:
        """Add documents to collection."""
        ...

    @abstractmethod
    def query(self, collection: str, text: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Query collection for similar documents."""
        ...


class ChromaVectorStoreAdapter(VectorStoreAdapter):
    """ChromaDB vector store adapter."""

    def __init__(self, persist_directory: Path | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize ChromaDB adapter.

        Args:
            persist_directory: Directory to persist ChromaDB data
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self._client = None
        self._available = False
        self.persist_directory = persist_directory or (PROJECT_ROOT / ".chroma")
        self.run_path = run_path
        self.trace_id = trace_id
        self._initialize()
        
        # Journal: Chroma init
        if self.run_path:
            append_event(
                self.run_path,
                "CHROMA_INIT",
                {
                    "persist_dir": str(self.persist_directory),
                },
                trace_id=self.trace_id,
            )

    def _initialize(self) -> None:
        """Initialize ChromaDB client."""
        try:
            import chromadb
            from chromadb.config import Settings

            self.persist_directory.mkdir(parents=True, exist_ok=True)

            self._client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False),
            )
            self._available = True
        except ImportError:
            self._available = False
        except Exception:
            self._available = False

    def is_available(self) -> bool:
        """Check if ChromaDB is available."""
        return self._available

    def _get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings using LiteLLM with Ollama."""
        try:
            import litellm

            embeddings = []
            for text in texts:
                response = litellm.embeddings(
                    model="ollama/nomic-embed-text",
                    input=[text],
                    api_base="http://localhost:11434",
                )
                embeddings.append(response.data[0].embedding)

            return embeddings
        except Exception:
            # Fallback: return empty embeddings (will fail gracefully)
            return [[0.0] * 768 for _ in texts]

    def add_documents(
        self, collection: str, documents: list[str], metadata: list[dict[str, Any]] | None = None
    ) -> None:
        """Add documents to ChromaDB collection."""
        if not self.is_available():
            raise RuntimeError("ChromaDB not available")

        if metadata is None:
            metadata = [{}] * len(documents)

        if len(metadata) != len(documents):
            raise ValueError("metadata list must have same length as documents")

        # Get embeddings
        embeddings = self._get_embeddings(documents)

        # Get or create collection
        coll = self._client.get_or_create_collection(name=collection)

        # Add documents
        ids = [f"doc_{i}_{hash(doc)}" for i, doc in enumerate(documents)]
        coll.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata,
            ids=ids,
        )

    def query(self, collection: str, text: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Query ChromaDB collection."""
        if not self.is_available():
            return []

        # Get embedding for query
        query_embedding = self._get_embeddings([text])[0]

        # Get collection
        try:
            coll = self._client.get_collection(name=collection)
        except Exception:
            return []  # Collection doesn't exist

        # Query
        results = coll.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        # Format results
        formatted_results = []
        if results["documents"] and len(results["documents"][0]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append(
                    {
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0.0,
                    }
                )
        
        # Journal: Chroma query
        if self.run_path:
            append_event(
                self.run_path,
                "CHROMA_QUERY",
                {
                    "collection": collection,
                    "query_length": len(text),
                    "results_count": len(formatted_results),
                },
                trace_id=self.trace_id,
            )

        return formatted_results

    def add(self, collection: str, documents: list[str], metadata: list[dict[str, Any]] | None = None) -> None:
        """
        Add documents to collection (alias for add_documents).
        
        Args:
            collection: Collection name
            documents: List of document texts
            metadata: Optional list of metadata dicts
        """
        self.add_documents(collection, documents, metadata)

    def search(self, collection: str, text: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Search collection for similar documents (alias for query).
        
        Args:
            collection: Collection name
            text: Search query text
            top_k: Number of results to return
            
        Returns:
            List of similar documents with metadata
        """
        return self.query(collection, text, top_k)


