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


# This module process commands from the script - where the user has
# defined a group of Led's as a logical grouping
# Based on the grouping e.g. {LedGroupeName: "pinkElephant", LedNrs:[1,2,3]}}
# the groupname can be used to control the Leds as opposed tp
# the spefic led Numbers - this makes it easier to control a buttons RGB values
# for example.

from ..utils.ledgroupname import _convertLEDGroupNameIntensityListToLedNrIntensityList
from ..utils.ledgroupname import _convertLEDGroupNameListToLedNrList
from ..utils.ledgroupname import _convertLEDGroupNameToLedNrList
from ..utils.ledgroupname import _convertLEDGroupNameStateListToLedStateList 

from ..utils.ledgroupname import _IsValidLedGroupName
from ..utils.ledgroupname import _IsValidLedGroupNameList 
from ..utils.ledgroupname import _IsValidLedGroupNameStateList
from ..utils.ledgroupname import _IsValidLedGroupNameIntensityList
from ..utils.ledgroupname import _IsValidRGBIntensityList

from ..common.validations import _IsValidFadeIntervalTime
from ..common.validations import _IsValidIpacUltimateDevice
from ..common.validations import _IsValidIntensityLevel
from ..common.validations import _IsValidFlashIntervalTime
from ..common.validations import _IsValidFlashCount
from ..common.validations import _IsValidFadeIncrement
from ..common.validations import _IsValidNrCycles
from ..common.validations import _IsValidCycleIntervalTime

from .setlednr import SetLedNrIntensity
from .setlednr import SetLedNrListIntensities
from .setlednr import SetLedNrIntensityList
from .setlednr import SetLedNrStateList
from .setlednr import SetLedNrListFadeReverb
from .setlednr import SetLedNrListFlash
from .setlednr import SetLedNrListFadeToOff
from .setlednr import SetLedNrListFadeToOn


def SetLedGroupNameListIntensities(DeviceID, LedGroupNameList, IntensityLevel=60):
#  Set all the Leds in the group to the same intensity level
# LedGroupNameList=[ "p1b1", "p1b2", "p1b3", "p1b4" ]
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedGroupNameListIntensities(): DeviceID not valid")
    if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedGroupNameListIntensities(): LedGroupNameList not valid")
    if not _IsValidIntensityLevel(IntensityLevel): raise Exception("SetLedGroupNameListIntensities(): IntensityLevel not valid")
    
    SetLedNrListIntensities(DeviceID=DeviceID, LedNrList = _convertLEDGroupNameListToLedNrList(LedGroupNameList), IntensityLevel=IntensityLevel)


def SetLedGroupNameIntensityList(DeviceID,LedGroupNameIntensityList):
#  Set all the Leds in the group to different intensity level
#    LedGroupNameIntensityList = [ {"LedGroupName" : "p1b1", "RGBIntensity" : [255,11,22] }, {"LedGroupName" : "p1b2", "RGBIntensity" : [255,11,22] }]
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedGroupNameIntensityList(): DeviceID not valid")
    if not _IsValidLedGroupNameIntensityList(LedGroupNameIntensityList): raise Exception("SetLedGroupNameIntensityList(): LedIntensityList not valid")

    SetLedNrIntensityList(DeviceID=DeviceID,LedNrIntensityList= _convertLEDGroupNameIntensityListToLedNrIntensityList(LedGroupNameIntensityList))

def SetLedGroupNameIntensity(DeviceID,LedGroupName, RGBIntensityList):
#  Set a secific group to their specific brightness
# LedGroupName="p1b1"
#  RGBIntensityList=[255,11,22] - note this was designed for 3 values for the Red Green Blue Leds
    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedGroupNameIntensity(): DeviceID not valid")
    if not _IsValidLedGroupName(LedGroupName):  raise Exception("SetLedGroupNameIntensity(): LedGroupName not valid")
    if not _IsValidRGBIntensityList(RGBIntensityList):  raise Exception("SetLedGroupNameIntensity(): RGBIntensityList not valid")

    LedsList = _convertLEDGroupNameToLedNrList(LedGroupName)
    SetLedNrIntensity(DeviceID=DeviceID,LedNr=LedsList[0] , IntensityLevel=RGBIntensityList[0])
    SetLedNrIntensity(DeviceID=DeviceID,LedNr=LedsList[1] , IntensityLevel=RGBIntensityList[1])
    SetLedNrIntensity(DeviceID=DeviceID,LedNr=LedsList[2] , IntensityLevel=RGBIntensityList[2])


