# WhatsApp-Scheduler

Watch it in aktion: https://www.youtube.com/watch?v=iwT5KKVJf6Y

Schedule WhatsApp messages using Telegram Bot + Python. Basically the Python script opens up WhatsApp Web & sends your message by interacting with the page using Selenium. NOTE: This project works only for a single user. Not sure how to go about implementing multi-user functionality.

# Follow these steps to get it up & running:

- Clone all the files from repository into a local folder. Create a new file "threadstatus.txt" and leave it blank inside.

- Inside each 'py' file, i've tagged spots which need modification by "#MODIFYYYYTHIS" (Ctrl F through all the files & modify as per your parameters).

- Create a Firefox Profile using any ubuntu based distro. To make the profile: fire up WhatsApp Web, login manually by scanning the QR code & then simply copy the folder over at /home/username/.mozilla/firefox/profiles. (folder should be between 10 to 40 MB in size) Place this folder next to the py files & modify the code to read the folder name correctly.

- To run locally on your PC: firstly Firefox should be installed & be in PATH alongwith Geckodriver. Start app.py. Start ngrok local server by running "ngrok http 5000". Copy the HTTPS url & put it inside creds.py. Then, browse to "YourNgrokURL/setwebhook" in your browswer & you should see "webhook set up ok". That's it! You can now start scheduling WhatsApp messages.

- To deploy on Heroku: Create a Heroku app. Add this buildpack (https://github.com/evosystem-jp/heroku-buildpack-firefox) & set the config vars as directed. Add Python buildpack. Update the URL to your app inside the creds.py file. Login to Heroku via terminal inside the folder containing the py files (Heroku CLI & Git must be pre-installed). Deploy everything to your app by following the steps shown under the 'Deploy' tab on your Heroku app page on the website. Browse "YourHerokuAppURL/setwebhook" and you should see "webhook set up ok", at which point all ops are a go!

# Quick overview of what each file does:

- app.py is the Flask application that runs & listens for incoming Telegram messages to the bot. It is the file that you need to execute to get everything off the ground.

- mastermind.py Processes whatever the user sent & replies accordingly.

- sendSWA.py gets run whenever the WA message was scheduled to be sent.

- creds.py contains a few credentials.

# Remarks:

- There is a delay of about 30-40 seconds in the message getting sent. For eg) if you schedule the message to be sent at 06:16, the message will get delivered around 6:16:35 or so. You can tweak the timing changes in the code if you want more accuracy.

- I have tested using Firefox profile made in Kali and it works swell. If you use a Firefox Profile made on Windows, the code won't work on Heroku, probably because WhatsApp Web verifies the OS on which the profile was made.

- I tried using Chrome but somehow i always got a ton of erros while trying to run Chrome + Selenium + UserDataDir + Headless. Tried a dozen different combinations of noSandbox, userAgentProfile, etc, but nothing worked. So ultimately just switched to Firefox. Thank you Firefox devs, you are awesome!

- Multiple people cannot use the same bot. If your friend wants to use it, you'll have to go through all the steps again to set it up for them. 😱

Notes to meself: took me 21 days in total to go from 'idea' to 'final product' (basic goal suggested by bro). 18 of which went into trying to make Headless broswer + Saved Profile work, firstly locally, then on Heroku. The logic building of mastermind.py & app.py flask application both combined took approx 3 days, once i saw selenium was successful on each Heroku attempt. 5/7 would do again lol.
