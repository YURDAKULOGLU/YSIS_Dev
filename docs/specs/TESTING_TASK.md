# TESTING INFRASTRUCTURE TASK

## Objective
Establish comprehensive testing infrastructure with proper coverage tracking, fixture management, mocking utilities, and CI integration.

## Current State
- **Test Directory:** `tests/` exists with ~40 test files
- **Coverage Config:** Basic (branch=true, source=src,cli)
- **Fixtures:** Only conftest.py with playwright/testcontainers detection
- **Mocking:** Ad-hoc, no shared utilities
- **CI Integration:** None configured
- **Test Categories:** unit/, integration/, e2e/ directories exist but sparse

---

## CRITICAL PRIORITY

### 1. Enhanced pytest Configuration

**Location:** Update `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = """
    -v
    --tb=short
    --strict-markers
    --strict-config
    -ra
"""
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
markers = [
    "unit: Fast isolated unit tests",
    "integration: Tests requiring external services",
    "e2e: End-to-end workflow tests",
    "slow: Tests taking > 5 seconds",
    "smoke: Quick sanity checks",
    "llm: Tests requiring LLM API (expensive)",
    "database: Tests requiring database",
    "vector_store: Tests requiring vector store",
]
filterwarnings = [
    "ignore::DeprecationWarning:httpx._models",
    "ignore::UserWarning:pydantic.main",
    "ignore::DeprecationWarning:litellm",
]

[tool.coverage.run]
branch = true
source = ["src/ybis"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/migrations/*",
]
parallel = true
concurrency = ["thread", "greenlet"]

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 60
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

---

### 2. Comprehensive conftest.py

**Location:** `tests/conftest.py`

```python
"""Pytest Configuration and Shared Fixtures.

Provides:
- Mock fixtures for LLM, database, vector store
- Temporary directory fixtures
- Test data factories
- Async test support
"""
from __future__ import annotations

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

    with patch("ybis.control_plane.db", mock):
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
    """Mock litellm.acompletion.

    Yields:
        Mocked litellm module
    """
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=mock_llm_response))
    ]

    async_mock = AsyncMock(return_value=mock_response)

    with patch("litellm.acompletion", async_mock) as mock:
        yield mock


@pytest.fixture
def mock_llm_empty() -> Generator[MagicMock, None, None]:
    """Mock litellm with empty response.

    Yields:
        Mocked litellm returning empty
    """
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=""))]

    async_mock = AsyncMock(return_value=mock_response)

    with patch("litellm.acompletion", async_mock) as mock:
        yield mock


