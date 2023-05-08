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

from ast import Try
from ..common.common_lib import my_func_name

from ..utils.ledgroupnamedefinitionslist import _convertLedGroupNameIntensityListToDevicesLedNrIntensityList
from ..utils.ledgroupnamedefinitionslist import _convertLedGroupNameListToDevicesLedNrList
from ..utils.ledgroupnamedefinitionslist import _convertLedGroupNameToDevicesLedNrList
from ..utils.ledgroupnamedefinitionslist import _convertLedGroupNameStateListToDevicesLedStateList 

from ..utils.ledgroupname import _IsValidLedGroupName
from ..utils.ledgroupname import _IsValidLedGroupNameList 
from ..utils.ledgroupname import _IsValidLedGroupNameStateList
from ..utils.ledgroupname import _IsValidLedGroupNameIntensityList
from ..utils.ledgroupname import _IsValidRGBIntensityList

from ..common.validations import _IsValidFadeIntervalTime
from ..common.validations import _IsValidIntensityLevel
from ..common.validations import _IsValidFlashIntervalTime
from ..common.validations import _IsValidFlashCount
from ..common.validations import _IsValidFadeIncrement
from ..common.validations import _IsValidNrCycles
from ..common.validations import _IsValidCycleIntervalTime

from .ipacultimateiovalidations import _IsValidIpacUltimateDevice

from .setlednr import SetLedNrIntensity
from .setlednr import SetLedNrListIntensities
from .setlednr import SetLedNrIntensityList
from .setlednr import SetLedNrStateList
from .setlednr import SetLedNrListFadeReverb
from .setlednr import SetLedNrListFlash
from .setlednr import SetLedNrListFadeToOff
from .setlednr import SetLedNrListFadeToOn
from .setlednr import SetDevicesLedNrListRainbowCycle

