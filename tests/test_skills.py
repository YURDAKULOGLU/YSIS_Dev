import sys
import os
import shutil

# Add project root
sys.path.insert(0, os.getcwd())

def test_spec_writer_skill():
    print("[INFO] Testing Skill: Spec Writer...")

    from src.agentic.skills.spec_writer import generate_spec, SpecWriterInput

    input_data = SpecWriterInput(
        project_name="Test Shop",
        description="A simple e-commerce site for testing skills.",
        tech_stack="Python, React"
    )

    result = generate_spec(input_data)
    print(f"   Result: {result}")

    # Verify files
    if os.path.exists("specs/test_shop/ARCHITECTURE.md"):
        print("[OK] Spec Kit Files Generated.")
        # Cleanup
        shutil.rmtree("specs/test_shop")
    else:
        print("[ERROR] Spec Kit Generation FAILED.")

if __name__ == "__main__":
    test_spec_writer_skill()
