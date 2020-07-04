import telegram, itertools, datetime, threading, requests, io, time, gspread
from creds import bot_token, bot_user_name,URL, my_chat_id
from mastermind import get_response, clearAllTasksFromGSheets
from flask import Flask, request
from sendSWA import sendScheduledMessage
from oauth2client.service_account import ServiceAccountCredentials

def checker_thread():
    i=0
    print("Checker thread starteddddddddddddd")
    while True:
        if i%240==0: # every 20 mins pings my webpage to keep alive otherwise Heroku will put to sleep. And since my app PULLS data from Telegram (to check for new messages), it doesn't get reactivated even after user messages when in sleep mode. Hence need this.
            resuscitate = requests.get(URL) #MODIFYYYYTHIS #SENSITIZE
        with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
        joblist = data.split('\n--+%$--\n')
        if data != "":
            joblist.pop()
            for job in joblist:
                jobSplitted = job.split("~^f*+")
                now = datetime.datetime.now()
                if datetime.datetime.strptime(jobSplitted[2],"%Y%d%m%H%M") < now:
                    print(f"""Sending scheduled message to {jobSplitted[0]} - \"{jobSplitted[1]}\"""")
                    output = sendScheduledMessage(jobSplitted[0],jobSplitted[1])
                    if output != "All Good! :)":
                        print(output)
                        bot.sendMessage(chat_id=MY_CHAT_ID, text=output) # not putting return here because otherwise it will exit the thread
                    else: print("All Good! :)")
                    joblist = [undonejob for undonejob in joblist if job not in undonejob] # NEED TO READ JOBS FROM FILE AGAIN. OTHERWISE IF A JOB IS SCHEDLED WHILE CODE IS PROCESSING SENDSWA.PY, THEN THAT NEW JOB WON'T GET LISTED WHEN THIS USES THE OLD JOBLIST ARRAY. read List comprehension like this: (ignore first word) "For undone job in joblist, if job is no int undonejob then assign undonejob to joblist list". Basically it adds all the jobs to the new array except the current job that is   being iterated over.
                    if joblist == []:  #in case it was the only job in oblist.txt, need to clear the same from gsheets as well.
                        x = threading.Thread(target=clearAllTasksFromGSheets)
                        x.start()
                    with io.open('joblist.txt', "w", encoding="utf-8") as f:
                        print("Unexecuted joblist as follows:")
                        for job in joblist:
                            f.write(job+"\n--+%$--\n")
                            print(job)
        try: #god knows just in case there's a google outage lel
            if i%24==0: #backup joblist.txt to gsheet every 2 mins. Not saving directly as pulling & pushing data everytime would greatly slow down user experience. Need to take backup because Heroku cycles/destroys dyno every 24hrs so backup essential.
                with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
                joblist = data.split('\n--+%$--\n')
                scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
                creds4gs = ServiceAccountCredentials.from_json_keyfile_name("credsForGSheets.json", scope) # you can make this using this tut: https://www.youtube.com/watch?v=cnPlKLEGR7E
                client = gspread.authorize(creds4gs)
                sheet = client.open("WhatsApp Scheduler DB Backup").sheet1 # see how to make this sheet in your GDrive using this tut: https://www.youtube.com/watch?v=cnPlKLEGR7E. In cells A1, B1, C1, ensure to keep exactly these values wout quotes: "Name", "Time", "Message"
                if data != "":
                    joblist.pop()
                    sheet.resize(rows=1); sheet.resize(rows=50) #deletes all rows except first, then adds 49 rows in next line
                    for job in joblist:
                        jobSplitted = job.split("~^f*+")
                        newrow = [jobSplitted[0], jobSplitted[2], jobSplitted[1]]; sheet.insert_row(newrow,2) #add a new row
                else: #in case data from joblist.txt is empty, means either of 2 things: 1) dyno just initatied & so it will restore everything from gsheet. 2) User cleared all tasks (hence joblist.txt is empty). Thankfully when user clears all tasks manually, i've coded both "/delete" & "/delete_all" commands to clear Gsheet as well. So in that case it will restore basically nothing.
                    data = sheet.get_all_records()
                    for d in data: #data is in dict format
                        with io.open('joblist.txt', "a", encoding="utf-8") as f:
                            f.write(d['Name']+"~^f*+"+d['Message']+"~^f*+"+str(d['Time'])+"\n--+%$--\n")
        except Exception as e:
            print(f"Error while working with Gsheetsssssssssssssssssssss: {e}")
        i+=1
        time.sleep(5) #checker thread checks every 5 secs if it is time to send the message.

global bot
global TOKEN
global MY_CHAT_ID
MY_CHAT_ID = my_chat_id
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
with open('threadstatus.txt') as f: data = f.read() #found this place to keep this code after putting print all over the place lol
if data != "thread started":
    with open('threadstatus.txt', "w") as f: f.write("thread started")
    x = threading.Thread(target=checker_thread)
    x.start()

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
    if chat_id != MY_CHAT_ID: #MODIFYYYYTHIS #SENSITIZE put your chat ID here
        bot.sendMessage(chat_id=MY_CHAT_ID, text=f"TeooNeeoTeeooNeooooo, rEdAlErT!!1!11! Unauthorized usage detected!!1!\n\nSender Chat ID: {update.message.chat.id}\nUsername: {update.message.chat.username}\nFirst Name: {update.message.chat.first_name}\nMessage: {update.message.text}") #MODIFYYYYTHIS #SENSITIZE
        for _ in itertools.repeat(None, 10):
            bot.sendMessage(chat_id=chat_id, text="boat note wokring :(")
        samay = datetime.datetime.now()
        with open(r"loggerboi.txt","a") as f: #this was stupid, ephemeral file system will delete it every 24hrs, but still left it jic i'm checking within 24hrs.
            f.write(f"""\n{samay} ~|~ {update.message.chat.id} ~|~ {update.message.chat.username} ~|~ {update.message.chat.first_name} ~|~ {update.message.text}""")
        return 'ok'
# here we call our super AI
    response = get_response(text1)
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

if __name__ == '__main__': #ihs portion doesn't even get run. GUARANTEED, when run on Heroku checked with print. It is running directly the app abve via gunicorn
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True, debug=True)
