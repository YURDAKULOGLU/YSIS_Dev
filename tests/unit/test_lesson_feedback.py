
import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.intelligence.lesson_engine import LessonEngine

def test_lesson_injection():
    print("[INFO] Testing Lesson Feedback Loop...")
    
    # 1. Run engine to ensure AUTO_RULES.md exists
    print("   Step 1: Running Lesson Engine...")
    engine = LessonEngine()
    engine.generate_rules()
    
    # 2. Instantiate SimplePlanner
    print("   Step 2: Checking SimplePlanner prompt...")
    planner = SimplePlanner()
    
    # We call _read_constitution directly to see what's injected
    combined_constitution = planner._read_constitution()
    
    print("\n--- INJECTED CONSTITUTION SNIPPET ---")
    print(combined_constitution[:500] + "...") 
    
    # 3. Assertions
    success = False
    if "### AUTOMATED LESSONS & RULES:" in combined_constitution:
        print("\n[SUCCESS] Auto-rules header found in prompt.")
        if "Aider fails on glob patterns" in combined_constitution:
            print("[SUCCESS] Specific lesson found in prompt.")
            success = True

    if not success:
        raise AssertionError("Auto-rules were not injected correctly.")

    print("\n[OK] Test passed.")

if __name__ == "__main__":
    test_lesson_injection()
