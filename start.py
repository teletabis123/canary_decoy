#!/bin/bash
import os

contents = ""
json = ""

def main_menu() :
    print("     0. About")
    print("     1. Installation")
    print("     2. Configure Server")
    print("     3. Start HoneyPot")
    print("     4. Display Log")
    print("     5. Exit")

def ReadFile():
    global contents
    fread = open("opencanary.log", "r")
    contents = fread.read()
    fread.close()
    
def Parser():
    global contents
    global json
    data = contents.split("\n")
    print("Data:\n")
    for d in data :
        print(d+"\n")
    
    json = "[\n"
    for i in range (0, len(data)):
        if i != 0  and i != len(data)-1:
            json = json + ", \n"
        json = json + "\t"+ data[i] 
    json = json + "\n]"
    print("Json: \n"+json)

def WriteFile():
    global json
    fwrite = open("logfile.txt", "w+")
    fwrite.write(json)
    fwrite.close()

# main
if __name__ == "__main__" :
    # os.system("sudo apt-get update")
    # os.system("sudo apt-get install python-dev python-pip python-virtualenv wget curl samba build-essential libssl-dev libffi-dev libpcap-dev gcc g++")
    # os.system("wget -c https://bootstrap.pypa.io/get-pip.py")
    # os.system("python get-pip.py")
    # os.system("rm get-pip.py")
    # os.system("sudo apt-get -y remove ntp")
    # os.system("clear")

    print("Initialized part 1")
    print("Activate Open Canary")

    # #os.system("apt-get update")
    # os.system("virtualenv honeypot")
    # os.system("source honeypot/bin/activate")
    # #os.system("cd opencanary")
    # os.system("pip install opencanary scapy pcapy rdpy")
    # os.system("opencanaryd --copyconfig")
    # #os.system("opencanaryd --start")
    # #os.system("opencanaryd --stop")

    i = 1
    #main loop
    while i == 1 :
        main_menu()
        break

    ReadFile()
    print("Contents: "+contents)
    Parser()
    WriteFile()
    
