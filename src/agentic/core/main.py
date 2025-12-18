import os
import sys
import time
import json
import glob
import re
from datetime import datetime
from pathlib import Path

# --- CONFIGURATION ---
WORKFORCE_ROOT = Path("/app/.YBIS_Dev/20_WORKFORCE/01_Python_Core")
MEMORY_ROOT = Path("/app/.YBIS_Dev/40_KNOWLEDGE_BASE/Memory")
# SYSTEM_ROADMAP is inside .YBIS_Dev, mapped to /app/.YBIS_Dev
STRATEGY_DIR = Path("/app/.YBIS_Dev/10_META/Strategy") 
INBOX_DIR = MEMORY_ROOT / "Inbox"
OUTBOX_DIR = MEMORY_ROOT / "Outbox"
LOGS_DIR = MEMORY_ROOT / "logs"

def setup_directories():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def log_message(message, level="INFO"):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    try:
        with open(LOGS_DIR / "agent_core.log", "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except:
        pass

def read_system_roadmap():
    """Reads the SYSTEM_ROADMAP.md to find internal YBIS Dev tasks."""
    roadmap_path = STRATEGY_DIR / "SYSTEM_ROADMAP.md"
    
    if not roadmap_path.exists():
        log_message(f"System Roadmap not found at {roadmap_path}", "ERROR")
        return None

    try:
        with open(roadmap_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            # Look for pending tasks: "- [ ] Sxxx Description"
            # Regex: - [ ] (S\d+) (.+)
            if line.startswith("- [ ]") and "S" in line:
                match = re.search(r'- \[ \] (S\d+)\s+(.+)', line)
                if match:
                    return {"id": match.group(1), "description": match.group(2).strip()}
        
        return None
    except Exception as e:
        log_message(f"Failed to read system roadmap: {e}", "ERROR")
        return None

def delegate_task(task_info):
    new_task_id = f"task_spec_for_{task_info['id']}"
    filename = f"{new_task_id}.json"
    
    # Enhanced Instruction
    instruction = (
        f"You are a Senior Systems Architect. Your goal is to write a comprehensive Technical Specification for task '{task_info['id']}: {task_info['description']}'.\n\n"
        f"**MANDATORY STEPS:**\n"
        f"1. **READ THE TEMPLATE:** Use `read_file` to read `.YBIS_Dev/40_KNOWLEDGE_BASE/Templates/spec-template.md`.\n"
        f"2. **ANALYZE:** Understand the requirements for a Performance Monitor script (Python) that calculates processing time from Inbox/Outbox timestamps.\n"
        f"3. **WRITE SPEC:** Create `.YBIS_Dev/40_KNOWLEDGE_BASE/Specs_Draft/SPEC_{task_info['id']}.md` using `write_file`.\n\n"
        f"**CONTENT REQUIREMENTS:**\n"
        f"- Follow the Template structure EXACTLY.\n"
        f"- **Detailed Design:** Class/Function definitions, Data structures (JSON schemas).\n"
        f"- **Configuration:** How to set paths via Env Vars or Args.\n"
        f"- **Error Handling:** How to handle missing files, corrupt JSON, locked files.\n"
        f"- **Logging:** Standard logging format.\n"
        f"- **Testing:** Unit test cases and integration test scenarios.\n\n"
        f"Make it professional, detailed, and ready for a Junior Developer to implement without asking questions."
    )
    
    task_data = {
        "id": new_task_id,
        "type": "execution_request",
        "instruction": instruction,
        "target_agent": "Node_Agent_v1"
    }
    
    with open(INBOX_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=2)
    
    log_message(f"👨‍💼 DELEGATED: Created detailed task {filename} for {task_info['id']}")

def process_task(task_file):
    try:
        log_message(f"Processing task: {task_file.name}")
        with open(task_file, "r", encoding="utf-8") as f:
            task_data = json.load(f)
        
        task_type = task_data.get("type", "generic")
        result_msg = ""
        
        if task_type == "orchestrate_system":
            log_message("🧠 Analyzing SYSTEM ROADMAP...")
            next_task = read_system_roadmap()
            
            if next_task:
                log_message(f"🎯 Found Pending System Task: {next_task['id']}")
                delegate_task(next_task)
                result_msg = f"Delegated {next_task['id']}"
            else:
                result_msg = "No pending system tasks found."
                log_message("✅ All system tasks seem complete.")
        
        result_file = OUTBOX_DIR / f"result_{task_file.name}"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump({"status": "COMPLETED", "result": result_msg}, f, indent=2)
            
        task_file.rename(task_file.with_suffix(".json.done"))

    except Exception as e:
        log_message(f"Error processing {task_file.name}: {e}", "ERROR")
        task_file.rename(task_file.with_suffix(".json.error"))

def main_loop():
    setup_directories()
    log_message("🚀 YBIS Orchestrator (Python) is ONLINE.")
    while True:
        task_files = list(INBOX_DIR.glob("trigger_*.json"))
        if task_files:
            for task_file in task_files:
                process_task(task_file)
        else:
            time.sleep(2)

if __name__ == "__main__":
    main_loop()