def SetLedGroupNameListIntensities(DeviceUUID=None, LedGroupNameList=[], IntensityLevel=60, debug=False):
#  Set all the Leds in the group to the same intensity level
# LedGroupNameList=[ "p1b1", "p1b2", "p1b3", "p1b4" ]
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)


    try:
        if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedGroupNameListIntensities(): LedGroupNameList not valid")
    
        for DeviceLedNrList in _convertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList, debug):
            SetLedNrListIntensities(DeviceUUID=DeviceLedNrList["DeviceUUID"],  
                                LedNrList = DeviceLedNrList["LedNrList"], IntensityLevel=IntensityLevel,debug=debug)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameIntensityList(DeviceUUID=None, LedGroupNameIntensityList=[], debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

#  Set all the Leds in the group to different intensity level
#    LedGroupNameIntensityList = [ {"LedGroupName" : "p1b1", "RGBIntensity" : [255,11,22] }, 
#    {"LedGroupName" : "p1b2", "RGBIntensity" : [255,11,22] }]
    try:
        if not _IsValidLedGroupNameIntensityList(LedGroupNameIntensityList): raise Exception("SetLedGroupNameIntensityList(): LedIntensityList not valid")
 
        for DeviceLedNrIntensityList in _convertLedGroupNameIntensityListToDevicesLedNrIntensityList(DeviceUUID, 
                                                                                                      LedGroupNameIntensityList, debug):
            for myDeviceUUID, myDeviceLedNrIntensityList in DevicesLedNrIntensityList:
                SetLedNrIntensityList(DeviceUUID=DeviceLedNrIntensityList["DeviceUUID"],  
                              LedNrIntensityList= DeviceLedNrIntensityList["LedNrIntensityList"], debug=debug)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

def SetLedGroupNameIntensity(DeviceUUID=None, LedGroupName="", RGBIntensityList=[], debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

#  Set a secific group to their specific brightness
# LedGroupName="p1b1"
#  RGBIntensityList=[255,11,22] - note this was designed for 3 values for the Red Green Blue Leds
    try:
        if not _IsValidLedGroupName(LedGroupName):  raise Exception("SetLedGroupNameIntensity(): LedGroupName not valid")
        if not _IsValidRGBIntensityList(RGBIntensityList):  raise Exception("SetLedGroupNameIntensity(): RGBIntensityList not valid")


                        
        for DeviceLedNrList in     _convertLedGroupNameToDevicesLedNrList(DeviceUUID,LedGroupName,debug=debug):
            SetLedNrIntensity(DeviceUUID=DeviceLedNrList["DeviceUUID"], LedNr=DeviceLedNrList["LedNrList"][0] , IntensityLevel=RGBIntensityList[0])
            SetLedNrIntensity(DeviceUUID=DeviceLedNrList["DeviceUUID"], LedNr=DeviceLedNrList["LedNrList"][1] , IntensityLevel=RGBIntensityList[1])
            SetLedNrIntensity(DeviceUUID=DeviceLedNrList["DeviceUUID"], LedNr=DeviceLedNrList["LedNrList"][2] , IntensityLevel=RGBIntensityList[2])
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameListFlash(DeviceUUID=None, LedGroupNameList=[], FlashCount=3, FlashIntervalTime=3, debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

# Set all the Leds in the group to flash
# 'FlashCount' times
# at a rate of 'FlashIntervalTime' seconds

    try:
        if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFlash(): LedNrList not valid")
    
        for DeviceLedNrList in _convertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList, debug):
            SetLedNrListFlash(DeviceUUID=DeviceLedNrList["DeviceUUID"], 
                          LedNrList = DeviceLedNrList["LedNrList"], 
                          FlashCount=FlashCount, FlashIntervalTime=FlashIntervalTime)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetLedGroupNameStateList(DeviceUUID=None, LedGroupNameStateList=[], debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

#  Set all the Leds in the group to on or off
    try:
        if not _IsValidLedGroupNameStateList(LedGroupNameStateList):  raise Exception("SetLedStateList(): State not valid")
        for DeviceLedStateList in _convertLedGroupNameStateListToDevicesLedStateList(DeviceUUID, LedGroupNameStateList):
            for myDeviceUUID, myDeviceLedNrStateList in DevicesLedStateList:
                SetLedNrStateList(DeviceUUID=DeviceLedStateList["DeviceUUID"],  
                          LedNrStateList=DeviceLedStateList["LedNrStateList"])
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

def SetLedGroupNameListFadeReverb(DeviceUUID=None, LedGroupNameList=[], FadeIncrement=10, FadeIntervalTime=0.1, debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

#  Set all the Leds in the group to
# Fade down and then up  to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
# and then..
# Increase brightness from 0 by 'FadeINcrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
#
    try:
        if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFadeReverb(): LedNrList not valid")
        for DeviceLedNrList in _convertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList, debug):
                SetLedNrListFadeReverb(DeviceUUID=DeviceLedNrList["DeviceUUID"], 
                               LedNrList = DeviceLedNrList["LedNrList"],
                               FadeIncrement=FadeIncrement, FadeIntervalTime=FadeIntervalTime, debug=debug)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return()

def SetLedGroupNameListFadeToOff(DeviceUUID=None, LedGroupNameList=[], FadeIncrement = 10, 
                                 FadeIntervalTime = 0.1, debug=False ):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

#  Set all the Leds in the group to
# Fade down  to their previously set brightness level
# Reduce brightness by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds until they are all set to zero brightness
    try:
        if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFadeToOff(): LedNrList not valid")

        for DeviceLedNrList in _convertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList, debug):
            SetLedNrListFadeToOff(DeviceUUID=DeviceLedNrList["DeviceUUID"],  
                              LedNrList= DeviceLedNrList["LedNrList"], 
                              FadeIncrement=FadeIncrement, FadeIntervalTime=FadeIntervalTime )
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))
    return()

def SetLedGroupNameListFadeToOn(DeviceUUID=None, LedGroupNameList=[], FadeIncrement = 10, 
                                FadeIntervalTime = 0.1, debug=False ):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)

# Set all the Leds in the group to
# Fade up to their previously set brightness level
# Increase brightness from 0 by 'FadeIncrement' and reduce the fade in
# steps of 'FadeIntervalTime' seconds
    try:
        if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedListFadeToOn(): LedList not valid")

        for DeviceLedNrList in _convertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList, debug):
            SetLedNrListFadeToOn(DeviceUUID=DeviceLedNrList["DeviceUUID"],  
                             LedNrList= DeviceLedNrList["LedNrList"], 
                             FadeIncrement=FadeIncrement, FadeIntervalTime=FadeIntervalTime)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return()

def SetLedGroupNameListRainbowCycle(DeviceUUID=None, LedGroupNameList=[], NrCycles=2, CycleIntervalTime=1, debug=False):
    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)


    try:
        if not _IsValidLedGroupNameList(LedGroupNameList): raise Exception("SetLedGroupNameListRainbowCycle(): LedList not valid")
        DevicesLedNrList = _convertLedGroupNameListToDevicesLedNrList(DeviceUUID, LedGroupNameList, debug)
        SetDevicesLedNrListRainbowCycle(DevicesLedNrList=DevicesLedNrList, 
                                     NrCycles=NrCycles, CycleIntervalTime=CycleIntervalTime)
        pass
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

if __name__ == '__main__':
    pass