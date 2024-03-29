# Copyright 2021-2021 Shaun Quick
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

# This utility will validate that all the commands to be sent to the LED
# Board have the correct format and paramaters.
# If there are errors an exception will be raised

from ..common.common_lib    import GetMyFuncName
from ..common.common_lib    import IsDebugOn

from .ledgroupname          import IsValidLedGroupNameList
from .ledgroupname          import IsValidLedGroupNameStateList
from .ledgroupname          import IsValidLedGroupNameIntensityList
from .ledgroupname          import IsValidLedGroupName 
from ..common.validations   import IsValidWaitIntervalTime
from ..common.validations   import IsValidFadeIntervalTime
from ..common.validations   import IsValidIntensityLevel
from ..common.validations   import IsValidLedNr
from ..common.validations   import IsValidLedNrList
from ..common.validations   import IsValidLedNrAndIntensityList
from ..common.validations   import IsValidFlashCount
from ..common.validations   import IsValidFlashIntervalTime
from ..common.validations   import IsValidState
from ..common.validations   import IsValidLedNrStateList
from ..common.validations   import IsValidFadeIncrement
from ..common.validations   import IsValidNrOfRepetitions
from ..common.validations   import IsValidNrCommandsToRepeat
from ..common.validations   import IsValidRGBIntensityList
from ..common.validations   import IsValidCycleIntervalTime
from ..common.validations   import IsValidNrCycles



def _isValidCommand(Command):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

