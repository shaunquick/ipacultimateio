# Copyright 2021-2021 Shaun Quick
# Copyright 2021-2021 contributors
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
#  met:
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


# This module process commands from the script - where the user has
# defined a group of Led's as a logical grouping
# Based on the grouping e.g. {LedGroupeName: "pinkElephant", LedNrs:[1,2,3]}}
# the groupname can be used to control the Leds as opposed tp
# the spefic led Numbers - this makes it easier to control a buttons RGB values
# for example.

import time

from ..common.common_lib                    import GetMyFuncName
from ..common.common_lib                    import IsDebugOn

from ..utils.ledgroupnamedefinitionslist    import ConvertLedGroupNameIntensityListToDevicesLedNrAndIntensityList
from ..utils.ledgroupnamedefinitionslist    import ConvertLedGroupNameListToDevicesLedNrList
from ..utils.ledgroupnamedefinitionslist    import ConvertLedGroupNameToDevicesLedNrList
from ..utils.ledgroupnamedefinitionslist    import ConvertLedGroupNameStateListToDevicesLedStateList 

from ..utils.ledgroupname                   import IsValidLedGroupName
from ..utils.ledgroupname                   import IsValidLedGroupNameList 
from ..utils.ledgroupname                   import IsValidLedGroupNameStateList
from ..utils.ledgroupname                   import IsValidLedGroupNameIntensityList
from ..utils.ledgroupname                   import IsValidRGBIntensityList

from ..common.validations                   import IsValidFadeIntervalTime
from ..common.validations                   import IsValidIntensityLevel
from ..common.validations                   import IsValidFlashIntervalTime
from ..common.validations                   import IsValidFlashCount
from ..common.validations                   import IsValidFadeIncrement
from ..common.validations                   import IsValidNrCycles
from ..common.validations                   import IsValidCycleIntervalTime

from .ipacultimateiovalidations             import IsValidIpacUltimateDevice

from .setlednr                              import SetDevicesLedNrListRainbowCycle

from ..utils.ledcurrentstateslist           import GetDeviceLEDCurrentStatesLedIntensity
from ..utils.ledcurrentstateslist           import GetDeviceLEDCurrentStatesLedFadeIntensity
from ..utils.ledcurrentstateslist           import SetDeviceLEDCurrentStatesLedIntensity  
from ..utils.ledcurrentstateslist           import SetDeviceLEDCurrentStatesLedState
from ..utils.ledcurrentstateslist           import SetDeviceLEDCurrentStatesLedFadeIntensity

from .ipacultimateioboard                   import SetLEDsToIndividualBrightness


def SetLedGroupNameListIntensities(DeviceUUID=None, LedGroupNameList=[], IntensityLevel=60):
#  Set all the Leds in the group to the same intensity level
# LedGroupNameList=[ "p1b1", "p1b2", "p1b3", "p1b4" ]
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if not IsValidLedGroupNameList(LedGroupNameList): raise Exception("LedGroupNameList not valid")
    
        for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
            if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                for LedNr in DeviceLedNrList["LedNrList"]:
                    SetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr,IntensityLevel)
        SetLEDsToIndividualBrightness(DeviceUUID)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameIntensity(DeviceUUID=None, LedGroupName="", RGBIntensityList=[]):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

#  Set a secific group to their specific brightness
# LedGroupName="p1b1"
#  RGBIntensityList=[255,11,22] - note this was designed for 3 values for the Red Green Blue Leds
    try:
        if not IsValidLedGroupName(LedGroupName):  raise Exception("LedGroupName not valid")
        if not IsValidRGBIntensityList(RGBIntensityList):  raise Exception("RGBIntensityList not valid")
                        
        for DeviceLedNrList in ConvertLedGroupNameToDevicesLedNrList(DeviceUUID,LedGroupName):
            RGBcounter = 0
            if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                for LedNr in DeviceLedNrList["LedNrList"]:
                    if RGBcounter > len(RGBIntensityList) : RGBcounter = 0
                    SetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr,RGBIntensityList[RGBcounter])
        SetLEDsToIndividualBrightness(DeviceUUID)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameListFlash(DeviceUUID=None, LedGroupNameList=[], FlashCount=3, FlashIntervalTime=3):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

# Set all the Leds in the group to flash
# 'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds

    try:
        counter1 = 0
        while counter1 < FlashCount:

            for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
                if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                    for LedNr in DeviceLedNrList["LedNrList"]:                    
                        SetDeviceLEDCurrentStatesLedState(DeviceLedNrList["DeviceUUID"],LedNr,False)

            SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)


            time.sleep(FlashIntervalTime)

            for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
                if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                    for LedNr in DeviceLedNrList["LedNrList"]:                    
                        SetDeviceLEDCurrentStatesLedState(DeviceLedNrList["DeviceUUID"],LedNr,True)

            SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)

            time.sleep(FlashIntervalTime)
            counter1 += 1


    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameListFadeReverb(DeviceUUID=None, LedGroupNameList=[], FadeIncrement=10, FadeIntervalTime=0.1):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

#  Set all the Leds in the group to
# Fade down and then up  to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
#
    try:
        SetLedGroupNameListFadeToOff(DeviceUUID, LedGroupNameList, FadeIncrement = 10, 
                                 FadeIntervalTime = 0.1 )
# Fade everythign back up 
        SetLedGroupNameListFadeToOn(DeviceUUID, LedGroupNameList, FadeIncrement = 10, 
                                FadeIntervalTime = 0.1 )
    
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return()

