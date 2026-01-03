
import sys
import os
import redis
import chromadb
from chromadb.config import Settings

def print_header(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def verify_imports():
    print_header("1. Framework Import Check")
    modules = [
        "langgraph",
        "crewai",
        "pyautogen",  # Fixed: pyautogen is the package name
        "aider",
        "mcp",
        "pydantic"
    ]
    all_passed = True
    for mod in modules:
        try:
            __import__(mod)
            print(f"✅ Import: {mod:<15} [OK]")
        except ImportError as e:
            print(f"❌ Import: {mod:<15} [FAILED] - {e}")
            all_passed = False
    return all_passed

def verify_redis():
    print_header("2. Redis Connectivity (The Nervous System)")
    redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    print(f"Connecting to: {redis_url}")
    try:
        r = redis.from_url(redis_url)
        if r.ping():
            print("✅ Redis PING: [OK]")
            return True
    except Exception as e:
        print(f"❌ Redis Connection: [FAILED] - {e}")
        return False

def verify_chroma():
    print_header("3. ChromaDB Connectivity (The Memory)")
    host = os.environ.get("CHROMA_HOST", "chromadb")
    port = os.environ.get("CHROMA_PORT", "8000")
    print(f"Connecting to: {host}:{port}")
    try:
        client = chromadb.HttpClient(host=host, port=port)
        hb = client.heartbeat()
        print(f"✅ Chroma Heartbeat: [OK] ({hb}ns)")
        return True
    except Exception as e:
        print(f"❌ Chroma Connection: [FAILED] - {e}")
        return False

def verify_environment():
    print_header("4. Environment Context")
    print(f"Python: {sys.version.split()[0]}")
    print(f"CWD:    {os.getcwd()}")
    print(f"Content of /app/.YBIS_Dev:")
    try:
        print(os.listdir("/app/.YBIS_Dev"))
    except Exception as e:
        print(f"Error listing dir: {e}")

if __name__ == "__main__":
    print("🐶 DOG SCALES DOG - SYSTEM DIAGNOSTIC 🐶")

    imports = verify_imports()
    red = verify_redis()
    chroma = verify_chroma()
    verify_environment()

    if imports and red and chroma:
        print_header("RESULT: SYSTEM ONLINE 🟢")
        sys.exit(0)
    else:
        print_header("RESULT: SYSTEM FAILED 🔴")
        sys.exit(1)
