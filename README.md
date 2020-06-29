# WhatsApp-Scheduler

Schedule WhatsApp messages using Telegram Bot + Python. Basically the Python script opens up WhatsApp Web & sends your message by interacting with the page using Selenium.

To get it up and running, follow these steps:

1 - Clone all the files from repository into a local folder. Create a new file "threadstatus.txt" and leave it blank inside.

2 - Inside each 'py' file, i've tagged spots which need modification by "#MODIFYYYYTHIS" (Ctrl F through all the files & modify as per your parameters).

3 - Create a Firefox Profile using any ubuntu based distro. To make the profile: fire up WhatsApp Web, login manually by scanning the QR code & then simply copy the folder over at /home/username/.mozilla/firefox/profiles. (folder should be between 10 to 40 MB in size) Place this folder next to the py files & modify the code to read the folder name correctly.

3 - To run locally on your PC: firstly Firefox should be installed & be in PATH alongwith Geckodriver. Start app.py. Start ngrok local server by running "ngrok http 5000". Copy the HTTPS url & put it inside creds.py. Then, browse to "YourNgrokURL/setwebhook" in your browswer & you should see "webhook set up ok". That's it! You can now start scheduling WhatsApp messages.

4 - To deploy to Heroku: Create a Heroku app. Add this buildpack (https://github.com/evosystem-jp/heroku-buildpack-firefox) & set the config vars as directed.

I have tested using profile made in Kali and it works swell. If you use a Firefox Profile made on Windows, the code won't work on Heroku, probably because WhatsApp Web 
