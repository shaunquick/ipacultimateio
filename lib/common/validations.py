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


# This module has all of the common validations used across multiple
# modules
from .common_lib import GetMyFuncName
from .common_lib import IsDebugOn

from .globalvar import MAX_INTENSITY_LEVEL
from .globalvar import MAX_LEDS
from .globalvar import MIN_LED_NR
from .globalvar import MAX_LED_NR
from .globalvar import MIN_FADE_INTERVAL_TIME
from .globalvar import MAX_FADE_INTERVAL_TIME
from .globalvar import MIN_FADE_INCREMENT
from .globalvar import MAX_FADE_INCREMENT
from .globalvar import MIN_FLASH_INTERVAL_TIME
from .globalvar import MAX_FLASH_INTERVAL_TIME
from .globalvar import MIN_FLASH_COUNT
from .globalvar import MAX_FLASH_COUNT
from .globalvar import MIN_WAIT_INTERVAL_TIME
from .globalvar import MAX_WAIT_INTERVAL_TIME
from .globalvar import MIN_FLASH_COUNT
from .globalvar import MAX_FLASH_COUNT
from .globalvar import MIN_NR_CYCLES
from .globalvar import MAX_NR_CYCLES
from .globalvar import MIN_CYCLE_INTERVAL_TIME
from .globalvar import MAX_CYCLE_INTERVAL_TIME


    
def IsValidLedNr(LedNr):
# Verify the LedNr is valid between 0 and 95
    if (type(LedNr) is not int): return (False)
    if not(LedNr >= MIN_LED_NR and LedNr <= MAX_LED_NR): return (False)
    return(True)

def IsValidLedNrList(LedNrList):
# Verify the List of LedNrs are valid
    if (type(LedNrList) is not list): return(False)
    for LedNr in LedNrList:
        if not IsValidLedNr(LedNr): return(False)
    return(True)

def IsValidState(State):
# Verify the State value is True or False
    if (type(State) is not bool): return (False)
    return(True)

def IsValidIntensityLevel(IntensityLevel):
# Verify the IntensityLevel value is between 0 and 255    
    if (type(IntensityLevel) is not int): return (False)
    if not(IntensityLevel >= 0 and IntensityLevel <= MAX_INTENSITY_LEVEL): return (False)
    return(True)

def _IsValidUseFadeValues(UseFadeValues):
# Verify the UseFadeValues value is True or False
    if (type(UseFadeValues) is not bool): return (False)
    return(True)

def IsValidFadeIntervalTime(IntervalTime):
# Verify the IntensityLevel value is between 0 and 255
    if not (type(IntervalTime) is int or float): return (False)
    if not (IntervalTime >= MIN_FADE_INTERVAL_TIME and IntervalTime <= MAX_FADE_INTERVAL_TIME): return (False)
    return(True)


def IsValidWaitIntervalTime(IntervalTime):
# Verify the IntensityLevel value is between 0 and 255
    if not (type(IntervalTime) is int or float): return (False)
    if not (IntervalTime >= MIN_WAIT_INTERVAL_TIME and IntervalTime <= MAX_WAIT_INTERVAL_TIME): return (False)
    return(True)


def IsValidFadeIncrement(FadeIncrement):
    if type(FadeIncrement) is not int: return (False)
    if not(FadeIncrement >= MIN_FADE_INCREMENT and FadeIncrement <= MAX_FADE_INCREMENT): return (False)
    return(True)

def IsValidFlashIntervalTime(FlashIntervalTime):
    if not (type(FlashIntervalTime) is int or float): return (False)
    if not (FlashIntervalTime >= MIN_FLASH_INTERVAL_TIME and FlashIntervalTime <= MAX_FLASH_INTERVAL_TIME): return (False)
    return(True)


def IsValidFlashCount(FlashCount):
    
    if type(FlashCount) is not int:
        print("Flashcount NOT int= {0}".format(FlashCount))
        return (False)
    if not (FlashCount >= MIN_FLASH_COUNT and FlashCount <= MAX_FLASH_COUNT):
        print("Flashcount NOT in range = {0}".format(FlashCount))
        return (False)
    return(True)
        

def IsValidLedNrStateList(LedNrStateList):
    if (type(LedNrStateList) is not list): return(False)
    for LedNrState in LedNrStateList:
        if not IsValidLedNr(LedNrState['LedNr']): return (False)
        if not IsValidState(LedNrState['State']): return (False)        
    return(True)

def IsValidLedNrAndIntensityList(LedNrAndIntensityList):
# LedIntensityList = [ (ledNr, IntensityLevel), (ledNr, IntensityLevel), ...]
# IntensityLevel= value between 0-255
# LedNr = value between 0 -96

    if (type(LedNrAndIntensityList) is not list): return (False)
    if len(LedNrAndIntensityList) > MAX_LEDS: return (False)
    for LedNrIntensity in LedNrAndIntensityList:
        if (not(IsValidLedNr(LedNrIntensity['LedNr']))): return(False)
        if (not(IsValidIntensityLevel(LedNrIntensity['IntensityLevel']))): return(False)
    return(True)
 
def IsValidRGBIntensityList(RGBIntensityList):
    # the list has to hold at least 3 values,
    # but if it holds more than 3 then it has to hold RGB triples
    if (type(RGBIntensityList) is not list): return (False)
    # if the RGB List is not divisible by 3 exactly then the list is wrong
    if len(RGBIntensityList) % 3 != 0: return (False)
    
    for RGBIntensity in RGBIntensityList:
        if type(RGBIntensity) is not int : return (False)
        if not IsValidIntensityLevel(RGBIntensity): return (False)
    return(True)

def IsValidRainbowRGBListIndex(RainbowRGBListIndex):
    if type(RainbowRGBListIndex) is not int : return (False)
    return(True)


def IsValidNrOfRepetitions(NrOfRepetitions):
    if type(NrOfRepetitions) is not int : return (False)
    return(True)

def IsValidNrCommandsToRepeat(NrCommandsToRepeat):
    if type(NrCommandsToRepeat) is not int : return (False)
    return(True)


def IsValidNrCycles(NrCycles):
    
    if type(NrCycles) is not int:
        return (False)
    if not (NrCycles >= MIN_NR_CYCLES and NrCycles <= MAX_NR_CYCLES):
        return (False)
    return(True)

def IsValidCycleIntervalTime(CycleIntervalTime):
    if not (type(CycleIntervalTime) is int or float): return (False)
    if not (CycleIntervalTime >= MIN_CYCLE_INTERVAL_TIME and CycleIntervalTime <= MAX_CYCLE_INTERVAL_TIME): return (False)
    return(True)



if __name__ == '__main__':
    pass