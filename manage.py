import datetime
from flask_script import Manager
from app import create_app, db
from app.models.todo import Todo
from app.api_v1.webhook import list_todo_items, send_message

app = create_app()
manager = Manager(app)

@manager.command
def resetdb():
    db.drop_all()
    db.create_all()

# app.logger.debug(t)

@manager.command
def remind_list():
    # remind every 6 hours
    if datetime.datetime.now().hour % 6 is 0:
        users = db.session.query(Todo.user_id).distinct()
        for user in users:
            id_user = user[0]
            resp = list_todo_items(id_user)
            send_message(id_user, resp)

# manager's doc = https://flask-script.readthedocs.io/en/latest/

if __name__ == "__main__":
    manager.run()
