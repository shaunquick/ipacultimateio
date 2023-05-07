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

from ..common.common_lib import my_func_name

from ..common.validations import _IsValidRGBIntensityList
from ..common.validations import _IsValidState

from .ledgroupnamedefinitionslist import IsLedGroupNameDefinitionsFileFound
from .ledgroupnamedefinitionslist import InitLedGroupNameDefinitionsList
#from .ledgroupnamedefinitionslist import GetLedGroupNameDefinitions

from ..common.globalvar import MAX_LEDS

def InitLEDGroupNameModule(debug=False):
# This will initialise the LedGroupNames and pre-load the LedGroupName Definitions from the
# file LedGroupNameDefinitions.json in the folder ultimarcio/data
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    try :
        LedGroupDefsList = InitLedGroupNameDefinitionsList()
        Initialise_LedGroupNameList(LedGroupDefsList)
    except Exception as err:
        raise Exception("InitLedGroupNameModule {0}".format(err))


LED_GROUP_NAMES_LIST = []

def Initialise_LedGroupNameList(LEDGroupNameDefinitionsList, debug=False):
# Create a unique list of group names - these are independant of the Device that may be associated to the gruopname
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    global LED_GROUP_NAMES_LIST
    LED_GROUP_NAMES_LIST = []
    for LEDGroupNameDefinition in LEDGroupNameDefinitionsList:
        if ("LedGroupName" in LEDGroupNameDefinition):
            if LEDGroupNameDefinition["LedGroupName"] not in LED_GROUP_NAMES_LIST:
                if debug: print("Added GroupName" + str(LEDGroupNameDefinition["LedGroupName"]))
                LED_GROUP_NAMES_LIST.append(LEDGroupNameDefinition["LedGroupName"])
            else:
                if debug: print("Exception Add GroupName: " + str(LEDGroupNameDefinition["LedGroupName"]))
                raise Exception("InitLEDGroupNamesList(): Groupname replicated in LedGroupNamesDefinition.json")
                return()
    if debug: 
        print("InitLEDGroupNamesList(): List of LED Group names is")
        print(LED_GROUP_NAMES_LIST)

def Get_LedGroupNamesList(debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    global LED_GROUP_NAMES_LIST
    return(LED_GROUP_NAMES_LIST)


def _IsValidLedGroupName(LedGroupName, debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    if (type(LedGroupName) is not str): raise Exception("LedGroupName not in string format")
    if LedGroupName not in LED_GROUP_NAMES_LIST: 
        raise Exception(
            "LedGroupName not in list of Led Group Names in definitiona file: {0}, {1}".format(LedGroupName, LED_GROUP_NAMES_LIST))
        return(False)
    else:
        return(True)

def _IsValidLedGroupNameList(LedGroupNameList,debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    if (type(LedGroupNameList) is not list): raise Exception("_IsValidLedGroupNameList: LedGroupName is not a list")
    for LedGroupName in LedGroupNameList:
        try:
            _IsValidLedGroupName(LedGroupName)
        except Exception as err:
            raise Exception("_IsValidLedGroupNameList:{0} {1}".format(LedGroupName, err))        
    return(True)


def _IsValidLedGroupNameIntensityList(LedGroupNameIntensityList, debug=False):
# Validate that the structure and content of LedGroupNameIntensityList is correct
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")

    if (type(LedGroupNameIntensityList) is not list): raise Exception("LedGroupNameIntensityList is not a list")
    if len(LedGroupNameIntensityList) > MAX_LEDS: raise Exception("LedGroupNameIntensityList is > 96 Leds")
    for LedGroupNameIntensity in LedGroupNameIntensityList:
        try:
            _IsValidLedGroupName(LedGroupNameIntensity['LedGroupName'])
            _IsValidRGBIntensityList(LedGroupNameIntensity['RGBIntensity'])
        except Exception as err:
            raise Exception("_IsValidLedGroupNameIntensityList:{0} {1}".format(LedGroupNameIntensity, err))        
            
    return(True)

def _IsValidLedGroupNameStateList(LedGroupNameStateList, debug=False):
# Validate that the structure and content of LedGroupNameStateList is correct
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")

    if (type(LedGroupNameStateList) is not list): raise Exception("LedGroupNameStateList is not a list")
    for LedGroupNameState in LedGroupNameStateList:
        try:
            _IsValidLedGroupName(LedGroupNameState['LedGroupName'])
            _IsValidState(LedGroupNameState['State'])
        except Exception as err:
            raise Exception("_IsValidLedGroupNameStateList{0}: {1}".format(LedGroupNameState, err))        
        
    return(True)



if __name__ == '__main__':
    pass