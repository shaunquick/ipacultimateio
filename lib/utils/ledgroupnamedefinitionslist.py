# Copyright 2021-2021 Shaun Quick
# Copyright 2021-2021 contributors
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This is a common module that parse the LedGroupNameDefinitions.json file
# that resides in the data folder and holds the list in memory for use
# by other modules

import json
from importlib import resources

from ..common.common_lib import GetMyFuncName
from ..common.common_lib import IsDebugOn

from ..core.ipacultimateiodevicelist import  GetDeviceList

from ..utils.ledgroupname import IsValidLedGroupNameList

from ..common.validations import IsValidLedNr

LED_GROUP_DEFINITIONS = []
LedGroupDefinitionsFileFound = True
DEVICE_LED_GROUP_DEFINITIONS = {}

def InitialiseLedGroupNameDefinitionsList():
# Load the definitions file, validate it and keep the list in memory for later use
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    global LED_GROUP_DEFINITIONS
    global LedGroupDefinitionsFileFound
    global DEVICE_LED_GROUP_DEFINITIONS
# DEVICE_LED_GROUP_DEFINITIONS = {'53769:1040:1:3': [{'LedGroupName': 'p1b1', 'LedNrRGB': [16, 17, 18]}, 
#                                                    {'LedGroupName': 'p1b4', 'LedNrRGB': [19, 20, 21]}],
#                                  '53769:1040:1:4': [{'LedGroupName': 'p1b1', 'LedNrRGB': [16, 17, 18]}, 
#                                                    {'LedGroupName': 'p1b4', 'LedNrRGB': [19, 20, 21]}]                  }

    try :
#    with open("LedGroupNameDefinitions.json", "r") as read_file:
        with resources.open_text("data", "LedGroupNameDefinitions.json") as read_file:
            filecontent = read_file.read()
    except FileNotFoundError as err:
# the LedGroupNameDefinitions.json is not found - the flag is set to False which will be used IF the input script tries to use a 'LedGroupName' coommand
        LedGroupDefinitionsFileFound = False
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    if  LedGroupDefinitionsFileFound:
        LED_GROUP_DEFINITIONS = json.loads(filecontent)
        try:
            _isValidLedGroupNameDefinitions(LED_GROUP_DEFINITIONS)
            # so we know that the file is good - we now need to create the multiple devices with their LedGroupNames
            # especially when the device is not specified
            DeviceIDList=GetDeviceList()
            for myDevice in DeviceIDList:
                DEVICE_LED_GROUP_DEFINITIONS[myDevice["DeviceUUID"]] = []
                for LedGroupDefinition in LED_GROUP_DEFINITIONS:
                    if LedGroupDefinition.get("DeviceUUID") != None:
                        if LedGroupDefinition["DeviceUUID"] == myDevice["DeviceUUID"]:
                            #if IsDebugOn(): print("the device is matched add to current device")
                            #if IsDebugOn(): print("Values are")
                            myVals = LedGroupDefinition.copy()
                            myVals.pop("DeviceUUID")
                            if myVals.get("comment") != None:
                                myVals.pop("comment")
                            #if IsDebugOn(): print(myVals)
                            if len(myVals) > 0 :
                                DEVICE_LED_GROUP_DEFINITIONS[myDevice["DeviceUUID"]].append(myVals)
                        else:
                            if IsDebugOn(): print("Not a mathced device")
                            pass

                    else:
                        #if IsDebugOn(): print("No device specified - add to current device")
                        #if IsDebugOn(): print("Values are")
                        myVals = LedGroupDefinition.copy()
                        if myVals.get("comment") != None:
                            myVals.pop("comment")
                        #if IsDebugOn(): print(myVals)
                        if len(myVals) > 0 :
                            DEVICE_LED_GROUP_DEFINITIONS[myDevice["DeviceUUID"]].append(myVals)
        except Exception as err:
            raise Exception("{0}LedGroupNameDefinitions.json not in expected format: {1}".format(FUNC_NAME, err))
#           if IsDebugOn(): print("\n\n\n\nDEVICE_LED_GROUP_DEFINITIONS")
#           if IsDebugOn(): print(DEVICE_LED_GROUP_DEFINITIONS)
#           if IsDebugOn(): print("\n\n\n\nLED_GROUP_DEFINITIONS")
#           if IsDebugOn(): print(LED_GROUP_DEFINITIONS)

    return(LED_GROUP_DEFINITIONS)

def IsLedGroupNameDefinitionsFileFound():
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    global LedGroupDefinitionsFileFound
    return(LedGroupDefinitionsFileFound)

