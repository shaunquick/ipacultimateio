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


from ..common.validations import _IsValidIpacUltimateDevice

from ..utils.ledcurrentstateslist import Get_LED_CURRENT_STATES

from .ipacultimateioboard import _sendMessageToBoard

from .setledall import SetAllLedIntensities

from ..common.globalvar import UM_VENDOR_ID
from ..common.globalvar import UM_PRODUCT_ID
from ..common.globalvar import USB_INTERFACE_INDEX



def InitDevice(FreeInterface = True):
#
#
    DeviceID = usb.core.find(idVendor=UM_VENDOR_ID, idProduct=UM_PRODUCT_ID)
    if (_IsValidIpacUltimateDevice(DeviceID) == False):
        raise Exception("InitDevice(): Could not find device(VendorID:{0}), ProductID:{1}".format(UM_VENDOR_ID, UM_PRODUCT_ID))

    if FreeInterface and DeviceID.is_kernel_driver_active(USB_INTERFACE_INDEX):
        try:
            DeviceID.detach_kernel_driver(USB_INTERFACE_INDEX)
        except usb.core.USBError as e:
            raise Exception("InitDevice(): Could not detatch kernel driver from interface({0}): {1}".format(USB_INTERFACE_INDEX, str(e)))
     
    SetAllLedIntensities(DeviceID, 0)
    return(DeviceID)


def GetDeviceType(DeviceID):
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("GetDeviceType(): DeviceID not valid")
    return("DEVICE ID {0}:{1} on Bus {2} Address {3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))

        
def GetVendorId(DeviceID):
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("GetVendorId(): DeviceID not valid")
    return(hex(DeviceID.idVendor))
       
       
def GetProductId(DeviceID):
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("GetProductId(): DeviceID not valid")
    return(hex(DeviceID.idProduct))
 
 
def GetVendorName(DeviceID):
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("GetVendorName(): DeviceID not valid")
    return(DeviceID.manufacturer)
       
 
def GetProductName(DeviceID):
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("GetProductName(): DeviceID not valid")
    return(DeviceID.product)
       
 
def GetSerialNumber(DeviceID):
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("GetSerialNumber(): DeviceID not valid")
    return(DeviceID.serial_number)
       

def GetLedIntensityStateList():
# shoudl return a listy of format
# LedIntensityList = [ (ledNr, Intensity), (ledNr, Intensity), ...]
    return(Get_LED_CURRENT_STATES())


def ResetBoard(DeviceID):
# Reset the board - this will mean the board will start to run the script previously
# held in the firmware
    
    if not _IsValidIpacUltimateDevice(DeviceID): raise Exception("ResetBoard(): DeviceID not valid")
    
    msg=[0x03,255,0,0,0]
    _sendMessageToBoard(DeviceID, msg)
    

    for Led in Get_LED_CURRENT_STATES():
        Led['LedIntensity'] = 0
        Led['LedFadeIntensity'] = 0
        Led['State'] = "Script"


if __name__ == '__main__':
    pass