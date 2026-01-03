"""
Unit tests for LocalRAG - Local Retrieval Augmented Generation.

Tests cover:
- Initialization and availability checks
- Document operations (add, search, count)
- Singleton pattern
- Edge cases and error handling
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.agentic.tools.local_rag import (
    DOC_PREVIEW_MAX_LENGTH,
    LocalRAG,
    _LocalRAGSingleton,
    get_local_rag,
)

# Test constants
EXPECTED_DOC_COUNT = 42
EXPECTED_RESULT_COUNT = 2
WHITELISTED_SOURCES = [
    "src/agentic/core/config.py",
    "src/agentic/core/protocols.py",
]


class TestLocalRAGWithoutChromaDB:
    """Tests for LocalRAG when ChromaDB is not available."""

    def test_chromadb_not_available(self):
        """Test graceful degradation when ChromaDB is not installed."""
        # Reset singleton for clean test
        _LocalRAGSingleton._instance = None

        # When ChromaDB is not available, is_available should return False
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = False
        assert rag.is_available() is False

    def test_is_initialized_property_false(self):
        """Test is_initialized returns False when not initialized."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = False
        assert rag.is_initialized is False

    def test_is_initialized_property_true(self):
        """Test is_initialized returns True when initialized."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = True
        assert rag.is_initialized is True


class TestLocalRAGDocumentOperations:
    """Tests for document operations with mocked ChromaDB."""

    @pytest.fixture
    def mock_rag(self):
        """Create a LocalRAG instance with mocked ChromaDB."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = True
        rag.collection = MagicMock()
        rag.client = MagicMock()
        rag.embedding_fn = MagicMock()
        rag.persist_path = "/tmp/test_rag"
        rag.embedding_model = "test-model"
        rag.ollama_url = "http://localhost:11434"

        return rag

    def test_document_count_initialized(self, mock_rag):
        """Test document_count when initialized."""
        mock_rag.collection.count.return_value = EXPECTED_DOC_COUNT
        assert mock_rag.document_count() == EXPECTED_DOC_COUNT

    def test_document_count_not_initialized(self):
        """Test document_count returns 0 when not initialized."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = False
        assert rag.document_count() == 0

    def test_document_count_exception(self, mock_rag):
        """Test document_count returns 0 on exception."""
        mock_rag.collection.count.side_effect = Exception("DB error")
        assert mock_rag.document_count() == 0

    def test_add_document_success(self, mock_rag):
        """Test successful document addition."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            result = mock_rag.add_document("doc1", "content", {"type": "test"})

            assert result is True
            mock_rag.collection.upsert.assert_called_once_with(
                documents=["content"],
                metadatas=[{"type": "test"}],
                ids=["doc1"]
            )

    def test_add_document_not_available(self, mock_rag):
        """Test add_document returns False when not available."""
        with patch.object(mock_rag, 'is_available', return_value=False):
            result = mock_rag.add_document("doc1", "content")
            assert result is False

    def test_add_document_with_none_metadata(self, mock_rag):
        """Test add_document handles None metadata."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            result = mock_rag.add_document("doc1", "content", None)

            assert result is True
            mock_rag.collection.upsert.assert_called_once_with(
                documents=["content"],
                metadatas=[{}],
                ids=["doc1"]
            )

    def test_add_document_exception(self, mock_rag):
        """Test add_document returns False on exception."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            mock_rag.collection.upsert.side_effect = Exception("DB error")
            result = mock_rag.add_document("doc1", "content")
            assert result is False


