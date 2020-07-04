import io, time, calendar, gspread, threading
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

def clearAllTasksFromGSheets():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds4gs = ServiceAccountCredentials.from_json_keyfile_name("credsForGSheets.json", scope)
    client = gspread.authorize(creds4gs)
    sheet = client.open("WhatsApp Scheduler DB Backup").sheet1
    sheet.resize(rows=1); sheet.resize(rows=50) #deletes all rows except first, then adds 49 rows in next line

def validateTimeInput(date_text):
    try:
        int(date_text)
    except:
        return """Time must be Numeric only, in 'h' OR 'hh' OR 'hmm' OR 'hhmm' OR 'DDMMhhmm' format only. Please resend.""", "nothing"
    if len(date_text) == 1:
        try:
            addedzero = "0"+date_text
            utcDtObj = datetime.strptime(addedzero, '%H') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'h'. Please resend.""", "nothing" #99% lol sure it will never hit this
    if len(date_text) == 2:
        try:
            utcDtObj = datetime.strptime(date_text, '%H') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'hh'. Please resend.""", "nothing"
    if len(date_text) == 3:
        try:
            addedzero = "0"+date_text
            utcDtObj = datetime.strptime(addedzero, '%H%M') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'hmm'. Please resend.""", "nothing"
    elif len(date_text) == 4:
        try:
            utcDtObj = datetime.strptime(date_text, '%H%M') - timedelta(hours=4) #making a time obj out of date_text variable. Later subtracting 4 to match UTC to Dubai #MODIFYYYYTHIS as per your timezone diff between UTC
            return "pass",  utcDtObj.strftime('%H%M') #returning string-ized utc time of the Dubai time.
        except:
            return """Incorrect digits in 'hhmm'. Please resend.""", "nothing"
    elif len(date_text) == 8:
        try:
            utcDtObj = datetime.strptime(date_text, '%d%m%H%M') - timedelta(hours=4) #MODIFYYYYTHIS as per diff btw your timezone & UTC
            return "pass", utcDtObj.strftime('%d%m%H%M')
        except:
            return "Incorrect digits in 'DDMMhhmm'. Please resend.", "nothing"
    else:
        return """Incorrect format, 'h' OR 'hh' OR 'hmm' OR 'hhmm' OR 'DDMMhhmm' only. Please resend.""", "nothing"

def get_response(text):
    text = text.strip()
    if text == "/start" or text == "/restart":
        with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
        return """🙏🏽 Vanakkam, to schedule a message for WhatsApp, first please send me recipient name."""
    elif text == "/tasks":
        with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
        if data=="":
            with io.open('job.txt', "w") as f: f.write("")
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
        with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
        if data=="":
            with io.open('job.txt', "w") as f: f.write("")
            return "No scheduled tasks available to delete."
        jobs = data.split("\n--+%$--\n")
        i=1; message=""; jobs.pop()
        for job in jobs:
            jobSplitted = job.split("~^f*+")
            dubaitime = (datetime.strptime(jobSplitted[2],'%Y%d%m%H%M') + timedelta(hours=4)).strftime("%H:%M on %d/%m/%Y") #MODIFYYYYTHIS #SENSITIZE
            message = message + (f"{i} - {jobSplitted[0]} @ {dubaitime} - {jobSplitted[1]}\n\n")
            i+=1
        message = message + "Send me the task number to delete. Or /restart to cancel.";
        with io.open('job.txt', "w") as f: f.write("deleting task~^f*+") #decided to write in jobs itself as opening another file tremendously slows down the bot
        return message
    elif text == "/delete_all":
        with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
        if data=="":
            with io.open('job.txt', "w") as f: f.write("")
            return "No scheduled tasks available to delete."
        with io.open('job.txt', "w") as f: f.write("""!)@(Delet!ng @LL)@(""") #decided to write in jobs itself as opening another file tremendously slows down the bot
        return "Holy moly! Are you sure you wanna nuke all scheduled tasks? Reply y to proceed or /restart to cancel."
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
                    if newjoblist == []: # in case user deletes one & only task in joblist.txt then, gsheets needs to be informed to clear all tasks as well.
                        x = threading.Thread(target=clearAllTasksFromGSheets)
                        x.start()
                    with io.open('joblist.txt', "w") as f:
                        for job in newjoblist: #when there is no task left, this list will be empty, so it will never enter this for loop
                            f.write(job+"\n--+%$--\n") #decided to write in jobs itself as opening another file tremendously slows down the bot
                    with io.open('job.txt', "w") as f: f.write("") #reset the job.txt file.
                    return f"Task number {jobs[1]} deleted."
                elif text.lower()=='n' or text.lower()=='no':
                    with io.open('job.txt', "w") as f: f.write("deleting task~^f*+") #decided to write in jobs itself as opening another file tremendously slows down the bot
                    return "Ok. Please resend task number or /restart to cancel."
                else:
                    return "Please reply with y/n only."
            except:
                try:
                    taskno = int(text)
                    if taskno == 0: return "There is no task numbered 0. Please resend task number you wish to delete." # this is to catch if user inputs 0
                    with io.open('joblist.txt', encoding="utf-8") as f: data = f.read()
                    joblist = data.split("\n--+%$--\n")
                    if taskno >= len(joblist): return f"You have only {len(joblist)-1} task/s. Please resend correct task number."
                    with io.open('job.txt', "a") as f: f.write(text+"~^f*+") #decided to write in jobs itself as opening another file tremendously slows down the bot
                    return f"Are you sure you wish to delete task number {text}? (Reply y/n only)"
                except:
                    return "Please send only the task number corresponding to the task you wish to delete." # this is to catch if user inputs text or float
        elif data == """!)@(Delet!ng @LL)@(""" and (text.lower() == "yes" or text.lower()=='y'):
            with io.open('joblist.txt', "w", encoding="utf-8") as f: f.write("")
            with io.open('job.txt', "w", encoding="utf-8") as f: f.write("") # reset the job.txt file
            x = threading.Thread(target=clearAllTasksFromGSheets) #hopefully i'm hoping no memory leak. 1- thread should automatically end as no loop. 2- the whole mstermind.py shuts down after each run, so should get killed then. 3 - If still persisting, should get killed at the 24hr Heroku cycles
            x.start()
            return "All scheduled tasks nuked."
        job = data.split("~^f*+") # i know i'm redundnatly doingthis splitting second time, but freak it i'm too tired to delete & then modify the dependats
        job[1]
        try:
            with io.open('job.txt', encoding="utf-8") as f: data = f.read()
            job = data.split("~^f*+")
            job[2]
            try:
                with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                job = data.split("~^f*+")
                job[3]
                if text.lower() == 'y' or text.lower() == 'yes': # enters here after userconfirms schedule
                    now = datetime.now()
                    with io.open('job.txt', encoding="utf-8") as f: details = f.read()
                    job = details.split("~^f*+")
                    if  datetime.strptime(job[2],'%Y%d%m%H%M') > now: #in case the 'y' from Dubai user is recvd after or on schedule time
                        with io.open('joblist.txt', "a", encoding="utf-8") as f: f.write(details+"\n--+%$--\n")
                        with io.open('job.txt', "w", encoding="utf-8") as f: f.write("")
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
                    now = datetime.now()
                    if int(utcDtStr) <= int(now.strftime('%H%M')):
                        fulldate = (now+timedelta(days=1)).strftime('%Y%d%m')+utcDtStr
                    else:
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
                    now = datetime.now()
                    todayfake = now.strftime('3333%d%m%H%M') #this & next 3 lines checks if user is reffering to current yr or next yr
                    todayfakedo = datetime.strptime(todayfake,'%Y%d%m%H%M')
                    textfake = '3333'+utcDtStr
                    textfakedo = datetime.strptime(textfake,'%Y%d%m%H%M')
                    if textfakedo > todayfakedo: # in case user entered today's date & gave time 1430 whereas current time is 1200 & other normal future cases.
                        fulldate = now.strftime('%Y')+utcDtStr
                        with io.open('job.txt', "a", encoding="utf-8") as f: f.write(fulldate + "~^f*+")
                        with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                        job = data.split("~^f*+")
                        return f"""Will send "{job[1]}" to "{job[0]}" on {text[:2]} {calendar.month_name[int(text[2:4])]} @ {text[-4:]} hrs. Confirm? (y/n)"""
                    else: # in case user entered either {today's date & gave time 1000 & curr time is 1200} or {3rdJun whereas today is 16Jun}. Ultimately, mssg will be scheduled for next year.
                        nextyear = str(int(now.strftime('%Y'))+1) #firstly it makes string then i convert to int add 1 then convert back to str, dumas me
                        fulldate = nextyear+utcDtStr
                        with io.open('job.txt', "a", encoding="utf-8") as f: f.write(fulldate + "~^f*+")
                        with io.open('job.txt', encoding="utf-8") as f: data = f.read()
                        job = data.split("~^f*+")
                        return f"""Will send "{job[1]}" to "{job[0]}" on {text[:2]} {calendar.month_name[int(text[2:4])]} {nextyear} @ {text[-4:]} hrs (NEXT YEAR). Confirm? (y/n)"""
                else:
                    print('UNKNOWNNNNN ERRRORRRR')
                    return 'UNKNOWNNNNN ERRRORRRR'
        except: #this part writes message to file
            with io.open('job.txt', "a", encoding="utf-8") as f: f.write(text + "~^f*+")
            return """Messaged noted. Time? ('h' OR 'hh' OR 'hmm' OR 'hhmm' OR 'DDMMhhmm' only)""" # if somehow this gets sent even after you submit time, means there was an error in the previously nested Except part above
    except: #this part writes recipient to file.
        with io.open('job.txt', "a", encoding="utf-8") as f: f.write(text + "~^f*+")
        return """Recipient noted. Message?"""
