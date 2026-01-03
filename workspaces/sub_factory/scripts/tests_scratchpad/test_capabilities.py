import sys
import os
import requests
import json
from pathlib import Path

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir)) # .YBIS_Dev/..
sys.path.append(os.path.join(project_root, ".YBIS_Dev"))

from Agentic.Tools.sandbox_manager import sandbox
from Agentic.inference.router import router, TaskType

def test_sandbox():
    print("\n--- Testing Sandbox ---")
    try:
        msg = sandbox.setup()
        print(f"[SUCCESS] Setup: {msg}")

        test_file = "src/test_file.txt"
        abs_path = sandbox.get_path(test_file)

        # Ensure dir exists in sandbox
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        with open(abs_path, "w") as f:
            f.write("Hello from Sandbox Test")

        print(f"[SUCCESS] Write: Successfully wrote to {abs_path}")

        if os.path.exists(abs_path) and not os.path.exists(os.path.join(project_root, test_file)):
            print("[SUCCESS] Isolation: File exists in sandbox but NOT in real project.")
        else:
            print("[ERROR] Isolation: FAILED! File might have leaked.")

    except Exception as e:
        print(f"[ERROR] Sandbox Error: {e}")

def test_ollama():
    print("\n--- Testing Local LLM (Ollama) ---")

    # 1. Check if Ollama is running
    ollama_url = router.config.ollama_host.replace("/v1", "")
    try:
        resp = requests.get(ollama_url)
        if resp.status_code == 200:
            print("[SUCCESS] Ollama Server: Online")
        else:
            print(f"⚠️ Ollama Server: Online but returned {resp.status_code}")
    except:
        print("[ERROR] Ollama Server: OFFLINE (Is 'ollama serve' running?)")
        return

    # 2. Check routing logic
    model_str, decision = router.route(TaskType.CODE_GENERATION, force_local=True)
    print(f"[SUCCESS] Routing: Selected '{model_str}' ({decision.reason})")

    # 3. Try generation (Real Test)
    model_name = decision.model
    print(f"⏳ Generating with {model_name}... (This might take a moment)")

    payload = {
        "model": model_name,
        "prompt": "Write a python function that prints 'Hello YBIS'. Only code.",
        "stream": False
    }

    try:
        # Note: router returns 'ollama:model', we need just 'model' for API
        # Or use OpenAI compatible endpoint if configured
        api_url = f"{ollama_url}/api/generate"
        resp = requests.post(api_url, json=payload)

        if resp.status_code == 200:
            result = resp.json().get("response", "")
            print(f"[SUCCESS] Generation Success:\n---\n{result.strip()[:100]}...\n---")
        else:
            print(f"[ERROR] Generation Failed: {resp.text}")
            # Fallback: Check installed models
            tags_resp = requests.get(f"{ollama_url}/api/tags")
            if tags_resp.status_code == 200:
                models = [m['name'] for m in tags_resp.json()['models']]
                print(f"ℹ️ Installed Models: {models}")
                print(f"⚠️ Configured model '{model_name}' might be missing.")

    except Exception as e:
        print(f"[ERROR] Generation Error: {e}")

if __name__ == "__main__":
    test_sandbox()
    test_ollama()