class TestLocalRAGSearch:
    """Tests for search functionality."""

    @pytest.fixture
    def mock_rag(self):
        """Create a LocalRAG instance with mocked ChromaDB."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = True
        rag.collection = MagicMock()
        return rag

    def test_search_not_available(self, mock_rag):
        """Test search returns message when not available."""
        with patch.object(mock_rag, 'is_available', return_value=False):
            result = mock_rag.search("query")
            assert "[LocalRAG] Not available" in result

    def test_search_no_results(self, mock_rag):
        """Test search returns message when no results found."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            mock_rag.collection.query.return_value = {
                'documents': [[]],
                'metadatas': [[]],
                'distances': [[]]
            }
            result = mock_rag.search("query")
            assert "[LocalRAG] No relevant context found" in result

    def test_search_with_results(self, mock_rag):
        """Test search formats results correctly."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            mock_rag.collection.query.return_value = {
                'documents': [["doc content"]],
                'metadatas': [[{"source": WHITELISTED_SOURCES[0]}]],
                'distances': [[0.1]]
            }
            result = mock_rag.search("query")

            assert "=== RELEVANT CODE CONTEXT" in result
            assert f"[{WHITELISTED_SOURCES[0]}]" in result
            assert "doc content" in result

    def test_search_truncates_long_documents(self, mock_rag):
        """Test search truncates documents longer than DOC_PREVIEW_MAX_LENGTH."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            long_doc = "x" * (DOC_PREVIEW_MAX_LENGTH + 100)
            mock_rag.collection.query.return_value = {
                'documents': [[long_doc]],
                'metadatas': [[{"source": WHITELISTED_SOURCES[0]}]],
                'distances': [[0.1]]
            }
            result = mock_rag.search("query")

            assert "..." in result
            # Result should not contain the full long document
            assert long_doc not in result

    def test_search_with_filter_type(self, mock_rag):
        """Test search passes filter to query."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            mock_rag.collection.query.return_value = {
                'documents': [[]],
                'metadatas': [[]],
                'distances': [[]]
            }
            mock_rag.search("query", filter_type="code")

            mock_rag.collection.query.assert_called_with(
                query_texts=["query"],
                n_results=15,
                where={"type": "code"}
            )

    def test_search_files_not_available(self, mock_rag):
        """Test search_files returns empty list when not available."""
        with patch.object(mock_rag, 'is_available', return_value=False):
            result = mock_rag.search_files("query")
            assert result == []

    def test_search_files_returns_paths(self, mock_rag):
        """Test search_files extracts file paths from results."""
        with patch.object(mock_rag, 'is_available', return_value=True):
            mock_rag.collection.query.return_value = {
                'documents': [["doc1", "doc2"]],
                'metadatas': [[
                    {"source": WHITELISTED_SOURCES[0]},
                    {"source": WHITELISTED_SOURCES[1]},
                ]],
                'distances': [[0.1, 0.2]]
            }
            result = mock_rag.search_files("query")

            assert len(result) == EXPECTED_RESULT_COUNT
            assert WHITELISTED_SOURCES[0] in result
            assert WHITELISTED_SOURCES[1] in result


class TestLocalRAGSingleton:
    """Tests for singleton pattern."""

    def test_singleton_returns_same_instance(self):
        """Test get_local_rag returns the same instance."""
        # Reset singleton
        _LocalRAGSingleton._instance = None

        # Mock LocalRAG to avoid actual initialization
        with patch.object(LocalRAG, '__init__', lambda self: None):
            instance1 = get_local_rag()
            instance2 = get_local_rag()

            assert instance1 is instance2

    def test_reset_instance(self):
        """Test reset_instance clears the singleton."""
        # Set up a mock instance
        mock_instance = MagicMock(spec=LocalRAG)
        _LocalRAGSingleton._instance = mock_instance

        # Reset
        _LocalRAGSingleton.reset_instance()

        assert _LocalRAGSingleton._instance is None


class TestLocalRAGFileOperations:
    """Tests for file-based operations."""

    @pytest.fixture
    def mock_rag(self):
        """Create a LocalRAG instance with mocked dependencies."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = True
        rag.collection = MagicMock()
        return rag

    def test_add_code_file_not_exists(self, mock_rag):
        """Test add_code_file returns False for non-existent file."""
        result = mock_rag.add_code_file("/nonexistent/file.py")
        assert result is False

    def test_add_code_file_success(self, mock_rag):
        """Test add_code_file successfully indexes a file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def hello(): pass")
            temp_path = f.name

        try:
            with patch.object(mock_rag, 'add_document', return_value=True) as mock_add:
                result = mock_rag.add_code_file(temp_path)

                assert result is True
                mock_add.assert_called_once()
                call_args = mock_add.call_args
                assert "def hello(): pass" in call_args[0][1]  # content
                assert call_args[0][2]['type'] == 'code'  # metadata
        finally:
            os.unlink(temp_path)

    def test_index_directory_not_exists(self, mock_rag):
        """Test index_directory returns 0 for non-existent directory."""
        result = mock_rag.index_directory("/nonexistent/directory")
        assert result == 0

    def test_index_directory_excludes_patterns(self, mock_rag):
        """Test index_directory respects exclude patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file in excluded directory
            pycache = Path(tmpdir) / "__pycache__"
            pycache.mkdir()
            (pycache / "test.py").write_text("excluded")

            # Create a normal file
            (Path(tmpdir) / "main.py").write_text("included")

            with patch.object(mock_rag, 'add_code_file', return_value=True) as mock_add:
                result = mock_rag.index_directory(tmpdir)

                # Should only index main.py, not __pycache__/test.py
                assert result == 1
                assert mock_add.call_count == 1


class TestLocalRAGClear:
    """Tests for collection clearing."""

    def test_clear_when_available(self):
        """Test clear deletes and recreates collection."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = True
        rag.client = MagicMock()
        rag.embedding_fn = MagicMock()
        rag.collection = MagicMock()

        with patch.object(rag, 'is_available', return_value=True):
            rag.clear()

            rag.client.delete_collection.assert_called_once_with("ybis_knowledge")
            rag.client.get_or_create_collection.assert_called_once()

    def test_clear_when_not_available(self):
        """Test clear does nothing when not available."""
        rag = LocalRAG.__new__(LocalRAG)
        rag._initialized = False
        rag.client = MagicMock()

        with patch.object(rag, 'is_available', return_value=False):
            rag.clear()

            rag.client.delete_collection.assert_not_called()
