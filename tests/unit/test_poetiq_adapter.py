import asyncio
from pathlib import Path

import pytest

from src.agentic.core.adapters.poetiq_adapter import PoetiqAdapter


def test_adapter_missing_tools_root_raises(tmp_path: Path) -> None:
    adapter = PoetiqAdapter(tools_root=tmp_path / "missing")

    with pytest.raises(RuntimeError, match="tools root missing"):
        asyncio.run(adapter.solve_async([], [], []))


def test_adapter_uses_injected_solver(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    adapter = PoetiqAdapter(tools_root=tmp_path)

    async def _fake_solver(train_in, train_out, test_in, problem_id=None):
        return [{"results": test_in, "problem_id": problem_id}]

    monkeypatch.setattr(adapter, "_get_solver", lambda: _fake_solver)

    result = asyncio.run(adapter.solve_async([[[]]], [[[]]], [[[]]], problem_id="demo"))

    assert isinstance(result, list)
    assert result[0]["problem_id"] == "demo"
