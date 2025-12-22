import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def list_models():
    print(f"Checking Ollama at: {OLLAMA_URL}")
    try:
        # Remove /v1 if present for the tags endpoint
        base_url = OLLAMA_URL.replace("/v1", "")
        response = requests.get(f"{base_url}/api/tags")
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Found {len(models)} models:")
            for m in models:
                print(f"   - {m['name']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    list_models()