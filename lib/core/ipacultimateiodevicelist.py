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

from ..common.common_lib        import GetMyFuncName
from ..common.common_lib        import IsDebugOn

from .ipacultimateiovalidations import IsValidIpacUltimateDevice

DEVICE_LIST =[]

def InitialiseDeviceList(DeviceUUID = None, xinput_flag=False):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
#
# if DeviceUUID is passed in - this will only return that device if it is found
# if xinput_flag is set to true - then find all device that we hope are ultimarc ones, including where they are set in XInput mode
# This will return a list of DeviceUUIDs and their associated usb DeviceID's

    global DEVICE_LIST

    FoundDeviceIDs = usb.core.find(find_all=True)
    for DeviceID in FoundDeviceIDs:
 #       if IsDebugOn():
 #          print(FUNC_NAME)
 #           print(DeviceID)
        if IsValidIpacUltimateDevice(DeviceID, xinput_flag=xinput_flag):
            if DeviceUUID == None: # Add all the boards
                myDevice= { "DeviceUUID": _getDeviceUUID(DeviceID), 
                           "DeviceID" : DeviceID }
                DEVICE_LIST.append(myDevice)
            else:
                # Only add the board that has been passed in
                if DeviceUUID == _getDeviceUUID(DeviceID):
                    myDevice= { "DeviceUUID": _getDeviceUUID(DeviceID), 
                           "DeviceID" : DeviceID }
                    DEVICE_LIST.append(myDevice)


    return(None)

def GetDeviceList(DeviceUUID=None):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    global DEVICE_LIST
    if DeviceUUID == None:
        return(DEVICE_LIST)
    else:
        NEW_DEVICE_LIST = []
        for myDevice in DEVICE_LIST:
 #           if IsDebugOn(): print("myDevice")
 #           if IsDebugOn(): print(myDevice)
 #           if IsDebugOn(): print("myDevice[DeviceUUID]")
 #           if IsDebugOn(): print(myDevice["DeviceUUID"])
            if DeviceUUID == myDevice["DeviceUUID"]:
                NEW_DEVICE_LIST.append(myDevice)
#        if IsDebugOn(): print(NEW_DEVICE_LIST)
        return(NEW_DEVICE_LIST)


def _getDeviceUUID(DeviceID):
    return("{0}:{1}:{2}:{3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))
