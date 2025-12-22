import sys
import os
from pathlib import Path

# --- PATH HACK (CRITICAL) ---
# Ensure project root is in sys.path so we can import 'src.agentic'
# Current file: src/dashboard/app.py
# Root is: ../../
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# -----------------------------

from flask import Flask, render_template
import json
from src.agentic.core.config import TASKS_DB_PATH

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # TASKS_DB_PATH is a Path object from config
        with open(TASKS_DB_PATH, 'r', encoding='utf-8') as file:
            tasks_data = json.load(file)
    except FileNotFoundError:
        # Fallback if file doesn't exist yet
        tasks_data = {"backlog": [], "in_progress": [], "done": []}
        
    return render_template('index.html', data=tasks_data)

if __name__ == '__main__':
    print(f"Starting Dashboard on port 5000...")
    print(f"Reading DB from: {TASKS_DB_PATH}")
    app.run(debug=True, port=5000)