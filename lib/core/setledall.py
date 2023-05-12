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

# This model holds all the functions to set all the leds to a common
# setting

import time
import random

from ..common.common_lib import GetMyFuncName
from ..common.common_lib import IsDebugOn

from ..utils.ledcurrentstateslist import SetAllDeviceLEDCurrentStates
from ..utils.ledcurrentstateslist import SetAllDeviceLEDCurrentStatesLedState

from ..utils.ledcurrentstateslist import GetDeviceLEDCurrentStatesLedIntensity
from ..utils.ledcurrentstateslist import GetDeviceLEDCurrentStatesLedFadeIntensity

from ..utils.ledcurrentstateslist import SetDeviceLEDCurrentStatesLedState
from ..utils.ledcurrentstateslist import SetDeviceLEDCurrentStatesLedFadeIntensity

from ..utils.ledcurrentstateslist import SetRandomDeviceLEDCurrentStates

from ..utils.lednrlist import Get_DeviceLEDList                   

from ..common.validations import IsValidFadeIntervalTime
from ..common.validations import IsValidIntensityLevel
from ..common.validations import IsValidLedNrList
from ..common.validations import IsValidFlashIntervalTime
from ..common.validations import IsValidFlashCount
from ..common.validations import IsValidFadeIncrement
from ..common.validations import IsValidState

from .ipacultimateiovalidations import IsValidIpacUltimateDevice
from .ipacultimateiodevicelist import  GetDeviceList

from .setlednr import SetLedNrListFlash
from .setlednr import SetLedNrListFadeToOff
from .setlednr import SetLedNrListFadeToOn

from .ipacultimateioboard import SetLEDsToIndividualBrightness

from ..common.globalvar import MIN_LED_NR
from ..common.globalvar import MAX_LED_NR


def SetAllLedIntensities(DeviceUUID=None,  IntensityLevel=88):
# This sets all LED to the same 'IntensityLevel' - basically white at different strengths
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    
    try:
        if not IsValidIntensityLevel(IntensityLevel): raise Exception("IntensityLevel not valid")

        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
    #            if IsDebugOn(): print(FUNC_NAME+"Set board with intensity level of " + str(IntensityLevel))
    #            if IsDebugOn(): print(FUNC_NAME+"DeviceUUID is :- " + str(DeviceUUID))
    #            if IsDebugOn(): print(FUNC_NAME+"mydevice is"+str(myDevice["DeviceID"].manufacturer))
                SetAllDeviceLEDCurrentStates(DeviceUUID=myDevice["DeviceUUID"],IntensityLevel=IntensityLevel,
                                               FadeIntensityLevel=IntensityLevel,State=True)
        SetLEDsToIndividualBrightness(DeviceUUID)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

def SetAllLedRandomStates(DeviceUUID=None):
# Randomly set Leds to be turned on or off
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    
    try:
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
                SetRandomDeviceLEDCurrentStates(myDevice["DeviceUUID"])

    # now use the random values and set all intensities !
    
        SetLEDsToIndividualBrightness(DeviceUUID)

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

def SetAllLedFlash(DeviceUUID=None, FlashCount=5, FlashIntervalTime=1):
# Flash all Leds  'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    try:
        if not IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("FlashIntervalTime not valid")
        if not IsValidFlashCount(FlashCount) : raise Exception("FlashCount not valid")

        counter1 = 0
        while counter1 < FlashCount:
            SetAllLedStates(DeviceUUID, True)
            time.sleep(FlashIntervalTime)
            SetAllLedStates(DeviceUUID, False)
            time.sleep(FlashIntervalTime)
            counter1 += 1

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