@pytest.fixture
def mock_llm_error() -> Generator[MagicMock, None, None]:
    """Mock litellm with API error.

    Yields:
        Mocked litellm that raises
    """
    async_mock = AsyncMock(side_effect=Exception("API rate limit exceeded"))

    with patch("litellm.acompletion", async_mock) as mock:
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

    with patch("ybis.data_plane.vector_store.VectorStore", return_value=mock):
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
) -> Generator[MagicMock, None, None]:
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
```

---

### 3. Unit Test Templates

**Location:** `tests/unit/` directory

#### `tests/unit/test_local_coder.py`

```python
"""Unit tests for LocalCoder adapter."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestLocalCoder:
    """Tests for LocalCoder class."""

    @pytest.fixture
    def coder(self):
        """Create LocalCoder instance."""
        from ybis.adapters.local_coder import LocalCoder

        return LocalCoder(model="gpt-4o-mini")

    @pytest.mark.asyncio
    async def test_edit_file_success(
        self,
        coder,
        sample_python_file: Path,
        mock_litellm: MagicMock,
        mock_run_context: MagicMock,
    ):
        """Test successful file edit."""
        mock_litellm.return_value.choices[0].message.content = '''
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b
'''

        result = await coder.edit_file(
            ctx=mock_run_context,
            file_path=sample_python_file,
            instruction="Add docstring with Args and Returns",
        )

        assert result.success
        assert "Args:" in sample_python_file.read_text()

    @pytest.mark.asyncio
    async def test_edit_file_empty_response(
        self,
        coder,
        sample_python_file: Path,
        mock_llm_empty: MagicMock,
        mock_run_context: MagicMock,
    ):
        """Test handling of empty LLM response."""
        original_content = sample_python_file.read_text()

        result = await coder.edit_file(
            ctx=mock_run_context,
            file_path=sample_python_file,
            instruction="Do something",
        )

        # Should not modify file on empty response
        assert sample_python_file.read_text() == original_content
        assert not result.success

    @pytest.mark.asyncio
    async def test_edit_file_size_validation(
        self,
        coder,
        sample_python_file: Path,
        mock_litellm: MagicMock,
        mock_run_context: MagicMock,
    ):
        """Test size ratio validation."""
        # Return very short content (should be rejected)
        mock_litellm.return_value.choices[0].message.content = "x = 1"

        original_content = sample_python_file.read_text()

        result = await coder.edit_file(
            ctx=mock_run_context,
            file_path=sample_python_file,
            instruction="Rewrite completely",
        )

        # Should reject due to size ratio
        assert sample_python_file.read_text() == original_content

    @pytest.mark.asyncio
    async def test_edit_protected_file(
        self,
        coder,
        tmp_workspace: Path,
        mock_run_context: MagicMock,
    ):
        """Test that protected files are skipped."""
        protected_file = tmp_workspace / "pyproject.toml"
        protected_file.write_text("[project]\nname = 'test'")

        result = await coder.edit_file(
            ctx=mock_run_context,
            file_path=protected_file,
            instruction="Change name",
        )

        assert not result.success
        assert "protected" in result.message.lower()


class TestLocalCoderValidation:
    """Tests for LocalCoder validation logic."""

    def test_content_similarity_check(self):
        """Test content similarity validation."""
        from ybis.adapters.local_coder import _check_content_similarity

        original = "def foo():\n    return 1\n"
        similar = "def foo():\n    return 2\n"
        different = "class Bar:\n    pass\n"

        assert _check_content_similarity(original, similar) > 0.5
        assert _check_content_similarity(original, different) < 0.5

    def test_size_ratio_validation(self):
        """Test size ratio validation."""
        from ybis.adapters.local_coder import _validate_size_ratio

        # Normal edit
        assert _validate_size_ratio(100, 120)  # 20% increase
        assert _validate_size_ratio(100, 80)  # 20% decrease

        # Suspicious edit
        assert not _validate_size_ratio(1000, 50)  # 95% decrease
        assert not _validate_size_ratio(100, 10000)  # 100x increase
```

#### `tests/unit/test_planner.py`

```python
"""Unit tests for Planner."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestPlanner:
    """Tests for Planner class."""

    @pytest.fixture
    def planner(self, mock_vector_store: MagicMock):
        """Create Planner instance."""
        from ybis.orchestrator.planner import Planner

        return Planner()

    @pytest.mark.asyncio
    async def test_create_plan_with_files(
        self,
        planner,
        mock_litellm: MagicMock,
        mock_run_context: MagicMock,
    ):
        """Test plan creation with file list."""
        mock_litellm.return_value.choices[0].message.content = '''
{
    "files": ["src/sample.py"],
    "steps": [
        {"action": "read", "file": "src/sample.py"},
        {"action": "edit", "file": "src/sample.py", "instruction": "Fix bug"}
    ]
}
'''

        plan = await planner.create_plan(
            ctx=mock_run_context,
            objective="Fix the calculation bug",
        )

        assert "files" in plan
        assert len(plan["files"]) > 0

    @pytest.mark.asyncio
    async def test_create_plan_fallback_on_error(
        self,
        planner,
        mock_llm_error: MagicMock,
        mock_run_context: MagicMock,
    ):
        """Test fallback when LLM fails."""
        plan = await planner.create_plan(
            ctx=mock_run_context,
            objective="Do something",
        )

        # Should return heuristic plan
        assert "files" in plan
        assert plan.get("fallback", False)


class TestPlanValidation:
    """Tests for plan validation."""

    def test_validate_file_exists(self, tmp_workspace: Path):
        """Test file existence validation."""
        from ybis.orchestrator.planner import _validate_files

        # Create real file
        real_file = tmp_workspace / "src" / "real.py"
        real_file.parent.mkdir(parents=True, exist_ok=True)
        real_file.write_text("# real")

        plan = {
            "files": ["src/real.py", "src/fake.py"],
        }

        validated = _validate_files(plan, tmp_workspace)

        assert "src/real.py" in validated["files"]
        assert "src/fake.py" not in validated["files"]

    def test_validate_step_structure(self):
        """Test step structure validation."""
        from ybis.orchestrator.planner import _validate_steps

        valid_steps = [
            {"action": "read", "file": "a.py"},
            {"action": "edit", "file": "a.py", "instruction": "fix"},
        ]

        invalid_steps = [
            {"action": "read"},  # missing file
            {"action": "unknown", "file": "b.py"},  # unknown action
        ]

        assert _validate_steps(valid_steps) == valid_steps
        assert len(_validate_steps(invalid_steps)) == 0
