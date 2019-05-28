#!/bin/bash

virtualenv honeypot
cp -r opencanary honeypot
source honeypot/bin/activate
cd honeypot/opencanary
pip install opencanary scapy pcapy rdpy
opencanaryd --copyconfig
opencanaryd --start