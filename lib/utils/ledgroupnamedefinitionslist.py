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



#from dataclasses import dataclass
from ast import Try
import json
from importlib import resources

from ..common.common_lib import my_func_name


from ..core.ipacultimateiodevicelist import  Get_DeviceList



from ..common.globalvar import MAX_LEDS

LED_GROUP_DEFINITIONS = []
LedGroupDefinitionsFileFound = True
DEVICE_LED_GROUP_DEFINITIONS = {}


def InitLedGroupNameDefinitionsList(debug=False):
# Load the definitions file, validate it and keep the list in memory for later use
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

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
            DeviceIDList=Get_DeviceList()
            for myDevice in DeviceIDList:
                DEVICE_LED_GROUP_DEFINITIONS[myDevice["DeviceUUID"]] = []
                for LedGroupDefinition in LED_GROUP_DEFINITIONS:
                    if LedGroupDefinition.get("DeviceUUID") != None:
                        if LedGroupDefinition["DeviceUUID"] == myDevice["DeviceUUID"]:
                            #if debug: print("the device is matched add to current device")
                            #if debug: print("Values are")
                            myVals = LedGroupDefinition.copy()
                            myVals.pop("DeviceUUID")
                            if myVals.get("comment") != None:
                                myVals.pop("comment")
                            #if debug: print(myVals)
                            if len(myVals) > 0 :
                                DEVICE_LED_GROUP_DEFINITIONS[myDevice["DeviceUUID"]].append(myVals)
                        else:
                            if debug: print("Not a mathced device")
                            pass

                    else:
                        #if debug: print("No device specified - add to current device")
                        #if debug: print("Values are")
                        myVals = LedGroupDefinition.copy()
                        if myVals.get("comment") != None:
                            myVals.pop("comment")
                        #if debug: print(myVals)
                        if len(myVals) > 0 :
                            DEVICE_LED_GROUP_DEFINITIONS[myDevice["DeviceUUID"]].append(myVals)
        except Exception as err:
            raise Exception("{0}LedGroupNameDefinitions.json not in expected format: {1}".format(FUNC_NAME, err))
#        if debug:
#           print("\n\n\n\nDEVICE_LED_GROUP_DEFINITIONS")
#           print(DEVICE_LED_GROUP_DEFINITIONS)
#           print("\n\n\n\nLED_GROUP_DEFINITIONS")
#           print(LED_GROUP_DEFINITIONS)

    return(LED_GROUP_DEFINITIONS)

