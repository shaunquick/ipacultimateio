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

from ..utils.ledcurrentstateslist import Set_All_LED_CURRENT_STATES
from ..utils.ledcurrentstateslist import Set_Random_LED_CURRENT_STATES
from ..utils.ledcurrentstateslist import Set_All_LED_CURRENT_STATES_LedState

from ..utils.lednrlist import Get_LED_LIST_ALL                   

from ..common.validations import _IsValidFadeIntervalTime
from ..common.validations import _IsValidIpacUltimateDevice
from ..common.validations import _IsValidIntensityLevel
from ..common.validations import _IsValidLedNrList
from ..common.validations import _IsValidFlashIntervalTime
from ..common.validations import _IsValidFlashCount
from ..common.validations import _IsValidFadeIncrement
from ..common.validations import _IsValidState

from .ipacultimateioboard import _setLedsToIndividualBrightness
from .ipacultimateioboard import _sendMessageToBoard

from .setlednr import SetLedNrListFlash
from .setlednr import SetLedNrListFadeToOff
from .setlednr import SetLedNrListFadeToOn

from ..common.globalvar import MIN_LED_NR
from ..common.globalvar import MAX_LED_NR

def SetAllLedIntensities(DeviceID, IntensityLevel=88):
# This sets all LED to the same 'IntensityLevel' - basically white at different strengths
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetAllLedIntensities(): DeviceID not valid")
    if not _IsValidIntensityLevel(IntensityLevel): raise Exception("SetAllLedIntensities(): IntensityLevel not valid")
    
    msg=[0x03,128,IntensityLevel,0,0]
    _sendMessageToBoard(DeviceID, msg)
    

    Set_All_LED_CURRENT_STATES(IntensityLevel,IntensityLevel,"On")


def SetAllLedRandomStates(DeviceID):
# Randomly set Leds to be turned on or off
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetAllLedRandomStates(): DeviceID not valid")
    Set_Random_LED_CURRENT_STATES()

# now use the random values and set all intensities !
    
    _setLedsToIndividualBrightness(DeviceID)


def SetAllLedFlash(DeviceID, FlashCount=5, FlashIntervalTime=1):
# Flash all Leds  'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetAllLedFlash(): DeviceID not valid")
    if not _IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("SetAllLedFlash(): FlashIntervalTime not valid")
    if not _IsValidFlashCount(FlashCount) : raise Exception("SetAllLedFlash(): FlashCount not valid")

    counter1 = 0
    while counter1 < FlashCount:
        SetAllLedStates(DeviceID, False)
        time.sleep(FlashIntervalTime)
        SetAllLedStates(DeviceID, True)
        time.sleep(FlashIntervalTime)
        counter1 += 1

def SetAllLedRandomFlash(DeviceID, FlashCount=5, FlashIntervalTime=1):
# Set the Leds to a random brightness and the flash them 'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetAllLedRandomFlash(): DeviceID not valid")
    if not _IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("SetAllLedRandomFlash(): FlashIntervalTime not valid")
    if not _IsValidFlashCount(FlashCount) : raise Exception("SetAllLedRandomFlash(): FlashCount not valid")


    LedNrList = []
    LedNr = MIN_LED_NR
    while LedNr <= MAX_LED_NR:
        if random.randint(0,1) == 0: LedNrList.append(LedNr)
        LedNr += 1
    SetLedNrListFlash(DeviceID, LedNrList, FlashCount, FlashIntervalTime)       


def SetAllLedStates(DeviceID, State = True):
# Set all Leds to be turned on or off
# The Leds will be turned back on at their previous brightness
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetAllLedStates(): DeviceID not valid")
    if not _IsValidState(State): raise Exception("SetAllLedStates(): State not valid (True or False are valid")
    
    Set_All_LED_CURRENT_STATES_LedState(State)
    
    _setLedsToIndividualBrightness(DeviceID)

def SetAllLedFadeReverb(DeviceID, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Fade down and then up all Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds

    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetAllLedFadeReverb(): DeviceID not valid")
    if not _IsValidLedNrList(Get_LED_LIST_ALL()): raise Exception("SetAllLedFadeReverb(): LedList not valid : {0}".format(Get_LED_LIST_ALL()))
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetAllLedFadeReverb(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetAllLedFadeReverb(): FadeIncrement not valid")
    SetLedNrListFadeToOff(DeviceID, Get_LED_LIST_ALL(), FadeIncrement, FadeIntervalTime)
    SetLedNrListFadeToOn(DeviceID, Get_LED_LIST_ALL(), FadeIncrement, FadeIntervalTime)
    return()

def SetAllLedFadeToOff(DeviceID, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Fade down all Leds to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness

    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetAllLedFadeToOff(): DeviceID not valid")
    if not _IsValidLedNrList(Get_LED_LIST_ALL()): raise Exception("SetAllLedFadeToOff(): LedList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetAllLedFadeToOff(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetAllLedFadeToOff(): FadeIncrement not valid")
    SetLedNrListFadeToOff(DeviceID, Get_LED_LIST_ALL(), FadeIncrement, FadeIntervalTime)
    
def SetAllLedFadeToOn(DeviceID, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Fade up all Leds to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetAllLedFadeToOn(): DeviceID not valid")
    if not _IsValidLedNrList(Get_LED_LIST_ALL()): raise Exception("SetAllLedFadeToOn(): LedList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetAllLedFadeToOn(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetAllLedFadeToOn(): FadeIncrement not valid")
    SetLedNrListFadeToOn(DeviceID, Get_LED_LIST_ALL(), FadeIncrement, FadeIntervalTime)






if __name__ == '__main__':
    pass