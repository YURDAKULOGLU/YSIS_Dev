import sys
import types

import pytest

from src.agentic import mcp_server


@pytest.fixture
def fake_cognee(monkeypatch):
    store = {"added": [], "search": []}

    async def add(data):
        store["added"].append(data)

    async def cognify():
        return None

    async def search(query, limit=5):
        store["search"].append((query, limit))
        return [f"found:{query}"]

    fake = types.SimpleNamespace(add=add, cognify=cognify, search=search)
    monkeypatch.setitem(sys.modules, "cognee", fake)
    monkeypatch.setattr(mcp_server, "send_message", lambda **kwargs: "OK")
    return store


def test_add_to_memory_uses_cognee(fake_cognee):
    result = mcp_server.add_to_memory("hello memory", agent_id="tester")
    assert "SUCCESS" in result
    assert fake_cognee["added"] == ["hello memory"]


def test_search_memory_uses_cognee(fake_cognee):
    result = mcp_server.search_memory("memory query", agent_id="tester", limit=3)
    assert "MEMORY SEARCH RESULTS" in result
    assert fake_cognee["search"] == [("memory query", 3)]