```

---

### 4. Integration Test Templates

**Location:** `tests/integration/`

#### `tests/integration/test_workflow_execution.py`

```python
"""Integration tests for workflow execution."""
from __future__ import annotations

import pytest


@pytest.mark.integration
class TestWorkflowExecution:
    """Integration tests for full workflow."""

    @pytest.mark.asyncio
    async def test_simple_workflow_runs(
        self,
        tmp_workspace: Path,
        mock_litellm: MagicMock,
        mock_vector_store: MagicMock,
    ):
        """Test that simple workflow completes."""
        from ybis.orchestrator.graph import create_workflow

        workflow = create_workflow()

        # Create minimal task
        task = {
            "id": "INT-001",
            "objective": "Add a print statement",
        }

        # Run workflow
        result = await workflow.ainvoke({"task": task})

        assert result["status"] in ["completed", "verified"]

    @pytest.mark.asyncio
    async def test_workflow_with_verification(
        self,
        tmp_workspace: Path,
        sample_python_file: Path,
        sample_test_file: Path,
        mock_litellm: MagicMock,
    ):
        """Test workflow with test verification."""
        from ybis.orchestrator.graph import create_workflow

        workflow = create_workflow()

        task = {
            "id": "INT-002",
            "objective": "Fix calculate_sum to handle negative numbers",
        }

        result = await workflow.ainvoke({
            "task": task,
            "workspace": tmp_workspace,
        })

        assert "verification" in result
```

#### `tests/integration/test_database_operations.py`

```python
"""Integration tests for database operations."""
from __future__ import annotations

import sqlite3

import pytest


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseOperations:
    """Integration tests for database layer."""

    def test_task_crud_operations(self, tmp_database: Path):
        """Test task CRUD operations."""
        from ybis.control_plane.db import TaskDB

        db = TaskDB(tmp_database)

        # Create
        task_id = db.create_task("Test Task", "Do something")
        assert task_id is not None

        # Read
        task = db.get_task(task_id)
        assert task["title"] == "Test Task"

        # Update
        db.update_task_status(task_id, "completed")
        task = db.get_task(task_id)
        assert task["status"] == "completed"

        # List
        tasks = db.list_tasks()
        assert len(tasks) >= 1

    def test_run_tracking(self, tmp_database: Path):
        """Test run tracking operations."""
        from ybis.control_plane.db import TaskDB

        db = TaskDB(tmp_database)

        task_id = db.create_task("Test", "Objective")
        run_id = db.create_run(task_id)

        assert run_id is not None

        run = db.get_run(run_id)
        assert run["task_id"] == task_id
        assert run["status"] == "running"

    def test_error_pattern_recording(self, tmp_database: Path):
        """Test error pattern storage."""
        from ybis.services.error_knowledge_base import ErrorKnowledgeBase

        kb = ErrorKnowledgeBase(tmp_database)

        kb.record_error(
            error_type="ImportError",
            message="No module named 'foo'",
            task_id="TEST-001",
        )

        patterns = kb.get_patterns("ImportError")
        assert len(patterns) >= 1
