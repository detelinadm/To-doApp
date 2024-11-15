import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def load_tasks():
    with open('tasks.json', "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("./index.html", tasks=tasks)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    form_data = request.form
    new_task = form_data.to_dict()
    new_task["status"] = "Pending"
    tasks = load_tasks()
    if any(task["id"] == new_task["id"] for task in tasks):
        return jsonify({"error": "Task with this ID already exists."}), 400
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_tasks_id(task_id):
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_tasks(task_id):
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"message": "Task deleted"}), 200


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    updated_data = request.get_json()
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_data)
            save_tasks(tasks)
            return jsonify(task)
        return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            save_tasks(tasks)
            return jsonify(task)
        return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
