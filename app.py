from datetime import datetime
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
supabase: Client = create_client(url, key)


@app.route('/')
def home():
    response = supabase.table('tasks').select(
        '*').order('id', desc=False).execute()
    return render_template('index.html', tasks=response.data)


@app.route('/add-task')
def add_task():
    return render_template('add_task.html')


@app.route('/submit-task', methods=['POST'])
def submit_task():
    title = request.form.get('title')
    priority = request.form.get('priority')
    status = request.form.get('status')
    due_date_and_time = request.form.get('due_date_and_time')

    task_data = {
        'title': title,
        'priority': priority,
        'status': status,
        'due_date_and_time': due_date_and_time
    }
    supabase.table('tasks').insert(task_data).execute()
    return redirect('/')


@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'GET':
        response = supabase.table('tasks').select('*').eq('id', id).execute()
        if response.data:
            # print(response.data)
            return render_template('edit_task.html', data=response.data)
        else:
            return "Not Found", 404
    elif request.method == 'POST':
        title = request.form.get('title')
        priority = request.form.get('priority')
        status = request.form.get('status')
        due_date_and_time = request.form.get('due_date_and_time')

        task_data = {
            'title': title,
            'priority': priority,
            'status': status,
            'due_date_and_time': due_date_and_time
        }
        supabase.table('tasks').update(task_data).eq('id', id).execute()
    return redirect('/')


@app.route("/complete/<int:id>")
def mark_as_complete(id):
    supabase.table('tasks').update(
        {"status": "Completed"}).eq('id', id).execute()
    return redirect("/")


@app.route("/delete_task/<int:id>")
def delete_task(id):
    supabase.table('tasks').delete().eq('id', id).execute()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
