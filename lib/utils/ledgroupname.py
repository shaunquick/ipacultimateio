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

from ..common.validations import _IsValidRGBIntensityList
from ..common.validations import _IsValidState

from .ledgroupnamedefinitionslist import IsLedGroupNameDefinitionsFileFound
from .ledgroupnamedefinitionslist import InitLedGroupNameDefinitionsList
from .ledgroupnamedefinitionslist import GetLedGroupNameDefinitions

from .ledgroupnameslist import InitLedGroupNamesList

from .ledgroupnameslist import _IsValidLedGroupName

from ..common.globalvar import MAX_LEDS

def InitLedGroupNameModule():
# This will initialise the LedGroupNames and pre-load the LedGroupName Definitions from the
# file LedGroupNameDefinitions.json in the folder ultimarcio/data
    try :
        LedGroupDefsList = InitLedGroupNameDefinitionsList()
        InitLedGroupNamesList(LedGroupDefsList)
    except Exception as err:
        raise Exception("InitLedGroupNameModule {0}".format(err))
 
def _IsValidLedGroupNameList(LedGroupNameList):
    if (type(LedGroupNameList) is not list): raise Exception("_IsValidLedGroupNameList: LedGroupName is not a list")
    for LedGroupName in LedGroupNameList:
        try:
            _IsValidLedGroupName(LedGroupName)
        except Exception as err:
            raise Exception("_IsValidLedGroupNameList:{0} {1}".format(LedGroupName, err))        
    return(True)


def _IsValidLedGroupNameIntensityList(LedGroupNameIntensityList):
# Validate that the structure and content of LedGroupNameIntensityList is correct
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

def _IsValidLedGroupNameStateList(LedGroupNameStateList):
# Validate that the structure and content of LedGroupNameStateList is correct
    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")

    if (type(LedGroupNameStateList) is not list): raise Exception("LedGroupNameStateList is not a list")
    for LedGroupNameState in LedGroupNameStateList:
        try:
            _IsValidLedGroupName(LedGroupNameState['LedGroupName'])
            _IsValidState(LedGroupNameState['State'])
        except Exception as err:
            raise Exception("_IsValidLedGroupNameStateList{0}: {1}".format(LedGroupNameState, err))        
        
    return(True)



def _convertLEDGroupNameToLedNrList(LedGroupName):
# translate the LedGroupName to its corresponding LedNrs.
    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    LedNrList = []
    for LedGroupNameDefinition in GetLedGroupNameDefinitions():
        if "LedGroupName" in LedGroupNameDefinition:
            if LedGroupNameDefinition["LedGroupName"] == LedGroupName : 
                for Led in LedGroupNameDefinition["LedNrRGB"]:
                    LedNrList.append(Led)
                break
    return(LedNrList)


def _convertLEDGroupNameListToLedNrList(LedGroupNameList):
# translate the LedGroupNameList to its corresponding LedNrs.
    LedNrList= []
    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
    for LedGroupName in LedGroupNameList:
        LedNrList.extend(_convertLEDGroupNameToLedNrList(LedGroupName))
    return(LedNrList)



def _convertLEDGroupNameStateListToLedStateList(LedGroupNameStateList):
# translate the LedGroupNameStateList to its corresponding LedNrStateList.
    LedStateList = []
    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
    for LedGroupNameState in LedGroupNameStateList:
        for LedGroupNameDefinition in GetLedGroupNameDefinitions():
            if "LedGroupName" in LedGroupNameDefinition:
                if LedGroupNameDefinition["LedGroupName"] == LedGroupNameState["LedGroupName"] :
                    for Led in LedGroupNameDefinition["LedNrRGB"]:
                        LedStateList.append({"LedNr": Led, "State": LedGroupNameState["State"]})
                    break
    return(LedStateList)


def _convertLEDGroupNameIntensityListToLedNrIntensityList(LedGroupNameIntensityList):
# translate the LedGroupNameIntensityList to its corresponding LedNrIntensityList.
    LedIntensityList = []
    if not IsLedGroupNameDefinitionsFileFound() : raise Exception("LedGroupDefinitions.json did not load - cannot use LedGroupNames")
    
    for LedGroupNameIntensity in LedGroupNameIntensityList:
        for LedGroupNameDefinition in GetLedGroupNameDefinitions():
            if "LedGroupName" in LedGroupNameDefinition:
                if LedGroupNameDefinition["LedGroupName"] == LedGroupNameIntensity["LedGroupName"] :
                    for Led in LedGroupNameDefinition["LedNrRGB"]:
                        LedIntensityList.append({"LedNr": Led, "IntensityLevel": LedGroupNameIntensity["RGBIntensity"][1]})
                    break
        
    return(LedIntensityList)


if __name__ == '__main__':
    pass