```

---

### 5. E2E Test Templates

**Location:** `tests/e2e/`

#### `tests/e2e/test_full_self_improve.py`

```python
"""End-to-end tests for self-improvement workflow."""
from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.mark.e2e
@pytest.mark.slow
class TestSelfImproveE2E:
    """E2E tests for self-improvement system."""

    @pytest.fixture
    def e2e_workspace(self, tmp_path: Path) -> Path:
        """Create E2E test workspace."""
        workspace = tmp_path / "e2e_workspace"
        workspace.mkdir()

        # Create minimal project structure
        src = workspace / "src"
        src.mkdir()

        (src / "main.py").write_text('''
"""Main module with intentional issues."""

def greet(name):
    # Missing type hints
    # Missing docstring
    print("Hello " + name)  # Could use f-string

def calculate(x, y):
    return x + y  # No validation
''')

        (workspace / "tests").mkdir()
        (workspace / "tests" / "test_main.py").write_text('''
from src.main import greet, calculate

def test_greet(capsys):
    greet("World")
    captured = capsys.readouterr()
    assert "Hello World" in captured.out

def test_calculate():
    assert calculate(2, 3) == 5
''')

        return workspace

    @pytest.mark.asyncio
    async def test_self_improve_identifies_issues(
        self,
        e2e_workspace: Path,
        mock_litellm: MagicMock,
    ):
        """Test that self-improve identifies code issues."""
        from ybis.orchestrator.self_improve import SelfImprover

        improver = SelfImprover()

        # Reflection phase
        issues = await improver.reflect(e2e_workspace)

        assert len(issues) > 0
        assert any("type hint" in str(i).lower() for i in issues)

    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not os.getenv("RUN_EXPENSIVE_E2E"),
        reason="Expensive E2E test",
    )
    async def test_full_self_improve_cycle(self, e2e_workspace: Path):
        """Test complete self-improvement cycle."""
        from ybis.orchestrator.self_improve import SelfImprover

        improver = SelfImprover()

        result = await improver.run_cycle(
            workspace=e2e_workspace,
            max_iterations=1,
        )

        assert result["completed"]
        assert result["improvements_made"] >= 0
```

---

## HIGH PRIORITY

### 6. Test Utilities Module

**Location:** `tests/utils/test_helpers.py` (NEW FILE)

```python
"""Test helper utilities."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock


def create_mock_llm_response(content: str) -> MagicMock:
    """Create mock LLM response.

    Args:
        content: Response content

    Returns:
        Mocked response object
    """
    mock = MagicMock()
    mock.choices = [MagicMock(message=MagicMock(content=content))]
    return mock


def create_mock_plan(
    files: list[str] | None = None,
    steps: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create mock plan.

    Args:
        files: List of files
        steps: List of steps

    Returns:
        Plan dictionary
    """
    return {
        "files": files or ["src/main.py"],
        "steps": steps
        or [
            {"action": "read", "file": "src/main.py"},
            {"action": "edit", "file": "src/main.py", "instruction": "Fix bug"},
        ],
    }


