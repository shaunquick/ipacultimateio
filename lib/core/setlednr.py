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


# LED_CURRENT_STATES holds the current led number (index valiue), setintensitylevel, fadeintensitylevel and State (On or Off or (setBy)Script) 
#from .ipacultimateio import LED_LIST_ALL
#from .corevariables import LED_CURRENT_STATES

from ..common.validations import _IsValidFadeIntervalTime
from ..common.validations import _IsValidIpacUltimateDevice
from ..common.validations import _IsValidIntensityLevel
from ..common.validations import _IsValidLedNrList
from ..common.validations import _IsValidFlashIntervalTime
from ..common.validations import _IsValidFlashCount
from ..common.validations import _IsValidFadeIncrement
from ..common.validations import _IsValidLedNr
from ..common.validations import _IsValidLedNrIntensityList
from ..common.validations import _IsValidLedNrStateList

from .ipacultimateioboard import _setLedsToIndividualBrightness
from .ipacultimateioboard import _sendMessageToBoard

from ..utils.ledcurrentstateslist import Set_LED_CURRENT_STATES_LedIntensity    
from ..utils.ledcurrentstateslist import Set_LED_CURRENT_STATES_LedFadeIntensity
from ..utils.ledcurrentstateslist import Set_LED_CURRENT_STATES_LedState        
from ..utils.ledcurrentstateslist import Get_LED_CURRENT_STATES_LedIntensity
from ..utils.ledcurrentstateslist import Get_LED_CURRENT_STATES_LedFadeIntensity
#from ..utils.ledcurrentstateslist import Get_LED_CURRENT_STATES

def SetLedNrIntensity(DeviceID, LedNr = 3, IntensityLevel=100):
# Set a specific 'LedNr' to a specific 'IntensityLevel'

    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedIntensity(): DeviceID not valid")
    if not _IsValidLedNr(LedNr): raise Exception("SetLedIntensity(): LedNr not valid")
    if not _IsValidIntensityLevel(IntensityLevel): raise Exception("SetLedIntensity(): IntensityLevel not valid")
    
# when interfacing with the board the LedNr starts from 0 - so we need to decrement by 1
    msg=[0x03,LedNr-1,IntensityLevel,0,0]
    _sendMessageToBoard(DeviceID, msg)


    Set_LED_CURRENT_STATES_LedIntensity(LedNr,IntensityLevel)
    Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,IntensityLevel)
    Set_LED_CURRENT_STATES_LedState(LedNr,"On")

def SetLedNrListIntensities(DeviceID, LedNrList, IntensityLevel=60):
# Set a list  of 'LedNr' to a specific 'IntensityLevel'
# LedNrList = [1,2,3]
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedListIntensities(): DeviceID not valid")
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListIntensities(): LedNrList not valid")
    if not _IsValidIntensityLevel(IntensityLevel): raise Exception("SetLedListIntensities(): IntensityLevel not valid")
    for LedNr in LedNrList:
        Set_LED_CURRENT_STATES_LedIntensity(LedNr,IntensityLevel)
        Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,IntensityLevel)
        Set_LED_CURRENT_STATES_LedState(LedNr,"On")
    
    _setLedsToIndividualBrightness(DeviceID)



def SetLedNrIntensityList(DeviceID,LedNrIntensityList):
# Set a list of Led's to a unique intensity level
# LedIntensityList = [ {"LedNr": 1, "IntensityLevel": 122}, {ledNr, IntensityLevel), ...]
    
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedIntensityList(): DeviceID not valid")
    if not _IsValidLedNrIntensityList(LedNrIntensityList): raise Exception("SetLedIntensityList(): LedIntensityList not valid")
    for LedIntensity in LedNrIntensityList:
        LedNr = LedIntensity['LedNr']
        IntensityLevel = LedIntensity['IntensityLevel']
        Set_LED_CURRENT_STATES_LedIntensity(LedNr,IntensityLevel)
        Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,IntensityLevel)
        Set_LED_CURRENT_STATES_LedState(LedNr,"On")        
    
    _setLedsToIndividualBrightness(DeviceID)

def SetLedNrListFlash(DeviceID, LedNrList, FlashCount, FlashIntervalTime):
# Flash a list Leds  'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
# LedNrList = [1,2,3]

    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedListFlash(): DeviceID not valid")
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFlash(): LedNrList not valid - {}".format(LedNrList))
    if not _IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("SetLedListFlash(): FlashIntervalTime not valid")
    if not _IsValidFlashCount(FlashCount) : raise Exception("SetLedListFlash(): FlashCount not valid")

    LedNrStateListOn = []
    LedNrStateListOff = []
    for LedNr in LedNrList:
        LedNrStateListOn.append({'LedNr': LedNr, 'State': True})
        LedNrStateListOff.append({'LedNr': LedNr, 'State': False})

    counter1 = 0
    while counter1 < FlashCount:
        SetLedNrStateList(DeviceID, LedNrStateListOff)
        time.sleep(FlashIntervalTime)
        SetLedNrStateList(DeviceID, LedNrStateListOn)
        time.sleep(FlashIntervalTime)
        counter1 += 1

