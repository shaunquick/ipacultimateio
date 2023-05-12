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


# This module validate led group name lists that are used oin the command
# scripts. It is converts from the led group name to the list of Led
# Numbers that it has been defined for. The Led NUmbers are normally
# be expected to match the LED Numbers on the ipac Ultimate IO Board
# and would normally bt the RGB numbers for a particular 'group name'
# THere is no check that this happends so you could if you really
# wanted to is to sleect multple led nrs and string them into a list


from ..common.common_lib import GetMyFuncName
from ..common.common_lib import IsDebugOn

from ..common.validations import IsValidRGBIntensityList
from ..common.validations import IsValidState

from ..common.globalvar import MAX_LEDS

LED_GROUP_NAMES_LIST = []


def InitialiseLedGroupNameList(LEDGroupNameDefinitionsList):
# Create a unique list of group names - these are independant of the Device that may be associated to the gruopname
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        global LED_GROUP_NAMES_LIST
        LED_GROUP_NAMES_LIST = []
        for LEDGroupNameDefinition in LEDGroupNameDefinitionsList:
            if ("LedGroupName" in LEDGroupNameDefinition):
                if LEDGroupNameDefinition["LedGroupName"] not in LED_GROUP_NAMES_LIST:
                    # if IsDebugOn(): print("Added GroupName" + str(LEDGroupNameDefinition["LedGroupName"]))
                    LED_GROUP_NAMES_LIST.append(LEDGroupNameDefinition["LedGroupName"])
                else:
                    # if IsDebugOn(): print("Exception Add GroupName: " + str(LEDGroupNameDefinition["LedGroupName"]))
                    raise Exception("{0} Groupname replicated in LedGroupNamesDefinition.json".format(FUNC_NAME))
                    return()
    #    if IsDebugOn(): 
    #        print("InitLEDGroupNamesList(): List of LED Group names is")
    #        print(LED_GROUP_NAMES_LIST)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def Get_LedGroupNamesList():
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    global LED_GROUP_NAMES_LIST
    return(LED_GROUP_NAMES_LIST)


def IsValidLedGroupName(LedGroupName):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    if (type(LedGroupName) is not str): raise Exception("LedGroupName not in string format")
    if LedGroupName not in LED_GROUP_NAMES_LIST: 
        raise Exception(
            "{0} LedGroupName not in list of Led Group Names in definitiona file: {1}, {2}".format(FUNC_NAME, LedGroupName, LED_GROUP_NAMES_LIST))
        return(False)
    else:
        return(True)

def IsValidLedGroupNameList(LedGroupNameList):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    if (type(LedGroupNameList) is not list): raise Exception("{0} LedGroupName is not a list".format(FUNC_NAME))
    for LedGroupName in LedGroupNameList:
        try:
            IsValidLedGroupName(LedGroupName)
        except Exception as err:
            raise Exception("{0}:{1} {2}".format(FUNC_NAME,LedGroupName, err))        
    return(True)


def IsValidLedGroupNameIntensityList(LedGroupNameIntensityList):
# Validate that the structure and content of LedGroupNameIntensityList is correct
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if (type(LedGroupNameIntensityList) is not list): raise Exception("LedGroupNameIntensityList is not a list")
        if len(LedGroupNameIntensityList) > MAX_LEDS: raise Exception("LedGroupNameIntensityList is > 96 Leds")
        for LedGroupNameIntensity in LedGroupNameIntensityList:
            try:
                IsValidLedGroupName(LedGroupNameIntensity['LedGroupName'])
                IsValidRGBIntensityList(LedGroupNameIntensity['RGBIntensity'])
            except Exception as err:
                raise Exception("{0}:{1} {2}".format(FUNC_NAME, LedGroupNameIntensity, err))        
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
            
    return(True)

def IsValidLedGroupNameStateList(LedGroupNameStateList=[]):
# Validate that the structure and content of LedGroupNameStateList is correct
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    if (type(LedGroupNameStateList) is not list): raise Exception("LedGroupNameStateList is not a list")
    for LedGroupNameState in LedGroupNameStateList:
        try:
            IsValidLedGroupName(LedGroupNameState['LedGroupName'])
            IsValidState(LedGroupNameState['State'])
        except Exception as err:
            raise Exception("{0}{1}: {2}".format(FUNC_NAME,LedGroupNameState, err))        
        
    return(True)



if __name__ == '__main__':
    pass