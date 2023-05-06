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


from ..utils.ledcurrentstateslist import Get_DEVICE_LED_CURRENT_STATES

from .ipacultimateioboard import _IsValidIpacUltimateDevice
from .ipacultimateioboard import _sendMessageToBoard
from .ipacultimateioboard import _setLedsToIndividualBrightness
from .ipacultimateioboard import _getUSBInterfaceNumber
from .ipacultimateioboard import _isKernalDriverActive
from .ipacultimateioboard import _detatchKernalDriver

from .ipacultimateioboard import  _getDeviceUUID

from .setledall import SetAllLedIntensities



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
        if _IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag):
            if DeviceUUID == None: # Add all the boards
                myDevice= { "DeviceUUID": _getDeviceUUID(DeviceID), 
                           "DeviceID" : DeviceID }
                DeviceIDList.append(myDevice)
            else:
                # Only add the board that has been passed in
                if DeviceUUID == _getDeviceUUID(DeviceID):
                    myDevice= { "DeviceUUID": _getDeviceUUID(DeviceID), 
                           "DeviceID" : DeviceID }
                    DeviceIDList.append(myDevice)

# Now initialise the LIST for holding LED status and LED Nr Status
    InitLedNrList(DeviceIDList, debug=debug)
    InitLedStatus(DeviceIDList, debug=debug)

#    if debug: 
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#        print (DeviceIDList)
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    try:    
        for myDevice in DeviceIDList: 
            if debug:
                pass
#               print(FUNC_NAME+"Device_UUID :"+str(myDevice["DeviceUUID"]))
#               print(FUNC_NAME+"DEVICE ;"+str(myDevice["DeviceID"]))
#            if debug: print(FUNC_NAME+"FreeInt = " + str(FreeInterface))
#            if debug: print(FUNC_NAME+"is driver active = " + str(_isKernalDriverActive(myDevice["DeviceID"], debug=debug)))
            if FreeInterface and _isKernalDriverActive(myDevice["DeviceID"], debug=debug):
                _detatchKernalDriver(myDevice["DeviceID"], debug=debug)

        SetAllLedIntensities(DeviceUUID=DeviceUUID,DeviceIDList=DeviceIDList, IntensityLevel=0, debug=debug)
    except Exception as err:
        raise Exception("InitDeviceList(): {0}".format(err))

    return(DeviceIDList)



def GetDeviceType(DeviceID, debug=False):
    return("DEVICE ID {0}:{1} on Bus {2} Address {3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))

        
def GetVendorId(DeviceID, debug=False):
    return(hex(DeviceID.idVendor))
       
       
def GetProductId(DeviceID, debug=False):
    return(hex(DeviceID.idProduct))
 
 
def GetVendorName(DeviceID, debug=False):
    return(DeviceID.manufacturer)
       
 
def GetProductName(DeviceID, debug=False):
    return(DeviceID.product)
       
 
def GetSerialNumber(DeviceID, debug=False):
    return(DeviceID.serial_number)


def ResetDevices(DeviceUUID=None, DeviceIDList=[], debug=False):
# Reset one or many devices/boards - this will mean the board(s) will start to run the script previously
# held in the firmware
# At present the message is wrong as it does not reset - this is now commented out
    
    for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
# Commented out as this command is not working on the board.    
#            msg=[0x03,255,0,0,0]
#            _sendMessageToBoard(myDevice["DeviceID"], msg)
    

            for Led in Get_DEVICE_LED_CURRENT_STATES(myDevice["DeviceUUID"]):
                Led['LedIntensity'] = 0
                Led['LedFadeIntensity'] = 0
                Led['State'] = "Script"

     _setLedsToIndividualBrightness(DeviceUUID, DeviceIDList)

if __name__ == '__main__':
    pass