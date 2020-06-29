import telegram, itertools, datetime
from creds import bot_token, bot_user_name,URL
from mastermind import get_response
from flask import Flask, request

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
# get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id
    # sender_id = update.sender.id
    # print(f"SENDERRRRRR {sender_id}")
# Telegram understands UTF-8, so encode text for unicode compatibility
    try:
        print("got text messageeeeee:", update.message.text)
    except Exception as e:
        print(f"got that WinError87 most porbably. This is errorrrrrrrrrrrr: {e}") #get this error whien user sends multi line message. No idea how to fix it.
    if update.message.text != None: #added this if condition by firoze because otherwise keeps giving AttributeError: 'NoneType' object has no attribute 'encode because i think it fetches a blank msg from Telegram continously.
        text1 = update.message.text.encode('utf-8').decode()
    else:
        return 'ok'
    if chat_id != xxxxxxxxxx: #MODIFYYYYTHIS #SENSITIZE put your chat ID here
        bot.sendMessage(chat_id=xxxxxxx, text=f"TeooNeeoTeeooNeooooo, rEdAlErT!!1!11! Unauthorized usage detected!!1!\n\nSender Chat ID: {update.message.chat.id}\nUsername: {update.message.chat.username}\nFirst Name: {update.message.chat.first_name}\nMessage: {update.message.text}") #MODIFYYYYTHIS #SENSITIZE
        for _ in itertools.repeat(None, 10):
            bot.sendMessage(chat_id=chat_id, text="boat note wokring :(")
        samay = datetime.datetime.now()
        with open(r"loggerboi.txt","a") as f:
            f.write(f"""\n{samay} ~|~ {update.message.chat.id} ~|~ {update.message.chat.username} ~|~ {update.message.chat.first_name} ~|~ {update.message.text}""")
        return 'ok'
# here we call our super AI
    response = get_response(text1, chat_id)
# now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return 'This is the WhatsApp Scheduler.'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True, debug=True)
