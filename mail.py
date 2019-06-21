# -*- coding:utf8 -*-


import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage


def send(sender, receiver, title, content):
    passwd = open('.password').read().strip()
    # print(passwd)
    print('Sending from', sender, 'to', receiver)
    msg = MIMEMultipart()
    msg['From'] = Header(sender)
    msg['To'] = Header(receiver)
    msg['Subject'] = Header(title, 'utf-8')
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    smtp = smtplib.SMTP()
    try:
        smtp.connect('smtp.163.com', '25')
        smtp.login(sender, passwd)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print('Sent')
    except smtplib.SMTPException as err:
        print('Failed')
        print(err)


if __name__ == '__main__':
    mail_sender = 'diamondzyy@163.com'
    mail_receiver = 'diamondzyy@sina.cn'
    send(mail_sender, mail_sender,
         'tt', 'test')
