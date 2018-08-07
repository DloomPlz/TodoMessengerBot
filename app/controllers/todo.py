from .. import db
from ..models.todo import Todo
from ..models.user import User
from .user import get_or_create_user


def add_todo_item(user_id, todo_item):
    if not (todo_item and todo_item.strip()):
        return "sorry your todo item is empty ¯\_(ツ)_/¯"
    user = get_or_create_user(user_id)
    todo = Todo()
    todo.content = todo_item
    todo.user_id = user.id
    db.session.add(todo)
    db.session.commit()
    return list_todo_items(user_id)


def list_todo_items(user_id):
    todos = Todo.query.filter(Todo.user_id==user_id).all()
    if todos is None :
        return "The list for this user is empty. Good Job!"
    resp = ""
    for i in range(0, len(todos)):
        resp += "#"+str(i+1)+": "+todos[i].content+ "\n"
    return resp


def search_todo_items(user_id, search):
    if not (search and search.strip()):
        return "sorry your search is empty ¯\_(ツ)_/¯"
    look_for = '%{0}%'.format(search)
    todos = Todo.query.filter(Todo.user_id==user_id).filter(Todo.content.ilike(look_for)).all()
    if todos is None :
        return "0 todo matches your search ¯\_(ツ)_/¯"
    resp = ""
    for i in range(0, len(todos)):
        resp += "- "+todos[i].content+ "\n"
    return resp


def delete_todo_item(user_id, str_item_id):
    if str_item_id is None:
        return "sorry your todo item ID is empty ¯\_(ツ)_/¯"
    item_id = int(str_item_id)
    todos = Todo.query.filter(Todo.user_id==user_id).all()
    if todos is None:
        return "404 todo item not found"
    if item_id < 1 or item_id > len(todos):
        return "index is incorrect"
    todo_item = todos[item_id-1]
    db.session.delete(todo_item)
    db.session.commit()
    return list_todo_items(user_id)
