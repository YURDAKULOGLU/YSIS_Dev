from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('tasks.json', 'r') as file:
        tasks_data = json.load(file)
    return render_template('index.html', tasks=tasks_data)

if __name__ == '__main__':
    app.run(debug=True)
