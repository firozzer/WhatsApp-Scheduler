import telegram, requests
import io, threading, time, calendar
from datetime import datetime, timedelta
from sendSWA import sendScheduledMessage

def validateTimeInput(date_text):
    chat_id = xxxxx #MODIFYYYYTHIS #SENSITIZE
    try:
        print('trying if it is intssssss')
        int(date_text)
    except:
        print('coming inside non-int error')
        return """Time must be Numeric only, in 'hhmm OR DDMMhhmm' format. Please resend.""", "nothing"

    if len(date_text) == 1:
        try:
            addedzero = "0"+date_text
            utcDtObj = datetime.strptime(addedzero, '%H') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            print(f"this is utcdtobj {utcDtObj}")
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'h'. Please resend.""", "nothing" #99% lol sure it will never hit this
    if len(date_text) == 2:
        try:
            utcDtObj = datetime.strptime(date_text, '%H') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            print(f"this is utcdtobj {utcDtObj}")
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'hh'. Please resend.""", "nothing"
    if len(date_text) == 3:
        try:
            addedzero = "0"+date_text
            utcDtObj = datetime.strptime(addedzero, '%H%M') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            print(f"this is utcdtobj {utcDtObj}")
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'hmm'. Please resend.""", "nothing"
    elif len(date_text) == 4:
        try:
            print('entered 4 digit check')
            utcDtObj = datetime.strptime(date_text, '%H%M') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            print(f"this is utcdtobj {utcDtObj}")
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'hhmm'. Please resend.""", "nothing"
    elif len(date_text) == 8:
        try:
            print('endtered 8 digit check   ')
            utcDtObj = datetime.strptime(date_text, '%d%m%H%M') - timedelta(hours=4) #MODIFYYYYTHIS as per diff btw your timezone & UTC
            return "pass", utcDtObj.strftime('%d%m%H%M')
        except:
            return "Incorrect digits in 'DDMMhhmm'. Please resend.", "nothing"
    else:
        return """Incorrect format, 'hhmm OR DDMMhhmm' only. Please resend.""", "nothing"

def checker_thread():
    bot = telegram.Bot(token="xxxxxxxxxx") #MODIFYYYYTHIS #SENSITIZE
    chat_id = xxxxxx #MODIFYYYYTHIS #SENSITIZE
    i=0
    while True:
        if i%120==0: # every 20 mins pings my webpage to keep alive otherwise Heroku will put to sleep. And since my app PULLS data from Telegram (to check for new messages), it doesn't get reactivated even after user messages when in sleep mode. Hence need this.
            resuscitate = requests.get('url to your heroku app') #MODIFYYYYTHIS #SENSITIZE
            if i%8640==0: print(f"Checker thread running fine, webpage showed this: {resuscitate.text}") # just logs to console every 1 day that thread is running, otherwise i'm totally blind regarding thread status.
        with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
        joblist = data.split('\n--+%$--\n')
        if data != "":
            joblist.pop()
            for job in joblist:
                jobSplitted = job.split("~^f*+")
                now = datetime.now()
                if datetime.strptime(jobSplitted[2],"%Y%d%m%H%M") < now:
                    print(f"""Sending to {jobSplitted[0]} - \"{jobSplitted[1]}\"""")
                    output = sendScheduledMessage(jobSplitted[0],jobSplitted[1])
                    if output != "All Good! :)":
                        print(output)
                        bot.sendMessage(chat_id=chat_id, text=output) # not putting return here because otherwise it will exit the thread
                    else: print("All Good! :)")
                    joblist = [undonejob for undonejob in joblist if job not in undonejob] # read List comprehension like this: (ignore first word) "For undone job in joblist, if job is no int undonejob then assign undonejob to joblist list". Basically it adds all the jobs to the new array except the current job that is being iterated over.
                    with io.open('joblist.txt', "w", encoding="utf-8") as f:
                        print("Unexecuted joblist as follows:")
                        for job in joblist:
                            f.write(job+"\n--+%$--\n")
                            print(job)
        i+=1
        time.sleep(10)

