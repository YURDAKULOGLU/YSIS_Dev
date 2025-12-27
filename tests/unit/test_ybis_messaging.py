import types

from scripts.ybis import YBISCli


class _FakeTools:
    def __init__(self):
        self.calls = []

    def send_message(self, **kwargs):
        self.calls.append(("send_message", kwargs))
        return "OK"

    def read_inbox(self, **kwargs):
        self.calls.append(("read_inbox", kwargs))
        return '{"messages": []}'

    def ack_message(self, **kwargs):
        self.calls.append(("ack_message", kwargs))
        return "OK"


def test_start_debate_uses_mcp_send_message():
    cli = YBISCli()
    tools = _FakeTools()

    def _fake_loader():
        return tools

    cli._load_mcp_tools = _fake_loader

    cli.start_debate("Topic", "Proposal", "agent-1")

    assert tools.calls
    name, payload = tools.calls[0]
    assert name == "send_message"
    assert payload["to"] == "all"
    assert payload["subject"] == "Topic"
    assert payload["content"] == "Proposal"
    assert payload["from_agent"] == "agent-1"
    assert payload["message_type"] == "debate"
    assert payload["priority"] == "HIGH"
    assert payload["tags"] == "debate"


def test_send_message_uses_mcp_tools():
    cli = YBISCli()
    tools = _FakeTools()

    def _fake_loader():
        return tools

    cli._load_mcp_tools = _fake_loader

    cli.send_message(
        to="all",
        subject="Hello",
        content="World",
        from_agent="tester",
        message_type="broadcast",
        priority="NORMAL",
        reply_to=None,
        tags=None,
    )

    assert tools.calls
    name, payload = tools.calls[0]
    assert name == "send_message"
    assert payload["to"] == "all"
    assert payload["subject"] == "Hello"
    assert payload["content"] == "World"
    assert payload["from_agent"] == "tester"
    assert payload["message_type"] == "broadcast"
