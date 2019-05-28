import json
from os.path import expanduser
import os
#import __root__

#confPath = "~/.opencanary.conf"
#confPath = os.path.dirname(__file__) + ".opencanary.conf"
#confPath = "../../.opencanary.conf"
#path = os.cwd()
confPath = expanduser("~") + "/.opencanary.conf"

def main():
    print("Configure opencanary as:")
    print("1. Linux default")
    print("2. Windows default")
    print("3. Default configuration")
    print("4. Manual configuration")
    while True :
        choose = int(input("Choose: "))
        if choose == 1:
            setLinuxDefault()
            break
        elif choose == 2:
            setWindowsDefault()
            break
        elif choose == 3:
            defaultSetting()
            break
        elif choose == 4:
            manualSetting()
            break
        elif choose == 0:
            test()
            break
        
        print("Choose invalid. choose again")

def setLinuxDefault():
    print("in function setLinuxDefault")
    
    # Baca linux.conf
    source = open("linux.conf", "r") #path ganti pas di kali
    sourceContent = source.read()
    source.close()

    # Baca .opencanary.conf
    destTest = open(confPath, "r") 
    destTestContent = destTest.read()
    destTest.close()

    # Cek apakah mereka sama
    # checkConfig(sourceContent, destTestContent)

    # Tulis ke windows.conf ke .opencanary.conf
    dest = open(confPath, "w")
    dest.write(sourceContent)
    dest.close()

    print("Config file has been configured to Linux environtment")
    # Dari sini kebawah bisa di ignore (comment) pas di kali
    # Cek apakah copy berhasil apa ngga
    # destTest = open(".opencanary.conf", "r") # Tulis ke config yang udh ada
    # destTestContent = destTest.read()
    # destTest.close()
    # checkConfig(sourceContent, destTestContent)

def setWindowsDefault():
    #print("in function setWindowsDefault")

    # Baca windows.conf
    source = open("windows.conf", "r") #path ganti pas di kali
    sourceContent = source.read()
    source.close()

    # Baca .opencanary.conf
    destTest = open(confPath, "r") 
    destTestContent = destTest.read()
    destTest.close()

    # Cek apakah mereka sama
    # checkConfig(sourceContent, destTestContent)

    # Tulis ke windows.conf ke .opencanary.conf
    dest = open(confPath, "w")
    dest.write(sourceContent)
    dest.close()

    print("Config file has been configured to Windows environtment")

    # Dari sini kebawah bisa di ignore (comment) pas di kali
    # Cek apakah copy berhasil apa ngga
    # destTest = open(".opencanary.conf", "r") # Tulis ke config yang udh ada
    # destTestContent = destTest.read()
    # destTest.close()
    # checkConfig(sourceContent, destTestContent)

def defaultSetting():
    print("In function defaultSetting")

    # Baca default.conf
    source = open(".default.conf", "r") #path ganti pas di kali
    sourceContent = source.read()
    source.close()

    # Baca .opencanary.conf
    destTest = open(confPath, "r") 
    destTestContent = destTest.read()
    destTest.close()

    if(checkConfig(sourceContent, destTestContent)):
        print("Config file has been configured to default setting")
        return

    # Tulis ke windows.conf ke .opencanary.conf
    dest = open(confPath, "w")
    dest.write(sourceContent)
    dest.close()

    print("Config file has been configured to default setting")

def manualSetting():
    print("You have choosen the wrong path.\nNow you need to configure them all!!!!!!!!!!")
    #Ribetnya disini
    printThePorts()


def printThePorts():
    dest = open(confPath, "r")
    destContent = dest.read()
    dest.close()
    #print(destContent)
    jsonObject = json.loads(destContent)
    #print(jsonObject["ftp.enabled"])

    print("1. FTP") # 21
    print("2. SSH") # 22
    print("3. Telnet") # 23
    print("4. TFTP") # 69
    print("5. HTTP") # 80
    print("6. NTP") # 123
    print("7. SNMP") # 161
    print("8. MSSQL") # 1433
    print("9. MySQL") # 3306
    print("10. VCN") # 5000
    print("11. HTTP Proxy") # 8080
    select = 0
    while True:
        #select = [int(select) for select in input("Choose (separated with space): ").split()]
        select = list(map(int, input("Input the numbers: ").split()))
        if (max(select) <= 11 and min(select) >= 1):
            break
        print("One or more input is invalid!!")
    #print(select)
    for n in select:
        jsonName = convertInputToJsonName(n)
        jsonObject[jsonName] = True

    jsonResult = json.dumps(jsonObject, indent=4)
    print(jsonResult)    

    res = open(confPath, "w")
    res.write(jsonResult)
    res.close()

def convertInputToJsonName(n):
    if(n == 1): return "ftp.enabled"
    if(n == 2): return "ssh.enabled"
    if(n == 3): return "telnet.enabled"
    if(n == 4): return "tftp.enabled"
    if(n == 5): return "http.enabled"
    if(n == 6): return "ntp.enabled"
    if(n == 7): return "snmp.enabled"
    if(n == 8): return "mssql.enabled"
    if(n == 9): return "mysql.enabled"
    if(n == 10): return "vcn.enabled"
    if(n == 11): return "httpproxy.enabled"

def checkConfig(config1, config2):
    if config1 == config2:
        #print("Config file is the same")
        return True
    else:
        #print("Config file is different")
        return False

if __name__ == "__main__":
    main()
