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
import usb.core
import usb.util
import usb.control

import time

from ..common.common_lib            import GetMyFuncName
from ..common.common_lib            import IsDebugOn

from .ipacultimateiodevicelist      import GetDeviceList
from ..utils.ledcurrentstateslist   import GetDeviceLEDCurrentStates

from .ipacultimateiovalidations     import IsValidIpacUltimateDevice


USB_BM_REQUESTTYPE_SET_CONFIGURATION = 0x21  # decimal = 33,  binary = 00100001
USB_B_REQUEST_SET_CONFIGURATION = 9          # hex = 8,       binary = 00001000
USB_W_VALUE = 0x0203                         # decimal = 515, binary = 0000001000000011

USB_INTERFACE_INDEX = 2      # The USB has an array of interfaces - set the interface to the correct interface endpoint

USB_XINPUT_INTERFACE_INDEX = 1      # The USB has an array of interfaces - set the interface to the correct interface endpoint

LAST_MESSAGE_TIME_TO_BOARD = None



def SetLEDsToIndividualBrightness(DeviceUUID=None, UseFadeValues = False):
# Use the LED States that are stored in a list and set the intensity level based on the
# list data
# the list holds 3 values for each LED
# State - if State is Off - then the Led will be set with intensity of 0
# Intesnity level - values will be used to set intensity unless calling program asks
#                  for fade values to be used instaed
# Fade Intensity Level - and alternate intesnity level which is used when the upstream command
# wishes to mimic a fade pattern

    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    try:
#        if IsDebugOn(): print("retriving Device IDs with id of ")
#        if IsDebugOn(): print(DeviceUUID)
#        if IsDebugOn(): print("End of DeviceUUID")
        DeviceIDList = GetDeviceList(DeviceUUID)
#        if IsDebugOn(): print("retrived Device IDs")
        for myDevice in DeviceIDList:
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                msg = [4]
#                if IsDebugOn(): print("myDevice")
#                if IsDebugOn(): print(myDevice)
#                if IsDebugOn(): print("EndmyDevice")
#                if IsDebugOn(): print("{0}{1}".format(FUNC_NAME, GetDeviceLEDCurrentStates(myDevice["DeviceUUID"])))
                for LEDCurrent in GetDeviceLEDCurrentStates(myDevice["DeviceUUID"]):
#                    if IsDebugOn(): print(LEDCurrent)
                    if LEDCurrent['State']:
                        if UseFadeValues:
                            Intensity = LEDCurrent['LedFadeIntensity']
                        else:
                            Intensity = LEDCurrent['LedIntensity']
                        msg.append(Intensity)
                    else:
                        msg.append(0)    
                _sendMessageToBoard(myDevice["DeviceID"], msg)
    
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))

def SetRampSpeed(DeviceUUID=None, Speed=0):
# Use the LED States that are stored in a list and set the intensity level based on the
# list data
# the list holds 3 values for each LED
# State - if State is Off - then the Led will be set with intensity of 0
# Intesnity level - values will be used to set intensity unless calling program asks
#                  for fade values to be used instaed
# Fade Intensity Level - and alternate intesnity level which is used when the upstream command
# wishes to mimic a fade pattern

    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    try:
#        if IsDebugOn(): print("retriving Device IDs with id of ")
#        if IsDebugOn(): print(DeviceUUID)
#        if IsDebugOn(): print("End of DeviceUUID")
        DeviceIDList = GetDeviceList(DeviceUUID)
#        if IsDebugOn(): print("retrived Device IDs")
        for myDevice in DeviceIDList:
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                msg = [3,192,Speed]
#                if IsDebugOn(): print("myDevice")
#                if IsDebugOn(): print(myDevice)
#                if IsDebugOn(): print("EndmyDevice")
#                if IsDebugOn(): print("{0}{1}".format(FUNC_NAME, GetDeviceLEDCurrentStates(myDevice["DeviceUUID"])))
                _sendMessageToBoard(myDevice["DeviceID"], msg)
    
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))


def SetDelayBetweenScriptCommands(DeviceUUID=None, Delay=0):
# Set the delay between the script commands 


    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)


    try:
#        if IsDebugOn(): print("retriving Device IDs with id of ")
#        if IsDebugOn(): print(DeviceUUID)
#        if IsDebugOn(): print("End of DeviceUUID")
        DeviceIDList = GetDeviceList(DeviceUUID)
#        if IsDebugOn(): print("retrived Device IDs")
        for myDevice in DeviceIDList:
            if (DeviceUUID == None) or (DeviceUUID == myDevice["DeviceUUID"]): 
                msg = [3,193,Delay]
