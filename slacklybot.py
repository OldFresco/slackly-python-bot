import time
import slackclient
import sys
import threading
from flask import Flask
from fuzzywuzzy import fuzz

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

# NLP word phrases (knowledge)
greeting_key_phrases = ['hi','hello','hey','welcome','yo']
opening_hours_query_key_phrases= ['when are you open?','what time are you open until?','are you closed?','what are your opening hours?','what time are you open until?','hours','time','opening','closed']

## HELPER FUNCTIONS ##

def log_event(event, out=sys.stdout):
    out.write('-- NEW EVENT LOG -- \n')
    out.write('\nUSER: ' + str(event.get('user')))
    out.write('\nCHANNEL: ' + str(event.get('channel')))
    out.write('\nTYPE: ' + str(event.get('type')))
    out.write('\nTEXT: ' + str(event.get('text')))
    out.write(' ')

def is_a_greeting(message):
    # Make all letters lower case
    message = message.lower()
    # Split the message into a word list
    message_word_list = message.split()

    # Try and find a match with our greeting key phrase list
    if any(word in message_word_list for word in greeting_key_phrases):
        return True
    else:
        return False

def is_a_opening_hours_query(message):
    # Make all letters lower case
    message = message.lower()

    for phrase in opening_hours_query_key_phrases:
        print ("message: "+ message)
        print ("phrase: "+ phrase)
        print ("fuzzy match score: " + str(fuzz.partial_ratio(phrase, message)))
        if (fuzz.partial_ratio(phrase, message) > 80):
            print ("found one")
            return True
    
    return False


## MAIN PROGRAM ##

# intialise our slack client
slack_client = slackclient.SlackClient(BOT_TOKEN)

# This functions handles direct messages sent to our slack bot
def handle_message(message, user, channel):
    if is_a_greeting(message):
        post_message(message='Hi, how can I help?', channel=channel)
    elif is_a_opening_hours_query(message):
        post_message(message='We are open from 8:00 a.m. until 20:00 p.m. tonight!', channel=channel)
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
                    if event.get('user') != BOT_ID and event.get('type') == 'message':
                        # call our handler function which posts a message to the channel of the incoming event
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(LOOP_DELAY)
    else:
        print '[!] Connection to Slack failed.'

def start_server():
    app.run()

# Python sets the __name__ var as equal to __main__ when this code runs without being imported, so will be true when executed as file.
if __name__ == '__main__':
    # Start the http server as a process in a child thread
    server_task = threading.Thread(target=start_server)
    server_task.start()
    # Start our slack communication event poller
    run()
