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


from cgi import print_directory
from pickle import NONE
from xml.sax.handler import property_interning_dict
import usb.core
import usb.util
import usb.control


from ..utils.ledcurrentstateslist import InitLedStatus
from ..utils.lednrlist import InitLedNrList

from ..common.validations import _IsValidIpacUltimateDevice

from ..utils.ledcurrentstateslist import Get_DEVICE_LED_CURRENT_STATES

from .ipacultimateioboard import _sendMessageToBoard

from .setledall import SetAllLedIntensities

from ..common.globalvar import UM_VENDOR_ID_LIST
from ..common.globalvar import UM_PRODUCT_ID_LIST
from ..common.globalvar import USB_INTERFACE_INDEX



def InitDeviceList(FreeInterface = True, DeviceUUID = None, debug = False, xinput_flag=False):
#
# if DeviceUUID is passed in - this will only return tht device if it is found
    FUNC_NAME="InitDeviceList(): "
    if debug:
       print(FUNC_NAME)

    DeviceIDList=[]
    FoundDeviceIDs = usb.core.find(find_all=True)
    for DeviceID in FoundDeviceIDs:
 #       if debug:
 #          print(FUNC_NAME)
 #           print(DeviceID)
        if (_IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag) == True):
            if DeviceUUID == None: # Add all the boards
                myDevice= { "DeviceUUID": "{0}:{1}:{2}:{3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address), 
                           "DeviceID" : DeviceID }
                DeviceIDList.append(myDevice)
            else:
                # for the moment add the device regardless if we were suppsed to only return one board.
                myDevice= { "DeviceUUID": "{0}:{1}:{2}:{3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address), 
                           "DeviceID" : DeviceID }
                DeviceIDList.append(myDevice)

# Now initialise the LIST for holding LED status and LED Nr Status
    InitLedNrList(DeviceIDList, debug=debug)
    InitLedStatus(DeviceIDList, debug=debug)

#    if debug: 
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#        print (DeviceIDList)
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    for myDevice in DeviceIDList: 
        if debug:
            pass
#            print("Device_UUID")
#            print(myDevice["DeviceUUID"])
#            print("DEVICE")
#            print(myDevice["DeviceID"])
        if FreeInterface and myDevice["DeviceID"].is_kernel_driver_active(USB_INTERFACE_INDEX):
            try:
                myDevice["DeviceID"].detach_kernel_driver(USB_INTERFACE_INDEX)
            except usb.core.USBError as e:
                raise Exception("InitDevice(): Could not detatch kernel driver from interface({0}): {1}".format(USB_INTERFACE_INDEX, str(e)))

        SetAllLedIntensities(DeviceUUID=None,DeviceIDList=DeviceIDList, IntensityLevel=0, debug=debug)

    return(DeviceIDList)



def GetDeviceType(DeviceID, debug=False, xinput_flag=False):
    if not _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag): raise Exception("GetDeviceType(): DeviceID not valid")
    return("DEVICE ID {0}:{1} on Bus {2} Address {3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))

        
def GetVendorId(DeviceID, debug=False, xinput_flag=False):
    if not _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag): raise Exception("GetVendorId(): DeviceID not valid")
    return(hex(DeviceID.idVendor))
       
       
def GetProductId(DeviceID, debug=False, xinput_flag=False):
    if not _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag): raise Exception("GetProductId(): DeviceID not valid")
    return(hex(DeviceID.idProduct))
 
 
def GetVendorName(DeviceID, debug=False, xinput_flag=False):
    if not _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag): raise Exception("GetVendorName(): DeviceID not valid")
    return(DeviceID.manufacturer)
       
 
def GetProductName(DeviceID, debug=False, xinput_flag=False):
    if not _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag): raise Exception("GetProductName(): DeviceID not valid")
    return(DeviceID.product)
       
 
def GetSerialNumber(DeviceID, debug=False, xinput_flag=False):
    if not _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag): raise Exception("GetSerialNumber(): DeviceID not valid")
    return(DeviceID.serial_number)
       

#def GetLedIntensityStateList():
# shoudl return a list of format
# LedIntensityList = [ (ledNr, Intensity), (ledNr, Intensity), ...]
#    return(Get_LED_CURRENT_STATES())


def ResetDevices(DeviceUUID=None, DeviceIDList=[], debug=False, xinput_flag=False):
# Reset one or many devices/boards - this will mean the board(s) will start to run the script previously
# held in the firmware
# At present the message is wrong as it does not reste - this is now commented out
    
    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
            if not _IsValidIpacUltimateDevice(myDevice["DeviceID"], xinput_flag=xinput_flag): raise Exception("ResetDevices(): DeviceID not valid")
    
#            msg=[0x03,255,0,0,0]
#            _sendMessageToBoard(myDevice["DeviceID"], msg)
    

            for Led in Get_DEVICE_LED_CURRENT_STATES(myDevice["DeviceUUID"]):
                Led['LedIntensity'] = 0
                Led['LedFadeIntensity'] = 0
                Led['State'] = "Script"


if __name__ == '__main__':
    pass