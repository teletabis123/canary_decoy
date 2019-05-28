#!/bin/bash
import os
import json
# import rhinoscriptsyntax as rs

contents = ""
json_str = ""

def main_menu() :
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
    f = open("logfile.txt","r")
    data = f.read()
    dataLog = json.loads(data)
    
    # print(dataLog)

    i = 1
    for d in dataLog:
        print(str(i)+": "+d["dst_host"])
        i = i+1
        # print(d)
        if(len(d["logdata"]) == 6):
            print("data: \n")
            print("\tDestination Port: " + str(d["dst_port"]))
            print("\tTime Accessed   : " + d["local_time"])
            print("\tSource Host IP  : " + d["src_host"])
            print("\tSource Host Port: " + str(d["src_port"])) 
            print("\tPassword Used   : " + d["logdata"]["PASSWORD"])
            print("\tUsername Used   : " + d["logdata"]["USERNAME"])
            print("\tUser Agent Used : " + d["logdata"]["USERAGENT"])
            


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
    # print("Contents: "+contents)
    Parser()
    WriteFile()
    # ReadWrite()

    ProcessJson()
    
