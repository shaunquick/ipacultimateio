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


# This module allows you to control each Led brightness either
# either individually or as a list of Led's


import time

from ..common.common_lib            import GetMyFuncName
from ..common.common_lib            import IsDebugOn

from ..common.validations           import IsValidFadeIntervalTime
from ..common.validations           import IsValidIntensityLevel
from ..common.validations           import IsValidLedNrList
from ..common.validations           import IsValidFlashIntervalTime
from ..common.validations           import IsValidFlashCount
from ..common.validations           import IsValidFadeIncrement
from ..common.validations           import IsValidLedNr
from ..common.validations           import IsValidLedNrAndIntensityList
from ..common.validations           import IsValidLedNrStateList
from ..common.validations           import IsValidNrCycles
from ..common.validations           import IsValidCycleIntervalTime
from ..common.validations           import IsValidRainbowRGBListIndex

from .ipacultimateiovalidations     import IsValidIpacUltimateDevice

from .ipacultimateiodevicelist      import GetDeviceList

from ..utils.ledcurrentstateslist   import SetDeviceLEDCurrentStatesLedIntensity    
from ..utils.ledcurrentstateslist   import SetDeviceLEDCurrentStatesLedFadeIntensity
from ..utils.ledcurrentstateslist   import SetDeviceLEDCurrentStatesLedState        
from ..utils.ledcurrentstateslist   import GetDeviceLEDCurrentStatesLedIntensity
from ..utils.ledcurrentstateslist   import GetDeviceLEDCurrentStatesLedFadeIntensity

from .ipacultimateioboard           import SetLEDsToIndividualBrightness


def SetLedNrToIntensityLevel(DeviceUUID=None, LedNr = 3, IntensityLevel=100):
# Set a specific 'LedNr' to a specific 'IntensityLevel'
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        SetLedNrListToSameIntensityLevel(DeviceUUID, [LedNr], IntensityLevel)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))




def SetLedNrListToSameIntensityLevel(DeviceUUID=None, LedNrList=[], IntensityLevel=60):
# Set a list  of 'LedNr' to a specific 'IntensityLevel'
# LedNrList = [1,2,3]
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    if IsDebugOn(): print(LedNrList)
    if IsDebugOn(): print(IntensityLevel)


    try:
        if not IsValidLedNrList(LedNrList): raise Exception("LedNrList not valid")
        if not IsValidIntensityLevel(IntensityLevel): raise Exception("IntensityLevel not valid")

        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for LedNr in LedNrList:
                    SetDeviceLEDCurrentStatesLedIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                    SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                    SetDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],LedNr,True)
        SetLEDsToIndividualBrightness(DeviceUUID)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedNrListFlash(DeviceUUID=None, LedNrList=[], FlashCount=3, FlashIntervalTime=3):
# Flash a list Leds  'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
# LedNrList = [1,2,3]
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if not IsValidLedNrList(LedNrList): raise Exception("LedNrList not valid - {1}".format(LedNrList))
        if not IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("FlashIntervalTime not valid")
        if not IsValidFlashCount(FlashCount) : raise Exception("FlashCount not valid")

        counter1 = 0
        while counter1 < FlashCount:
            for myDevice in GetDeviceList():
                if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                    for LedNr in LedNrList:
                        SetDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],LedNr,False)
            SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)
            time.sleep(FlashIntervalTime)

            for myDevice in GetDeviceList():
                if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                    for LedNr in LedNrList:
                        SetDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],LedNr,True)
            SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)
            time.sleep(FlashIntervalTime)

            counter1 += 1
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedNrAndStateList(DeviceUUID=None, LedNrStateList=[]):
# Set a list of Led's to a uniques state - either on or off
# LedNrStateList = [ {"ledNr": 1, "State" : True}, {"ledNr": 1, "State" : False} ...]
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    #if IsDebugOn(): print("LedNrStateList")
    #if IsDebugOn(): print(LedNrStateList)
    
    try:
        if not IsValidLedNrStateList(LedNrStateList):  raise Exception("StateList not valid")
    
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for LedState in LedNrStateList:
                    LedNr = LedState['LedNr']
                    LedState = LedState['State']
                    if LedState : SetDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],LedNr,True)
                    else:        SetDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],LedNr,False)
        SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
        

