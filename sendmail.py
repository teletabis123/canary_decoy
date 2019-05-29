#!/bin/bash
import os
import smtplib
import time
import start
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from os.path import expanduser

email_user = 'cerdascom11@gmail.com'
email_password = 'cerdasngentot'

subject = 'Server Attack Warning [Denary]'

path = expanduser("~") + "/../var/tmp/opencanary.log"

emailtarget = ""

def getemail() :
    global emailtarget
    fread = open("useremail.txt","r")
    emailtarget = fread.read()
    fread.close()

    fwrite = open("checkmail.txt","w")
    fwrite.write(emailtarget+"\n")
    fwrite.close()
    return emailtarget

def attachment(email_user, email_password, email_send):

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Alert from Denary, Please Check the log files !!'
    msg.attach(MIMEText(body,'plain'))

    filename=path
    start.ProcessJson()
    attachment  =open("LogActivities.txt",'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename=LogActivities.txt")

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()

#attachment(email_user, email_password, email_send)

i = 1
tmp = 0
filesize = 0

while i == 1 :   
    files = os.stat(path)
    filesize = files.st_size
    if filesize != tmp :
        email_send = getemail()
        attachment(email_user, email_password, email_send)
    tmp = filesize
    