def GetLedGroupNameDefinitions():
    global LED_GROUP_DEFINITIONS

    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    return(LED_GROUP_DEFINITIONS)

def GetDeviceLedGroupNameDefinitions(DeviceUUID=None):
    global DEVICE_LED_GROUP_DEFINITIONS

    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    #if IsDebugOn(): print(DEVICE_LED_GROUP_DEFINITIONS)
    if DeviceUUID == None:
        return(DEVICE_LED_GROUP_DEFINITIONS)
    else:
        #if IsDebugOn(): print("Search for the device")
        if DeviceUUID in DEVICE_LED_GROUP_DEFINITIONS:
            #if IsDebugOn(): print("Found the device - let's return it")
            return({ DeviceUUID : DEVICE_LED_GROUP_DEFINITIONS.get(DeviceUUID) })
    raise Exception("{0}DeviceUUID not found : {1}".format(FUNC_NAME, DeviceUUID))


def _isValidLedGroupNameDefinition(LedGroupNameDefinition):
# validate the  definition    
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    try:
        if not LedGroupDefinitionsFileFound : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
        if "LedGroupName" in LedGroupNameDefinition:
            if not "LedNrRGB" in LedGroupNameDefinition:
                raise Exception("LedNrRGB name not found")
            else:
                if type(LedGroupNameDefinition["LedNrRGB"]) is not list :
                    raise Exception("LedNrRGB not a list: {0}".format(LedGroupNameDefinition))
                if len(LedGroupNameDefinition["LedNrRGB"]) < 3:
                    raise Exception("LedNrRGB expecting at least 3 values: {0}".format(LedGroupNameDefinition))
                for LedNr in LedGroupNameDefinition["LedNrRGB"]:
                    if not IsValidLedNr(LedNr):
                        raise Exception("LedNr not valid: {0}".format(LedGroupNameDefinition))
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
            
    return (True)

def _isValidLedGroupNameDefinitions(LedGroupNameDefinitions):
# validate the  definitions file content 
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if not LedGroupDefinitionsFileFound : raise Exception("LedGroupDefinitions.json did not load - cannot use LedGroupNames")
    
        if type(LedGroupNameDefinitions) is not list: raise Exception("LedGroupNameDefinitions is not a list")
        for LedGroupNameDefinition in LedGroupNameDefinitions:
            try:
                _isValidLedGroupNameDefinition(LedGroupNameDefinition)
            except Exception as err:
                raise Exception("Led Group Name Definition Invalid:{0}: {1}".format(LedGroupNameDefinition, err))        

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(True)




def ConvertLedGroupNameToDevicesLedNrList(DeviceUUID=None, LedGroupName=""):

#    DevicesLedNrList=[{"DeviceUUID":"0:0:0:0", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[4,5,6]}]

# 
# DEVICE_LED_GROUP_DEFINITIONS = {'53769:1040:1:3': [{'LedGroupName': 'p1b1', 'LedNrRGB': [16, 17, 18]}, 
#                                                    {'LedGroupName': 'p1b4', 'LedNrRGB': [19, 20, 21]}],
#                                  '53769:1040:1:4': [{'LedGroupName': 'p1b1', 'LedNrRGB': [16, 17, 18]}, 
#                                                    {'LedGroupName': 'p1b4', 'LedNrRGB': [19, 20, 21]}]



# translate the LedGroupName to its corresponding LedNrs.
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    DevicesLedNrList = []
    try:
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
        LedNrList = []
        for LedGroupNameDefinition in GetLedGroupNameDefinitions():
            if "LedGroupName" in LedGroupNameDefinition:
                if LedGroupNameDefinition["LedGroupName"] == LedGroupName : 
                    for Led in LedGroupNameDefinition["LedNrRGB"]:
                        LedNrList.append(Led)

        # if IsDebugOn(): print("{0}DeviceUUID is:{1}".format(FUNC_NAME, DeviceUUID))
        # if IsDebugOn(): print("{0}DeviceLEDGroupDefns is:{1}".format(FUNC_NAME, GetDeviceLedGroupNameDefinitions(DeviceUUID).items()))
        for myDeviceUUID, myDeviceLedGroupNames  in GetDeviceLedGroupNameDefinitions(DeviceUUID).items():
            if (DeviceUUID == None) or (DeviceUUID == myDeviceUUID): 
# Now check if the LedGroupName is in th list myDeviceLedGroupNames if so then add it to the dict.
                for myDeviceLedGroupName in myDeviceLedGroupNames:
                    if myDeviceLedGroupName['LedGroupName'] == LedGroupName:
                        DevicesLedNrList.append({"DeviceUUID" : myDeviceUUID, "LedNrList" : LedNrList})

