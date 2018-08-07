import datetime
from flask_script import Manager
from app import create_app, db
from app.models.todo import Todo
from app.api_v1.webhook import send_message
from app.controllers.todo import list_todo_items

app = create_app()
manager = Manager(app)

@manager.command
def resetdb():
    db.drop_all()
    db.create_all()

# app.logger.debug(t)

@manager.command
def scheduled_reminder():
    current_hour = datetime.datetime.now().hour
    users = User.query.all()
    for user in users:
        if current_hour % user.reminder is 0:
            resp = list_todo_items(user.id)
            send_message(user.id, resp)

# manager's doc = https://flask-script.readthedocs.io/en/latest/

if __name__ == "__main__":
    manager.run()
