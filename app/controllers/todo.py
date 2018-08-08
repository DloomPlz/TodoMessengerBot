from .. import db
from ..models.todo import Todo
from ..models.user import User
from .user import get_or_create_user


def add_todo_item(user_id, todo_item):
    user = get_or_create_user(user_id)
    todo = Todo()
    todo.content = todo_item
    todo.user_id = user.id
    db.session.add(todo)
    db.session.commit()
    return list_todo_items(user_id)


def list_todo_items(user_id):
    todos = Todo.query.filter(Todo.user_id==user_id).all()
    if len(todos) is 0 :
        return "You have no more todos ! Good job ¯\_(ツ)_/¯"
    resp = ""
    for i in range(0, len(todos)):
        resp += "#"+str(i+1)+": "+todos[i].content+"\n"
    return resp


def find_todo_items(user_id, search):
    look_for = '%{0}%'.format(search)
    todos = Todo.query.filter(Todo.user_id==user_id).filter(Todo.content.ilike(look_for)).all()
    if len(todos) is 0 :
        return "0 todo matches your search ¯\_(ツ)_/¯"
    resp = "Found "+str(len(todos))+" todos : \n"
    for i in range(0, len(todos)):
        resp += "- "+todos[i].content+ "\n"
    return resp


def delete_todo_item(user_id, item_id):
    todos = Todo.query.filter(Todo.user_id==user_id).all()
    if todos is None:
        return "404 todo item not found"
    if item_id < 1 or item_id > len(todos):
        return "index is incorrect"
    todo_item = todos[item_id-1]
    db.session.delete(todo_item)
    db.session.commit()
    return list_todo_items(user_id)
