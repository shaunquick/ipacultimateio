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

# This module will read from a file that either is in the
# scripts folder, or a fully qualified filename is expected to be
# provided to run a script in another folder.
# the script is expected to be in json format and follow the definiton.
# the definiiton is shown on the help page or in the reame doc

import time
import json
from importlib import  resources
from os import path

# Load all the functions as their names - to be used across the utility

#from libs.globalvar import *  # load the global variable
from .commandscriptvalidations import _isValidCommandScript

from ..core.ipacultimateiocore import ResetDevices

from ..core.setledall import SetAllLedIntensities
from ..core.setledall import SetAllLedRandomStates
from ..core.setledall import SetAllLedFlash
from ..core.setledall import SetAllLedRandomFlash
from ..core.setledall import SetAllLedStates
from ..core.setledall import SetAllLedFadeReverb
from ..core.setledall import SetAllLedFadeToOff
from ..core.setledall import SetAllLedFadeToOn

from ..core.setlednr import SetLedNrIntensity
from ..core.setlednr import SetLedNrListIntensities
from ..core.setlednr import SetLedNrIntensityList
from ..core.setlednr import SetLedNrListFlash
from ..core.setlednr import SetLedNrStateList
from ..core.setlednr import SetLedNrListFadeReverb
from ..core.setlednr import SetLedNrListFadeToOn
from ..core.setlednr import SetLedNrListFadeToOff

from ..core.setledgroupname import SetLedGroupNameListIntensities 
from ..core.setledgroupname import SetLedGroupNameIntensityList
from ..core.setledgroupname import SetLedGroupNameIntensity 
from ..core.setledgroupname import SetLedGroupNameListFlash
from ..core.setledgroupname import SetLedGroupNameStateList 
from ..core.setledgroupname import SetLedGroupNameListFadeReverb 
from ..core.setledgroupname import SetLedGroupNameListFadeToOff
from ..core.setledgroupname import SetLedGroupNameListFadeToOn
from ..core.setledgroupname import SetLedGroupNameListRainbowCycle


def RunCommandsFromFile(DeviceIDList, filename, debug = False):
# Load the script file, validate the script fila and then execute the commands in the file.
    try:
        FileCommandList = GetLedCommandsFromFile(filename)
        RunLedCommands(DeviceIDList=DeviceIDList, CommandScriptList=FileCommandList, debug = debug)
    except Exception as err:
        raise Exception("RunCommandsFromFile(): {0}".format(err))

def GetLedCommandsFromFile(filename, debug=False):
# use the default test script if no filename is provided
    if filename == "":
        filename = "default_script.json"

# if the filename is passed without a path then open the file from the scripts folder
# if a path is provided check that the file exists and open
# if no filename provided the script will run with the default default_script.json file
# otherwise raise an exception
    try:
        if len(path.split(filename)[0]) == 0:
            with resources.open_text("scripts", filename) as read_file:
                filecontent = read_file.read()  
        elif path.isfile(filename):
            with open(filename, "r") as read_file:
                filecontent = read_file.read()
        else:
            raise Exception("File is not found : {0}".format(filename))
    except Exception as err:
        raise Exception("{0}".format(err))



    try:
        CommandScript = json.loads(filecontent)
        if type(CommandScript) is not list: raise Exception("GetLedCommandsFromFile(): file structure not valid - Expecting a json list")
        _isValidCommandScript(CommandScript)
    except Exception as err:
        raise Exception("GetLedCommandsFromFile(): {0}".format(err))
    return (CommandScript)


