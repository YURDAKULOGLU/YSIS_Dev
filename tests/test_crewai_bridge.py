import sys
import os
import warnings
import requests
import re

# Add project root
sys.path.insert(0, os.getcwd())


def _pick_light_model(base_url: str) -> str:
    try:
        resp = requests.get(f"{base_url.rstrip('/')}/v1/models", timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        raise AssertionError(f"Ollama not reachable at {base_url}: {exc}") from exc

    data = resp.json()
    models = [m.get("id") for m in data.get("data", []) if m.get("id")]
    if not models:
        raise AssertionError("No Ollama models available via /v1/models.")

    preferred = ["3b", "7b", "8b", "14b", "latest"]
    scored = []
    for name in models:
        size_match = re.search(r":(\\d+)b", name)
        if size_match:
            size = int(size_match.group(1))
            scored.append((size, name))
            continue
        if name.endswith(":latest"):
            scored.append((100, name))
            continue
        scored.append((999, name))
    scored.sort(key=lambda item: item[0])

    for _, name in scored:
        for token in preferred:
            if token in name:
                return name
    return scored[0][1]


def test_crewai_integration():
    warnings.filterwarnings("ignore")
    os.environ.setdefault("CREWAI_TESTING", "true")
    os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")
    os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
    os.environ.setdefault("CREWAI_DISABLE_TRACKING", "true")
    from crewai.crew import Crew
    from crewai.events.utils.console_formatter import ConsoleFormatter
    from crewai.events import crewai_event_bus
    from src.agentic.bridges.crewai_bridge import CrewAIBridge

    def _suppress_tracing_message(self) -> None:
        return None

    Crew._show_tracing_disabled_message = _suppress_tracing_message
    ConsoleFormatter._show_tracing_disabled_message_if_needed = _suppress_tracing_message
    crewai_event_bus.emit = lambda *args, **kwargs: None

    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name = os.getenv("YBIS_CREWAI_TEST_MODEL") or _pick_light_model(base_url)

    bridge = CrewAIBridge(model_name=model_name)
    result = bridge.create_research_crew("Artificial General Intelligence")
    assert isinstance(result, str) and result.strip()
