import pytest
from Agentic.Agents.developer import developer

def test_extract_json_clean():
    text = '{"key": "value"}'
    result = developer._extract_json(text)
    assert result == text

def test_extract_json_markdown():
    # Use triple quotes for multiline strings
    text = """```json
{"key": "value"}
```"""
    result = developer._extract_json(text)
    # The extraction logic strips whitespace, so we expect clean json
    assert '{"key": "value"}' in result

def test_extract_json_with_text_around():
    text = """Here is the code:
```json
{"key": "value"}
```
Hope it helps."""
    result = developer._extract_json(text)
    assert '{"key": "value"}' in result

def test_extract_json_agent_repr():
    # Simulate AgentRunResult string representation
    # Double escaping backslashes for python string literal
    text = "AgentRunResult(output='```json\n{\n  \"file_path\": \"test.ts\"\n}\n```')"
    result = developer._extract_json(text)
    assert '"file_path": "test.ts"' in result