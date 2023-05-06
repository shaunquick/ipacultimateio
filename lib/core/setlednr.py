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

from ..common.validations import _IsValidFadeIntervalTime
from ..common.validations import _IsValidIntensityLevel
from ..common.validations import _IsValidLedNrList
from ..common.validations import _IsValidFlashIntervalTime
from ..common.validations import _IsValidFlashCount
from ..common.validations import _IsValidFadeIncrement
from ..common.validations import _IsValidLedNr
from ..common.validations import _IsValidLedNrIntensityList
from ..common.validations import _IsValidLedNrStateList

from .ipacultimateioboard import _setLEDsToIndividualBrightness
#from .ipacultimateioboard import _sendMessageToBoard
from .ipacultimateioboard import _IsValidIpacUltimateDevice

from ..utils.ledcurrentstateslist import Set_DeviceLEDCurrentStates_LedIntensity    
from ..utils.ledcurrentstateslist import Set_DeviceLEDCurrentStates_LedFadeIntensity
from ..utils.ledcurrentstateslist import Set_DeviceLEDCurrentStates_LedState        
from ..utils.ledcurrentstateslist import Get_DeviceLEDCurrentStates_LedIntensity
from ..utils.ledcurrentstateslist import Get_DeviceLEDCurrentStates_LedFadeIntensity

def SetLedNrIntensity(DeviceUUID=None, DeviceIDList=[], LedNr = 3, IntensityLevel=100, debug=False):
# Set a specific 'LedNr' to a specific 'IntensityLevel'

    if not _IsValidLedNr(LedNr): raise Exception("SetLedIntensity(): LedNr not valid")
    if not _IsValidIntensityLevel(IntensityLevel): raise Exception("SetLedIntensity(): IntensityLevel not valid")

    for myDevice in DeviceIDList:   
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
        # when interfacing with the board the LedNr starts from 0 - so we need to decrement by 1
# WE have many devices - just re-use now the standard of calling     _setLedsToIndividualBrightness
# #
##        msg=[0x03,LedNr-1,IntensityLevel,0,0]
#        _sendMessageToBoard(myDevice["DeviceID"], msg)

            Set_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
            Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
            Set_DeviceLEDCurrentStates_LedState(myDevice["DeviceUUID"],LedNr,True)
    _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, debug==debug)

def SetLedNrListIntensities(DeviceUUID=None, DeviceIDList=[], LedNrList=[], IntensityLevel=60, debug=False):
# Set a list  of 'LedNr' to a specific 'IntensityLevel'
# LedNrList = [1,2,3]
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListIntensities(): LedNrList not valid")
    if not _IsValidIntensityLevel(IntensityLevel): raise Exception("SetLedListIntensities(): IntensityLevel not valid")

    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            for LedNr in LedNrList:
                Set_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                Set_DeviceLEDCurrentStates_LedState(myDevice["DeviceUUID"],LedNr,True)
    
    _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, debug==debug)



def SetLedNrIntensityList(DeviceUUID=None, DeviceIDList=[], LedNrIntensityList=[], debug=False):
# Set a list of Led's to a unique intensity level
# LedIntensityList = [ {"LedNr": 1, "IntensityLevel": 122}, {ledNr, IntensityLevel), ...]
    if not _IsValidLedNrIntensityList(LedNrIntensityList): raise Exception("SetLedIntensityList(): LedIntensityList not valid")
    
    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            for LedIntensity in LedNrIntensityList:
                LedNr = LedIntensity['LedNr']
                IntensityLevel = LedIntensity['IntensityLevel']
                Set_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,IntensityLevel)
                Set_DeviceLEDCurrentStates_LedState(myDevice["DeviceUUID"],LedNr,True)        
    
    _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, debug=debug)

def SetLedNrListFlash(DeviceUUID=None, DeviceIDList=[], LedNrList=[], FlashCount=3, FlashIntervalTime=3, debug=False):
# Flash a list Leds  'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
# LedNrList = [1,2,3]
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFlash(): LedNrList not valid - {}".format(LedNrList))
    if not _IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("SetLedListFlash(): FlashIntervalTime not valid")
    if not _IsValidFlashCount(FlashCount) : raise Exception("SetLedListFlash(): FlashCount not valid")

    LedNrStateListOn = []
    LedNrStateListOff = []

    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            for LedNr in LedNrList:
                LedNrStateListOn.append({'LedNr': LedNr, 'State': True})
                LedNrStateListOff.append({'LedNr': LedNr, 'State': False})

            counter1 = 0
            while counter1 < FlashCount:
                SetLedNrStateList(myDevice["DeviceUUID"], DeviceIDList, LedNrStateListOff)
                time.sleep(FlashIntervalTime)
                SetLedNrStateList(myDevice["DeviceUUID"], DeviceIDList, LedNrStateListOn)
                time.sleep(FlashIntervalTime)
                counter1 += 1

