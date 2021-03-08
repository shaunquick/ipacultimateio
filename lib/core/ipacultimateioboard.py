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



# THis module holds the functions that communicate directly with the
# ultimarc-io LED Board
# 

from ..utils.ledcurrentstateslist import Get_LED_CURRENT_STATES 

USB_BM_REQUESTTYPE_SET_CONFIGURATION = 0x21  # decimal = 33,  binary = 00100001
USB_B_REQUEST_SET_CONFIGURATION = 9          # hex = 8,       binary = 00001000
USB_W_VALUE = 0x0203                         # decimal = 515, binary = 0000001000000011
USB_INTERFACE_INDEX = 2      # The USB has an array of interfaces - set the interface to the correct interface endpoint


def _setLedsToIndividualBrightness(DeviceID, UseFadeValues = False):
# Use the LED States that are stored in a list and set the intensity level based on the
# list data
# the list holds 3 values for each LED
# State - if State is Off - then the Led will be set with intensity of 0
# Intesnity level - values will be used to set intensity unless calling program asks
#                  for fade values to be used instaed
# Fade Intensity Level - and alternate intesnity level which is used when the upstream command
# wishes to mimic a fade pattern
    msg = [4]
    for LedCurrent in Get_LED_CURRENT_STATES():
        if LedCurrent['State'] == "On":
            if UseFadeValues:
                Intensity = LedCurrent['LedFadeIntensity']
            else:
                Intensity = LedCurrent['LedIntensity']
            msg.append(Intensity)
        else:
            msg.append(0)    
    _sendMessageToBoard(DeviceID, msg)
    
def _sendMessageToBoard(DeviceID, payload):
# send a message to usb board - it is up to the upstream function to ensure
#message is in the correct format for the board to action it correctly
    DeviceID.ctrl_transfer(USB_BM_REQUESTTYPE_SET_CONFIGURATION, USB_B_REQUEST_SET_CONFIGURATION, USB_W_VALUE, USB_INTERFACE_INDEX, payload)


if __name__ == '__main__':
    pass