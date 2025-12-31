"""
LocalRAG - Local Retrieval Augmented Generation using ChromaDB + Ollama.

Restored from legacy/20_WORKFORCE/01_Python_Core/Tools/local_rag.py
Provides context enrichment for planning and execution.
"""

import os
from pathlib import Path

# Optional dependency - ChromaDB may not be installed
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from src.agentic.core.config import PROJECT_ROOT

# Constants
DOC_PREVIEW_MAX_LENGTH = 500


class LocalRAG:
    """
    Local RAG tool using ChromaDB for vector storage and Ollama for embeddings.

    Features:
    - Persistent vector store
    - Ollama-based embeddings (nomic-embed-text)
    - Code-aware document indexing
    - Semantic search for context retrieval
    """

    def __init__(
        self,
        persist_path: str = None,
        embedding_model: str = "nomic-embed-text",
        ollama_url: str = None
    ):
        self.persist_path = persist_path or str(PROJECT_ROOT / "Knowledge" / "VectorDB")
        self.embedding_model = embedding_model
        self.ollama_url = ollama_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        self.client = None
        self.collection = None
        self._initialized = False

        if CHROMADB_AVAILABLE:
            self._initialize()
        else:
            print("[LocalRAG] ChromaDB not available. Install with: pip install chromadb")

    def _initialize(self):
        """Initialize ChromaDB client and collection."""
        try:
            # Ensure persist path exists
            Path(self.persist_path).mkdir(parents=True, exist_ok=True)

            # Initialize persistent client
            self.client = chromadb.PersistentClient(path=self.persist_path)

            # Use Ollama for embeddings
            # Requires Ollama running with embedding model
            self.embedding_fn = embedding_functions.OllamaEmbeddingFunction(
                url=f"{self.ollama_url.rstrip('/')}/api/embeddings",
                model_name=self.embedding_model
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="ybis_knowledge",
                embedding_function=self.embedding_fn,
                metadata={"description": "YBIS codebase knowledge"}
            )

            self._initialized = True
            print(f"[LocalRAG] Initialized with {self.collection.count()} documents")

        except Exception as e:
            print(f"[LocalRAG] Init failed: {e}")
            self._initialized = False

    def is_available(self) -> bool:
        """Check if RAG is available and initialized."""
        return CHROMADB_AVAILABLE and self._initialized

    def document_count(self) -> int:
        """Get the number of documents in the collection."""
        if not self._initialized:
            return 0
        try:
            return self.collection.count()
        except Exception:
            return 0

    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: dict[str, str] | None = None
    ) -> bool:
        """
        Add a document to the knowledge base.

        Args:
            doc_id: Unique document identifier
            content: Document text content
            metadata: Optional metadata (source, type, etc.)

        Returns:
            True if successful
        """
        if not self.is_available():
            print("[LocalRAG] Not available, skipping document add")
            return False

        metadata = metadata or {}

        try:
            self.collection.upsert(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            return True
        except Exception as e:
            print(f"[LocalRAG] Add document failed: {e}")
            return False

    def add_code_file(self, file_path: str) -> bool:
        """
        Index a code file into the knowledge base.

        Args:
            file_path: Path to the code file

        Returns:
            True if successful
        """
        path = Path(file_path)
        if not path.exists():
            return False

        try:
            content = path.read_text(encoding='utf-8')

            # Create metadata
            metadata = {
                'source': str(path),
                'type': 'code',
                'extension': path.suffix,
                'name': path.name
            }

            # Use relative path as ID
            try:
                rel_path = path.relative_to(PROJECT_ROOT)
                doc_id = str(rel_path).replace('\\', '/')
            except ValueError:
                doc_id = str(path)

            return self.add_document(doc_id, content, metadata)

        except Exception as e:
            print(f"[LocalRAG] Index file failed: {e}")
            return False

    def search(
        self,
        query: str,
        limit: int = 5,
        filter_type: str = None
    ) -> str:
        """
        Search for relevant context.

        Args:
            query (str): Search query.
            limit (int, optional): Maximum results. Defaults to 5.
            filter_type (str, optional): Optional filter by document type. Defaults to None.

        Returns:
            str: Formatted context string.
        """
        if not self.is_available():
            return "[LocalRAG] Not available - proceeding without knowledge base context."

        try:
            # Build where filter
            where = {"type": filter_type} if filter_type else None

            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where
            )

            if not results['documents'] or not results['documents'][0]:
                return "[LocalRAG] No relevant context found."

            # Format results
            formatted = "=== RELEVANT CODE CONTEXT ===\n"
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                source = meta.get('source', 'unknown')
                distance = results['distances'][0][i] if results.get('distances') else 0

                # Truncate long documents
                doc_preview = doc[:DOC_PREVIEW_MAX_LENGTH] + "..." if len(doc) > DOC_PREVIEW_MAX_LENGTH else doc

                formatted += f"\n--- [{source}] (relevance: {1-distance:.2f}) ---\n"
                formatted += doc_preview
                formatted += "\n"

            return formatted

        except Exception as e:
            return f"[LocalRAG] Search error: {e}"

    def search_files(self, query: str, limit: int = 5) -> list[str]:
        """
        Search and return list of relevant file paths.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of file paths
        """
        if not self.is_available():
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )

            files = []
            if results['metadatas']:
                for meta in results['metadatas'][0]:
                    if meta.get('source'):
                        files.append(meta['source'])

            return files

        except Exception:
            return []

    def index_directory(
        self,
        directory: str,
        extensions: list[str] = None,
        exclude_patterns: list[str] = None
    ) -> int:
        """
        Index all code files in a directory.

        Args:
            directory: Directory path
            extensions: File extensions to index (default: .py, .ts, .js)
            exclude_patterns: Patterns to exclude

        Returns:
            Number of files indexed
        """
        extensions = extensions or ['.py', '.ts', '.js', '.tsx', '.jsx']
        exclude_patterns = exclude_patterns or ['__pycache__', 'node_modules', '.venv', '.git']

        dir_path = Path(directory)
        if not dir_path.exists():
            return 0

        count = 0
        for ext in extensions:
            for file_path in dir_path.rglob(f'*{ext}'):
                # Check exclusions
                if any(p in str(file_path) for p in exclude_patterns):
                    continue

                if self.add_code_file(str(file_path)):
                    count += 1

        print(f"[LocalRAG] Indexed {count} files from {directory}")
        return count

    def clear(self):
        """Clear all documents from the collection."""
        if self.is_available():
            try:
                # Delete and recreate collection
                self.client.delete_collection("ybis_knowledge")
                self.collection = self.client.get_or_create_collection(
                    name="ybis_knowledge",
                    embedding_function=self.embedding_fn
                )
                print("[LocalRAG] Collection cleared")
            except Exception as e:
                print(f"[LocalRAG] Clear failed: {e}")


class _LocalRAGSingleton:
    """Singleton holder to avoid global statement."""

    _instance: LocalRAG | None = None

    @classmethod
    def get_instance(cls) -> LocalRAG:
        """
        Get or create the singleton LocalRAG instance.

        Returns:
            LocalRAG: The singleton instance of LocalRAG.
        """
        if cls._instance is None:
            cls._instance = LocalRAG()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance to None for testing scenarios."""
        cls._instance = None


def get_local_rag() -> LocalRAG:
    """Get or create the singleton LocalRAG instance."""
    return _LocalRAGSingleton.get_instance()


# Convenience alias
local_rag = get_local_rag()
