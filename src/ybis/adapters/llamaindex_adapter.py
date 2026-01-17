"""
LlamaIndex Adapter - Context management for legacy and new code.

Uses LlamaIndex to index and query codebase for semantic search.
"""

from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..syscalls.journal import append_event


class LlamaIndexAdapter:
    """
    LlamaIndex adapter for codebase context management.

    Indexes legacy (src/agentic/) and new (src/ybis/) code for semantic search.
    """

    def __init__(self, project_root: Path | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize LlamaIndex adapter.

        Args:
            project_root: Optional project root directory (defaults to PROJECT_ROOT)
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.project_root = project_root or PROJECT_ROOT
        self._index = None
        self._initialized = False
        self.run_path = run_path
        self.trace_id = trace_id
        
        # Journal: LlamaIndex init
        if self.run_path:
            append_event(
                self.run_path,
                "LLAMAINDEX_INIT",
                {
                    "project_root": str(self.project_root),
                },
                trace_id=self.trace_id,
            )

    def _initialize_index(self) -> None:
        """Initialize LlamaIndex index (lazy loading)."""
        if self._initialized:
            return

        try:
            from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
            from llama_index.core.node_parser import CodeSplitter

            # Index both legacy and new code
            legacy_path = self.project_root / "src" / "agentic"
            new_path = self.project_root / "src" / "ybis"

            documents = []

            # Read legacy code
            if legacy_path.exists():
                try:
                    legacy_reader = SimpleDirectoryReader(
                        str(legacy_path),
                        recursive=True,
                    )
                    legacy_docs = legacy_reader.load_data()
                    documents.extend(legacy_docs)
                except Exception:
                    pass

            # Read new code
            if new_path.exists():
                try:
                    new_reader = SimpleDirectoryReader(
                        str(new_path),
                        recursive=True,
                    )
                    new_docs = new_reader.load_data()
                    documents.extend(new_docs)
                except Exception:
                    pass

            if documents:
                # Use code splitter for better chunking
                splitter = CodeSplitter(
                    language="python",
                    max_chars=1500,
                )
                nodes = splitter.get_nodes_from_documents(documents)

                # Create vector store index
                self._index = VectorStoreIndex(nodes)
                self._initialized = True
                
                # Journal: Index created
                if self.run_path:
                    append_event(
                        self.run_path,
                        "LLAMAINDEX_INDEX",
                        {
                            "documents_count": len(documents),
                            "nodes_count": len(nodes),
                        },
                        trace_id=self.trace_id,
                    )
            else:
                self._initialized = False

        except ImportError:
            # LlamaIndex not installed, skip silently
            self._initialized = False
        except Exception:
            self._initialized = False

    def query_codebase(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Query codebase using semantic search.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant code snippets with metadata
        """
        self._initialize_index()

        if not self._index or not self._initialized:
            return []

        try:
            from llama_index.core import QueryBundle

            query_engine = self._index.as_query_engine(similarity_top_k=top_k)
            query_bundle = QueryBundle(query_str=query)
            response = query_engine.query(query_bundle)

            results = []
            for node in response.source_nodes:
                results.append(
                    {
                        "document": node.text,
                        "file_path": node.node_id,
                        "score": node.score if hasattr(node, "score") else 0.0,
                    }
                )
            
            # Journal: Query executed
            if self.run_path:
                append_event(
                    self.run_path,
                    "LLAMAINDEX_QUERY",
                    {
                        "query_length": len(query),
                        "results_count": len(results),
                    },
                    trace_id=self.trace_id,
                )

            return results

        except Exception:
            return []

    def is_available(self) -> bool:
        """
        Check if LlamaIndex is available and initialized.

        Returns:
            True if LlamaIndex is ready to use
        """
        self._initialize_index()
        return self._initialized and self._index is not None