# check that we have a Command a valid Function name and each function has the correct paramaters required
    if not "Command" in Command: raise Exception("Command missing: {0}".format(Command))
    if not "Function" in Command["Command"]: raise Exception("Function missing from Command : {0}".format(Command))
    if Command["Command"]["Function"] == "Wait":
        if not "WaitIntervalTime" in Command["Command"]: raise Exception("WaitIntervalTime missing from command : {0}".format(Command))
        if not IsValidWaitIntervalTime(Command["Command"]["WaitIntervalTime"]) : raise Exception("WaitIntervalTime invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetAllLedIntensities":
        if not "IntensityLevel" in Command["Command"]: raise Exception("IntensityLevel missing from command: {0}".format(Command))
        if not IsValidIntensityLevel(Command["Command"]["IntensityLevel"]) : raise Exception("IntensityLevel Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedNrToIntensityLevel":
        if not "LedNr" in Command["Command"]: raise Exception("LedNr missing from command: {0}".format(Command))
        if not IsValidLedNr(Command["Command"]["LedNr"]) : raise Exception("LedNr Invalid: {0}".format(Command))
        if not "IntensityLevel" in Command["Command"]: raise Exception("IntensityLevel missing from command: {0}".format(Command))
        if not IsValidIntensityLevel(Command["Command"]["IntensityLevel"]) : raise Exception("IntensityLevel Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedNrListToSameIntensityLevel":
        if not "LedNrList" in Command["Command"]: raise Exception("LedNrList missing from command: {0}".format(Command))
        if not IsValidLedNrList(Command["Command"]["LedNrList"]) : raise Exception("LedNrList Invalid: {0}".format(Command))
        if not "IntensityLevel" in Command["Command"]: raise Exception("IntensityLevel missing from command: {0}".format(Command))
        if not IsValidIntensityLevel(Command["Command"]["IntensityLevel"]) : raise Exception("IntensityLevel Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetAllLedRandomStates":
        pass
    elif Command["Command"]["Function"] == "SetLedNrAndIntensityLevelList":
        if not "LedNrIntensityList" in Command["Command"]: raise Exception("LedNrIntensityList missing from command: {0}".format(Command))
        if not IsValidLedNrAndIntensityList(Command["Command"]["LedNrIntensityList"]) : raise Exception("LedNrIntensityList Invalid: {0}:{1}".format(Command,Command["Command"]["LedNrIntensityList"] ))
    elif Command["Command"]["Function"] == "SetAllLedFlash" or \
                 Command["Command"]["Function"] == "SetAllLedRandomFlash":
        if not "FlashCount" in Command["Command"]: raise Exception("FlashCount missing from command: {0}".format(Command))
        if not IsValidFlashCount(Command["Command"]["FlashCount"]) : raise Exception("FlashCount Invalid: {0}".format(Command))
        if not "FlashIntervalTime" in Command["Command"]: raise Exception("FlashIntervalTime missing from command: {0}".format(Command))
        if not IsValidFlashIntervalTime(Command["Command"]["FlashIntervalTime"]) : raise Exception("FlashIntervalTime Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedNrListFlash":
        if not "FlashCount" in Command["Command"]: raise Exception("FlashCount missing from command: {0}".format(Command))
        if not IsValidFlashCount(Command["Command"]["FlashCount"]) : raise Exception("FlashCount Invalid: {0}".format(Command))
        if not "FlashIntervalTime" in Command["Command"]: raise Exception("FlashIntervalTime missing from command: {0}".format(Command))
        if not IsValidFlashIntervalTime(Command["Command"]["FlashIntervalTime"]) : raise Exception("FlashIntervalTime Invalid: {0}".format(Command))
        if not "LedNrList" in Command["Command"]: return(False)
        if not IsValidLedNrList(Command["Command"]["LedNrList"]) : raise Exception("LedNrList Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetAllLedStates":
        if not "State" in Command["Command"]: raise Exception("State missing from command: {0}".format(Command))
        if not IsValidState(Command["Command"]["State"]) : raise Exception("State Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedNrAndStateList":
        if not "LedNrStateList" in Command["Command"]: raise Exception("LedStateList missing from command: {0}".format(Command))
        if not IsValidLedNrStateList(Command["Command"]["LedNrStateList"]) : raise Exception("LedNrStateList Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedNrListFadeReverb" or \
            Command["Command"]["Function"] == "SetLedNrListFadeToOn" or \
            Command["Command"]["Function"] == "SetLedNrListFadeToOff":
        if not "FadeIncrement" in Command["Command"]: raise Exception("FadeIncrement missing from command: {0}".format(Command))
        if not IsValidFadeIncrement(Command["Command"]["FadeIncrement"]) : raise Exception("FadeIncrement Invalid: {0}".format(Command))
        if not "FadeIntervalTime" in Command["Command"]: raise Exception("FadeIntervalTime missing from command: {0}".format(Command))
        if not IsValidFadeIntervalTime(Command["Command"]["FadeIntervalTime"]) : raise Exception("FadeIntervalTime Invalid: {0}".format(Command))
        if not "LedNrList" in Command["Command"]:raise Exception("LedNrList missing from command: {0}".format(Command)) 
        if not IsValidLedNrList(Command["Command"]["LedNrList"]) : raise Exception("LedNrList Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetAllLedFadeReverb" or \
            Command["Command"]["Function"] == "SetAllLedFadeToOff" or \
            Command["Command"]["Function"] == "SetAllLedFadeToOn":
        if not "FadeIncrement" in Command["Command"]: raise Exception("FadeIncrement missing from command: {0}".format(Command))
        if not IsValidFadeIncrement(Command["Command"]["FadeIncrement"]) : raise Exception("FadeIncrement Invalid: {0}".format(Command))
        if not "FadeIntervalTime" in Command["Command"]: raise Exception("FadeIntervalTime missing from command: {0}".format(Command))
        if not IsValidFadeIntervalTime(Command["Command"]["FadeIntervalTime"]) : raise Exception("FadeIntervalTime Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedGroupNameListIntensities":
        if not "LedGroupNameList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameList(Command["Command"]["LedGroupNameList"]) : raise Exception("LedGroupNameList Invalid: {0}".format(Command))
        if not "IntensityLevel" in Command["Command"]: raise Exception("IntensityLevel missing from command: {0}".format(Command))
        if not IsValidIntensityLevel(Command["Command"]["IntensityLevel"]) : raise Exception("IntensityLevel Invalid: {0}".format(Command))

    elif Command["Command"]["Function"] == "SetLedGroupNameIntensity":

        if not "LedGroupName" in Command["Command"]: raise Exception("LedGroupName missing from command: {0}".format(Command))
        if not IsValidLedGroupName(Command["Command"]["LedGroupName"]) : raise Exception("LedGroupName Invalid: {0}".format(Command))
        if not "RGBIntensity" in Command["Command"]: raise Exception("RGBIntensity missing from command: {0}".format(Command))
        if not IsValidRGBIntensityList(Command["Command"]["RGBIntensity"]) : raise Exception("RGBIntensity Invalid: {0}".format(Command))
    
    elif Command["Command"]["Function"] == "SetLedGroupNameIntensityList":
        
        if not "LedGroupNameIntensityList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not (Command["Command"]["LedGroupNameIntensityList"]) : raise Exception("LedGroupNameIntensityList Invalid: {0}".format(Command))
    
    elif Command["Command"]["Function"] == "SetLedGroupNameListFlash":
        
        if not "LedGroupNameList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameList(Command["Command"]["LedGroupNameList"]) : raise Exception("json Invalid: {0}".format(Command))
        if not "FlashCount" in Command["Command"]: raise Exception("FlashCount missing from command: {0}".format(Command))
        if not IsValidFlashCount(Command["Command"]["FlashCount"]) : raise Exception("FlashCount Invalid: {0}".format(Command))
        if not "FlashIntervalTime" in Command["Command"]: raise Exception("FlashIntervalTime missing from command: {0}".format(Command))
        if not IsValidFlashIntervalTime(Command["Command"]["FlashIntervalTime"]) : raise Exception("json Invalid: {0}".format(Command))
    
    elif Command["Command"]["Function"] == "SetLedGroupNameStateList":
        
        if not "LedGroupNameStateList" in Command["Command"]: raise Exception("LedGroupNameStateList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameStateList(Command["Command"]["LedGroupNameStateList"]) : raise Exception("LedGroupNameStateList Invalid: {0}".format(Command))
    
    elif Command["Command"]["Function"] == "SetLedGroupNameListFadeReverb":
        if not "LedGroupNameList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameList(Command["Command"]["LedGroupNameList"]) : raise Exception("LedGroupNameList Invalid: {0}".format(Command))
        if not "FadeIncrement" in Command["Command"]: raise Exception("FadeIncrement missing from command: {0}".format(Command))
        if not IsValidFadeIncrement(Command["Command"]["FadeIncrement"]) : raise Exception("FadeIncrement Invalid: {0}".format(Command))
        if not "FadeIntervalTime" in Command["Command"]: raise Exception("FadeIntervalTime missing from command: {0}".format(Command))
        if not IsValidFadeIntervalTime(Command["Command"]["FadeIntervalTime"]) : raise Exception("FadeIntervalTime Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedGroupNameListFadeToOff":
        if not "LedGroupNameList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameList(Command["Command"]["LedGroupNameList"]) : raise Exception("LedGroupNameList Invalid: {0}".format(Command))
        if not "FadeIncrement" in Command["Command"]: raise Exception("FadeIncrement missing from command: {0}".format(Command))
        if not IsValidFadeIncrement(Command["Command"]["FadeIncrement"]) : raise Exception("FadeIncrement Invalid: {0}".format(Command))
        if not "FadeIntervalTime" in Command["Command"]: raise Exception("FadeIntervalTime missing from command: {0}".format(Command))
        if not IsValidFadeIntervalTime(Command["Command"]["FadeIntervalTime"]) : raise Exception("FadeIntervalTime Invalid: {0}".format(Command))
    elif Command["Command"]["Function"] == "SetLedGroupNameListFadeToOn":
        if not "LedGroupNameList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameList(Command["Command"]["LedGroupNameList"]) : raise Exception("LedGroupNameList Invalid: {0}".format(Command))
        if not "FadeIncrement" in Command["Command"]: raise Exception("FadeIncrement missing from command: {0}".format(Command))
        if not IsValidFadeIncrement(Command["Command"]["FadeIncrement"]) : raise Exception("FadeIncrement Invalid: {0}".format(Command))
        if not "FadeIntervalTime" in Command["Command"]: raise Exception("FadeIntervalTime missing from command: {0}".format(Command))
        if not IsValidFadeIntervalTime(Command["Command"]["FadeIntervalTime"]) : raise Exception("FadeIntervalTime Invalid: {0}".format(Command))


    elif Command["Command"]["Function"] == "SetLedGroupNameListRainbowCycle":
        if not "LedGroupNameList" in Command["Command"]: raise Exception("LedGroupNameList missing from command: {0}".format(Command))
        if not IsValidLedGroupNameList(Command["Command"]["LedGroupNameList"]) : raise Exception("LedGroupNameList Invalid: {0}".format(Command))
        if not "NrCycles" in Command["Command"]: raise Exception("NrCycles missing from command: {0}".format(Command))
        if not IsValidNrCycles(Command["Command"]["NrCycles"]) : raise Exception("NrCycles Invalid: {0}".format(Command))
        if not "CycleIntervalTime" in Command["Command"]: raise Exception("CycleIntervalTime missing from command: {0}".format(Command))
        if not IsValidCycleIntervalTime(Command["Command"]["CycleIntervalTime"]) : raise Exception("CycleIntervalTime Invalid: {0}".format(Command))


    elif Command["Command"]["Function"] == "RepeatLastCommands":
        if not "NrPreviousCommandsToRepeat" in Command["Command"]: raise Exception("NrPreviousCommandsToRepeat missing from command: {0}".format(Command))
        if not IsValidNrCommandsToRepeat(Command["Command"]["NrPreviousCommandsToRepeat"]) : raise Exception("NrPreviousCommandsToRepeat Invalid: {0}".format(Command))
        if not "NrOfRepetitions" in Command["Command"]: raise Exception("NrOfRepetitions missing from command: {0}".format(Command))
        if not IsValidNrOfRepetitions(Command["Command"]["NrOfRepetitions"]) : raise Exception("NrOfRepetitions Invalid: {0}".format(Command))
        
    elif Command["Command"]["Function"] == "ResetBoard":
        pass
    else:
        raise Exception("{0}Unknown 'Function': {1}".format(FUNC_NAME, Command))
    return (True)


def IsValidCommandScript(CommandScriptList):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

# verify that the script and its commands are in the correct format, if not raise an exception
    for Command in CommandScriptList:
        try:
            not _isValidCommand(Command)
        except Exception as err:
            raise Exception("{0} {1}".format(FUNC_NAME,err))
    return(True)


if __name__ == '__main__':
    pass