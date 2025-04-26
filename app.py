# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    keyword = request.args.get('q', '')
    if keyword:
        tasks = Task.query.filter(Task.title.contains(keyword)).order_by(Task.id.desc()).all()
    else:
        tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('index.html', tasks=tasks, keyword=keyword)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        new_title = request.form['title']
        if new_title:
            task.title = new_title
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/completed')
def show_completed():
    tasks = Task.query.filter_by(complete=True).order_by(Task.id.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/pending')
def show_pending():
    tasks = Task.query.filter_by(complete=False).order_by(Task.id.desc()).all()
    return render_template('index.html', tasks=tasks)

# AJAX API 路由
@app.route('/api/delete/<int:task_id>', methods=['POST'])
def api_delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'status': 'success', 'action': 'deleted', 'task_id': task_id})

@app.route('/api/complete/<int:task_id>', methods=['POST'])
def api_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.complete = True
    db.session.commit()
    return jsonify({'status': 'success', 'action': 'completed', 'task_id': task_id})

if __name__ == '__main__':
    app.run(debug=True)