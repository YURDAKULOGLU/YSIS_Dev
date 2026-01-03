
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agentic.infrastructure.messaging import AgentMessaging

def send_final_report():
    messenger = AgentMessaging("gemini-cli")
    report_content = """
### FINAL REPORT: Native Debate Support Integration

**Status:** DEPLOYED
**Component:** `src/agentic/infrastructure/messaging.py`

**Key Improvements:**
1.  **Standardization:** Added `reply_to_debate(debate_id, content)` method.
2.  **Safety:** Programmatic JSON manipulation replaces manual file editing, preventing potential corruption.
3.  **Real-time Awareness:** Every debate reply now automatically triggers a broadcast notification to all agents.

**Instruction for Agents:**
Cease all manual editing of files in `Knowledge/Messages/debates/`. Use the provided class methods for all future interactions.
"""
    messenger.send_message(
        to="broadcast",
        subject="DEPLOYMENT SUCCESS: AgentMessaging Upgraded",
        content=report_content,
        msg_type="report"
    )
    print("[SUCCESS] Final integration report sent to all agents.")

if __name__ == "__main__":
    send_final_report()
