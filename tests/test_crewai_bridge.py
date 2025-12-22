import sys
import os

# Add project root
sys.path.insert(0, os.getcwd())

def test_crewai_integration():
    print("🤖 Testing CrewAI Integration...")
    
    from src.agentic.bridges.crewai_bridge import CrewAIBridge
    
    try:
        # Use a smaller model for testing speed if available, else standard
        bridge = CrewAIBridge(model_name="qwen2.5-coder:32b")
        
        print("🚀 Kicking off Research Crew...")
        result = bridge.create_research_crew("Artificial General Intelligence")
        
        print(f"\n✅ Crew Result:\n{result}")
        print("✅ CrewAI Test PASSED.")
        
    except Exception as e:
        print(f"❌ CrewAI Test FAILED: {e}")

if __name__ == "__main__":
    test_crewai_integration()
