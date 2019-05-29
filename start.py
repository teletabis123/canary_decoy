#!/bin/bash
import os
import json
import subprocess
import settingConfigFile as settingConfig
from os.path import expanduser
from six.moves import input
from datetime import datetime

contents = ""
json_str = ""
startcanary = False

def main_logo() :
    print(" _______   _______ .__   __.      ___      .______     ____    ____ ")
    print("|       \\ |   ____||  \\ |  |     /   \\     |   _  \\    \\   \\  /   / ")
    print("|  .--.  ||  |__   |   \\|  |    /  ^  \\    |  |_)  |    \\   \\/   /  ")
    print("|  |  |  ||   __|  |  . `  |   /  /_\\  \\   |      /      \\_    _/   ")
    print("|  '--'  ||  |____ |  |\\   |  /  _____  \\  |  |\\  \\----.   |  |     ")
    print("|_______/ |_______||__| \\__| /__/     \\__\\ | _| `._____|   |__|     ")
    print("")

def main_menu() :
    os.system("clear")
    main_logo()
    print("     0. About")
    print("     1. Installation")
    print("     2. Start HoneyPot")
    print("     3. Display Log")
    print("     4. Stop Honeypot")
    print("     5. Exit")

def ReadFile():
    global contents
    logPath = expanduser("~") + "/../var/tmp/opencanary.log"
    fread = open(logPath, "r")
    #fread = open("opencanary.log", "r")
    contents = fread.read()
    # print(contents)
    fread.close()
    
def Parser():
    global contents
    global json_str
    data = contents.split("\n")
    
    json_str = "[\n"
    for i in range (0, len(data)):
        if i != 0  and i != len(data)-1:
            json_str = json_str + ", \n"
        json_str = json_str + "\t"+ data[i] 
    json_str = json_str + "\n]"
    # print("Json: \n"+json)

def WriteFile():
    global json_str
    fwrite = open("logfile.txt", "w+")
    fwrite.write(json_str)
    fwrite.close()

def ReadWrite():
    f = open("steps.txt", "r+")
    temp = f.read()
    # print(temp)
    f.write(temp + "\nasdf")
    f.close()

