import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

senderEmail = "pingryquizbowl@gmail.com"
senderPassword = "S1mplep@ss"
appPassword = "rsxieenaquhajgdr"
receiversList = ["srichardson@pingry.org"]
todaysDate = datetime.datetime.now()

fo = open("finalemail.html", "r")
emailText = fo.read()
fo.close()

message = MIMEMultipart("alternative")
message["Subject"] = "Pingry Quizbowl Question of the Day for " + str(todaysDate.month) + "/" + str(todaysDate.day) + "/" + str(todaysDate.year) + "\n\n"

TEXT = emailText
body = MIMEText(TEXT, "html")
message.attach(body)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(senderEmail, appPassword)
    smtp.sendmail(senderEmail, receiversList, message.as_string())
