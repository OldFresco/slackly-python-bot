import time
import slackclient
import sys
import threading
from flask import Flask

## HTTP SERVER ##
app = Flask(__name__)

@app.route('/')
def main_route():
  return 'OK'

## DEFINE CONSTANTS ##

# delay in seconds before checking for new events
LOOP_DELAY = 1

# credentials
BOT_NAME = 'testbot'
BOT_TOKEN = ''
BOT_ID = 'U5ZC51482'

## HELPER FUNCTIONS ##

def log_event(event, out=sys.stdout):
    out.write('-- NEW EVENT LOG -- \n')
    out.write('\nUSER: ' + str(event.get('user')))
    out.write('\nCHANNEL: ' + str(event.get('channel')))
    out.write('\nTYPE: ' + str(event.get('type')))
    out.write('\nTEXT: ' + str(event.get('text')))
    out.write(' ')

def is_a_greeting(message):
    greeting_key_words = ['hi','hello','hey','welcome','how are you?']

    message = message.lower()

    if any(word in message for word in greeting_key_words):
        return True
    else:
        return False

## MAIN PROGRAM ##

# intialise our slack client
slack_client = slackclient.SlackClient(BOT_TOKEN)

# This functions handles direct messages sent to our slack bot
def handle_message(message, user, channel):
    if is_a_greeting(message):
        post_message(message='Hi, how can I help?', channel=channel)
    else:
        post_message(message='Sorry, I don\'t know what that means!', channel=channel)

# This function uses the slack client to post a message back in the channel passed in as an arg
def post_message(message, channel):
    slack_client.api_call('chat.postMessage', channel=channel,text=message, as_user=True)

# This is the main function, which when ran
# - creates a 1 second infinite loop
# - gets any events registered through the rtm connection
# - for each event post a hello message to the channel of the inbound event
def run():
    # Check real time connection is live
    if slack_client.rtm_connect():
        print'[.] Testbot is ON...'
        while True:
            # gets events
            event_list = slack_client.rtm_read()
            # if there are any then...
            if len(event_list) > 0:
                for event in event_list:
                    log_event(event)
                    # if the event does not come from us and is a message then...
                    if event.get('user') != 'U5ZC51482' and event.get('type') == 'message':
                        # call our handler function which posts a message to the channel of the incoming event
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(LOOP_DELAY)
    else:
        print '[!] Connection to Slack failed.'

def start_server():
    app.run()

# Python sets the __name__ var as equal to __main__ when this code runs without being imported, so will be true when executed as file.
if __name__ == '__main__':
    server_task = threading.Thread(target=start_server)
    server_task.start()
    run()
