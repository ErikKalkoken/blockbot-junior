import os, slack
from flask import Flask, json, request
from config import *

app = Flask(__name__) #create the Flask app

@app.route('/events', methods=['POST'])
def events_endpoint():                
    """ endpoint for events from Slack """

    payload = request.get_json()

    # URL verification handshake
    if payload['type'] == 'url_verification' and  'challenge' in payload:
        challenge = payload['challenge']        
        return challenge
    
    # All other event types
    else:
        # if this payload contains a normal event start the event handler
        if payload['type'] == 'event_callback' and 'event' in payload:
            event = payload['event']
                        
            # if event is a normal message and user is not allowed to speak
            # start new thread for deleting message
            # and continue the main process quick to remain below 3 seconds            
            if event['type'] == 'message' and 'subtype' not in event \
                and event['user'] not in ALLOWED_USERS:
                    delete_message(event)            
            
    return ""

def delete_message(event):
    # init slack client with access token
    client_user = slack.WebClient(token=os.environ['SLACK_ACCESS_TOKEN'])

    # delete message                    
    response = client_user.chat_delete(
        channel=event['channel'],
        ts=event['ts']
    )
    assert response["ok"]    


if __name__ == '__main__':
    app.run(debug=True, port=8000) #run app in debug mode on port 8000
