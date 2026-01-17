"""
Qdrant Vector Store Adapter.

Adapter for Qdrant vector database integration.
"""

from typing import Any

from .vector_store_chroma import VectorStoreAdapter


class QdrantVectorStoreAdapter(VectorStoreAdapter):
    """Qdrant vector store adapter."""

    def __init__(self, url: str | None = None, api_key: str | None = None):
        """
        Initialize Qdrant adapter.

        Args:
            url: Qdrant server URL (default: http://localhost:6333)
            api_key: Optional API key for Qdrant Cloud
        """
        self._client = None
        self._available = False
        self.url = url or "http://localhost:6333"
        self.api_key = api_key
        self._initialize()

    def _initialize(self) -> None:
        """Initialize Qdrant client."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            if self.api_key:
                self._client = QdrantClient(url=self.url, api_key=self.api_key)
            else:
                self._client = QdrantClient(url=self.url)

            # Test connection
            self._client.get_collections()
            self._available = True
        except ImportError:
            self._available = False
        except Exception:
            self._available = False

    def is_available(self) -> bool:
        """Check if Qdrant is available."""
        return self._available

    def _get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings using LiteLLM with Ollama."""
        try:
            import litellm

            embeddings = []
            for text in texts:
                response = litellm.embedding(
                    model="ollama/nomic-embed-text",
                    input=text,
                    api_base="http://localhost:11434",
                )
                embeddings.append(response["data"][0]["embedding"])

            return embeddings
        except Exception:
            return [[0.0] * 768 for _ in texts]

    def add_documents(
        self, collection: str, documents: list[str], metadata: list[dict[str, Any]] | None = None
    ) -> None:
        """Add documents to Qdrant collection."""
        if not self.is_available():
            raise RuntimeError("Qdrant not available")

        if metadata is None:
            metadata = [{}] * len(documents)

        # Get embeddings
        embeddings = self._get_embeddings(documents)

        # Create collection if it doesn't exist
        try:
            from qdrant_client.models import Distance, VectorParams

            try:
                self._client.get_collection(collection)
            except Exception:
                # Collection doesn't exist, create it
                self._client.create_collection(
                    collection_name=collection,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
        except Exception:
            pass  # Collection might already exist

        # Add documents
        from qdrant_client.models import PointStruct

        points = []
        for i, (doc, emb, meta) in enumerate(zip(documents, embeddings, metadata)):
            points.append(
                PointStruct(
                    id=i,
                    vector=emb,
                    payload={"document": doc, **meta},
                )
            )

        self._client.upsert(collection_name=collection, points=points)

    def query(self, collection: str, text: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Query Qdrant collection."""
        if not self.is_available():
            return []

        # Get embedding for query
        query_embedding = self._get_embeddings([text])[0]

        # Query
        try:
            results = self._client.search(
                collection_name=collection,
                query_vector=query_embedding,
                limit=top_k,
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append(
                    {
                        "document": result.payload.get("document", ""),
                        "metadata": {k: v for k, v in result.payload.items() if k != "document"},
                        "distance": 1.0 - result.score,  # Convert similarity to distance
                    }
                )

            return formatted_results
        except Exception:
            return []  # Collection doesn't exist or query failed

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


