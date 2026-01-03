from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any, Callable, Coroutine, Optional

from src.agentic.core.config import PROJECT_ROOT
from src.agentic.core.utils.logging_utils import log_event

PoetiqSolver = Callable[
    [list[list[list[int]]], list[list[list[int]]], list[list[list[int]]], Optional[str]],
    Coroutine[Any, Any, list[dict[str, Any]]],
]


class PoetiqAdapter:
    """
    Spine adapter for the Poetiq ARC-AGI solver.

    The adapter isolates all external imports and exposes a stable interface
    for orchestrator strategies. Do not import Poetiq directly from core code.
    """

    def __init__(self, tools_root: Optional[Path] = None) -> None:
        self.tools_root = tools_root or PROJECT_ROOT / "tools" / "poetiq-arc-agi-solver"
        self._solver: Optional[PoetiqSolver] = None
        self._component = "poetiq_adapter"

    def is_available(self) -> bool:
        return self.tools_root.exists()

    def _import_solver(self) -> PoetiqSolver:
        if not self.tools_root.exists():
            raise RuntimeError(f"Poetiq tool root not found: {self.tools_root}")

        tool_path = str(self.tools_root)
        if tool_path not in sys.path:
            sys.path.insert(0, tool_path)

        try:
            from arc_agi.solve import solve as poetiq_solve  # type: ignore
        except Exception as exc:  # pragma: no cover - import failures depend on env
            raise RuntimeError(f"Failed to import Poetiq solver: {exc}") from exc

        return poetiq_solve

    def _get_solver(self) -> PoetiqSolver:
        if self._solver is None:
            self._solver = self._import_solver()
        return self._solver

    async def solve_async(
        self,
        train_in: list[list[list[int]]],
        train_out: list[list[list[int]]],
        test_in: list[list[list[int]]],
        problem_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        if not self.is_available():
            raise RuntimeError("Poetiq adapter not available; tools root missing")

        log_event(
            f"Solving ARC task via Poetiq adapter (problem_id={problem_id})",
            component=self._component,
        )
        solver = self._get_solver()
        results = await solver(train_in, train_out, test_in, problem_id=problem_id)
        log_event(
            f"Poetiq solve completed with {len(results)} candidates",
            component=self._component,
            level="success",
        )
        return results

    def solve(
        self,
        train_in: list[list[list[int]]],
        train_out: list[list[list[int]]],
        test_in: list[list[list[int]]],
        problem_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            raise RuntimeError("PoetiqAdapter.solve() cannot run inside an event loop")

        return asyncio.run(self.solve_async(train_in, train_out, test_in, problem_id))
