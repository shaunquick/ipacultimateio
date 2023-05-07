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



# This module holds the functions that communicate directly with the
# ultimarc-io LED Board
# 

from ..utils.ledcurrentstateslist import Get_DeviceLEDCurrentStates
from ..common.common_lib import my_func_name

from .ipacultimateiodevicelist import Get_DeviceList

from .ipacultimateiovalidations import _IsValidIpacUltimateDevice


import usb.core
import usb.util
import usb.control


USB_BM_REQUESTTYPE_SET_CONFIGURATION = 0x21  # decimal = 33,  binary = 00100001
USB_B_REQUEST_SET_CONFIGURATION = 9          # hex = 8,       binary = 00001000
USB_W_VALUE = 0x0203                         # decimal = 515, binary = 0000001000000011

USB_INTERFACE_INDEX = 2      # The USB has an array of interfaces - set the interface to the correct interface endpoint

USB_XINPUT_INTERFACE_INDEX = 1      # The USB has an array of interfaces - set the interface to the correct interface endpoint


def _setLEDsToIndividualBrightness(DeviceUUID=None, UseFadeValues = False, debug=False):
# Use the LED States that are stored in a list and set the intensity level based on the
# list data
# the list holds 3 values for each LED
# State - if State is Off - then the Led will be set with intensity of 0
# Intesnity level - values will be used to set intensity unless calling program asks
#                  for fade values to be used instaed
# Fade Intensity Level - and alternate intesnity level which is used when the upstream command
# wishes to mimic a fade pattern

    FUNC_NAME=my_func_name()
    if debug: print(FUNC_NAME)


    try:
#        if debug: print("retriving Device IDs with id of ")
#        if debug: print(DeviceUUID)
#        if debug: print("End of DeviceUUID")
        DeviceIDList = Get_DeviceList(DeviceUUID, debug)
#        if debug: print("retrived Device IDs")
        for myDevice in DeviceIDList:
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                msg = [4]
#                if debug: print("myDevice")
#                if debug: print(myDevice)
#                if debug: print("EndmyDevice")
                for LEDCurrent in Get_DeviceLEDCurrentStates(myDevice["DeviceUUID"]):
#                    if debug: print(LEDCurrent)
                    if LEDCurrent['State']:
                        if UseFadeValues:
                            Intensity = LEDCurrent['LedFadeIntensity']
                        else:
                            Intensity = LEDCurrent['LedIntensity']
                        msg.append(Intensity)
                    else:
                        msg.append(0)    
                    _sendMessageToBoard(myDevice["DeviceID"], msg, debug=debug)
    
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))



def _sendMessageToBoard(DeviceID, payload, debug=False):
    FUNC_NAME="_sendMessageToBoard(): "
#    if debug: print(FUNC_NAME)
# send a message to usb board - it is up to the upstream function to ensure
#message is in the correct format for the board to action it correctly
    try:
        if _IsValidIpacUltimateDevice(DeviceID, xinput_flag=True):
            if debug: 
                pass
#                print(FUNC_NAME+"USB interface Nr:- " + str(_getUSBInterfaceNumber(DeviceID)))
#                print(FUNC_NAME+"Payload is :-")
#                print(payload)
            DeviceID.ctrl_transfer(USB_BM_REQUESTTYPE_SET_CONFIGURATION, USB_B_REQUEST_SET_CONFIGURATION, USB_W_VALUE,
                                _getUSBInterfaceNumber(DeviceID), payload)
        else:
            raise Exception("{0}{1}".format(FUNC_NAME,"DeviceID not valid"))

    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))



def _getUSBInterfaceNumber(DeviceID, debug=False):
    FUNC_NAME="_getUSBInterfaceNumber(): "
# return the interface index depening if it is the io board in default mode
# or retrun a different value 
    if _IsValidIpacUltimateDevice(DeviceID, debug=debug):
#        if debug: print(FUNC_NAME+"Index=" + str(USB_INTERFACE_INDEX))
        return(USB_INTERFACE_INDEX)
    elif _IsValidIpacUltimateDevice(DeviceID, xinput_flag=True, debug=debug):
#        if debug: print(FUNC_NAME+"Index=" + str(USB_XINPUT_INTERFACE_INDEX))
        return(USB_XINPUT_INTERFACE_INDEX)
    else:
#        if debug: print(FUNC_NAME+"Exception")
        raise Exception("GetUSBInterfaceNumber(): DeviceID not valid")





def _isKernalDriverActive(DeviceID, debug=False):
    FUNC_NAME="_isKernalDriverActive(): "
    if debug: print(FUNC_NAME)
    result=False
    try:

        result= DeviceID.is_kernel_driver_active(_getUSBInterfaceNumber(DeviceID))
        if debug: print(FUNC_NAME+"Driver Active is :-" + str(result))
    except usb.core.USBError as e:
        raise Exception(FUNC_NAME+"Could not check active kernel driver from interface({0}): {1}".format(_getUSBInterfaceNumber(myDevice["DeviceID"]), str(e)))

    return(result)


def _detatchKernalDriver(DeviceID, debug=False):
    FUNC_NAME="_detatchKernalDriver(): "
    if debug: print(FUNC_NAME)
    result=False
    try:
        result = DeviceID.detach_kernel_driver(_getUSBInterfaceNumber(DeviceID)) 
        if debug: print(FUNC_NAME+"detached driver is :-" + str(result))
    except usb.core.USBError as e:
        raise Exception(FUNC_NAME+"Could not detatch kernel driver from interface({0}): {1}".format(_getUSBInterfaceNumber(myDevice["DeviceID"]), str(e)))


    return(result)



def _resetDevice(DeviceID):
    # 
# Commented out as this command is not working on the board.    
#            msg=[0x03,255,0,0,0]
#            _sendMessageToBoard(myDevice["DeviceID"], msg)   pass
    pass


if __name__ == '__main__':
    pass