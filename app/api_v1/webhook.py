import requests, json
from flask import Response, request, current_app
from . import api
from .. import db
from ..models.todo import Todo
import os

# env_variables
# token to verify that this bot is legit
verify_token = os.getenv('FB_VERIFY_TOKEN', None)
# token to send messages through facebook messenger
access_token = os.getenv('FB_ACCESS_TOKEN', None)


@api.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@api.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_message = entry['messaging'][0]['message']['text']
        user_id = entry['messaging'][0]['sender']['id']
        text = action(user_id, user_message)
        send_message(user_id, text)
    return Response(response="EVENT RECEIVED",status=200)

@api.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    return handle_message_dev(user_id, user_message)

@api.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."

def handle_message_dev(user_id, user_message):
    text = action(user_id, user_message)
    response = {
        'recipient': {'id': user_id},
        'message': {'text': text}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

def send_message(user_id, user_message):
    response = {
        'recipient': {'id': user_id},
        'message': {'text': user_message}
    }
    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)





def action(user_id, user_message):
    message_parsed = user_message.split()
    action = message_parsed[0]
    content = " ".join(message_parsed[1:])

    if action == "/add":
        return add_todo_item(user_id, content)

    if action == "/list":
        return list_todo_items(user_id)

    if action == "/delete":
        return delete_todo_item(user_id, content)

    # unknown action -> show usage
    return show_usage()

def show_usage():
    return "Please choose between /add, /delete or /list, thx :)"

def add_todo_item(user_id, content):
    """add an item in the todo list

    get a new item to add to the todo list of the use

    Arguments:
        user_id {string} -- the facebook ID of the user
        content {string} -- the todo item content
    """
    # sanitize the content
    # save object in DB
    if not (content and content.strip()):
        return "sorry your todo item is empty ¯\_(ツ)_/¯"
        # content is empty
    t = Todo()
    t.content = content
    t.user_id = user_id
    db.session.add(t)
    db.session.commit()
    return list_todo_items(user_id)
       

def list_todo_items(user_id):
    """list all todo items

    list all the items of the user's todo list

    Arguments:
        user_id {string} -- the facebook ID of the user
    """
    # get list of all items where user_id == user_id
    items = Todo.query.filter(Todo.user_id==user_id).all()
    # Test if todolist is empty
    if not items :
        return "The list for this user is empty. Good Job!"
    resp= ""
    for i in range(0,len(items)):
        # create a string with new_lines
        resp += "#"+str(i+1)+": "+items[i].content+ "\n"
    return resp
    # convert each item to string
    # create a string with new_lines
    # return the string

def delete_todo_item(user_id, content):
    """delete an item

    delete an item, by index, from the user's todo list

    Arguments:
        user_id {string} -- the facebook ID of the user
        content {string} -- index of the todo item
    """
    # create object based on TodoItem model sqlalchemy
    if not (content and content.strip()):
        return "sorry your todo item ID is empty ¯\_(ツ)_/¯"
    item_id = int(content)
    t = Todo.query.filter(Todo.user_id==user_id).all()
    if t is None:
        return "404 todo item not found"
    if item_id < 1 or item_id > len(t):
        return "index is incorrect"
    db.session.delete(t[item_id-1])
    db.session.commit()
    return list_todo_items(user_id)
    # convert content to integer
    # get object where id == content
    # delete object
    # save in DB
    # return true or list of updated items ?