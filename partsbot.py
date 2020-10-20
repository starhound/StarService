import json
import threading
from RocketChatBot import RocketChatBot
import logging

# constants
SERVER = 'https://rocketchaturl.com'
BOTNAME = 'botname'
BOTPASSWORD = 'botpassword'
PARTS_ID = 'partsroomID'
PARTS_HISTORY_ID = 'partshistoryroomID'

bot = RocketChatBot(BOTNAME, BOTPASSWORD, SERVER)
logging.basicConfig(filename='partsbot.log', level=logging.INFO)

def update_chat(message, message_id, new_message):
    bot.api.chat_update(room_id=PARTS_ID, msg_id=message_id, text=new_message)

def parts_history():
    return bot.api.groups_history(room_id=PARTS_ID, count=1000).content

def delete_trigger(message):
    id = message["_id"]
    bot.api.chat_delete(room_id=PARTS_ID, msg_id=id)

def check_triggers():
    history = parts_history()
    messages = json.loads(history)
    for message in messages['messages']:
        msg = message['msg']
        if "!parts" in msg:
            delete_trigger(message)

def get_action_card_message(reference_number):
    check_triggers()
    history = parts_history()
    messages = json.loads(history)
    for message in messages['messages']:
        msg = message['msg']
        if "Please click the link to view the parts order form for customer" in msg:
            action_card_reference_number = msg.split()[-1]
            if action_card_reference_number == reference_number:
                return message
    return 0

def get_completed_action_card_message(reference_number):
    history = parts_history()
    messages = json.loads(history)
    for message in messages['messages']:
        msg = message['msg']
        if "has taken care of this for" in msg:
            action_card_reference_number = msg.split()[-1]
            if action_card_reference_number == reference_number:
                return message
    return 0

def get_user_completed_form_message(reference_number):
    history = parts_history()
    messages = json.loads(history)
    for message in messages['messages']:
        msg = message['msg']
        if "GOT IT" in msg:
            completed_action_card_reference_number = msg.split()[-1]
            if completed_action_card_reference_number == reference_number:
                return message
    return

def archive_action_card(reference_number):
    completed_form = get_completed_action_card_message(reference_number)
    if completed_form is 0:
        return
    link = completed_form['attachments'][0]['text']
    ts = completed_form['ts']
    id = completed_form["_id"]
    message = completed_form['msg']
    user = completed_form['u']['username']
    bot.send_message("[" + ts + "]: " + message + " (" + link + ")", channel_id=PARTS_HISTORY_ID)
    bot.api.chat_delete(room_id=PARTS_ID, msg_id=id)
    logging.info(message + " -- " + link)

def archive_user_completed_button(reference_number):
    card = get_user_completed_form_message(reference_number)
    if card is 0:
        return
    id = card["_id"]
    bot.api.chat_delete(room_id=PARTS_ID, msg_id=id)

def action_event(msg, user, channel_id):
    message_id = msg['_id']
    ts = msg['ts']
    message = msg['msg']
    content = message.split()
    del content[:3]
    content.pop()
    content = " ".join(content)
    message = message.split()[-1]
    action_card_message = get_action_card_message(message)
    if action_card_message is 0:
        print(user + "tried to take care of " + message + " [already completed]")
        bot.api.chat_post_message(text= user + ", parts order " + message + " is already taken care of.", room_id=PARTS_ID)
        bot.api.chat_delete(room_id=channel_id, msg_id=message_id)
        return
    action_card_id = action_card_message['_id']
    new_message = user + " has taken care of this for " + content + " -- " + message
    print("[" + ts + "]: " + user + " took care of " + message)
    update_chat(action_card_message, action_card_id, new_message)
    archive_action_card(message)
    archive_user_completed_button(message)

def report_forms(msg, user, channel_id):
    print(user + " requested open form count")
    history = parts_history()
    messages = json.loads(history)
    count = 0;
    for message in messages['messages']:
        if "Please click the link to view the parts order form" in message['msg']:
            count += 1
    count_message = ""
    if count == 1:
        count_message = "There is 1 form that needs to be taken care of."
    else:
        count_message = "There are " + str(count) + " forms that need to be taken care of."

    bot.send_message(count_message, channel_id=channel_id)
    logging.info(user + " requested form count: " + str(count))

def clean_channel(msg, user, channel_id):
    check_triggers()

def clean_timer():
    check_triggers()
    threading.Timer(180.0, clean_timer).start()

def main():
    try:
        bot.add_dm_handler('got it', action_event)
        bot.add_dm_handler('form count', report_forms)
        print("PartsBot starting")
        clean_timer()
        bot.run()
        logging.info("Parts bot started.")
    except:
        print("Timeout occured on main thread")
        logging.warning("Parts bot timed out or errored.")

main()
