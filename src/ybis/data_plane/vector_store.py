"""
Vector Store Service - Local vector database for semantic search.

Uses ChromaDB for persistent vector storage and LiteLLM for embeddings.
"""

import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except (ImportError, Exception) as e:
    chromadb = None
    CHROMADB_AVAILABLE = False
    CHROMADB_ERROR = str(e)

from ..constants import PROJECT_ROOT
from ..services.policy import get_policy_provider
from ..syscalls.journal import append_event


class VectorStore:
    """
    Vector Store - ChromaDB-based semantic search service.

    Provides document storage and retrieval using embeddings.
    """

    def __init__(self, persist_directory: Path | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize vector store.

        Args:
            persist_directory: Directory to persist ChromaDB data (default: .chroma in project root)
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        if persist_directory is None:
            persist_directory = PROJECT_ROOT / ".chroma"
        self.persist_directory = Path(persist_directory)
        self.run_path = run_path
        self.trace_id = trace_id
        self._adapter = None
        self._provider = None
        self.client = None

        policy_provider = get_policy_provider()
        adapters = policy_provider.get_policy().get("adapters", {})
        prefer_qdrant = adapters.get("qdrant_vector_store", {}).get("enabled", False)

        if prefer_qdrant:
            try:
                from ..adapters.vector_store_qdrant import QdrantVectorStoreAdapter

                qdrant_adapter = QdrantVectorStoreAdapter()
                if qdrant_adapter.is_available():
                    self._adapter = qdrant_adapter
                    self._provider = "qdrant"
            except Exception as e:
                logger.debug(f"Qdrant adapter unavailable: {e}")

        if self._adapter is None:
            try:
                from ..adapters.vector_store_chroma import ChromaVectorStoreAdapter

                chroma_adapter = ChromaVectorStoreAdapter(
                    persist_directory=self.persist_directory,
                    run_path=self.run_path,
                    trace_id=self.trace_id,
                )
                if chroma_adapter.is_available():
                    self._adapter = chroma_adapter
                    self._provider = "chroma"
            except Exception as e:
                logger.debug(f"Chroma adapter unavailable: {e}")

        if self._adapter is not None:
            if self.run_path:
                append_event(
                    self.run_path,
                    "VECTOR_STORE_INIT",
                    {
                        "provider": self._provider or "adapter",
                    },
                    trace_id=self.trace_id,
                )
            return

        if not CHROMADB_AVAILABLE:
            error_msg = CHROMADB_ERROR if CHROMADB_ERROR else "ChromaDB not installed"
            raise ImportError(f"Vector store not available: {error_msg}. Install with: pip install chromadb")

        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False),
        )

        # Journal: Vector store init
        if self.run_path:
            append_event(
                self.run_path,
                "VECTOR_STORE_INIT",
                {
                    "provider": "chromadb",
                    "persist_dir": str(self.persist_directory),
                },
                trace_id=self.trace_id,
            )

    def get_collection(self, collection_name: str):
        """
        Get or create a collection.

        Args:
            collection_name: Name of the collection

        Returns:
            ChromaDB collection
        """
        return self.client.get_or_create_collection(name=collection_name)

    def _get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Get embeddings for texts using LiteLLM with Ollama.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        try:
            import litellm

            embeddings = []
            for text in texts:
                # Use nomic-embed-text model via Ollama
                # Note: litellm uses 'embedding' (singular) not 'embeddings'
                response = litellm.embedding(
                    model="ollama/nomic-embed-text",
                    input=text,
                    api_base="http://localhost:11434",
                )
                # Response format: {"data": [{"embedding": [...]}]}
                embeddings.append(response["data"][0]["embedding"])

            return embeddings

        except ImportError:
            raise ImportError("LiteLLM not installed. Install with: pip install litellm")
        except Exception as e:
            raise Exception(f"Embedding generation failed: {e!s}")

    def add_documents(self, collection: str, documents: list[str], metadata: list[dict] | None = None) -> None:
        """
        Add documents to a collection.

        Args:
            collection: Collection name
            documents: List of document texts
            metadata: Optional list of metadata dicts (one per document)
        """
        if self._adapter is not None:
            self._adapter.add_documents(collection, documents, metadata)
            if self.run_path:
                append_event(
                    self.run_path,
                    "VECTOR_STORE_ADD",
                    {
                        "collection": collection,
                        "doc_count": len(documents),
                        "provider": self._provider or "adapter",
                    },
                    trace_id=self.trace_id,
                )
            return
        if metadata is None:
            metadata = [{}] * len(documents)

        if len(metadata) != len(documents):
            raise ValueError("metadata list must have same length as documents")

        # Get embeddings
        embeddings = self._get_embeddings(documents)

        # Get collection
        coll = self.get_collection(collection)

        # Add documents
        ids = [f"doc_{i}" for i in range(len(documents))]
        coll.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata,
            ids=ids,
        )

        # Journal: Documents added
        if self.run_path:
            append_event(
                self.run_path,
                "VECTOR_STORE_ADD",
                {
                    "collection": collection,
                    "doc_count": len(documents),
                },
                trace_id=self.trace_id,
            )

    def query(self, collection: str, text: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Query a collection for similar documents.

        Args:
            collection: Collection name
            text: Query text
            top_k: Number of results to return

        Returns:
            List of result dictionaries with 'document', 'metadata', 'distance'
        """
        start_time = time.time()
        try:
            if self._adapter is not None:
                results = self._adapter.query(collection, text, top_k=top_k)
                elapsed_ms = (time.time() - start_time) * 1000
                if self.run_path:
                    append_event(
                        self.run_path,
                        "VECTOR_STORE_QUERY",
                        {
                            "collection": collection,
                            "query_length": len(text),
                            "results_count": len(results),
                            "duration_ms": round(elapsed_ms, 2),
                            "provider": self._provider or "adapter",
                        },
                        trace_id=self.trace_id,
                    )
                return results
            # Get embedding for query
            query_embedding = self._get_embeddings([text])[0]

            # Get collection
            coll = self.get_collection(collection)

            # Query
            results = coll.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
            )

            # Format results
            formatted_results = []
            if results["documents"] and len(results["documents"][0]) > 0:
                for i in range(len(results["documents"][0])):
                    formatted_results.append({
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0.0,
                    })

            elapsed_ms = (time.time() - start_time) * 1000

            # Journal: Query executed
            if self.run_path:
                append_event(
                    self.run_path,
                    "VECTOR_STORE_QUERY",
                    {
                        "collection": collection,
                        "query_length": len(text),
                        "results_count": len(formatted_results),
                        "duration_ms": round(elapsed_ms, 2),
                    },
                    trace_id=self.trace_id,
                )

            return formatted_results
        except Exception as e:
            # Journal: Query error
            if self.run_path:
                append_event(
                    self.run_path,
                    "VECTOR_STORE_ERROR",
                    {
                        "operation": "query",
                        "error": str(e)[:200],
                    },
                    trace_id=self.trace_id,
                )
            raise
