import requests, json
from flask import Response, request, current_app
from . import api
from .. import db
from ..controllers.todo import add_todo_item, list_todo_items, delete_todo_item
from ..controllers.user import change_reminder, get_status
import os

verify_token = os.getenv('FB_VERIFY_TOKEN', None)
access_token = os.getenv('FB_ACCESS_TOKEN', None)

@api.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to list your things and remind you of doing it. That's all. We don't use it in any other way."

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

def action(user_id, user_message):
    message_parsed = user_message.split()
    action = message_parsed[0]

    if action == "/add":
        todo_item_content = " ".join(message_parsed[1:])
        return add_todo_item(user_id, todo_item_content)

    if action == "/list":
        return list_todo_items(user_id)

    if action == "/delete":
        todo_item_id = message_parsed[1]
        return delete_todo_item(user_id, todo_item_id)

    if action == "/remind":
        remind_timer_hours = message_parsed[1]
        return change_reminder(user_id, remind_timer_hours)

    if action == "/status":
        return get_status(user_id)

    return show_usage()

def show_usage():
    return "Please choose between /add, /delete, /list, /remind or /status thx :)"

def send_message(user_id, user_message):
    response = {
        'recipient': {'id': user_id},
        'message': {'text': user_message}
    }
    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
