from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import os
import datetime as dt

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy()
db.init_app(app)

#Table Configuration
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    completed_task = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()

date = dt.datetime.now()

global text
text = "My TODO List"

@app.route("/", methods=["GET","POST"])
def main():
    results = db.session.execute(db.select(Tasks))
    tasks = results.scalars().all()
    ids = []
    for i in tasks:
        ids.append(i.id)

    if request.method == "POST":
        with app.app_context():
            add_task = Tasks(
                task_name = request.form.get('task-value'),
                date = date.strftime("%b. %d,%Y"),
                completed_task = bool(0)
            )
        db.session.add(add_task)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template("index.html", task_items = tasks, check_id = ids, len_ids = len(ids), todo_text = text, today_date = date.strftime("%b. %d,%Y"))


@app.route("/delete/<int:task_id>", methods=["GET","POST"])
def delete(task_id):
    task_item_delete = db.get_or_404(Tasks, task_id)
    db.session.delete(task_item_delete)
    db.session.commit()
    return redirect(url_for('main'))


@app.route("/modify-task/<int:task_id>/<int:c_id>", methods=["GET","POST"])
def completed_task(task_id, c_id):
    completed = db.get_or_404(Tasks, task_id)
    completed.completed_task = c_id
    print(completed.completed_task)
    db.session.commit()
    return redirect(url_for('main'))


@app.route("/modify-title-list", methods=["GET","POST"])
def change_todolist_name():
    if request.method == "POST":
        new_text = request.form.get('todolist-title')
        text = new_text
        print(text)
        return redirect(url_for('main', todo_text = text))





if __name__ == "__main__":
    app.run(debug=True, port=5005)