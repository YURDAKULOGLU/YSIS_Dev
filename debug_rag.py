import chromadb
from chromadb.config import Settings
import os
import shutil

# NEW STANDARD PATH
DB_PATH = os.path.join(os.getcwd(), "Knowledge", "LocalDB", "chroma_db")

def test_chroma():
    print(f"🧹 Cleaning up {DB_PATH}...")
    if os.path.exists(DB_PATH):
        try:
            shutil.rmtree(DB_PATH)
            print("✅ Cleaned.")
        except Exception as e:
            print(f"❌ Failed to clean: {e}")
            # Try to force remove files inside
            # On Windows, sometimes file locks prevent rmtree
            pass

    print(f"🧪 Initializing ChromaDB at {DB_PATH}...")
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        client = chromadb.PersistentClient(path=DB_PATH)
        print("✅ Client initialized.")
        
        print("🧪 Creating collection...")
        collection = client.get_or_create_collection(name="test_collection")
        print("✅ Collection created.")
        
        print("🧪 Adding data...")
        collection.add(
            documents=["This is a test document"],
            metadatas=[{"source": "test"}],
            ids=["id1"]
        )
        print("✅ Data added.")
        
        print("🎉 ChromaDB is WORKING at Standard Path!")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chroma()