def RunLedCommands(CommandScriptList=[], debug=False):
    FUNC_NAME="RunLedCommands(): "
    
    # temporary fix to only run on one board
    if len(DeviceIDList) == 0:
        raise Exception("Error: Could not find Ultimarc I/O Board")
    if debug:
        print(FUNC_NAME)


    try:
        Counter = 0
        for FileCommand in CommandScriptList:
            if FileCommand["Command"]["Function"] == "Wait":
                time.sleep(FileCommand["Command"]["WaitIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetAllLedIntensities":
                SetAllLedIntensities(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   IntensityLevel=FileCommand["Command"]["IntensityLevel"])
            elif FileCommand["Command"]["Function"] == "SetLedNrIntensity":
                SetLedNrIntensity(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNr=FileCommand["Command"]["LedNr"], IntensityLevel=FileCommand["Command"]["IntensityLevel"])
            elif FileCommand["Command"]["Function"] == "SetLedNrListIntensities":
                SetLedNrListIntensities(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrList = FileCommand["Command"]["LedNrList"], 
                                   IntensityLevel=FileCommand["Command"]["IntensityLevel"])
            elif FileCommand["Command"]["Function"] == "SetAllLedRandomStates":
                SetAllLedRandomStates(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug)
            elif FileCommand["Command"]["Function"] == "SetLedNrIntensityList":
                SetLedNrIntensityList(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrIntensityList=FileCommand["Command"]["LedNrIntensityList"])
            elif FileCommand["Command"]["Function"] == "SetAllLedFlash":
                SetAllLedFlash(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   FlashCount=FileCommand["Command"]["FlashCount"], 
                                   FlashIntervalTime=FileCommand["Command"]["FlashIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetAllLedRandomFlash":
                SetAllLedRandomFlash(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   FlashCount=FileCommand["Command"]["FlashCount"], 
                                   FlashIntervalTime=FileCommand["Command"]["FlashIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetLedNrListFlash":
                SetLedNrListFlash(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrList = FileCommand["Command"]["LedNrList"], 
                                   FlashCount=FileCommand["Command"]["FlashCount"], 
                                   FlashIntervalTime=FileCommand["Command"]["FlashIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetAllLedStates":
                SetAllLedStates(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   State=FileCommand["Command"]["State"])
            elif FileCommand["Command"]["Function"] == "SetLedNrStateList":
                SetLedNrStateList(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrStateList=FileCommand["Command"]["LedNrStateList"])
            elif FileCommand["Command"]["Function"] == "SetLedNrListFadeReverb":
                SetLedNrListFadeReverb(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrList = FileCommand["Command"]["LedNrList"], 
                                   FadeIncrement=FileCommand["Command"]["FadeIncrement"], 
                                   FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetLedNrListFadeToOn":
                SetLedNrListFadeToOn(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrList = FileCommand["Command"]["LedNrList"], 
                                   FadeIncrement=FileCommand["Command"]["FadeIncrement"], 
                                   FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetLedNrListFadeToOff":
                SetLedNrListFadeToOff(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   LedNrList = FileCommand["Command"]["LedNrList"], 
                                   FadeIncrement=FileCommand["Command"]["FadeIncrement"], 
                                   FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetAllLedFadeReverb":
                SetAllLedFadeReverb(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                   FadeIncrement=FileCommand["Command"]["FadeIncrement"], 
                                   FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetAllLedFadeToOff":
                SetAllLedFadeToOff(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                  FadeIncrement=FileCommand["Command"]["FadeIncrement"], 
                                  FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetAllLedFadeToOn":
                SetAllLedFadeToOn(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                  FadeIncrement=FileCommand["Command"]["FadeIncrement"], 
                                  FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])

            elif FileCommand["Command"]["Function"] == "SetLedGroupNameListIntensities":
                SetLedGroupNameListIntensities(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   DeviceIDList=DeviceIDList, debug=debug,
                                  LedGroupNameList=FileCommand["Command"]["LedGroupNameList"], 
                                  IntensityLevel=FileCommand["Command"]["IntensityLevel"])
            elif FileCommand["Command"]["Function"] == "SetLedGroupNameIntensity":
                SetLedGroupNameIntensity(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                  debug=debug,
                                  LedGroupName=FileCommand["Command"]["LedGroupName"], 
                                  RGBIntensityList=FileCommand["Command"]["RGBIntensity"])
            elif FileCommand["Command"]["Function"] == "SetLedGroupNameIntensityList":
                SetLedGroupNameIntensityList(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   debug=debug,
                                  LedGroupNameIntensityList=FileCommand["Command"]["LedGroupNameIntensityList"])
                
                
            elif FileCommand["Command"]["Function"] == "SetLedGroupNameListFlash":
                SetLedGroupNameListFlash(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                  debug=debug,
                                  LedGroupNameList=FileCommand["Command"]["LedGroupNameList"],
                                  FlashCount= FileCommand["Command"]["FlashCount"],
                                  FlashIntervalTime= FileCommand["Command"]["FlashIntervalTime"])
            elif FileCommand["Command"]["Function"] == "SetLedGroupNameStateList":
                SetLedGroupNameStateList(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   debug=debug,
                                   LedGroupNameStateList=FileCommand["Command"]["LedGroupNameStateList"])
            elif FileCommand["Command"]["Function"] == "SetLedGroupNameListFadeReverb":
                SetLedGroupNameListFadeReverb(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                  debug=debug,
                                  LedGroupNameList=FileCommand["Command"]["LedGroupNameList"],
                                  FadeIncrement=FileCommand["Command"]["FadeIncrement"],
                                  FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])


            elif FileCommand["Command"]["Function"] == "SetLedGroupNameListFadeToOff":
                SetLedGroupNameListFadeToOff(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                  debug=debug,
                                  LedGroupNameList=FileCommand["Command"]["LedGroupNameList"],
                                  FadeIncrement=FileCommand["Command"]["FadeIncrement"],
                                  FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])

            elif FileCommand["Command"]["Function"] == "SetLedGroupNameListFadeToOn":
                SetLedGroupNameListFadeToOn(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                   debug=debug,
                                   LedGroupNameList=FileCommand["Command"]["LedGroupNameList"],
                                   FadeIncrement=FileCommand["Command"]["FadeIncrement"],
                                   FadeIntervalTime=FileCommand["Command"]["FadeIntervalTime"])

            elif FileCommand["Command"]["Function"] == "SetLedGroupNameListRainbowCycle":
                SetLedGroupNameListRainbowCycle(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                                  debug=debug,
                                  LedGroupNameList=FileCommand["Command"]["LedGroupNameList"],
                                  NrCycles=FileCommand["Command"]["NrCycles"],
                                  CycleIntervalTime=FileCommand["Command"]["CycleIntervalTime"])

            elif FileCommand["Command"]["Function"] == "RepeatLastCommands":
                ListofCommands = _GetCommandsToRepeat(CommandScriptList=CommandScriptList, LastItemCount=Counter, 
                                  NrPreviousCommandsToRepeat=FileCommand["Command"]["NrPreviousCommandsToRepeat"])
                Repetitions = 0
                while Repetitions < FileCommand["Command"]["NrOfRepetitions"]:
                    Repetitions += 1
                    RunLedCommands(DeviceIDList=DeviceIDList, debug=debug,
                                  CommandScriptList=ListofCommands)
                
                pass

            elif FileCommand["Command"]["Function"] == "ResetBoard":
                ResetDevices(DeviceUUID=FileCommand["Command"].get("DeviceUUID"), 
                           DeviceIDList=DeviceIDList, debug=debug)
            else:
                raise Exception("RunLedCommands: Command not known: {0}".format(FileCommand))
            Counter += 1
    except Exception as err:
        raise Exception("RunLedCommands: {0}".format(err))
    

def _GetCommandsToRepeat(CommandScriptList, LastItemCount, NrPreviousCommandsToRepeat, debug=False):
    NewCommandScriptList = CommandScriptList[LastItemCount-NrPreviousCommandsToRepeat:LastItemCount]
    return(NewCommandScriptList)


if __name__ == '__main__':
    pass