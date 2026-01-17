"""Pytest Configuration and Shared Fixtures.

Provides:
- Mock fixtures for LLM, database, vector store
- Temporary directory fixtures
- Test data factories
- Async test support
"""

import os
import shutil
import sqlite3
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ============================================================================
# Environment Setup
# ============================================================================


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest environment."""
    # Set test environment
    os.environ["YBIS_ENV"] = "test"
    os.environ["YBIS_TEST_MODE"] = "1"

    # Disable external calls by default
    os.environ.setdefault("YBIS_MOCK_LLM", "1")
    os.environ.setdefault("YBIS_MOCK_VECTOR_STORE", "1")

    # Playwright/testcontainers auto-detection
    if os.getenv("PLAYWRIGHT_E2E") is None:
        try:
            import playwright  # noqa: F401

            os.environ["PLAYWRIGHT_E2E"] = "1"
        except ImportError:
            pass

    if os.getenv("TESTCONTAINERS_SMOKE") is None:
        try:
            import testcontainers  # noqa: F401

            os.environ["TESTCONTAINERS_SMOKE"] = "1"
        except ImportError:
            pass


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Auto-mark tests based on location and name."""
    for item in items:
        # Auto-mark based on directory
        if "/unit/" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "/e2e/" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)

        # Auto-mark slow tests
        if "slow" in item.name.lower():
            item.add_marker(pytest.mark.slow)

        # Auto-mark LLM tests
        if "llm" in item.name.lower() or "local_coder" in item.name.lower():
            item.add_marker(pytest.mark.llm)


# ============================================================================
# Path Fixtures
# ============================================================================


