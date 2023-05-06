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

from ..utils.ledcurrentstateslist import Get_DEVICE_LED_CURRENT_STATES 

import usb.core
import usb.util
import usb.control


USB_BM_REQUESTTYPE_SET_CONFIGURATION = 0x21  # decimal = 33,  binary = 00100001
USB_B_REQUEST_SET_CONFIGURATION = 9          # hex = 8,       binary = 00001000
USB_W_VALUE = 0x0203                         # decimal = 515, binary = 0000001000000011

UM_VENDOR_ID_LIST = [ 0xD209 ] # There should only be one Vendor - but there may be an issue when setup as XInput
UM_PRODUCT_ID_LIST = [ 0x0410, 0x0411, 0x0412, 0x0413 ]
USB_INTERFACE_INDEX = 2      # The USB has an array of interfaces - set the interface to the correct interface endpoint

UM_XINPUT_VENDOR_ID_LIST = [ 0X045e ]
UM_XINPUT_PRODUCT_ID_LIST =[ 0X028e ]
USB_XINPUT_INTERFACE_INDEX = 1      # The USB has an array of interfaces - set the interface to the correct interface endpoint


def _setLedsToIndividualBrightness(DeviceUUID=None, DeviceIDList=[], UseFadeValues = False, debug=False):
# Use the LED States that are stored in a list and set the intensity level based on the
# list data
# the list holds 3 values for each LED
# State - if State is Off - then the Led will be set with intensity of 0
# Intesnity level - values will be used to set intensity unless calling program asks
#                  for fade values to be used instaed
# Fade Intensity Level - and alternate intesnity level which is used when the upstream command
# wishes to mimic a fade pattern
   for myDevice in DeviceIDList:
        if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
            msg = [4]
            for LedCurrent in Get_DEVICE_LED_CURRENT_STATES(myDevice["DeviceUUID"]):
                if LedCurrent['State']:
                    if UseFadeValues:
                        Intensity = LedCurrent['LedFadeIntensity']
                    else:
                        Intensity = LedCurrent['LedIntensity']
                    msg.append(Intensity)
                else:
                    msg.append(0)    
            try:
                _sendMessageToBoard(myDevice["DeviceID"], msg, debug=debug)
            except Exception as err:
                raise Exception("_setLedsToIndividualBrightness(): {0}".format(err))
    
def _sendMessageToBoard(DeviceID, payload, debug=False):
    FUNC_NAME="_sendMessageToBoard(): "
# send a message to usb board - it is up to the upstream function to ensure
#message is in the correct format for the board to action it correctly
    if _IsValidIpacUltimateDevice(DeviceID, xinput_flag=True):
        try:
            if debug: 
                pass
#                print(FUNC_NAME+"USB interface Nr:- " + str(_getUSBInterfaceNumber(DeviceID)))
#                print(FUNC_NAME+"Payload is :-")
#                print(payload)
            DeviceID.ctrl_transfer(USB_BM_REQUESTTYPE_SET_CONFIGURATION, USB_B_REQUEST_SET_CONFIGURATION, USB_W_VALUE,
                              _getUSBInterfaceNumber(DeviceID), payload)
        except Exception as err:
            raise Exception("_sendMessageToBoard(): {0}".format(err))
    else:
        raise Exception("_sendMessageToBoard(): DeviceID not valid")

def _getUSBInterfaceNumber(DeviceID, debug=False):
    FUNC_NAME="_getUSBInterfaceNumber(): "
# return the interface index depening if it is the io board in default mode
# or retrun a different value 
    if _IsValidIpacUltimateDevice(DeviceID, debug=debug):
        if debug: print(FUNC_NAME+"Index=" + str(USB_INTERFACE_INDEX))
        return(USB_INTERFACE_INDEX)
    elif _IsValidIpacUltimateDevice(DeviceID, xinput_flag=True, debug=debug):
        if debug: print(FUNC_NAME+"Index=" + str(USB_XINPUT_INTERFACE_INDEX))
        return(USB_XINPUT_INTERFACE_INDEX)
    else:
        if debug: print(FUNC_NAME+"Exception")
        raise Exception("GetUSBInterfaceNumber(): DeviceID not valid")


def _IsValidIpacUltimateDevice(DeviceID, debug=False, xinput_flag=False):
# Verify the board is an iPAC Ultimate IO
    if (DeviceID != None and DeviceID.idProduct in UM_PRODUCT_ID_LIST and DeviceID.idVendor in UM_VENDOR_ID_LIST ):
        return (True)
    elif xinput_flag and DeviceID.idProduct in UM_XINPUT_PRODUCT_ID_LIST and DeviceID.idVendor in UM_XINPUT_VENDOR_ID_LIST:
        return (True)
    else:
        return(False)


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

def _getDeviceUUID(DeviceID):
    return("{0}:{1}:{2}:{3}".format(DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))

def _resetDevice(DeviceID):
    # 
# Commented out as this command is not working on the board.    
#            msg=[0x03,255,0,0,0]
#            _sendMessageToBoard(myDevice["DeviceID"], msg)   pass
    pass


if __name__ == '__main__':
    pass