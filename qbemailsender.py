import datetime
import smtplib
from email.message import EmailMessage

senderEmail = "pingryquizbowl@gmail.com"
senderPassword = # not putting the password here for obvious reasons

receiversList = [] # fill this with any email accs you wanna add to your email list, but remember to make them strings

todaysDate = datetime.datetime.now()

fo = open("finalemail.html", "r")
emailText = fo.read()
fo.close()

message = EmailMessage()
message["Subject"] = "Pingry Quizbowl Question of the Day for " + str(todaysDate.month) + "/" + str(todaysDate.day) + "/" + str(todaysDate.year)
message["From"] = senderEmail
message["To"] = receiversList
message.set_content(emailText, subtype = "html")

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(senderEmail, senderPassword)
    smtp.send_message(message)