def get_response(text, chat_id):
    text = text.strip()
    if text == "/start" or text == "/restart":
        with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
        return """Vanakkam, to schedule a message for WhatsApp, first please send me recipient name."""
    elif text == "/tasks":
        try: # in try in case user sends this before the file is created.
            with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
            if data=="": return "You have no scheduled tasks."
        except:
            return "You have no scheduled tasks."
        jobs = data.split("\n--+%$--\n")
        i=1; message=""; jobs.pop()
        for job in jobs:
            jobSplitted = job.split("~^f*+")
            dubaitime = (datetime.strptime(jobSplitted[2],'%Y%d%m%H%M') + timedelta(hours=4)).strftime("%H:%M on %d/%m/%Y") #MODIFYYYYTHIS as per your timezone
            message = message + (f"{i} - {jobSplitted[0]} @ {dubaitime} - {jobSplitted[1]}\n\n")
            i+=1
        message = message + "*All dates in dd/mm/yyyy format."; return message
    elif text == "/delete":
        try: # in try in case user sends this before the file is created.
            with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
            if data=="": return "No scheduled tasks available to delete."
            jobs = data.split("\n--+%$--\n")
            i=1; message=""; jobs.pop()
            for job in jobs:
                jobSplitted = job.split("~^f*+")
                dubaitime = (datetime.strptime(jobSplitted[2],'%Y%d%m%H%M') + timedelta(hours=4)).strftime("%H:%M on %d/%m/%Y") #MODIFYYYYTHIS you need to put the time difference btw you and UTC time. I live in UAE, so it is 4hrs for me.
                message = message + (f"{i} - {jobSplitted[0]} @ {dubaitime} - {jobSplitted[1]}\n\n")
                i+=1
            message = message + "Send me the task number to delete.";
            with io.open('job.txt', "w") as f: f.write("deleting task~^f*+") #decided to write in jobs itself as opening another file tremendously slows down the bot
            return message
        except:
            return "No scheduled tasks available to delete."
    elif text == "/delete_all":
        with io.open('job.txt', "w") as f: f.write("""!)@(Delet!ng @LL)@(""") #decided to write in jobs itself as opening another file tremendously slows down the bot
        return "Holy moly! Are you sure you wanna nuke all scheduled tasks? Reply y to proceed or /restart to cancel."
    elif text == "/backup":
        try: # in try in case user sends this before the file is created.
            with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
            if data=="": return "No scheduled tasks available to backup."
            bot = telegram.Bot(token="xxxxxx") #MODIFYYYYTHIS #SENSITIZE
            bot.sendMessage(chat_id=xxxxx, text=data) # not putting return here because otherwise it will exit the thread
            return "Copy the above message and keep it safe somewhere. DO NOT alter it; paste it back in unaltered while restoring, otherwise you'll face unexpected problems."
        except:
            return "Nooooo scheduled tasks available to backup."
    elif text == "/restore":
        with io.open('job.txt', "w") as f: f.write("""!)@(Restor!ng!)@(""") #decided to write in jobs itself as opening another file tremendously slows down the bot
        return "HOL' UP! This will overwrite your existing scheduled tasks if any. To continue, send the message you received as backup else send /restart to cancel. "
    try:
        with io.open('job.txt', encoding="utf-8") as f: data = f.read()
        jobs = data.split("~^f*+")
        if jobs[0] == "deleting task":
            try:
                jobs[2]
                if text.lower() == 'y' or text.lower()=='yes':
                    with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
                    joblist = data.split("\n--+%$--\n")
                    newjoblist = [job for job in joblist if joblist[int(jobs[1])-1] not in job]; newjoblist.pop() # read like this: for job in joblist, put the job in the new list if the jobToBeDeleted is not in job. Pop is to delete empty string at end
                    with io.open('joblist.txt', "w") as f:
                        for job in newjoblist:
                            f.write(job+"\n--+%$--\n") #decided to write in jobs itself as opening another file tremendously slows down the bot
                    with io.open('job.txt', "w") as f: f.write("") #reset the job.txt file.
                    return f"Task number {jobs[1]} deleted."
                elif text.lower()=='n' or text.lower()=='no':
                    with io.open('job.txt', "w") as f: f.write("deleting task~^f*+") #decided to write in jobs itself as opening another file tremendously slows down the bot
                    return "Ok. Please resend task number."
                else:
                    return "Please reply with y/n only."
            except:
                try:
                    taskno = int(text)
                    if taskno == 0: return "There is no task numbered 0. Please resend task number you wish to delete." # this is to catch if user inputs 0
                    with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
                    joblist = data.split("\n--+%$--\n")
                    print(len(joblist))
                    if taskno >= len(joblist): return f"You have only {len(joblist)-1} tasks. Please resend correct task number."
                    with io.open('job.txt', "a") as f: f.write(text+"~^f*+") #decided to write in jobs itself as opening another file tremendously slows down the bot
                    return f"Are you sure you wish to delete task number {text}? (Reply y/n only)"
                except:
                    return "Please send only the task number corresponding to the task you wish to delete." # this is to catch if user inputs text or float
        elif data == """!)@(Delet!ng @LL)@(""" and (text.lower() == "yes" or text.lower()=='y'):
            with io.open('joblist.txt', "w", encoding="utf-8") as f: f.write("")
            with io.open('job.txt', "w", encoding="utf-8") as f: f.write("") # reset the job.txt file
            return "All scheduled tasks nuked."
        elif data == """!)@(Restor!ng!)@(""":
            with io.open('joblist.txt', "w", encoding="utf-8") as f: f.write(text+"\n") #\n needed otherwise it gets popped when showing /tasks
            with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
            return "Tasks restored successfully."
        job = data.split("~^f*+")
        job[1]
        try:
            with io.open('job.txt', encoding="utf-8") as f: data = f.read()
            job = data.split("~^f*+")
            job[2]
            print('passed job2')
            try:
                print('about to test job3')
                with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                job = data.split("~^f*+")
                job[3]
                print('passed job3')
                if text.lower() == 'y' or text.lower() == 'yes': # enters here after userconfirms schedule
                    now = datetime.now()
                    with io.open('job.txt', encoding="utf-8") as f: details = f.read()
                    job = details.split("~^f*+")
                    print(f"job2 is {job[2]} and now is {now}")
                    if  datetime.strptime(job[2],'%Y%d%m%H%M') > now: #in case the 'y' from Dubai user is recvd after or on schedule time
                        with io.open('joblist.txt', "a", encoding="utf-8") as f: f.write(details+"\n--+%$--\n")
                        with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
                        with io.open('threadstatus.txt', encoding="utf-8") as f: data = f.read()
                        if data != "Thread started.":
                            print('Starting the checker threaddddddddddd')
                            with io.open('threadstatus.txt', "w", encoding="utf-8") as f: f.write("Thread started.")
                            x = threading.Thread(target=checker_thread)
                            x.start()
                        with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
                        joblist = data.split('\n--+%$--\n')
                        print("Unexecuted joblist as follows:")
                        for job in joblist:
                            print(job)
                        return f"""Message scheduled. To view scheduled tasks, send /tasks. If you want to schedule another message, send me recipient name first."""
                    else:
                        with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
                        return "Sorry! The schedule time has already passed. Please restart by sending me recipient name."

                elif text.lower() == 'n' or text.lower() == 'no':
                    with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
                    return """Message discarded. You can schedule another message by sending recipient name."""
                else:
                    return """Invalid response. Please send 'y' or 'n' only."""
            except: # this part writes time to file
                output, utcDtStr = validateTimeInput(text)
                if output != "pass": return output
                if len(utcDtStr) == 4:
                    print('coming inside small one')
                    now = datetime.now()
                    print(f"This is now {now} and this is utctime: {utcDtStr}")
                    if int(utcDtStr) <= int(now.strftime('%H%M')):
                        print('came inside less than')
                        fulldate = (now+timedelta(days=1)).strftime('%Y%d%m')+utcDtStr
                        print(fulldate)
                    else:
                        print('came inside the Else')
                        fulldate = now.strftime('%Y%d%m')+utcDtStr
                    with io.open('job.txt', "a", encoding="utf-8") as f: f.write(fulldate + "~^f*+") #writing time to file here instead of in last step as otherwise i'd lose this variable on the next run
                    with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                    job = data.split("~^f*+")
                    if len(text) == 1 or len(text) == 2: # thought a lot how to compare with date object, but impossible. needs to be done this method only
                        if int(text) <= int(now.strftime('%H')):
                            return f"""Will send "{job[1]}" to "{job[0]}" tomorrow @ {text} hrs. Confirm? (y/n)"""
                        else:
                            return f"""Will send "{job[1]}" to "{job[0]}" today @ {text} hrs. Confirm? (y/n)"""
                    elif int(text) <= int(now.strftime('%H%M')):
                        return f"""Will send "{job[1]}" to "{job[0]}" tomorrow @ {text} hrs. Confirm? (y/n)"""
                    else:
                        return f"""Will send "{job[1]}" to "{job[0]}" today @ {text} hrs. Confirm? (y/n)"""
                elif len(utcDtStr) == 8:
                    print('coming inside big one')
                    now = datetime.now()
                    print('passed 1')
                    todayfake = now.strftime('3333%d%m%H%M') #this & next 3 lines checks if user is reffering to current yr or next yr
                    print(todayfake)
                    print('passed2')
                    todayfakedo = datetime.strptime(todayfake,'%Y%d%m%H%M')
                    print('3')
                    textfake = '3333'+utcDtStr
                    print('4')
                    textfakedo = datetime.strptime(textfake,'%Y%d%m%H%M')
                    print('5')
                    if textfakedo > todayfakedo: # in case user entered today's date & gave time 1430 whereas current time is 1200 & other normal future cases.
                        print('came inside first one')
                        fulldate = now.strftime('%Y')+utcDtStr
                        with io.open('job.txt', "a", encoding="utf-8") as f: f.write(fulldate + "~^f*+")
                        with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                        job = data.split("~^f*+")
                        return f"""Will send "{job[1]}" to "{job[0]}" on {text[:2]} {calendar.month_name[int(text[2:4])]} @ {text[-4:]} hrs. Confirm? (y/n)"""
                    else: # in case user entered either {today's date & gave time 1000 & curr time is 1200} or {3rdJun whereas today is 16Jun}. Ultimately, mssg will be scheduled for next year.
                        print('came inside second one')
                        nextyear = str(int(now.strftime('%Y'))+1) #firstly it makes string then i convert to int add 1 then convert back to str, dumas me
                        fulldate = nextyear+utcDtStr
                        with io.open('job.txt', "a", encoding="utf-8") as f: f.write(fulldate + "~^f*+")
                        with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                        job = data.split("~^f*+")
                        return f"""Will send "{job[1]}" to "{job[0]}" on {text[:2]} {calendar.month_name[int(text[2:4])]} {nextyear} @ {text[-4:]} hrs (NEXT YEAR). Confirm? (y/n)"""
                else:
                    print('UNKNOWNNNNN ERRRORRRR')
        except: #this part writes message to file
            print('came inside time asker?')
            with io.open('job.txt', "a", encoding="utf-8") as f: f.write(text + "~^f*+")
            return """Messaged noted. Time? (hhmm OR DDMMhhmm)""" # if somehow this gets sent even after you submit time, means there was an error in the previously nested Except part above
    except: #this part writes recipient to file.
        with io.open('job.txt', "a", encoding="utf-8") as f: f.write(text + "~^f*+")
        return """Recipient noted. Message?"""