def SetAllLedRandomFlash(DeviceUUID=None, FlashCount=5, FlashIntervalTime=1):
# Set the Leds to a random brightness and the flash them 'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
 
    try:
        if not IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("FlashIntervalTime not valid")
        if not IsValidFlashCount(FlashCount) : raise Exception("FlashCount not valid")

        counter1 = 0
        myrandomdeviceleds= {}
        if IsDebugOn(): print("My random format legnth is :{0}".format(len(myrandomdeviceleds)))
    # create rand ledNrList for each device    
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
                LedNrList = []
                LedNr = MIN_LED_NR
                while LedNr <= MAX_LED_NR:
                    if random.randint(0,1) == 0:
                        LedNrList.append(LedNr)
                    LedNr += 1
                myrandomdeviceleds[myDevice["DeviceUUID"]] = LedNrList
                # myrandomdeviceleds = {"0:0:0:0" : [1,6,26,56],
                #                        "0:0:0:1" : [1,6,26,56],   }
                # we have now picked random Leds from all the devices - now flash tem on and off
        if IsDebugOn(): print("My random format legnth is :{0}".format(len(myrandomdeviceleds)))
        if IsDebugOn(): print(myrandomdeviceleds)

        while counter1 < FlashCount:
            for myDeviceUUID, myLedNrList in myrandomdeviceleds.items():
                if IsDebugOn(): print("Device UUID os :{0}".format(myDeviceUUID))
                if IsDebugOn(): print("myLedNrList os :{0}".format(myLedNrList))
                for LedNr in LedNrList:
                    SetDeviceLEDCurrentStatesLedState(myDeviceUUID,LedNr,False)
            SetLEDsToIndividualBrightness(DeviceUUID)
            time.sleep(FlashIntervalTime)

            for myDeviceUUID, LedNrList in myrandomdeviceleds.items():
                for LedNr in LedNrList:
                    SetDeviceLEDCurrentStatesLedState(myDeviceUUID,LedNr,True)
            SetLEDsToIndividualBrightness(DeviceUUID=DeviceUUID)
            time.sleep(FlashIntervalTime)
            counter1 += 1

    except Exception as err:
        raise Exception("{0} {1}".format(FUNC_NAME,err))


def SetAllLedStates(DeviceUUID=None, State = True):
# Set all Leds to be turned on or off
# The Leds will be turned back on at their previous brightness
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    
    try:
        if not IsValidState(State): raise Exception("{0}State not valid (True or False are valid".format(FUNC_NAME))
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
                SetAllDeviceLEDCurrentStatesLedState(myDevice["DeviceUUID"],State)
    
        SetLEDsToIndividualBrightness(DeviceUUID)

    except Exception as err:
        raise Exception("{0} {1}".format(FUNC_NAME,err))

def SetAllLedFadeReverb(DeviceUUID=None, FadeIncrement = 10, FadeIntervalTime = 0.1):
# Fade down and then up all Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
 
    try:
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("{0}IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("{0}FadeIncrement not valid")


        SetAllLedFadeToOff(DeviceUUID, FadeIncrement, FadeIntervalTime)
        SetAllLedFadeToOn(DeviceUUID, FadeIncrement, FadeIntervalTime)

    except Exception as err:
        raise Exception("{0} {1}".format(FUNC_NAME,err))

    return()

def SetAllLedFadeToOff(DeviceUUID=None, FadeIncrement = 10, FadeIntervalTime = 0.1):
# Fade down all Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    
    try:
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")

        maxIntensity = 0

        for myDevice in GetDeviceList():
            if DeviceUUID == None or DeviceUUID == myDevice["DeviceUUID"]: 
                LedNrList = Get_DeviceLEDList(myDevice["DeviceUUID"])
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
                    LedNrList = Get_DeviceLEDList(myDevice["DeviceUUID"])

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
    
def SetAllLedFadeToOn(DeviceUUID=None, FadeIncrement = 10, FadeIntervalTime = 0.1):
# Fade up all Leds to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    
    try:
        if not IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("IntervalTime not valid")
        if not IsValidFadeIncrement(FadeIncrement):  raise Exception("FadeIncrement not valid")

        maxIntensity = 0
    
        for myDevice in GetDeviceList():
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                LedNrList = Get_DeviceLEDList(myDevice["DeviceUUID"])
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
                    LedNrList = Get_DeviceLEDList(myDevice["DeviceUUID"])
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


if __name__ == '__main__':
    pass