# -*- coding:utf8 -*-


import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage


def send(sender, receiver, content):
    print 'Sending from', sender, 'to', receiver
    msg = MIMEMultipart()
    msg['From'] = Header(sender)
    msg['To'] = Header(receiver)
    msg['Subject'] = Header('cheap hardware', 'utf-8')
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    smtp = smtplib.SMTP()
    try:
        smtp.connect('smtp.163.com', '25')
        smtp.login(sender, 'zhouyaoyang')
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print 'Sent'
    except smtplib.SMTPException, err:
        print 'Failed'
        print err