def SetLedNrStateList(DeviceUUID=None, DeviceIDList=[], LedNrStateList=[], debug=False):
# Set a list of Led's to a uniques state - either on or off
# LedNrStateList = [ {"ledNr": 1, "State" : True}, {"ledNr": 1, "State" : False} ...]
    if not _IsValidLedNrStateList(LedNrStateList):  raise Exception("SetLedStateList(): State not valid")
    
    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            for LedState in LedNrStateList:
                LedNr = LedState['LedNr']
                LedState = LedState['State']
                if LedState : Set_DeviceLEDCurrentStates_LedState(myDevice["DeviceUUID"],LedNr,True)
                else:        Set_DeviceLEDCurrentStates_LedState(myDevice["DeviceUUID"],LedNr,False)
    _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, debug=debug)
        

def SetLedNrListFadeReverb(DeviceUUID=None, DeviceIDList=[], LedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1, debug=False):
# Fade down and then up a list of Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFadeReverb(): LedNrList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeReverb(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeReverb(): FadeIncrement not valid")
  
    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            SetLedNrListFadeToOff(myDevice["DeviceUUID"],DeviceIDList, LedNrList, FadeIncrement, FadeIntervalTime)
            SetLedNrListFadeToOn(myDevice["DeviceUUID"],DeviceIDList, LedNrList, FadeIncrement, FadeIntervalTime)
    return()


def SetLedNrListFadeToOff(DeviceUUID=None, DeviceIDList=[], LedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1, debug=False):
# Fade down a list of Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
    
    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFadeToOff(): LedNrList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeToOff(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeToOff(): FadeIncrement not valid")

    maxIntensity = 0

    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            for LedNr in LedNrList:
                LedIntensity = Get_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr)
                Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr, LedIntensity)
                if (LedIntensity> maxIntensity): maxIntensity = LedIntensity
            _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, UseFadeValues=True, debug=debug)

    NrOfIterations = int(maxIntensity/FadeIncrement)
    counter1 = 1
    while counter1 < NrOfIterations + 1:
        for myDevice in DeviceIDList:
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for LedNr in LedNrList:
                    NewLedIntensity = Get_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr) - FadeIncrement
                    if NewLedIntensity >= 0 :
                        Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,NewLedIntensity)
                    else:
                        Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,0)
                _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, UseFadeValues=True)
        counter1 += 1
        time.sleep(FadeIntervalTime)
    return()


def SetLedNrListFadeToOn(DeviceUUID=None, DeviceIDList=[], LedNrList=[], FadeIncrement = 10, FadeIntervalTime = 0.1,debug=False):
# Fade up a list of Leds to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedListFadeToOn(): LedList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeToOn(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeToOn(): FadeIncrement not valid")

    maxIntensity = 0
    
    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            for LedNr in LedNrList:
                Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,0)
                LedIntensity = Get_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr)
                if (LedIntensity > maxIntensity): maxIntensity = LedIntensity           
            _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, UseFadeValues=True)

    NrOfIterations = int(maxIntensity/FadeIncrement)
    counter1 = 1
    while counter1 < NrOfIterations + 1:
        for myDevice in DeviceIDList:
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                for LedNr in LedNrList:
                    MaxSetLedIntensity = Get_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr)
                    NewFadeLedIntensity = Get_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr) + FadeIncrement
                    if NewFadeLedIntensity < MaxSetLedIntensity:
                        Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,NewFadeLedIntensity)
                    else:
                        Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr, MaxSetLedIntensity)
                _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList, UseFadeValues=True)
        counter1 += 1
        time.sleep(FadeIntervalTime)
    return()


def SetLedNrListRainbowCycle(DeviceUUID=None, DeviceIDList=[], LedNrList=[], NrCycles=3, 
                             CycleIntervalTime=3, RainbowRGBListIndex = 0, debug=False):
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

    if not _IsValidLedNrList(LedNrList): raise Exception("SetLedNrListRainbowCycle(): LedNrList not valid")
    curr_index = RainbowRGBListIndex * 3
    cycle_count = 0
    first_LedNr = LedNrList[0]
    while cycle_count <= NrCycles:
        is_cycle_finished = False
        while not is_cycle_finished:
            for myDevice in DeviceIDList:
                if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                    for LedNr in LedNrList:
                        if curr_index >= RainbowRGBListLength:
                            curr_index = 0

                        Set_DeviceLEDCurrentStates_LedIntensity(myDevice["DeviceUUID"],LedNr,RainbowRGBList[curr_index])
                        Set_DeviceLEDCurrentStates_LedFadeIntensity(myDevice["DeviceUUID"],LedNr,RainbowRGBList[curr_index])
                        Set_DeviceLEDCurrentStates_LedState(myDevice["DeviceUUID"],LedNr,True)
                        curr_index += 1
            if not is_cycle_finished:
                _setLEDsToIndividualBrightness(DeviceUUID, DeviceIDList)
                time.sleep(CycleIntervalTime)
                curr_index = curr_index - len(LedNrList) + 3
                if curr_index < 0:
                    curr_index += len(RainbowRGBList)
                if curr_index == RainbowRGBListIndex:
                  is_cycle_finished = True


        cycle_count += 1


if __name__ == '__main__':
    pass