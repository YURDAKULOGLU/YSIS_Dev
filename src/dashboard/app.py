from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Path fix: src/dashboard/app.py -> src/dashboard -> src -> ROOT -> Knowledge/LocalDB
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up 2 levels to reach root
    project_root = os.path.dirname(os.path.dirname(base_dir))
    json_path = os.path.join(project_root, 'Knowledge', 'LocalDB', 'tasks.json')
    
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
