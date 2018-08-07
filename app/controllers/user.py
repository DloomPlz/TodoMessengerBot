from .. import db
from ..models.user import User

def change_reminder(facebook_id, str_remind_timer_hours):
    if str_remind_timer_hours is None:
        return "sorry your remind timer ¯\_(ツ)_/¯"
    remind_timer_hours = int(str_remind_timer_hours) % 23
    user = get_or_create_user(facebook_id)
    user.reminder = remind_timer_hours
    db.session.add(user)
    db.session.commit()
    return "all good :)"

def get_status(facebook_id):
    user = User.query.get(facebook_id)
    nb_todos = len(user.todos)
    return "you have "+str(nb_todos)+" todos. You will be reminded every "+str(user.reminder)+" hours."

def get_or_create_user(facebook_id):
    user = User.query.get(facebook_id)
    if user is None:
        user = User()
        user.id = facebook_id
        db.session.add(user)
        db.session.commit()
    return user
