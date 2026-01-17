"""
Codebase Ingestor - Index codebase into vector store.

Scans src/ybis and src/agentic (legacy) and ingests into ChromaDB for RAG.
"""

import ast
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..data_plane.vector_store import VectorStore
from ..syscalls.journal import append_event


class CodebaseIngestor:
    """
    Codebase Ingestor - Scans and indexes codebase into vector store.

    Chunks files logically by class/function and ingests into ChromaDB.
    """

    def __init__(self, vector_store: VectorStore | None = None):
        """
        Initialize ingestor.

        Args:
            vector_store: Vector store instance (creates new if None)
        """
        try:
            self.vector_store = vector_store or VectorStore()
        except (ImportError, Exception) as e:
            raise ImportError(f"Vector store not available: {e}. Install ChromaDB: pip install chromadb")
        self.collection_name = "codebase"

    def ingest_codebase(self, root_paths: list[Path] | None = None) -> int:
        """
        Ingest codebase into vector store.

        Args:
            root_paths: List of root paths to scan (default: src/ybis and src/agentic)

        Returns:
            Number of documents ingested
        """
        if root_paths is None:
            root_paths = [
                PROJECT_ROOT / "src" / "ybis",
                PROJECT_ROOT / "src" / "agentic",
            ]

        documents = []
        metadata_list = []

        for root_path in root_paths:
            if not root_path.exists():
                continue

            # Scan Python files
            for py_file in root_path.rglob("*.py"):
                # Skip __pycache__ and test files for now
                if "__pycache__" in str(py_file) or "test_" in py_file.name:
                    continue

                chunks = self._chunk_file(py_file, root_path)
                for chunk in chunks:
                    documents.append(chunk["content"])
                    metadata_list.append(chunk["metadata"])

        # Ingest in batches
        batch_size = 10
        total_ingested = 0

        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i : i + batch_size]
            batch_metadata = metadata_list[i : i + batch_size]

            self.vector_store.add_documents(self.collection_name, batch_docs, batch_metadata)
            total_ingested += len(batch_docs)

        # Record ingestion event
        run_path = PROJECT_ROOT / "workspaces" / "ingestion" / "runs" / "ingest-1"
        run_path.mkdir(parents=True, exist_ok=True)
        append_event(
            run_path,
            "KNOWLEDGE_INGESTED",
            {
                "collection": self.collection_name,
                "documents_count": total_ingested,
                "root_paths": [str(p) for p in root_paths],
            },
        )

        return total_ingested

    def _chunk_file(self, file_path: Path, root_path: Path) -> list[dict[str, Any]]:
        """
        Chunk a Python file by class/function.

        Args:
            file_path: Path to Python file
            root_path: Root path for relative path calculation

        Returns:
            List of chunk dictionaries with 'content' and 'metadata'
        """
        chunks = []

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))

            # Calculate relative path
            rel_path = file_path.relative_to(root_path)

            # Extract module-level docstring
            module_docstring = ast.get_docstring(tree)
            if module_docstring:
                chunks.append({
                    "content": f"Module: {rel_path}\n\n{module_docstring}",
                    "metadata": {
                        "type": "module",
                        "file": str(rel_path),
                        "path": str(file_path),
                    },
                })

            # Extract classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_docstring = ast.get_docstring(node)
                    class_code = ast.unparse(node)

                    chunks.append({
                        "content": f"Class: {node.name} in {rel_path}\n\n{class_docstring or 'No docstring'}\n\n{class_code}",
                        "metadata": {
                            "type": "class",
                            "name": node.name,
                            "file": str(rel_path),
                            "path": str(file_path),
                            "line": node.lineno,
                        },
                    })

            # Extract functions (top-level and methods)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Skip if it's a method (inside a class)
                    is_method = any(
                        isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) if hasattr(parent, "body") and node in getattr(parent, "body", [])
                    )
                    if is_method:
                        continue

                    func_docstring = ast.get_docstring(node)
                    func_code = ast.unparse(node)

                    chunks.append({
                        "content": f"Function: {node.name} in {rel_path}\n\n{func_docstring or 'No docstring'}\n\n{func_code}",
                        "metadata": {
                            "type": "function",
                            "name": node.name,
                            "file": str(rel_path),
                            "path": str(file_path),
                            "line": node.lineno,
                        },
                    })

        except SyntaxError:
            # Skip files with syntax errors
            pass
        except Exception:
            # Fallback: add entire file as one chunk
            try:
                content = file_path.read_text(encoding="utf-8")
                chunks.append({
                    "content": f"File: {rel_path}\n\n{content}",
                    "metadata": {
                        "type": "file",
                        "file": str(rel_path),
                        "path": str(file_path),
                    },
                })
            except Exception:
                pass

        return chunks


def ingest_codebase() -> int:
    """
    Ingest codebase into vector store.

    Returns:
        Number of documents ingested
    """
    ingestor = CodebaseIngestor()
    return ingestor.ingest_codebase()

