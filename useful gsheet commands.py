# how to setup gsheets creds stuff: https://www.youtube.com/watch?v=cnPlKLEGR7E didin't bother understanding it, just followed whatever he said.
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds4gs = ServiceAccountCredentials.from_json_keyfile_name("credsForGSheets.json", scope)
client = gspread.authorize(creds4gs)
sheet = client.open("wasup").sheet1

with io.open('job.txt', encoding="utf-8") as f: details = f.read()
job = details.split("~^f*+")


newrow = [job[0], job[2], job[1]]; sheet.insert_row(newrow,2) #add a new row


sheet.delete_rows(5) #n+1

data = sheet.get_all_records() # send all tasks

sheet.resize(rows=1); sheet.resize(rows=50) #deletes all rows except first, then adds 49 rows in next line

sheet.update_cell(16,11, "awesome") #will be useful for adding modification code.
