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


from ..utils.lednrlist import Initialise_DeviceListLEDList

from ..utils.ledgroupname import Initialise_LedGroupNameList
from ..utils.ledgroupnamedefinitionslist import InitLedGroupNameDefinitionsList


from ..utils.ledcurrentstateslist import Get_DeviceLEDCurrentStates
from ..utils.ledcurrentstateslist import Initialise_DeviceListLEDCurrentStates

from .ipacultimateioboard import _IsValidIpacUltimateDevice
from .ipacultimateioboard import _resetDevice
from .ipacultimateioboard import _setLEDsToIndividualBrightness
from .ipacultimateioboard import _getUSBInterfaceNumber
from .ipacultimateioboard import _isKernalDriverActive
from .ipacultimateioboard import _detatchKernalDriver

from .ipacultimateioboard import  _getDeviceUUID

from .ipacultimateiodevicelist import  Initialise_DeviceList


from .setledall import SetAllLedIntensities

def Initialise_DeviceLists(FreeInterface = True, DeviceUUID = None, debug = False, xinput_flag=False):
#
# if DeviceUUID is passed in - this will only return that device if it is found
# if xinput_flag is set to true - then find all device that we hope are ultimarc ones, including where they are set in XInput mode
# This will return a list of DeviceUUIDs and their associated usb DeviceID's
    FUNC_NAME="Initialise_DeviceLists(): "
    if debug:
       print(FUNC_NAME)


    Initialise_DeviceList(DeviceUUID)
# Now initialise the LIST for holding LED status and LED Nr Status
    try:    
        LEDGroupDefsList = InitLedGroupNameDefinitionsList(DEVICE_LIST, debug)
        Initialise_LedGroupNameList(LEDGroupDefsList,debug)
        Initialise_DeviceListLEDList(DEVICE_LIST, debug=debug)
        Initialise_DeviceListLEDCurrentStates(DEVICE_LIST, debug=debug)

#    if debug: 
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#        print (DeviceIDList)
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        for myDevice in DEVICE_LIST: 
            if debug:
                pass
#               print(FUNC_NAME+"Device_UUID :"+str(myDevice["DeviceUUID"]))
#               print(FUNC_NAME+"DEVICE ;"+str(myDevice["DeviceID"]))
#            if debug: print(FUNC_NAME+"FreeInt = " + str(FreeInterface))
#            if debug: print(FUNC_NAME+"is driver active = " + str(_isKernalDriverActive(myDevice["DeviceID"], debug=debug)))
            if FreeInterface and _isKernalDriverActive(myDevice["DeviceID"], debug=debug):
                _detatchKernalDriver(myDevice["DeviceID"], debug=debug)

        SetAllLedIntensities(DeviceUUID=DeviceUUID,DeviceIDList=DEVICE_LIST, IntensityLevel=0, debug=debug)
    except Exception as err:
        raise Exception("Initialise_DeviceList(): {0}".format(err))

    return(DEVICE_LIST)

def GetDeviceType(DeviceUUID, debug=False):
    DeviceID=Get_DeviceList(DeviceUUID)["DeviceID"]
    return("DEVICE ID {0}:{1} on Bus {2} Address {3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))

        
def GetVendorId(DeviceUUID, debug=False):
    DeviceID=Get_DeviceList(DeviceUUID)["DeviceID"]
    return(hex(DeviceID.idVendor))
       
       
def GetProductId(DeviceUUID, debug=False):
    DeviceID=Get_DeviceList(DeviceUUID)["DeviceID"]
    return(hex(DeviceID.idProduct))
 
 
def GetVendorName(DeviceUUID, debug=False):
    DeviceID=Get_DeviceList(DeviceUUID)["DeviceID"]
    return(DeviceID.manufacturer)
       
 
def GetProductName(DeviceUUID, debug=False):
    DeviceID=Get_DeviceList(DeviceUUID)["DeviceID"]
    return(DeviceID.product)
       
 
def GetSerialNumber(DeviceUUID, debug=False):
    DeviceID=Get_DeviceList(DeviceUUID)["DeviceID"]
    return(DeviceID.serial_number)


def ResetDevices(DeviceUUID=None, debug=False):
# Reset one or many devices/boards - this will mean the board(s) will start to run the script previously
# held in the firmware
# At present the message is wrong as it does not reset - this is now commented out
    
    for myDevice in Get_DeviceList(DeviceUUID, debug=debug):
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]):
# Commented out as this command is not working on the board.  
# # This should then run the default script  
#            _resetDevice(myDevice["DeviceID"])
    

            for Led in Get_DeviceLEDCurrentStates(myDevice["DeviceUUID"]):
                Led['LedIntensity'] = 0
                Led['LedFadeIntensity'] = 0
                Led['State'] = "Script"

     # as we cannot call _resetDevice - just set the LED's to the resetted values
    _setLedsToIndividualBrightness(DeviceUUID, DeviceIDList)

if __name__ == '__main__':
    pass