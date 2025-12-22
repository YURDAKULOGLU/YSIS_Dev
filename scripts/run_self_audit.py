import sys
import os

# Add project root
sys.path.insert(0, os.getcwd())

from src.agentic.bridges.investigator_bridge import InvestigatorBridge

def main():
    print("🔮 PROJECT MIRROR: Starting Self-Audit...")
    print("Hardware: RTX 5090 detected (Beast Mode)")
    
    investigator = InvestigatorBridge(model_name="qwen2.5-coder:32b")
    
    report = investigator.run_audit(project_root=os.getcwd())
    
    print("\n" + "="*50)
    print("📊 FINAL SELF-AUDIT REPORT")
    print("="*50)
    print(report)
    
    # Save the report
    with open("SELF_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# YBIS SELF-AUDIT REPORT\n\n")
        f.write(str(report))
        
    print("\n✅ Report saved to SELF_AUDIT_REPORT.md")

if __name__ == "__main__":
    main()

