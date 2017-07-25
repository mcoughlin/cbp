import smtplib
from email.mime.text import MIMEText
import ConfigParser
import sys

if sys.platform == "win32":
    cf = "D:\gitrepo\cbp\pushbullet_api.cfg"
elif sys.platform == "linux2":
    cf = "/home/pi/Code/cbp_2/pushbullet_api.cfg"

recipients = ["eric.coughlin2014@gmail.com"]

class CbpEmail:
    def __init__(self,msg="",sender="",recipients=None, subject=""):
        self.msg = msg
        self.sender= sender
        self.recipients = recipients
        self.subject = subject

    def send(self):
        config = ConfigParser.RawConfigParser()
        config.read(cf)

        msg = MIMEText(self.msg)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipients
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(config.get('gmail','user'),config.get('gmail','password'))
            server.sendmail(config.get('gmail','user'),[config.get('gmail','user')],msg.as_string())
            # ...send emails
        except Exception as e:
            print(e)
            print('Something went wrong...')

class CbpEmailComplete:
    def __init__(self,program=""):
        self.msg = "{0} is complete.".format(program)
        self.sender = "eric.coughlin2014@gmail.com"
        self.recipients = recipients
        self.subject = "[CBP Notifications] {0} Complete".format(program)

    def send(self):
        config = ConfigParser.RawConfigParser()
        config.read(cf)

        msg = MIMEText(self.msg)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = ','.join(self.recipients)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(config.get('gmail', 'user'), config.get('gmail', 'password'))
            server.sendmail(self.sender, self.recipients, msg.as_string())
            # ...send emails
        except Exception as e:
            print(e)
            print('Something went wrong...')

class CbpEmailError:
    def __init__(self,program="",error=""):
        self.msg = "{0} had an error {1}".format(program,error)
        self.sender = "eric.coughlin2014@gmail.com"
        self.recipients = recipients
        self.subject = "[CBP Notifications] {0} Error".format(program)

    def send(self):
        config = ConfigParser.RawConfigParser()
        config.read(cf)

        msg = MIMEText(self.msg)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = ','.join(self.recipients)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(config.get('gmail', 'user'), config.get('gmail', 'password'))
            server.sendmail(self.sender, self.recipients, msg.as_string())
            # ...send emails
        except Exception as e:
            print(e)
            print('Something went wrong...')