#                if IsDebugOn(): print(myDeviceUUID)
#                if IsDebugOn(): print(myDeviceLedGroupNames)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
        if IsDebugOn(): print("{0} Dictionary is".format(FUNC_NAME))
        if IsDebugOn(): print(DevicesLedNrList)
    return(DevicesLedNrList)


def ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
#    DevicesLedNrList=[{"DeviceUUID":"0:0:0:0", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[4,5,6]}]
# We can then reference the values as DeviceLedNr["DevicUUID"] and DeviceLedNr["LedNrList"]
# # translate the LedGroupNameList to its corresponding Devices and LedNrs.
# Keep the GroupNameList in the same order
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DevicesLedNrList =[]
    try:
        if not IsValidLedGroupNameList(LedGroupNameList): raise Exception("LedGroupNameList not valid")
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
        for LedGroupName in LedGroupNameList:
            for DeviceLedNrList in ConvertLedGroupNameToDevicesLedNrList(DeviceUUID, LedGroupName):
                DevicesLedNrList.append(DeviceLedNrList)
            # Now I need to add to mey existing digtaionay
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
        if IsDebugOn(): print("DevicesLedNrList")
        if IsDebugOn(): print(DevicesLedNrList)

    return(DevicesLedNrList)


def _convertLedGroupNameStateToDevicesLedStateList(DeviceUUID, LedGroupNameState):
# translate the LedGroupNameStateList to its corresponding LedNrStateList.
#			"LedGroupNameStateList": [{"LedGroupName": "p1b1", "State": true},
#				{"LedGroupName": "p1b2","State": false}
#			]




# DevicesLedStateList=[{ "DeviceUUID":"0:0:0:0", "LedStateList": [ { "LedNr": "1", "State": True},  { "LedNr": "2", "State": True}],
#                    { "DeviceUUID":"0:0:0:2", "LedStateList": [ "LedNr": "3", "State": True}, { "LedNr": "1", "State": True}],
#                    { "DeviceUUID":"0:0:0:0", "LedStateList": [ "LedNr": "5", "State": True}, { "LedNr": "1", "State": True}],
#                    { "DeviceUUID":"0:0:0:0", "LedStateList": [ "LedNr": "6", "State": True},  { "LedNr": "1", "State": True}]]


    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DevicesLedStateList = []
    try:
        LedStateList = []
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
        for LedGroupNameDefinition in GetLedGroupNameDefinitions():
            if "LedGroupName" in LedGroupNameDefinition:
                if LedGroupNameDefinition["LedGroupName"] == LedGroupNameState["LedGroupName"] :
                    for Led in LedGroupNameDefinition["LedNrRGB"]:
                        LedStateList.append({"LedNr": Led, "State": LedGroupNameState["State"]})

        for myDeviceUUID, myDeviceLedGroupNames  in GetDeviceLedGroupNameDefinitions(DeviceUUID).items():
            if (DeviceUUID == None) or (DeviceUUID == myDeviceUUID): 
# Now check if the LedGroupName is in th list myDeviceLedGroupNames if so then add it to the dict.
                for myDeviceLedGroupName in myDeviceLedGroupNames:
                    if myDeviceLedGroupName['LedGroupName'] == LedGroupNameState["LedGroupName"]:
                        DevicesLedStateList.append({"DeviceUUID" : myDeviceUUID, "LedNrStateList" : LedStateList })

        # if IsDebugOn(): print("{0} DevicesStateList :".format(FUNC_NAME,DevicesLedStateList))

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(DevicesLedStateList)


def ConvertLedGroupNameStateListToDevicesLedStateList(DeviceUUID, LedGroupNameStateList):
# translate the LedGroupNameStateList to its corresponding LedNrStateList.
#			"LedGroupNameStateList": [{"LedGroupName": "p1b1", "State": true},
#				{"LedGroupName": "p1b2","State": false}
#			]

# DevicesLedStateList=[{ "DeviceUUID":"0:0:0:0", "LedStateList": [ { "LedNr": "1", "State": True},  { "LedNr": "2", "State": True}],
#                    { "DeviceUUID":"0:0:0:2", "LedStateList": [ "LedNr": "3", "State": True}, { "LedNr": "1", "State": True}],
#                    { "DeviceUUID":"0:0:0:0", "LedStateList": [ "LedNr": "5", "State": True}, { "LedNr": "1", "State": True}],
#                    { "DeviceUUID":"0:0:0:0", "LedStateList": [ "LedNr": "6", "State": True},  { "LedNr": "1", "State": True}]]


    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DevicesLedStateList = []

    try:
    
        for LedGroupNameState in LedGroupNameStateList:
            for DeviceLedStateList in _convertLedGroupNameStateToDevicesLedStateList(DeviceUUID, LedGroupNameState):
                DevicesLedStateList.append(DeviceLedStateList)

        # if IsDebugOn(): print("{0} DevicesLedStateList:".format(FUNC_NAME,DevicesLedStateList))

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(DevicesLedStateList)


