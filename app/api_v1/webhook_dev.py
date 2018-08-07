import json
from flask import Response, request
from . import api

@api.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    return handle_message_dev(user_id, user_message)

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