def ProcessJson():
    ReadFile()
    Parser()
    WriteFile()

    f = open("logfile.txt","r")
    data = f.read()
    dataLog = json.loads(data)
    f.close()
    
    # print("\n\n")
    logFileHTMLSign = []
    logFileHTMLIn = []
    logFileSynScan = []
    logFileFTP = []
    i=0
    for d in dataLog:
        if(d["logtype"] == 3000):
            # print(str(i) + " Data HTML Not Input")
            logFileHTMLIn.append(d)

        elif(d["logtype"] == 3001):
            # print(str(i) + " Data HTML Input")
            logFileHTMLSign.append(d)

        elif(d["logtype"] == 5001):
            # print(str(i) + " Data Scan SYN")
            logFileSynScan.append(d)

        elif(d["logtype"] == 2000):
            # print(str(i) + " Data FTP")
            # ada username dan password
            logFileFTP.append(d)

        i = i+1

    scanIP = []
    scanHostPort = []
    scanPort = []
    scanTime = []
    tempPort = []
    tempTime = []

    i = 0
    
    for i in range(0, len(logFileSynScan)) :
        if(i == 0): # masukkan IP baru
            dateTime1 = datetime.strptime(logFileSynScan[i]["local_time"], "%Y-%m-%d %H:%M:%S.%f")
            ipMulai = logFileSynScan[i]["src_host"]
            scanIP.append(ipMulai)
            scanHostPort.append(logFileSynScan[i]["src_port"])
            tempPort.append(logFileSynScan[i]["dst_port"])
            tempTime.append(dateTime1)
        else:
            dateTime2 = datetime.strptime(logFileSynScan[i]["local_time"], "%Y-%m-%d %H:%M:%S.%f")
            if(logFileSynScan[i]["src_host"] == ipMulai): # cek tanggal, kalau sama tambah temp, kalo beda tambah semua, temp kosongin
                dif = (dateTime2-dateTime1).total_seconds()
                timeDif = dif
                if((dif > 0 and dif < 4) or (dif < -56)): # masih sama
                    tempPort.append(logFileSynScan[i]["dst_port"])
                    if(len(tempTime) == 1):
                        tempTime.append(dateTime2)
                    else:
                        tempTime[1] = dateTime2
                else: # udah beda
                    scanPort.append(tempPort)
                    scanTime.append(tempTime)
                    tempPort = []
                    tempTime = []
                    ipMulai = logFileSynScan[i]["src_host"]
                    scanIP.append(ipMulai)
                    scanHostPort.append(logFileSynScan[i]["src_port"])
                    tempPort.append(logFileSynScan[i]["dst_port"])
                    tempTime.append(dateTime2)                
            else: # beda, jadi tambah IP baru
                scanPort.append(tempPort)
                scanTime.append(tempTime)
                tempPort = []
                tempTime = []
                ipMulai = logFileSynScan[i]["src_host"]
                scanIP.append(ipMulai)
                scanHostPort.append(logFileSynScan[i]["src_port"])
                tempPort.append(logFileSynScan[i]["dst_port"])
                tempTime.append(dateTime2) 
            dateTime1 = dateTime2
    scanPort.append(tempPort)
    scanTime.append(tempTime)

    # print("\nIP: ")
    # print(scanIP)
    # print("\nHostPort: ")
    # print(scanHostPort)
    # print("\nPort: ")
    # print(scanPort)
    # print("\nTime: ")
    # print(scanTime)


    f = open("LogActivities.txt", "w+")

    f.write("Detected activities:\n")
    f.write("\nHost get inside HTML:\n")
    i=1
    for d in logFileHTMLIn:
        f.write(str(i) + ". Data "+str(i)+": \n")
        f.write("\tDestination Port: " + str(d["dst_port"])+"\n")
        f.write("\tTime Accessed   : " + d["local_time"]+"\n")
        f.write("\tSource Host IP  : " + d["src_host"]+"\n")
        f.write("\tSource Host Port: " + str(d["src_port"])+"\n") 
        # print(d['logdata']['USERAGENT'])
        f.write("\tUser Agent Used : " + d['logdata']['USERAGENT']+"\n")
        i = i+1
    f.write("\nHost Sign in into HTML:\n")
    i=1
    for d in logFileHTMLSign:
        f.write(str(i) + ". Data "+str(i)+": \n")
        f.write("\tDestination Port: " + str(d["dst_port"])+"\n")
        f.write("\tTime Accessed   : " + d["local_time"]+"\n")
        f.write("\tSource Host IP  : " + d["src_host"]+"\n")
        f.write("\tSource Host Port: " + str(d["src_port"])+"\n") 
        f.write("\tPassword Used   : " + d["logdata"]["PASSWORD"]+"\n")
        f.write("\tUsername Used   : " + d["logdata"]["USERNAME"]+"\n")
        f.write("\tUser Agent Used : " + d["logdata"]["USERAGENT"]+"\n")
        i = i+1
    f.write("\nHost Doing SYN Scan:\n")
    i=1
    for i in range(0, len(scanIP)):
        f.write(str(i) + ". Data "+str(i)+": \n")
        f.write("\tSource Host IP  : " + scanIP[i]+"\n")
        f.write("\tSource Host Port: " + scanHostPort[i]+"\n") 
        f.write("\tDestination Port: ")
        for j in range(0, len(scanPort[i])):
            f.write(str(scanPort[i][j]))
            if(j != len(scanPort[i])-1):
                f.write(", ")
        # print(scanTime[i][0], scanTime[i][1])
        f.write("\n\tTime Accessed   : " )
        if(len(scanTime[i]) == 2):
            f.write(str(scanTime[i][0]) + " - " + str(scanTime[i][1]) +"\n")
        else:
            f.write(str(scanTime[i][0]) + "\n")
        

        
    f.write("\nHost Trying FTP:\n")
    i=1
    for d in logFileFTP:
        f.write(str(i) + ". Data "+str(i)+": \n")
        f.write("\tDestination Port: " + str(d["dst_port"])+"\n")
        f.write("\tTime Accessed   : " + d["local_time"]+"\n")
        f.write("\tSource Host IP  : " + d["src_host"]+"\n")
        f.write("\tSource Host Port: " + str(d["src_port"])+"\n") 
        f.write("\tPassword Used   : " + d["logdata"]["PASSWORD"]+"\n")
        f.write("\tUsername Used   : " + d["logdata"]["USERNAME"]+"\n")
        i = i+1

    f.close()

    print("Log Data is saved in LogActivities.txt")
            
