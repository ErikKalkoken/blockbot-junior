import os, slack
from flask import Flask, json, request
from config import *

app = Flask(__name__) #create the Flask app


@app.route('/')
def dummy_endpoint():                
    """ endpoint for calls to the root """
    return "blockbot-junior is alive"

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
        # make sure request is coming from Slack
        assert "token" in payload \
            and payload['token'] == os.environ['SLACK_VERIFICATION_TOKEN']

        # if this payload contains a normal event start the event handler
        if payload['type'] == 'event_callback' and 'event' in payload:
            event = payload['event']
                        
            # if event is a normal message and user is not allowed to speak
            # start new thread for deleting message
            # and continue the main process quick to remain below 3 seconds            
            if event['type'] == 'message' and 'subtype' not in event \
                and event['user'] not in get_allowed_users(event['channel']):
                    delete_message(event)            
            
    return ""


def get_allowed_users(channel_id):
    """ returns the list of allowed users for a channel """        
    if channel_id in ALLOWED_CHANNEL_USERS:        
        users = ADMIN_USERS + ALLOWED_CHANNEL_USERS[channel_id]
    else:        
        users = ADMIN_USERS
    return users


def delete_message(event):
    """ delete message referenced by this event """
    client_user = slack.WebClient(token=os.environ['SLACK_ACCESS_TOKEN'])
    response = client_user.chat_delete(
        channel=event['channel'],
        ts=event['ts']
    )
    assert response["ok"]    


@app.route('/slash', methods=['POST'])
def slash_endpoint():                
    """ endpoint for slash requests from Slack """
    
    # make sure request is coming from Slack
    assert "token" in request.form \
        and request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']

    # get context of current request
    user_id = request.form['user_id']
    channel_id = request.form['channel_id']
    
    if user_id not in ADMIN_USERS:
        text = 'Sorry, but you are not authorized to use this slash command.'
    else:                
        # get channels of bot
        client_user = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        response = client_user.users_conversations(
            types="public_channel,private_channel"
        )
        assert response["ok"]    
        channels = list(get_col(response["channels"], "id"))
        
        print(channel_id)
        allowed_users = get_allowed_users(channel_id)
        print(allowed_users)

        # compile results into text
        text = "Welcome to blockbot-junior!\n"
        if channel_id in channels:
            text += ":heavy_check_mark: This channel is in *announcement* mode.\n"
            text += "Only the following users can post here:\n"
            for user in allowed_users:
                text += "><@" + user + ">\n"        
        else:
            text += ":x: This channel is *not* in announcement mode.\n"
            text += "Invite the blockbot-junior user to this channel to activate it.\n"

    response = {
        "text": text
    }
    
    # send response back to Slack channel
    return json.jsonify(response)


def get_col(arr, col_name):
    """ returns the column from a multi-dimensional array """
    return map(lambda x : x[col_name], arr)    

if __name__ == '__main__':
    app.run(debug=True, port=8000) #run app in debug mode on port 8000
