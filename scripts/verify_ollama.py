#!/usr/bin/env python3
"""
Verify Ollama Connection - Test LiteLLM can talk to Ollama.

DoD:
- Script runs and prints a response from Ollama
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def verify_ollama() -> None:
    """Verify Ollama connection."""
    try:
        import litellm

        print("Testing Ollama connection...")
        print(f"API Base: http://localhost:11434")
        print(f"Model: ollama/llama3.2:3b")
        print()

        response = litellm.completion(
            model="ollama/llama3.2:3b",
            messages=[{"role": "user", "content": "hi"}],
            api_base="http://localhost:11434",
        )

        result = response.choices[0].message.content
        print("[OK] Ollama connection successful!")
        print(f"Response: {result}")

    except ImportError:
        print("[ERROR] LiteLLM not installed")
        print("Install with: pip install litellm")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Ollama connection failed: {e}")
        print("\nMake sure:")
        print("  1. Ollama is running: ollama serve")
        print("  2. Model is available: ollama pull llama3.2:3b")
        sys.exit(1)


if __name__ == "__main__":
    verify_ollama()