def SetLedNrListFadeReverb(DeviceUUID=None, LedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1):
# Fade down and then up a list of Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if not IsValidLedNrList(LedNrList): raise Exception("LedNrList not valid")
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")
  
        SetLedNrListFadeToOff(DeviceUUID, LedNrList, FadeIncrement, FadeIntervalTime)
        SetLedNrListFadeToOn(DeviceUUID, LedNrList, FadeIncrement, FadeIntervalTime)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
    return()

def SetLedNrListFadeToOff(DeviceUUID=None, LedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1):
# Fade down a list of Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    
    try:
        if not IsValidLedNrList(LedNrList): raise Exception("LedNrList not valid")
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")

        maxIntensity = 0

        for myDevice in GetDeviceList():
            if DeviceUUID == None or DeviceUUID == myDevice["DeviceUUID"]: 
                for LedNr in LedNrList:
                    LedIntensity = GetDeviceLEDCurrentStatesLedIntensity(myDevice["DeviceUUID"],LedNr)
                    SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr, LedIntensity)
                    if (LedIntensity> maxIntensity): maxIntensity = LedIntensity
        SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)

        NrOfIterations = int(maxIntensity/FadeIncrement)
        counter1 = 1
        while counter1 < NrOfIterations + 1:
            for myDevice in GetDeviceList():
                if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                    for LedNr in LedNrList:
                        NewLedIntensity = GetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr) - FadeIncrement
                        if NewLedIntensity >= 0 :
                            SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr,NewLedIntensity)
                        else:
                            SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr,0)
            SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)
            counter1 += 1
            time.sleep(FadeIntervalTime)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
    return()


def SetLedNrListFadeToOn(DeviceUUID=None, LedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1):

# Fade up a list of Leds to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds


    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    try:
        if not IsValidLedNrList(LedNrList): raise Exception("LedList not valid")
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")

        maxIntensity = 0
    
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for LedNr in LedNrList:
                    SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr,0)
                    LedIntensity = GetDeviceLEDCurrentStatesLedIntensity(myDevice["DeviceUUID"],LedNr)
                    if (LedIntensity > maxIntensity): maxIntensity = LedIntensity           
        SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)

        NrOfIterations = int(maxIntensity/FadeIncrement)
        counter1 = 1
        while counter1 < NrOfIterations + 1:
            for myDevice in GetDeviceList():
                if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                    for LedNr in LedNrList:
                        MaxSetLedIntensity = GetDeviceLEDCurrentStatesLedIntensity(myDevice["DeviceUUID"],LedNr)
                        NewFadeLedIntensity = GetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr) + FadeIncrement
                        if NewFadeLedIntensity < MaxSetLedIntensity:
                            SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr,NewFadeLedIntensity)
                        else:
                            SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr, MaxSetLedIntensity)
            SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)
            counter1 += 1
            time.sleep(FadeIntervalTime)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
    return()


def SetLedNrAndIntensityLevelList(DeviceUUID=None, LedNrAndIntensityList=[]):
# Set a list of Led's to a unique intensity level
# LedIntensityList = [ {"LedNr": 1, "IntensityLevel": 122}, {ledNr, IntensityLevel), ...]
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    try:
        if not IsValidLedNrAndIntensityList(LedNrAndIntensityList): raise Exception("LedIntensityList not valid")
    
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for LedIntensity in LedNrAndIntensityList:
                    LedNr = LedIntensity['LedNr']
                    IntensityLevel = LedIntensity['IntensityLevel']
                    SetDeviceLEDCurrentStatesLedIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                    SetDeviceLEDCurrentStatesLedFadeIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                    SetDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],LedNr,True)        
    
        SetLEDsToIndividualBrightness(DeviceUUID)
    #    if IsDebugOn(): print(FUNC_NAME+"Finished")
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))






def SetDevicesLedNrListFadeToOn(DeviceUUID=None, DevicesLedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1):
# Fade up a list of Leds to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

# is a list of a paired set of LEDs and DeviceUUID
#    DevicesLedNrList=[{"DeviceUUID":"0:0:0:0", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[4,5,6]},
#    ]

    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")

        maxIntensity = 0
    
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for DeviceLedNrList in DevicesLedNrList:
                    if not IsValidLedNrList(DeviceLedNrList["LedNrList"]): raise Exception("{0}LedList not valid".format(FUNC_NAME))
                    for LedNr in DeviceLedNrList["LedNrList"]:
                        SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr,0)
                        LedIntensity = GetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr)
                        if (LedIntensity > maxIntensity): maxIntensity = LedIntensity           
        SetLEDsToIndividualBrightness(DeviceUUID, UseFadeValues=True)

        NrOfIterations = int(maxIntensity/FadeIncrement)
        counter1 = 1
        while counter1 < NrOfIterations + 1:
            for myDevice in GetDeviceList():
                if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                    for DeviceLedNrList in DeviceLedNrList["LedNrList"]:
                        for LedNr in LedNrList:
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



