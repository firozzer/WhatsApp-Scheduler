# to finally make this work i got the Firefox profile from Kali Linux & used it here without any user agent. Kali Linux i went into Live mode & used the default ESR Firefox & got the profile from /home/kali/.mozilla/firefox.
# Common errors: argument of type 'NoneType' is not iterable - remove path locations of binary & geckodriver

import requests
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait #t5his & next two both needed for waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# import telegram
import os

def sendImage(fotu): #this is useful to debug in headless mode by sending screenshots that selenium takes to your Telegram.
    url = "https://api.telegram.org/xxxxxx"; #MODIFYYYYTHIS #SENSITIZE
    files = {'photo': open(fotu, 'rb')}
    data = {'chat_id' : "xxxxxx"} #MODIFYYYYTHIS #SENSITIZE enter your Chat ID here
    requests.post(url, files=files, data=data)

def sendScheduledMessage(name, message):
    try:
        print("sendScheduledMessage processssssssssssss starte")
        driveron = False; options = FirefoxOptions()
        fp = webdriver.FirefoxProfile("kali2") #enter your saved Firefox Profile name here
        # useragent = "Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0" #works perfectly fine without useragent modification in windows awa heroku
        # fp.set_preference("general.useragent.override", useragent)
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_profile=fp, options=options, executable_path=os.environ.get("GECKODRIVER_PATH"),firefox_binary=os.environ.get("FIREFOX_BIN"))
        driver.get('https://web.whatsapp.com')
        driveron = True # just to prevent driver.quit() error in exception
        print('enroute to the webpage (will wait 30 secs for searchbar to show up)')
        try: #catches non connection to internet of WA
            searchbar = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"""//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*""")))
        except:
            driver.save_screenshot('ss.png')
            sendImage('ss.png')
            driver.quit()
            return f"""Error: WA W could not reach your phone when to trying to send "{message}" to {name}."""
        print('got searchbar')
        # I know i am getting searchbar total 3 times, but unfortunately this is the only way it works. If it stupids, it is not work.
        searchbar = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"""//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*""")))
        try:
            searchbar.send_keys(name, Keys.RETURN)
        except:
            print("getting searhbar again as wasn't typable")
            searchbar = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"""//div[text()=\"Search or start new chat\"]/following-sibling::*/child::*/child::*/following-sibling::*""")))
            searchbar.send_keys(name, Keys.RETURN)
        try: # in case user hsa entered a wrong contacgt name, gets  catched.
            time.sleep(5) # multiline messages get messed up on heroku due to proablby cursor jumping to front after 1 or 2 secs, so this waits for that dance to get over.
            textfield = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, """//div[text()="Type a message"]/following-sibling::*""")))
        except:
            driver.save_screenshot('ss.png')
            sendImage('ss.png')
            driver.quit()
            return f"""Error: Could not find contact by the name of {name}."""
        if '\n' in message: #special input treatment into text box if user's message contains new lines
            print('yes')
            splitup=message.split('\n')
            for s in splitup:
                if s=="":
                    textfield.send_keys(u'\ue008', Keys.RETURN) #this is shift + enter
                    continue
                textfield.send_keys(s)
                textfield.send_keys(u'\ue008', Keys.RETURN)
            time.sleep(3); textfield.send_keys(Keys.RETURN) #Sleeping 3 secs so if link is there it can generate preview.
        else:
            textfield.send_keys(message); time.sleep(3); textfield.send_keys(Keys.RETURN) #Sleeping 3 secs so if link is there it can generate preview.
        time.sleep(2)
        try:
            i = 0
            while i < 120:
                driver.find_element(By.XPATH,"""//span[@aria-label=" Pending "]""")
                if i == 0: print("Message delivery pending, will wait 2 mins for it to get sent.")
                time.sleep(1)
                i += 1
            return f"""Error: "{message}" posted to chat of {name} but got stuck at the pending 'clock' icon. It won't get sent, dw."""
        except:
            if i != 0: print(f"Message sent after {i} seconds.")
            driver.quit()
            return "All Good! :)"
    except Exception as e:
        if driveron == True: driver.quit()
        return f"""Error: Some unkown error occured while trying to send "{message}" to {name}. Could be this- {e}"""


# driver = webdriver.Firefox(firefox_profile=fp, options=options, executable_path=os.environ.get("GECKODRIVER_PATH"),firefox_binary=os.environ.get("FIREFOX_BIN"))
# https://api.whatsapp.com/send?phone=971508984405&text=thisisatest direct API call but doesn't work unless you click on it inside web whatsapp as a chat
# https://web.whatsapp.com/send?phone=971508984405&text=thisisatest goes directly nice tho
