import smtplib
from email.mime.text import MIMEText
import ConfigParser

class CbpEmail:
    def __init__(self,msg="",sender="",recipients=None, subject=""):
        self.msg = msg
        self.sender= sender
        self.recipients = recipients
        self.subject = subject

    def send(self):
        config = ConfigParser.RawConfigParser()
        config.read("D:\gitrepo\cbp\pushbullet_api.cfg")

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
