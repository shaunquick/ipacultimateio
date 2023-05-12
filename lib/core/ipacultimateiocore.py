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

# This module provide some core functions, such as initiale the board
# for use by other modules
# Basic Board information can also be returned by the following
# functions

import usb.core
import usb.util
import usb.control

from ..common.common_lib import GetMyFuncName
from ..common.common_lib import IsDebugOn

from .ipacultimateiovalidations import IsValidIpacUltimateDevice

from ..utils.lednrlist import InitialiseDeviceListLEDList

from ..utils.ledgroupname import InitialiseLedGroupNameList
from ..utils.ledgroupnamedefinitionslist import InitialiseLedGroupNameDefinitionsList

from ..utils.ledcurrentstateslist import GetDeviceLEDCurrentStates
from ..utils.ledcurrentstateslist import InitialiseDeviceListLEDCurrentStates

from .ipacultimateiodevicelist import  InitialiseDeviceList
from .ipacultimateiodevicelist import  GetDeviceList


from .ipacultimateioboard import ResetIODevice
from .ipacultimateioboard import SetLEDsToIndividualBrightness
from .ipacultimateioboard import GetUSBInterfaceNumber
from .ipacultimateioboard import IsKernalDriverActive
from .ipacultimateioboard import DetatchKernalDriver

from .setledall import SetAllLedIntensities


def InitialiseDeviceLists(FreeInterface = True, DeviceUUID = None, xinput_flag=False):
#
# if DeviceUUID is passed in - this will only return that device if it is found
# if xinput_flag is set to true - then find all device that we hope are ultimarc ones, including where they are set in XInput mode
# This will return a list of DeviceUUIDs and their associated usb DeviceID's
 
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
 
    InitialiseDeviceList(DeviceUUID)
# Now initialise the LIST for holding LED status and LED Nr Status
    try:    
        myDeviceList=GetDeviceList()
        LEDGroupDefsList = InitialiseLedGroupNameDefinitionsList()
        InitialiseLedGroupNameList(LEDGroupDefsList)
        InitialiseDeviceListLEDList(myDeviceList)
        InitialiseDeviceListLEDCurrentStates(myDeviceList)


        for myDevice in myDeviceList: 
#            if IsDebugOn():    print(FUNC_NAME+"Device_UUID :"+str(myDevice["DeviceUUID"]))
#            if IsDebugOn():    print(FUNC_NAME+"DEVICE ;"+str(myDevice["DeviceID"]))
#            if IsDebugOn(): print(FUNC_NAME+"FreeInt = " + str(FreeInterface))
#            if IsDebugOn(): print(FUNC_NAME+"is driver active = " + str(IsKernalDriverActive(myDevice["DeviceID"])))
            if FreeInterface and IsKernalDriverActive(myDevice["DeviceID"]):
                DetatchKernalDriver(myDevice["DeviceID"])

        SetAllLedIntensities(DeviceUUID=DeviceUUID, IntensityLevel=0)
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

    return(myDeviceList)

def GetDeviceType(DeviceUUID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DeviceID=GetDeviceList(DeviceUUID)["DeviceID"]
    return("DEVICE ID {0}:{1} on Bus {2} Address {3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))

        
def GetVendorId(DeviceUUID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DeviceID=GetDeviceList(DeviceUUID)["DeviceID"]
    return(hex(DeviceID.idVendor))
       
       
def GetProductId(DeviceUUID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DeviceID=GetDeviceList(DeviceUUID)["DeviceID"]
    return(hex(DeviceID.idProduct))
 
 
def GetVendorName(DeviceUUID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DeviceID=GetDeviceList(DeviceUUID)["DeviceID"]
    return(DeviceID.manufacturer)
       
 
def GetProductName(DeviceUUID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DeviceID=GetDeviceList(DeviceUUID)["DeviceID"]
    return(DeviceID.product)
       
 
def GetSerialNumber(DeviceUUID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    DeviceID=GetDeviceList(DeviceUUID)["DeviceID"]
    return(DeviceID.serial_number)

def ResetDevices(DeviceUUID=None):
# Reset one or many devices/boards - this will mean the board(s) will start to run the script previously
# held in the firmware
# At present the message is wrong as it does not reset - this is now commented out
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    
    for myDevice in GetDeviceList(DeviceUUID):
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
# Commented out as this command is not working on the board.  
# # This should then run the default script  
#            ResetIODevice(myDevice["DeviceID"])
    

            for Led in GetDeviceLEDCurrentStates(myDevice["DeviceUUID"]):
                Led['LedIntensity'] = 0
                Led['LedFadeIntensity'] = 0
                Led['State'] = "Script"

     # as we cannot call ResetIODevice - just set the LED's to the resetted values
    SetLEDsToIndividualBrightness(DeviceUUID)

if __name__ == '__main__':
    pass