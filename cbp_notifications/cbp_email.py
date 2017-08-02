"""
.. module:: cbp_email
    :platform: unix
    :synopsis: This module contains classes which will send email notifications.

This is the cbp_email module
"""

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
    """
    This is the CbpEmail class which is a class for sending generic emails, meaning you have to specify both message
    and subject.
    """
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
    """
    This is a template email which tells the recipient that a program is done
    """
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
    """
    This is an email template that tells the recipient that the program had an error that it could not get past.
    """
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