@pytest.fixture
def project_root() -> Path:
    """Return project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary workspace directory.

    Yields:
        Path to temporary workspace
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "src").mkdir()
    (workspace / "tests").mkdir()

    yield workspace

    # Cleanup
    shutil.rmtree(workspace, ignore_errors=True)


@pytest.fixture
def tmp_platform_data(tmp_path: Path) -> Generator[Path, None, None]:
    """Create temporary platform_data directory.

    Yields:
        Path to temporary platform_data
    """
    platform_data = tmp_path / "platform_data"
    platform_data.mkdir()
    (platform_data / "runs").mkdir()
    (platform_data / "cache").mkdir()

    yield platform_data


# ============================================================================
# Database Fixtures
# ============================================================================


@pytest.fixture
def tmp_database(tmp_path: Path) -> Generator[Path, None, None]:
    """Create temporary SQLite database.

    Yields:
        Path to database file
    """
    db_path = tmp_path / "test.db"

    # Create schema
    conn = sqlite3.connect(str(db_path))
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            task_id TEXT NOT NULL,
            status TEXT DEFAULT 'running',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        );

        CREATE TABLE IF NOT EXISTS error_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT NOT NULL,
            pattern TEXT,
            occurrence_count INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_type TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.close()

    yield db_path


@pytest.fixture
def mock_db(tmp_database: Path) -> Generator[MagicMock, None, None]:
    """Mock database module.

    Yields:
        Mocked database
    """
    mock = MagicMock()
    mock.db_path = tmp_database
    mock.get_task.return_value = {"id": "TEST-001", "status": "pending"}
    mock.get_run.return_value = {"id": "R-test", "status": "running"}

    with patch("src.ybis.control_plane.db", mock):
        yield mock


# ============================================================================
# LLM Fixtures
# ============================================================================


@pytest.fixture
def mock_llm_response() -> str:
    """Default mock LLM response."""
    return "def hello():\n    return 'Hello, World!'\n"


@pytest.fixture
def mock_litellm(mock_llm_response: str) -> Generator[MagicMock, None, None]:
    """Mock litellm.completion.

    Yields:
        Mocked litellm module
    """
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=mock_llm_response))
    ]

    with patch("litellm.completion", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_llm_empty() -> Generator[MagicMock, None, None]:
    """Mock litellm with empty response.

    Yields:
        Mocked litellm returning empty
    """
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=""))]

    with patch("litellm.completion", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_llm_error() -> Generator[MagicMock, None, None]:
    """Mock litellm with API error.

    Yields:
        Mocked litellm that raises
    """
    with patch("litellm.completion", side_effect=Exception("API rate limit exceeded")) as mock:
        yield mock


# ============================================================================
# Vector Store Fixtures
# ============================================================================


@pytest.fixture
def mock_vector_store() -> Generator[MagicMock, None, None]:
    """Mock vector store.

    Yields:
        Mocked vector store
    """
    mock = MagicMock()
    mock.query.return_value = [
        {"content": "Test document 1", "metadata": {"source": "test.py"}},
        {"content": "Test document 2", "metadata": {"source": "test2.py"}},
    ]
    mock.add.return_value = None
    mock.delete.return_value = None

    with patch("src.ybis.data_plane.vector_store.VectorStore", return_value=mock):
        yield mock


@pytest.fixture
def mock_chroma(tmp_path: Path) -> Generator[MagicMock, None, None]:
    """Mock ChromaDB.

    Yields:
        Mocked ChromaDB client
    """
    mock_collection = MagicMock()
    mock_collection.query.return_value = {
        "documents": [["doc1", "doc2"]],
        "metadatas": [[{"source": "a.py"}, {"source": "b.py"}]],
        "distances": [[0.1, 0.2]],
    }

    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection

    with patch("chromadb.PersistentClient", return_value=mock_client):
        yield mock_client


# ============================================================================
# Run Context Fixtures
# ============================================================================


@pytest.fixture
def mock_run_context(
    tmp_workspace: Path,
    tmp_platform_data: Path,
) -> Generator[Any, None, None]:
    """Create mock RunContext.

    Yields:
        Mocked RunContext
    """
    from dataclasses import dataclass

    @dataclass
    class MockRunContext:
        task_id: str = "TEST-001"
        run_id: str = "R-test-001"
        workspace_path: Path = tmp_workspace
        run_path: Path = tmp_platform_data / "runs" / "R-test-001"
        trace_id: str = "trace-test-001"
        project_root: Path = tmp_workspace

        def __post_init__(self) -> None:
            self.run_path.mkdir(parents=True, exist_ok=True)
            (self.run_path / "journal").mkdir(exist_ok=True)
            (self.run_path / "artifacts").mkdir(exist_ok=True)

    ctx = MockRunContext()
    ctx.__post_init__()

    yield ctx  # type: ignore


# ============================================================================
# Sample Data Fixtures
# ============================================================================


@pytest.fixture
def sample_python_file(tmp_workspace: Path) -> Path:
    """Create sample Python file.

    Returns:
        Path to sample file
    """
    file_path = tmp_workspace / "src" / "sample.py"
    file_path.write_text(
        '''"""Sample module."""

def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b


def calculate_product(a: int, b: int) -> int:
    """Calculate product of two numbers."""
    return a * b


class Calculator:
    """Simple calculator class."""

    def __init__(self) -> None:
        self.history: list[str] = []

    def add(self, a: int, b: int) -> int:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
''',
        encoding="utf-8",
    )
    return file_path


@pytest.fixture
def sample_test_file(tmp_workspace: Path) -> Path:
    """Create sample test file.

    Returns:
        Path to sample test
    """
    file_path = tmp_workspace / "tests" / "test_sample.py"
    file_path.write_text(
        '''"""Tests for sample module."""
import pytest
from src.sample import calculate_sum, calculate_product, Calculator


def test_calculate_sum():
    assert calculate_sum(2, 3) == 5


def test_calculate_product():
    assert calculate_product(4, 5) == 20


class TestCalculator:
    def test_add(self):
        calc = Calculator()
        assert calc.add(1, 2) == 3
        assert len(calc.history) == 1
''',
        encoding="utf-8",
    )
    return file_path


@pytest.fixture
def sample_plan() -> dict[str, Any]:
    """Create sample plan data."""
    return {
        "files": ["src/sample.py", "src/utils.py"],
        "steps": [
            {"action": "read", "file": "src/sample.py"},
            {"action": "edit", "file": "src/sample.py", "description": "Add docstring"},
            {"action": "verify", "command": "pytest tests/"},
        ],
        "context": "Fix documentation",
    }


@pytest.fixture
def sample_task() -> dict[str, Any]:
    """Create sample task data."""
    return {
        "id": "TEST-001",
        "title": "Fix calculation bug",
        "objective": "The calculate_sum function returns wrong result for negative numbers",
        "status": "pending",
    }


# ============================================================================
# Async Fixtures
# ============================================================================


@pytest.fixture
def event_loop_policy():
    """Use default event loop policy."""
    import asyncio

    return asyncio.DefaultEventLoopPolicy()


# ============================================================================
# Skip Markers
# ============================================================================


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests based on markers and environment."""
    # Skip LLM tests if mock is disabled and no API key
    if item.get_closest_marker("llm"):
        if os.getenv("YBIS_MOCK_LLM") != "1" and not os.getenv("OPENAI_API_KEY"):
            pytest.skip("LLM tests require API key or YBIS_MOCK_LLM=1")

    # Skip integration tests unless explicitly enabled
    if item.get_closest_marker("integration"):
        if not os.getenv("RUN_INTEGRATION_TESTS"):
            pytest.skip("Integration tests disabled (set RUN_INTEGRATION_TESTS=1)")

    # Skip E2E tests unless explicitly enabled
    if item.get_closest_marker("e2e"):
        if not os.getenv("RUN_E2E_TESTS"):
            pytest.skip("E2E tests disabled (set RUN_E2E_TESTS=1)")
