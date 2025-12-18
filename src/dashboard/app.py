from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    from src.agentic.core.config import TASKS_DB_PATH

    json_path = TASKS_DB_PATH
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            tasks_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: DB not found at {json_path}")
        tasks_data = {"backlog": [], "in_progress": [], "done": []}
        
    return render_template('index.html', data=tasks_data)

if __name__ == '__main__':
    print("Starting YSIS Dashboard...")
    app.run(debug=True, port=5000)
