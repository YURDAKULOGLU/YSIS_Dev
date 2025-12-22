import sys
import os
import shutil

# Add project root
sys.path.insert(0, os.getcwd())

def test_mem0_integration():
    print("🧠 Testing Mem0 Integration...")
    
    from src.agentic.bridges.mem0_bridge import Mem0Bridge
    
    # 1. Initialize
    try:
        memory = Mem0Bridge(user_id="test_user")
    except Exception as e:
        print(f"❌ Failed to initialize Mem0: {e}")
        return

    # 2. Add Memory
    print("📝 Adding memory: 'The user prefers Python over Java.'")
    memory.add("The user prefers Python over Java.", metadata={"category": "preference"})
    
    # 3. Search Memory
    print("🔍 Searching for 'programming preference'...")
    results = memory.search("programming preference")
    print(f"   Found: {results}")
    
    if any("Python" in r for r in results):
        print("✅ Mem0 Test PASSED: Memory retrieved successfully.")
    else:
        print("❌ Mem0 Test FAILED: Could not retrieve memory.")

if __name__ == "__main__":
    # Clean up old test db if needed, but Mem0 handles it well
    test_mem0_integration()