def SetLedGroupNameListFadeToOff(DeviceUUID=None, LedGroupNameList=[], FadeIncrement = 10, 
                                 FadeIntervalTime = 0.1 ):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

#  Set all the Leds in the group to
# Fade down  to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness

    try:
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")
        # Fade everything down to zero
        maxIntensity = 0

        for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
            if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                for LedNr in DeviceLedNrList["LedNrList"]:
                    LedIntensity = GetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr)
                    SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr, LedIntensity)
                    if (LedIntensity> maxIntensity): maxIntensity = LedIntensity
        SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)

        counter1 = 1
        NrOfIterations = int(maxIntensity/FadeIncrement)

        while counter1 < NrOfIterations + 1:
            for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
                if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                    for LedNr in DeviceLedNrList["LedNrList"]:
                        NewLedIntensity = GetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr) - FadeIncrement
                        if NewLedIntensity >= 0 :
                            SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr,NewLedIntensity)
                        else:
                            SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr,0)
            SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)
            counter1 += 1
            time.sleep(FadeIntervalTime)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
    return()

def SetLedGroupNameListFadeToOn(DeviceUUID=None, LedGroupNameList=[], FadeIncrement = 10, 
                                FadeIntervalTime = 0.1 ):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

# Set all the Leds in the group to
# Fade up to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

    try:
        if not IsValidLedGroupNameList(LedGroupNameList): raise Exception("LedGroupNameList not valid")
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")


        maxIntensity = 0
    
        for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
            if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                for LedNr in DeviceLedNrList["LedNrList"]:
                    SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr,0)
                    LedIntensity = GetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr)
                    if (LedIntensity > maxIntensity): maxIntensity = LedIntensity           
        SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)

        NrOfIterations = int(maxIntensity/FadeIncrement)
        counter1 = 1
        while counter1 < NrOfIterations + 1:
            for DeviceLedNrList in ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList):
                if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrList["DeviceUUID"]): 
                    for LedNr in DeviceLedNrList["LedNrList"]:
                        MaxSetLedIntensity = GetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr)
                        NewFadeLedIntensity = GetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr) + FadeIncrement
                        if NewFadeLedIntensity < MaxSetLedIntensity:
                            SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr,NewFadeLedIntensity)
                        else:
                            SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr, MaxSetLedIntensity)
            SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)
            counter1 += 1
            time.sleep(FadeIntervalTime)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return()

def SetLedGroupNameListRainbowCycle(DeviceUUID=None, LedGroupNameList=[], NrCycles=2, CycleIntervalTime=1):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    try:
        if not IsValidLedGroupNameList(LedGroupNameList): raise Exception("LedList not valid")
        DevicesLedNrList = ConvertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList)
        SetDevicesLedNrListRainbowCycle(DevicesLedNrList=DevicesLedNrList, 
                                     NrCycles=NrCycles, CycleIntervalTime=CycleIntervalTime)
        pass
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameIntensityList(DeviceUUID=None, LedGroupNameIntensityList=[]):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

#  Set all the Leds in the group to different intensity level
#    LedGroupNameIntensityList = [ {"LedGroupName" : "p1b1", "RGBIntensity" : [255,11,22] }, 
#    {"LedGroupName" : "p1b2", "RGBIntensity" : [255,11,22] }]
    try:
        if not IsValidLedGroupNameIntensityList(LedGroupNameIntensityList): raise Exception("LedIntensityList not valid")
 
        for DeviceLedNrAndIntensityList in ConvertLedGroupNameIntensityListToDevicesLedNrAndIntensityList(DeviceUUID, 
                                                                                                      LedGroupNameIntensityList):

            if (DeviceUUID == None) or (DeviceUUID == DeviceLedNrAndIntensityList["DeviceUUID"]): 
                for LedIntensity in DeviceLedNrAndIntensityList["LedNrAndIntensityList"]:
                    LedNr = LedIntensity['LedNr']
                    IntensityLevel = LedIntensity['IntensityLevel']
                    SetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrAndIntensityList["DeviceUUID"],LedNr,IntensityLevel)
                    SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrAndIntensityList["DeviceUUID"],LedNr,IntensityLevel)
                    SetDeviceLEDCurrentStatesLedState(DeviceLedNrAndIntensityList["DeviceUUID"],LedNr,True)        
    
        SetLEDsToIndividualBrightness(DeviceUUID)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


    
def SetLedGroupNameStateList(DeviceUUID=None, LedGroupNameStateList=[]):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

#  Set all the Leds in the group to on or off
    try:
        if not IsValidLedGroupNameStateList(LedGroupNameStateList):  raise Exception("StateList not valid")
        for DeviceLedStateList in ConvertLedGroupNameStateListToDevicesLedStateList(DeviceUUID, LedGroupNameStateList):
            if (DeviceUUID == None) or (DeviceUUID == DeviceLedStateList["DeviceUUID"]): 
                for LedState in DeviceLedStateList["LedNrStateList"]:
                    LedNr = LedState['LedNr']
                    LedState = LedState['State']
                    if LedState : SetDeviceLEDCurrentStatesLedState(DeviceLedStateList["DeviceUUID"],LedNr,True)
                    else:        SetDeviceLEDCurrentStatesLedState(DeviceLedStateList["DeviceUUID"],LedNr,False)
        SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))



if __name__ == '__main__':
    pass