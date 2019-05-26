#!/bin/bash
import os

# main
if __name__ == "__main__" :
    os.system("sudo apt-get update")
    os.system("sudo apt-get install python-dev python-pip python-virtualenv wget curl samba build-essential libssl-dev libffi-dev libpcap-dev gcc g++")
    os.system("wget -c https://bootstrap.pypa.io/get-pip.py")
    os.system("python get-pip.py")
    os.system("rm get-pip.py")
    os.system("sudo apt-get -y remove ntp")
    os.system("clear")

    print("Initialized part 1")
    print("Activate Open Canary")

    #os.system("apt-get update")
    os.system("virtualenv honeypot")
    os.system("source honeypot/bin/activate")
    #os.system("cd opencanary")
    os.system("pip install opencanary scapy pcapy rdpy")
    os.system("opencanaryd --copyconfig")
    #os.system("opencanaryd --start")
    #os.system("opencanaryd --stop")

    i = 1
    #main loop
    while i == 1 :
        break