def _convertLedGroupNameIntensityToDevicesLedNrAndIntensityList(DeviceUUID, LedGroupNameIntensity):
# DevicesLedIntensityList=[{ "DeviceUUID":"0:0:0:0", "LedIntensityList": [ { "LedNr": "1", "IntensityLevel": 34},  { "LedNr": "2", "IntensityLevel": 223}],
#                    { "DeviceUUID":"0:0:0:2", "LedIntensityList": [ "LedNr": "3", "IntensityLevel": 32}, { "LedNr": "1", "IntensityLevel": 134}],
#                    { "DeviceUUID":"0:0:0:0", "LedIntensityList": [ "LedNr": "5", "IntensityLevel": 11}, { "LedNr": "1", "IntensityLevel": 156}],
#                    { "DeviceUUID":"0:0:0:0", "LedIntensityList": [ "LedNr": "6", "IntensityLevel": 98},  { "LedNr": "1", "IntensityLevel": 111}]]


# translate the LedGroupNameIntensityList to its corresponding LedNrAndIntensityList.
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DevicesLedIntensityList = []
    try:
        LedIntensityList = []
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupDefinitions.json did not load - cannot use LedGroupNames")
    
        for LedGroupNameDefinition in GetLedGroupNameDefinitions():
            if "LedGroupName" in LedGroupNameDefinition:
                if LedGroupNameDefinition["LedGroupName"] == LedGroupNameIntensity["LedGroupName"] :
                    counter = 0
                    for Led in LedGroupNameDefinition["LedNrRGB"]:
                        LedIntensityList.append({"LedNr": Led, "IntensityLevel": LedGroupNameIntensity["RGBIntensity"][counter]})
                        counter += 1
#                    break
 
        
        for myDeviceUUID, myDeviceLedGroupNames  in GetDeviceLedGroupNameDefinitions(DeviceUUID).items():
            if (DeviceUUID == None) or (DeviceUUID == myDeviceUUID): 
# Now check if the LedGroupName is in th list myDeviceLedGroupNames if so then add it to the dict.
                for myDeviceLedGroupName in myDeviceLedGroupNames:
                    if myDeviceLedGroupName['LedGroupName'] == LedGroupNameIntensity["LedGroupName"]:
                        DevicesLedIntensityList.append({"DeviceUUID" : myDeviceUUID, "LedNrAndIntensityList" : LedIntensityList})
                        

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
       
#    if IsDebugOn(): print(DevicesLedIntensityList)
    return(DevicesLedIntensityList)


def ConvertLedGroupNameIntensityListToDevicesLedNrAndIntensityList(DeviceUUID, LedGroupNameIntensityList):
# DevicesLedIntensityList=[{ "DeviceUUID":"0:0:0:0", "LedIntensityList": [ { "LedNr": "1", "IntensityLevel": 34},  { "LedNr": "2", "IntensityLevel": 223}],
#                    { "DeviceUUID":"0:0:0:2", "LedIntensityList": [ "LedNr": "3", "IntensityLevel": 32}, { "LedNr": "1", "IntensityLevel": 134}],
#                    { "DeviceUUID":"0:0:0:0", "LedIntensityList": [ "LedNr": "5", "IntensityLevel": 11}, { "LedNr": "1", "IntensityLevel": 156}],
#                    { "DeviceUUID":"0:0:0:0", "LedIntensityList": [ "LedNr": "6", "IntensityLevel": 98},  { "LedNr": "1", "IntensityLevel": 111}]]


# translate the LedGroupNameIntensityList to its corresponding LedNrAndIntensityList.
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DevicesLedIntensityList = []
    try:       
        for LedGroupNameIntensity in LedGroupNameIntensityList:
            for DeviceLedIntensityList in _convertLedGroupNameIntensityToDevicesLedNrAndIntensityList(DeviceUUID, LedGroupNameIntensity):
                DevicesLedIntensityList.append(DeviceLedIntensityList)
        #if IsDebugOn(): print(DevicesLedIntensityList)

                    
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
        
    return(DevicesLedIntensityList)






if __name__ == '__main__':
    pass