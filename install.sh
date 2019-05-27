#!/bin/bash
sudo apt-get update
sudo apt-get install python-dev python-pip python-virtualenv wget curl samba build-essential libssl-dev libffi-dev libpcap-dev gcc g++
wget -c https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py
sudo apt-get -y remove ntp

virtualenv honeypot
cp -r opencanary honeypot
source honeypot/bin/activate
cd honeypot/opencanary
pip install opencanary scapy pcapy rdpy
opencanaryd --copyconfig
opencanaryd --start