#                if IsDebugOn(): print("myDevice")
#                if IsDebugOn(): print(myDevice)
#                if IsDebugOn(): print("EndmyDevice")
#                if IsDebugOn(): print("{0}{1}".format(FUNC_NAME, GetDeviceLEDCurrentStates(myDevice["DeviceUUID"])))
                _sendMessageToBoard(myDevice["DeviceID"], msg)
    
    except Exception as err:
        raise Exception("{0}{1}".format(FUNC_NAME,err))





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




def _sendMessageToBoard(DeviceID, payload):
    FUNC_NAME=GetMyFuncName()
#    if IsDebugOn(): print(FUNC_NAME)

#    send a message to usb board - it is up to the upstream function to ensure
#    message is in the correct format for the board to action it correctly
    try:
        global LAST_MESSAGE_TIME_TO_BOARD
        
        if LAST_MESSAGE_TIME_TO_BOARD == None:
            LAST_MESSAGE_TIME_TO_BOARD = time.perf_counter_ns()
        THIS_MESSAGE_TIME_TO_BOARD = time.perf_counter_ns()
        timeBetweenUSBMessage = (THIS_MESSAGE_TIME_TO_BOARD-LAST_MESSAGE_TIME_TO_BOARD)/ 1000000000
        LAST_MESSAGE_TIME_TO_BOARD = THIS_MESSAGE_TIME_TO_BOARD
        if IsValidIpacUltimateDevice(DeviceID):
#            if IsDebugOn(): print(FUNC_NAME+"USB interface Nr:- " + str(GetUSBInterfaceNumber(DeviceID)))
#            if IsDebugOn(): print("{0}Payload is :- {1}".format(FUNC_NAME,payload))
            DeviceID.ctrl_transfer(USB_BM_REQUESTTYPE_SET_CONFIGURATION, USB_B_REQUEST_SET_CONFIGURATION, USB_W_VALUE,
                                GetUSBInterfaceNumber(DeviceID), payload)
        else:
            raise Exception("DeviceID not valid")

    except Exception as err:
        if IsDebugOn(): print(str("{0}Number of seconds between last call to board is :- {1:.10f}".format(FUNC_NAME,timeBetweenUSBMessage)))
        if IsDebugOn(): print(str(err)[0:11])
        if (str(err)[0:10] == "[Errno 19]" or 
            str(err)[0:11] == "[Errno 110]" or
            str(err)[0:10] == "[Errno 32]" 
            ):
            if IsDebugOn(): print("{0} Payload is:{1}".format(FUNC_NAME,payload))
 
            raise Exception("{0}{1}".format(FUNC_NAME,err))
        else:
            print("{0} : Exception IGNORED : {1}".format(FUNC_NAME,err))
            print("{0} : DeviceID : {1}:{2}:{3}:{4}".format(FUNC_NAME,DeviceID.idVendor, DeviceID.idProduct, DeviceID.bus, DeviceID.address))



def GetUSBInterfaceNumber(DeviceID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
# return the interface index depening if it is the io board in default mode
# or retrun a different value 
    if IsValidIpacUltimateDevice(DeviceID):
#        if IsDebugOn(): print(FUNC_NAME+"Index=" + str(USB_INTERFACE_INDEX))
        return(USB_INTERFACE_INDEX)
    else:
#        if IsDebugOn(): print(FUNC_NAME+"Exception")
        raise Exception("{0}DeviceID not valid".format(FUNC_NAME))





def IsKernalDriverActive(DeviceID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)

    result=False
    try:

        result= DeviceID.is_kernel_driver_active(GetUSBInterfaceNumber(DeviceID))
        #if IsDebugOn(): print(FUNC_NAME+"Driver Active is :-" + str(result))
    except usb.core.USBError as e:
        raise Exception("{0}Could not check active kernel driver from interface({1}): {2}".format(FUNC_NAME,GetUSBInterfaceNumber(myDevice["DeviceID"]), str(e)))

    return(result)


def DetatchKernalDriver(DeviceID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    result=False
    try:
        result = DeviceID.detach_kernel_driver(GetUSBInterfaceNumber(DeviceID)) 
        #if IsDebugOn(): print(FUNC_NAME+"detached driver is :-" + str(result))
    except usb.core.USBError as e:
        raise Exception("{0}Could not detatch kernel driver from interface({1}): {2}".format(FUNC_NAME,GetUSBInterfaceNumber(myDevice["DeviceID"]), str(e)))


    return(result)



def ResetIODevice(DeviceID):
    FUNC_NAME=GetMyFuncName()
    if IsDebugOn(): print(FUNC_NAME)
    # 
# Commented out as this command is not working on the board.    
#            msg=[0x03,255,0,0,0]
#            _sendMessageToBoard(myDevice["DeviceID"], msg)   pass
    pass


if __name__ == '__main__':
    pass