def SetLedNrStateList(DeviceID, LedNrStateList):
# Set a list of Led's to a uniques state - either on or off
# LedNrStateList = [ {"ledNr": 1, "State" : True}, {"ledNr": 1, "State" : False} ...]
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedStateList(): DeviceID not valid")
    if not _IsValidLedNrStateList(LedNrStateList):  raise Exception("SetLedStateList(): State not valid")

    for LedState in LedNrStateList:
        LedNr = LedState['LedNr']
        LedState = LedState['State']
        if LedState: Set_LED_CURRENT_STATES_LedState(LedNr,"On")
        else:        Set_LED_CURRENT_STATES_LedState(LedNr,"Off")
    _setLedsToIndividualBrightness(DeviceID)
        

def SetLedNrListFadeReverb(DeviceID, LedNrList, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Fade down and then up a list of Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedListFadeReverb(): DeviceID not valid")
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFadeReverb(): LedNrList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeReverb(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeReverb(): FadeIncrement not valid")
    SetLedNrListFadeToOff(DeviceID, LedNrList, FadeIncrement, FadeIntervalTime)
    SetLedNrListFadeToOn(DeviceID, LedNrList, FadeIncrement, FadeIntervalTime)
    return()


def SetLedNrListFadeToOff(DeviceID, LedNrList, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Fade down a list of Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedListFadeToOff(): DeviceID not valid")
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFadeToOff(): LedNrList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeToOff(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeToOff(): FadeIncrement not valid")

    maxIntensity = 0

    for LedNr in LedNrList:
        LedIntensity = Get_LED_CURRENT_STATES_LedIntensity(LedNr)
        Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr, LedIntensity)
        if (LedIntensity> maxIntensity): maxIntensity = LedIntensity

    _setLedsToIndividualBrightness(DeviceID, UseFadeValues=True)

    NrOfIterations = int(maxIntensity/FadeIncrement)
    counter1 = 1
    while counter1 < NrOfIterations + 1:
        for LedNr in LedNrList:

            NewLedIntensity = Get_LED_CURRENT_STATES_LedFadeIntensity(LedNr) - FadeIncrement
            if NewLedIntensity >= 0 :
                Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,NewLedIntensity)
            else:
                Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,0)
        _setLedsToIndividualBrightness(DeviceID, UseFadeValues=True)
        counter1 += 1
        time.sleep(FadeIntervalTime)
    return()


def SetLedNrListFadeToOn(DeviceID, LedNrList, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Fade up a list of Leds to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedListFadeToOn(): DeviceID not valid")
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFadeToOn(): LedList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeToOn(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeToOn(): FadeIncrement not valid")
    maxIntensity = 0
    
    for LedNr in LedNrList:
        Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,0)
        LedIntensity = Get_LED_CURRENT_STATES_LedIntensity(LedNr)
        if (LedIntensity > maxIntensity): maxIntensity = LedIntensity
            
    _setLedsToIndividualBrightness(DeviceID, UseFadeValues=True)

    NrOfIterations = int(maxIntensity/FadeIncrement)
    counter1 = 1
    while counter1 < NrOfIterations + 1:
        for LedNr in LedNrList:
            MaxSetLedIntensity = Get_LED_CURRENT_STATES_LedIntensity(LedNr)
            NewFadeLedIntensity = Get_LED_CURRENT_STATES_LedFadeIntensity(LedNr) + FadeIncrement
            if NewFadeLedIntensity < MaxSetLedIntensity:
                Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,NewFadeLedIntensity)
            else:
                Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr, MaxSetLedIntensity)

        _setLedsToIndividualBrightness(DeviceID, UseFadeValues=True)
        counter1 += 1
        time.sleep(FadeIntervalTime)
    return()


def SetLedNrListRainbowCycle(DeviceID, LedNrList, NrCycles, CycleIntervalTime, RainbowRGBListIndex = 0):
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

    RainbowRGBListLength = len(RainbowRGBList)


    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedListIntensities(): DeviceID not valid")
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListIntensities(): LedNrList not valid")
    curr_index = RainbowRGBListIndex * 3
    cycle_count = 0
    while cycle_count <= NrCycles:
        for LedNr in LedNrList:
            if curr_index > RainbowRGBListLength:
                curr_index = 0

            Set_LED_CURRENT_STATES_LedIntensity(LedNr,RainbowRGBList[curr_index])
            Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,RainbowRGBList[curr_index])
            Set_LED_CURRENT_STATES_LedState(LedNr,"On")
            curr_index += 1
        _setLedsToIndividualBrightness(DeviceID)
        time.wait(CycleIntervalTime)
        cycle_count += 1

if __name__ == '__main__':
    pass