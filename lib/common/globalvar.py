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

# Holds all the global constants used across the modules


UM_VENDOR_ID_LIST = [ 0xD209 ] # There should only be one Vendor - but there may be an issue when setup as XInput
UM_PRODUCT_ID_LIST = [ 0x0410, 0x0411, 0x0412, 0x0413 ]

UM_XINPUT_VENDOR_ID_LIST = [ 0X045e ]
UM_XINPUT_PRODUCT_ID_LIST =[ 0X028e ]



USB_BM_REQUESTTYPE_SET_CONFIGURATION = 0x21  # decimal = 33,  binary = 00100001
USB_B_REQUEST_SET_CONFIGURATION = 9          # hex = 8,       binary = 00001000
USB_W_VALUE = 0x0203                         # decimal = 515, binary = 0000001000000011
USB_INTERFACE_INDEX = 2      # The USB has an array of interfaces - set the interface to the correct interface endpoint
USB_XINPUT_INTERFACE_INDEX = 1      # The USB has an array of interfaces - set the interface to the correct interface endpoint

MAX_LEDS = 96

MIN_LED_NR = 1
MAX_LED_NR = 96

MAX_INTENSITY_LEVEL = 255

MIN_WAIT_INTERVAL_TIME = 0
MAX_WAIT_INTERVAL_TIME = 10

# this holds, in seconds the minimum and maximam nr seconds between flashes
MIN_FADE_INTERVAL_TIME = 0.02
MAX_FADE_INTERVAL_TIME = 2

MIN_FADE_INCREMENT = 0
MAX_FADE_INCREMENT = 60


# this holds, in seconds the minimum and maximam nr seconds between teh bottuns being faded down
MIN_FLASH_INTERVAL_TIME = 0.02
MAX_FLASH_INTERVAL_TIME = 2


MIN_FLASH_COUNT = 0
MAX_FLASH_COUNT = 10

MIN_NR_CYCLES = 0
MAX_NR_CYCLES = 1000000

MIN_CYCLE_INTERVAL_TIME = 0.02
MAX_CYCLE_INTERVAL_TIME = 2


if __name__ == '__main__':
    pass
