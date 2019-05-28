#!/bin/bash
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = 'cerdascom11@gmail.com'
email_password = 'cerdasngentot'
# email_send = 'vanillasexmatcha@gmail.com'

subject = 'Server Attack Warning [Denary]'

emailtarget = ""

def getemail() :
    global emailtarget
    fread = open("useremail.txt","r")
    emailtarget = fread.read()
    return emailtarget

def attachment(email_user, email_password, email_send):

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Hi there, sending this email from Python!'
    msg.attach(MIMEText(body,'plain'))

    filename='LogActivities.txt'
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()

attachment(email_user, email_password, email_send)

i = 1
tmp = ""
filesize = ""
while i == 1 :
    if filesize != tmp :
        email_user = getemail()
        attachment(email_user, email_password, email_send)
    filesize = os.getsize("opencanary.log")
    time.sleep(1000)
    tmp = filesize
    
