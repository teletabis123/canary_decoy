#!/bin/bash
import os
import json
import subprocess
import settingConfigFile as settingConfig
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
    fread = open("opencanary.log", "r")
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

# main
if __name__ == "__main__" :

    print("Initialized part 1")
    print("Activate Open Canary")

    i = 1
    #main loop
    while i == 1 :
        main_menu()
        nav = input("Choose a Menu (0 - 6) : ")
        if(nav == "0"):
            print("Menu About")
            fread = open("logfileScan.txt", "r")
            contents = fread.read()
            print(contents)
            fread.close()

        elif(nav == "1"):
            print("Menu Installation")
            doInstallation()

        elif(nav == "2"):
            os.system("clear")
            main_logo()
            print("Menu Start Honeypot")
            print("  1. Use default configuration")
            print("  2. Use Linux configuration")
            print("  3. Use Windows configuration")
            print("  4. Use custom configuration")
            inp = int(input("Choose: "))
            configFile()
            if inp == 1:
                print("Default")
                settingConfig.defaultSetting()
            if inp == 2:
                print("Linux")
                settingConfig.setLinuxDefault()
            if inp == 3:
                print("Windows")
                settingConfig.setWindowsDefault()
            if inp == 4:
                print("Custom")
                settingConfig.manualSetting()
            global startcanary
            startcanary = True
            startCanary()

        elif(nav == "3"):
            print("Menu Display Log")
            ProcessJson()

        elif(nav == "4"):
            print("Menu Stop Honeypot")
            stopCanary()
            global startcanary
            startcanary = False

        elif(nav == "5"):
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
            continue;
        input("Press any button to continue")
        os.system("clear")

    
    # ReadWrite()

    
    
