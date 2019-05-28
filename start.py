#!/bin/bash
import os
import json
import subprocess

contents = ""
json_str = ""
startCanary = False

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
    print("     2. Configure Server")
    print("     3. Start HoneyPot")
    print("     4. Display Log")
    print("     5. Stop Honeypot")
    print("     6. Exit")

def ReadFile():
    global contents
    fread = open("opencanary.log", "r")
    contents = fread.read()
    print(contents)
    fread.close()
    
def Parser():
    global contents
    global json_str
    data = contents.split("\n")
    # print("Data:\n")
    # for d in data :
    #     print(d+"\n")
    
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
    
    # print(dataLog)
    logFileHTMLSign = []
    logFileHTMLIn = []
    logFileSynScan = []
    logFileFTP = []
    i=0
    for d in dataLog:
        if(d["logtype"] == 3000):
            print(str(i) + " Data HTML Not Input")
            logFileHTMLIn.append(d)

        elif(d["logtype"] == 3001):
            print(str(i) + " Data HTML Input")
            logFileHTMLSign.append(d)

        # elif(d["logtype"] == 1001):
        #     print(str(i) + " Data Initiate")
        #     logFileHTMLIn.append(d)

        elif(d["logtype"] == 5001):
            print(str(i) + " Data Scan SYN")
            logFileSynScan.append(d)

        elif(d["logtype"] == 2000):
            print(str(i) + " Data FTP")
            # ada username dan password
            logFileFTP.append(d)

        i = i+1

    print("\nHTML IN")
    print(logFileHTMLIn) #3000
    print("\nHTML Sign")
    print(logFileHTMLSign) #3001
    print("\nSYN Scan")
    print(logFileSynScan) #5001
    print("\nFTP File")
    print(logFileSynScan) # 2000

    print("Log data for HTML: \n")
    i = 1
    for d in dataLog:
        # print(str(i)+": "+d["dst_host"])
        # print(d)
        if(len(d["logdata"]) == 6):
            print("Data "+str(i)+": ")
            print("\tDestination Port: " + str(d["dst_port"]))
            print("\tTime Accessed   : " + d["local_time"])
            print("\tSource Host IP  : " + d["src_host"])
            print("\tSource Host Port: " + str(d["src_port"])) 
            print("\tPassword Used   : " + d["logdata"]["PASSWORD"])
            print("\tUsername Used   : " + d["logdata"]["USERNAME"])
            print("\tUser Agent Used : " + d["logdata"]["USERAGENT"])
            i = i+1
            
def doInstallation():
    subprocess.call("./install.sh")

def startCanary():
    shellscript = subprocess.Popen(["start.sh"], stdin=subprocess.PIPE)
    shellscript.stdin.write("yes\n")
    shellscript.stdin.close()
    returncode = shellscript.wait()

# main
if __name__ == "__main__" :

    print("Initialized part 1")
    print("Activate Open Canary")

    i = 1
    #main loop
    while i == 1 :
        main_menu()
        nav = input("Choose a Menu (0 - 6) : ")
        if(int(nav) == 0):
            print("Menu About")
            fread = open("logfileScan.txt", "r")
            contents = fread.read()
            print(contents)
            fread.close()

        elif(int(nav) == 1):
            print("Menu Installation")
            doInstallation()

        elif(int(nav) == 2):
            print("Menu Configure Server")

        elif(int(nav) == 3):
            print("Menu Start Honeypot")
            startCanary()
            startCanary = True

        elif(int(nav) == 4):
            print("Menu Display Log")
            ProcessJson()

        elif(int(nav) == 5):
            print("Menu Stop Honeypot")
            os.system("opencanaryd --stop")
            startCanary = False

        elif(int(nav) == 6):
            print("Menu Exit")
            if(startCanary):
                print("Stop Decanary")
                os.system("opencanaryd --stop")
                os.system("clear")
            else:
                print("Out from program")
                os.system("clear")
            break
        raw_input("Press any button to continue")
        os.system("clear")

    
    # ReadWrite()

    
    
