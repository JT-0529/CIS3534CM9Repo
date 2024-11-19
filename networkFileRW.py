#!/usr/bin/env python3
#networkFileRW.py
#Joslen Tardencilla
#Thursday, November 18, 2024
#Update routers and switches;
#read equipment from a file, write updates & errors to file

##---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Could not find json module")

##---->>>> Create file constants for the file names; file constants can be reused
EQUIP_R = 'equip_r.txt'
EQUIP_S = 'equip_s.txt'
UPDATED_EQUIP = 'updated.txt'
BAD_IP = 'errors.txt'

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    # Open and read files into dictionaries
    with open(EQUIP_R) as inFile:
        routers = json.load(inFile)

    with open(EQUIP_S) as inFile:
        switches = json.load(inFile)

    updated = {}
    invalidIPAddresses = []
    devicesUpdatedCount = 0
    invalidIPCount = 0
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items():
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        # Get valid device
        device = getValidDevice(routers, switches)
        if device == 'x':
            quitNow = True
            break
        
        # Get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        # Update device
        if 'r' in device:
            routers[device] = ipAddress
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    print("\nSummary:")
    print("Number of devices updated:", devicesUpdatedCount)

    # Write updated data to file
    with open(UPDATED_EQUIP, 'w') as outFile:
        json.dump(updated, outFile)

    print("Updated equipment written to file 'updated.txt'")

    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write invalid IP addresses to file
    with open(BAD_IP, 'w') as outFile:
        json.dump(invalidIPAddresses, outFile)

    print("List of invalid addresses written to file 'errors.txt'")

if __name__ == "__main__":
    main()
