from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending',
                    due_date_and_time DATETIME NOT NULL
            )""")
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM tasks ")
    tasks = cursor.fetchall()
    conn.close()
    formatted_tasks = [
        {
            "id": task[0],
            "title": task[1],
            "priority": task[2],
            "status": task[3],
            "due_date_and_time": task[4],
        }
        for task in tasks
    ]
    return render_template("index.html", tasks=formatted_tasks)


@app.route("/add-task")
def add_task():
    return render_template("add_task.html")


@app.route("/submit-task", methods=["POST"])
def submit_task():
    title = request.form["title"]
    priority = request.form["priority"]
    status = "Pending"
    due_date_and_time_str = request.form["due_date_and_time"]
    due_date_and_time = datetime.strptime(
        due_date_and_time_str, "%Y-%m-%dT%H:%M")

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(" INSERT INTO tasks (title, priority, status, due_date_and_time) VALUES (?, ?, ?, ?)",
                   (title, priority, status, due_date_and_time))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit_task/<int:id>", methods=["GET", "POST"])
def edit_task(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute(" SELECT * FROM tasks WHERE id = ? ", (id,))
        data = cursor.fetchone()
        conn.close()

        if data:
            return render_template("edit_task.html", data=data)
        else:
            return "Entry Not Found", 404
    elif request.method == "POST":
        title = request.form["title"]
        priority = request.form["priority"]
        status = request.form["status"]
        due_date_and_time_str = request.form["due_date_and_time"]
        due_date_and_time = datetime.strptime(
            due_date_and_time_str, "%Y-%m-%dT%H:%M")
        cursor.execute(" UPDATE tasks SET title = ?, priority = ?, status = ?, due_date_and_time = ? WHERE id = ? ",
                       (title, priority, status, due_date_and_time, id))
        conn.commit()
        conn.close()

        return redirect("/")


@app.route("/delete_task/<int:id>")
def delete_task(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(" DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/complete/<int:id>")
def mark_as_complete(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        " UPDATE tasks SET status = 'Completed' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