def SetDevicesLedNrListRainbowCycle( DevicesLedNrList=[], NrCycles=3, 
                             CycleIntervalTime=3, RainbowRGBListIndex = 0):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


# is a list of a paired set of LEDs and DeviceUUID
#    DevicesLedNrList=[{"DeviceUUID":"0:0:0:0", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[1,2,3]},
#                       {"DeviceUUID":"0:0:0:1", LedNrList :[4,5,6]},
#    ]

# Set a list  of 'LedNr' to a specific 'IntensityLevel'
# LedNrList = [1,2,3]
    RainbowRGBList = [
255,0,32,
255,0,64, 
255,0,96, 
255,0,128, 
255,0,160, 
255,0,192, 
255,0,224, 
255,0,255, 
224,0,255, 
192,0,255, 
160,0,255, 
128,0,255, 
96,0,255, 
64,0,255, 
32,0,255, 
0,0,255, 
0,32,255, 
0,64,255, 
0,96,255, 
0,128,255,
0,160,255,
0,192,255,
0,224,255,
0,255,255,
0,255,224,
0,255,192,
0,255,160,
0,255,128,
0,255,96,
0,255,64,
0,255,32,
0,255,0,
32,255,0,
64,255,0,
96,255,0,
128,255,0,
160,255,0,
192,255,0,
224,255,0,
255,255,0,
255,224,0,
255,192,0,
255,160,0,
255,128,0,
255,96,0,
255,64,0,
255,32,0,
255,0,0    
    ]

    try:
        RainbowRGBListLength = len(RainbowRGBList)


        if IsDebugOn(): print(FUNC_NAME)
        # if IsDebugOn(): print("{0}DevicesLedNrList={1}".format(FUNC_NAME,DevicesLedNrList))

        if not IsValidNrCycles(NrCycles): raise Exception("NrCycles not valid")
        if not IsValidCycleIntervalTime(CycleIntervalTime): raise Exception("CycleIntervalTime not valid")
        if not IsValidRainbowRGBListIndex(RainbowRGBListIndex) : raise Exception("CycleIntervalTime not valid")

        curr_index = RainbowRGBListIndex * 3
        cycle_count = 0
        # first_LedNr = LedNrList[0]
        # Now get the total numer of led's across all of the devices.
        LedNrlength = 0
        for DeviceLedNrList in DevicesLedNrList:
            LedNrlength += len(DeviceLedNrList["LedNrList"])

        while cycle_count <= NrCycles:
            is_cycle_finished = False
            while not is_cycle_finished:

                for DeviceLedNrList in DevicesLedNrList:
                    if not IsValidLedNrList(DeviceLedNrList["LedNrList"]): raise Exception("{0}LedNrList not valid".format(FUNC_NAME))
                    for LedNr in DeviceLedNrList["LedNrList"]:
                        if curr_index >= RainbowRGBListLength:
                            curr_index = 0
                            # Needs to be uncommented
                        SetDeviceLEDCurrentStatesLedIntensity(DeviceLedNrList["DeviceUUID"],LedNr,RainbowRGBList[curr_index])
                        SetDeviceLEDCurrentStatesLedFadeIntensity(DeviceLedNrList["DeviceUUID"],LedNr,RainbowRGBList[curr_index])
                        SetDeviceLEDCurrentStatesLedState(DeviceLedNrList["DeviceUUID"],LedNr,True)
                        curr_index += 1
                if not is_cycle_finished:
                    SetLEDsToIndividualBrightness(DeviceUUID=None)
                    time.sleep(CycleIntervalTime)
                    curr_index = curr_index - LedNrlength + 3
                    if curr_index < 0:
                        curr_index += len(RainbowRGBList)
                    if curr_index == RainbowRGBListIndex:
                      is_cycle_finished = True


            cycle_count += 1
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


if __name__ == '__main__':
    pass