def load_fixture(name: str) -> dict[str, Any]:
    """Load JSON fixture.

    Args:
        name: Fixture name (without extension)

    Returns:
        Parsed fixture data
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / f"{name}.json"
    return json.loads(fixture_path.read_text())


def assert_journal_has_event(
    journal_path: Path,
    event_type: str,
    payload_contains: dict[str, Any] | None = None,
) -> None:
    """Assert journal contains event.

    Args:
        journal_path: Path to journal directory
        event_type: Expected event type
        payload_contains: Expected payload keys/values
    """
    events_file = journal_path / "events.jsonl"
    assert events_file.exists(), f"Journal file not found: {events_file}"

    events = [
        json.loads(line)
        for line in events_file.read_text().strip().split("\n")
        if line
    ]

    matching = [e for e in events if e.get("event_type") == event_type]
    assert matching, f"No events of type {event_type} found"

    if payload_contains:
        for key, value in payload_contains.items():
            assert any(
                e.get("payload", {}).get(key) == value for e in matching
            ), f"No event with {key}={value} found"
```

---

### 7. Test Fixtures Directory

**Location:** `tests/fixtures/`

```
tests/fixtures/
├── plans/
│   ├── simple_plan.json
│   └── complex_plan.json
├── tasks/
│   ├── bug_fix_task.json
│   └── feature_task.json
├── llm_responses/
│   ├── edit_response.txt
│   └── plan_response.json
└── code_samples/
    ├── python_with_issues.py
    └── python_clean.py
```

#### `tests/fixtures/plans/simple_plan.json`

```json
{
  "files": ["src/main.py"],
  "steps": [
    {
      "action": "read",
      "file": "src/main.py"
    },
    {
      "action": "edit",
      "file": "src/main.py",
      "instruction": "Add type hints to all functions"
    },
    {
      "action": "verify",
      "command": "pytest tests/"
    }
  ],
  "context": "Improve type safety"
}
```

#### `tests/fixtures/tasks/bug_fix_task.json`

```json
{
  "id": "BUG-001",
  "title": "Fix calculation error",
  "objective": "The calculate_sum function returns incorrect results for floating point numbers",
  "status": "pending",
  "priority": "high",
  "labels": ["bug", "math"]
}
```

---

### 8. Coverage Configuration Script

**Location:** `scripts/run_tests.py` (NEW FILE)

```python
#!/usr/bin/env python3
"""Test runner with coverage and reporting."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(
    category: str = "all",
    coverage: bool = True,
    verbose: bool = False,
    failfast: bool = False,
) -> int:
    """Run tests with specified options.

    Args:
        category: Test category (unit, integration, e2e, all)
        coverage: Enable coverage reporting
        verbose: Verbose output
        failfast: Stop on first failure

    Returns:
        Exit code
    """
    cmd = ["pytest"]

    # Category selection
    if category == "unit":
        cmd.extend(["tests/unit", "-m", "unit"])
    elif category == "integration":
        cmd.extend(["tests/integration", "-m", "integration"])
    elif category == "e2e":
        cmd.extend(["tests/e2e", "-m", "e2e"])
    else:
        cmd.append("tests/")

    # Options
    if verbose:
        cmd.append("-v")
    if failfast:
        cmd.append("-x")

    # Coverage
    if coverage:
        cmd.extend([
            "--cov=src/ybis",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=xml:coverage.xml",
            "--cov-fail-under=60",
        ])

    # Run
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    return result.returncode


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument(
        "category",
        nargs="?",
        default="all",
        choices=["unit", "integration", "e2e", "all"],
        help="Test category",
    )
    parser.add_argument("--no-coverage", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-x", "--failfast", action="store_true")

    args = parser.parse_args()

    sys.exit(
        run_tests(
            category=args.category,
            coverage=not args.no_coverage,
            verbose=args.verbose,
            failfast=args.failfast,
        )
    )


if __name__ == "__main__":
    main()
```

---

## MEDIUM PRIORITY

### 9. GitHub Actions CI Configuration

**Location:** `.github/workflows/test.yml`

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run unit tests
        run: |
          pytest tests/unit -v --cov=src/ybis --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
          fail_ci_if_error: false

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    env:
      RUN_INTEGRATION_TESTS: "1"

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run integration tests
        run: |
          pytest tests/integration -v --timeout=300

  lint:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install ruff mypy

      - name: Run ruff
        run: ruff check src/

      - name: Run mypy
        run: mypy src/ybis --ignore-missing-imports
```

---

### 10. Pre-commit Hooks

**Location:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest quick check
        entry: pytest tests/unit -x -q --no-cov
        language: system
        pass_filenames: false
        always_run: true
```

---

## Verification Checklist

```bash
# Run all tests with coverage
pytest tests/ --cov=src/ybis --cov-report=term-missing

# Run only unit tests
pytest tests/unit -m unit

# Run with verbose output
pytest tests/ -v --tb=long

# Generate HTML coverage report
pytest tests/ --cov=src/ybis --cov-report=html
open htmlcov/index.html

# Check coverage threshold
pytest tests/ --cov=src/ybis --cov-fail-under=60
```

---

## Success Criteria

- [ ] pytest runs without errors on fresh clone
- [ ] All fixtures work (tmp_workspace, mock_llm, etc.)
- [ ] Unit tests complete in < 30 seconds
- [ ] Coverage > 60% for src/ybis
- [ ] `pytest -m unit` runs only unit tests
- [ ] `pytest -m integration` runs only integration tests
- [ ] CI pipeline passes on GitHub Actions
- [ ] Pre-commit hooks catch lint errors

---

## Priority Order

1. **conftest.py** - Foundation for all tests
2. **pytest configuration** - Proper markers and settings
3. **Unit test templates** - Core coverage
4. **Test utilities** - Reusable helpers
5. **Integration tests** - Component interaction
6. **E2E tests** - Full system validation
7. **CI configuration** - Automated testing
8. **Pre-commit hooks** - Developer experience

---

## Test Categories Quick Reference

| Category | Command | When to Run |
|----------|---------|-------------|
| Unit | `pytest -m unit` | Every commit |
| Integration | `pytest -m integration` | Before merge |
| E2E | `pytest -m e2e` | Release candidate |
| Smoke | `pytest -m smoke` | Quick sanity check |
| All | `pytest` | CI pipeline |