def doInstallation():
    subprocess.call("./install.sh")

def configFile():
    subprocess.call("./config.sh")

def startCanary():
    subprocess.call("./start.sh")

def stopCanary():
    subprocess.call("./stop.sh")

def about():
    print("""
        Hello welcome to Denary, an app to help you create an Honeypot that can act as a decoy
        to protect and detect possible attacks. This application was made using OpenCanary to
        Make the decoy Server.

        -----How it works----- 
 
        1. Installation
           => This option helps you with the installation of OpenCanary and its depedencies. All you need to do is to wait
              for the installation to be completed and you can move on to the Start Honeypot menu
        2. Start Honeypot
           => Before starting the honeypot this option will ask you if you want to be notified by email if something happens
              to the honeypot. Then you will be asked to choose between 4 Configurations that you would like for the honeypot.
               - Default
               - Linux Server Configuration
               - Windows Server Configuration
               - Use a Custom Configuration
              The honeypot will run after the configuration has been done and you will be directed to the Main menu.
        3. Display Logs
           => This option will show you the Logs of the Honeypot, it contains activities that was recorded when the Honeypot is running.
        4. Stop Honeypot
           => This option will help you stop the decoy honeypot from running.
        5. Exit
           => Exits the Application.
        
        -----Creators-----
       
        Created by students from Universitas Multimedia Nusantara : http://www.umn.ac.id/
       	       1. Aldric Leonardo
               2. James Christian
               3. Matthew Evans
               4. Vionie Laorensa

        -----Links and References-----

        Here is the link to the OpenCanary Documentation : https://buildmedia.readthedocs.org/media/pdf/opencanary/latest/opencanary.pdf

        Here is the link to the Steps to make the Decoy : https://niiconsulting.com/checkmate/2017/05/canary-an-open-source-decoy/ 

        Finally, here is the link to our Github : https://github.com/teletabis123/canary_decoy

        These Links will help you understand better how this application works.    """)
    print("")
    print("")

# main
if __name__ == "__main__" :

    print("Initialized part 1")
    print("Activate Open Canary")

    i = 1
    #main loop
    while i == 1 :
        main_menu()
        nav = input("Choose a Menu (0 - 5) : ")
        if(nav == "0"):
            os.system("clear")
            main_logo()
            print("Menu About")
            about()

        elif(nav == "1"):
            print("Menu Installation")
            doInstallation()

        elif(nav == "2"):
            os.system("clear")
            main_logo()
            ans  = input("Would you like to be notified by email, about actvities that happen to the decoy ? (y/n) : ")
            if(ans == "y") :
                ans2 = input("Please enter a gmail account :")
                femail = open("useremail.txt","w")
                femail.write(ans2 + "\n")
                femail.close()
                os.system("python sendmail.py &")
            os.system("clear")
            main_logo() 
            print("Menu Start Honeypot")
            print("  1. Use default configuration")
            print("  2. Use Linux configuration")
            print("  3. Use Windows configuration")
            print("  4. Use custom configuration")
            inp = int(input("Choose: "))
            configFile()
            if inp == "1":
                print("Default")
                settingConfig.defaultSetting()
            elif inp == "2":
                print("Linux")
                settingConfig.setLinuxDefault()
            elif inp == "3":
                print("Windows")
                settingConfig.setWindowsDefault()
            elif inp == "4":
                print("Custom")
                settingConfig.manualSetting()
            else :
                continue
            startcanary = True
            startCanary()

        elif(nav == "3"):
            print("Menu Display Log")
            ProcessJson()

        elif(nav == "4"):
            print("Menu Stop Honeypot")
            os.system("pkill -f sendmail.py")
            stopCanary()
            startcanary = False

        elif(nav == "5"):
            os.system("pkill -f sendmail.py")
            print("Menu Exit")
            if(startCanary):
                print("Stop Decanary")
                os.system("opencanaryd --stop")
                os.system("clear")
            else:
                print("Out from program")
                os.system("clear")
            break
        else :
            continue
        input("Press any button to continue")
        os.system("clear")

    
    # ReadWrite()

    
    