def IsLedGroupNameDefinitionsFileFound(debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    global LedGroupDefinitionsFileFound
    return(LedGroupDefinitionsFileFound)

def GetLedGroupNameDefinitions(debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)
    global LED_GROUP_DEFINITIONS
    return(LED_GROUP_DEFINITIONS)

def GetDeviceLedGroupNameDefinitions(DeviceUUID=None, debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    global DEVICE_LED_GROUP_DEFINITIONS
    if DeviceUUID == None:
        return(DEVICE_LED_GROUP_DEFINITIONS)
    else:
        return(DEVICE_LED_GROUP_DEFINITIONS[DeviceUUID])


def _isValidLedGroupNameDefinition(LedGroupNameDefinition, debug=False):
# validate the  definition    
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

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
                if not (LedNr  >= 0 and LedNr  < MAX_LEDS) :
                    raise Exception("LedNr not between 0 and 95: {0}".format(LedGroupNameDefinition))
            
    return (True)

def _isValidLedGroupNameDefinitions(LedGroupNameDefinitions, debug=False):
# validate the  definitions file content 
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    if not LedGroupDefinitionsFileFound : raise Exception("LedGroupDefinitions.json did not load - cannot use LedGroupNames")
    
    if type(LedGroupNameDefinitions) is not list: raise Exception("LedGroupNameDefinitions is not a list")
    for LedGroupNameDefinition in LedGroupNameDefinitions:
        try:
            _isValidLedGroupNameDefinition(LedGroupNameDefinition)
        except Exception as err:
            raise Exception("Led Group Name Definition Invalid:{0}: {1}".format(LedGroupNameDefinition, err))        
    return(True)




def _convertLedGroupNameToDevicesLedNrList(LedGroupName, debug=False):
# DevicesLedNrList=[{"DeviceUUID":"0:0:0:0", "LedNrList" : [1,2,3] },
#                   {"DeviceUUID":"0:0:0:1", "LedNrList" : [1,2,3] }]
# 
# DEVICE_LED_GROUP_DEFINITIONS = {'53769:1040:1:3': [{'LedGroupName': 'p1b1', 'LedNrRGB': [16, 17, 18]}, 
#                                                    {'LedGroupName': 'p1b4', 'LedNrRGB': [19, 20, 21]}],
#                                  '53769:1040:1:4': [{'LedGroupName': 'p1b1', 'LedNrRGB': [16, 17, 18]}, 
#                                                    {'LedGroupName': 'p1b4', 'LedNrRGB': [19, 20, 21]}]



# translate the LedGroupName to its corresponding LedNrs.
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)


    try:
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
        DevicesLedNrList = {}
        LedNrList = []
        for LedGroupNameDefinition in GetLedGroupNameDefinitions():
            if "LedGroupName" in LedGroupNameDefinition:
                if LedGroupNameDefinition["LedGroupName"] == LedGroupName : 
                    for Led in LedGroupNameDefinition["LedNrRGB"]:
                        LedNrList.append(Led)
                    break
        for myDeviceGroupName in GetDeviceLedGroupNameDefinitions():
            if debug: print(myDeviceGroupName)

            pass
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(DevicesLedNrDict)


def _convertLedGroupNameListToDevicesLedNrList(LedGroupNameList, debug=False):
# DevicesLedNrList=[{"DeviceUUID":"0:0:0:0", "LedNrList" : [1,2,3] },
#                   {"DeviceUUID":"0:0:0:1", "LedNrList" : [1,2,3] }]
# We can then reference the values as DeviceLedNr["DevicUUID"] and DeviceLedNr["LedNrList"]
# # translate the LedGroupNameList to its corresponding Devices and LedNrs.
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    try:
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
        for LedGroupName in LedGroupNameList:
            myNewDevicesLedNrDict=_convertLedGroupNameToDevicesLedNrDict(LedGroupName)
            # Now I need to add to mey existing digtaionay
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(DevicesLedNrDict)

#def _convertLedGroupNameStateListToDevicesLedStateDict(LedGroupNameStateList):
def _convertLedGroupNameStateListToDevicesLedStateDict(LedGroupNameStateList, debug=False):
# translate the LedGroupNameStateList to its corresponding LedNrStateList.
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    try:
        DevicesLedStateDict = {}
        LedStateList = []
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
        for LedGroupNameState in LedGroupNameStateList:
            for LedGroupNameDefinition in GetLedGroupNameDefinitions():
                if "LedGroupName" in LedGroupNameDefinition:
                    if LedGroupNameDefinition["LedGroupName"] == LedGroupNameState["LedGroupName"] :
                        for Led in LedGroupNameDefinition["LedNrRGB"]:
                            LedStateList.append({"LedNr": Led, "State": LedGroupNameState["State"]})
                        break

        for myDeviceGroupName in GetDeviceLedGroupNameDefinitions():
            pass
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(DevicesLedStateDict)


#def _convertLedGroupNameIntensityListToDevicesLedNrIntensityDict(LedGroupNameIntensityList):
def _convertLedGroupNameIntensityListToDevicesLedNrIntensityDict(LedGroupNameIntensityList, debug=False):
# translate the LedGroupNameIntensityList to its corresponding LedNrIntensityList.
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    try:
        LedIntensityList = []
        if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupDefinitions.json did not load - cannot use LedGroupNames")
    
        for LedGroupNameIntensity in LedGroupNameIntensityList:
            for LedGroupNameDefinition in GetLedGroupNameDefinitions():
                if "LedGroupName" in LedGroupNameDefinition:
                    if LedGroupNameDefinition["LedGroupName"] == LedGroupNameIntensity["LedGroupName"] :
                        counter = 0
                        for Led in LedGroupNameDefinition["LedNrRGB"]:
                            LedIntensityList.append({"LedNr": Led, "IntensityLevel": LedGroupNameIntensity["RGBIntensity"][counter]})
                            counter += 1
                        break
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
        
    return(LedIntensityList)






if __name__ == '__main__':
    pass