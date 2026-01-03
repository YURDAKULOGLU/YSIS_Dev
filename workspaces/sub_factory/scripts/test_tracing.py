
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agentic.core.llm.litellm_provider import get_provider
from src.agentic.core.observability.tracer import tracer

import asyncio
import os
import sys
import warnings
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Suppress everything noisy
warnings.filterwarnings("ignore", category=RuntimeWarning)
os.environ["LITELLM_LOG"] = "ERROR"

from src.agentic.core.llm.litellm_provider import get_provider
from src.agentic.core.observability.tracer import tracer

async def test_tracing():
    # Setup - suppress external logs
    import logging
    logging.getLogger("litellm").setLevel(logging.CRITICAL)

    provider = get_provider()

    # Execution
    try:
        response = await provider.generate(
            prompt="What is 2+2?",
            model="ollama/qwen2.5-coder:32b",
            use_caching=False
        )

        if "4" in response['content']:
            print(f"[OK] LLM Integration Validated.")
            print(f"[OK] Provider: {response['provider']}")
        else:
            print(f"[FAIL] Unexpected LLM response.")

    except Exception as e:
        print(f"[FAIL] Generation error: {e}")

    # Cleanup
    tracer.flush()

if __name__ == "__main__":
    asyncio.run(test_tracing())