def SetLedGroupNameListFlash(DeviceID, LedGroupNameList, FlashCount, FlashIntervalTime):
# Set all the Leds in the group to flash
# 'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds

    if not _IsValidIpacUltimateDevice(DeviceID):  raise Exception("SetLedListFlash(): DeviceID not valid")
    if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFlash(): LedNrList not valid")
    if not _IsValidFlashIntervalTime(FlashIntervalTime) : raise Exception("SetLedListFlash(): FlashIntervalTime not valid")
    if not _IsValidFlashCount(FlashCount) : raise Exception("SetLedListFlash(): FlashCount not valid")
    
    SetLedNrListFlash(DeviceID=DeviceID, LedNrList = _convertLEDGroupNameListToLedNrList(LedGroupNameList), FlashCount=FlashCount, FlashIntervalTime=FlashIntervalTime)

def SetLedGroupNameStateList(DeviceID, LedGroupNameStateList):
#  Set all the Leds in the group to on or off
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedStateList(): DeviceID not valid")
    if not _IsValidLedGroupNameStateList(LedGroupNameStateList):  raise Exception("SetLedStateList(): State not valid")
    
    SetLedNrStateList(DeviceID=DeviceID, LedNrStateList=_convertLEDGroupNameStateListToLedStateList(LedGroupNameStateList))

def SetLedGroupNameListFadeReverb(DeviceID, LedGroupNameList, FadeIncrement, FadeIntervalTime):
#  Set all the Leds in the group to
# Fade down and then up  to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
#
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedListFadeReverb(): DeviceID not valid")
    if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFadeReverb(): LedNrList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeReverb(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeReverb(): FadeIncrement not valid")
    
    
    SetLedNrListFadeReverb(DeviceID=DeviceID, LedNrList = _convertLEDGroupNameListToLedNrList(LedGroupNameList),
                           FadeIncrement=FadeIncrement, FadeIntervalTime=FadeIntervalTime)

    return()

def SetLedGroupNameListFadeToOff(DeviceID, LedGroupNameList, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
#  Set all the Leds in the group to
# Fade down  to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedListFadeToOff(): DeviceID not valid")
    if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFadeToOff(): LedNrList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeToOff(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeToOff(): FadeIncrement not valid")

    
    SetLedNrListFadeToOff(DeviceID=DeviceID, LedNrList= _convertLEDGroupNameListToLedNrList(LedGroupNameList), FadeIncrement=FadeIncrement, FadeIntervalTime=FadeIntervalTime )
    return()

def SetLedGroupNameListFadeToOn(DeviceID, LedGroupNameList, FadeIncrement = 10, FadeIntervalTime = 0.1 ):
# Set all the Leds in the group to
# Fade up to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedListFadeToOn(): DeviceID not valid")
    if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFadeToOn(): LedList not valid")
    if not _IsValidFadeIntervalTime(FadeIntervalTime):  raise Exception("SetLedListFadeToOn(): IntervalTime not valid")
    if not _IsValidFadeIncrement(FadeIncrement):  raise Exception("SetLedListFadeToOn(): FadeIncrement not valid")

    SetLedNrListFadeToOn(DeviceID=DeviceID, LedNrList= _convertLEDGroupNameListToLedNrList(LedGroupNameList), FadeIncrement=FadeIncrement, FadeIntervalTime=FadeIntervalTime)

    return()

def SetLedGroupNameListRainbowCycle(DeviceID, LedGroupNameList, NrCycles, CycleIntervalTime):

    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("SetLedGroupNameListRainbowCycle(): DeviceID not valid")
    if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedGroupNameListRainbowCycle(): LedList not valid")
    if not _IsValidNrCycles(NrCycles):  raise Exception("SetLedGroupNameListRainbowCycle(): NrCycles not valid")
    if not _IsValidCycleIntervalTime(CycleIntervalTime):  raise Exception("SetLedGroupNameListRainbowCycle(): CycleIntervalTime not valid")


    LedNrList= _convertLEDGroupNameListToLedNrList(LedGroupNameList)
    SetLedNrListRainbow(DeviceID, LedNrList, NrCycles, CycleIntervalTime)
    pass

if __name__ == '__main__':
    pass