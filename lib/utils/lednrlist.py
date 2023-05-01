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


# This module creates a list with all the led numers - this can then be used for when actions need to be taken against all Leds
# Get_LED_LIST_ALL returns a list of LedNrs from 1 to 96

from ..common.globalvar import MAX_LEDS

# LED_CURRENT_STATES holds the current led number (index valiue), setintensitylevel, fadeintensitylevel and State (On or Off or (setBy)Script) 
LED_LIST_ALL = {}

def InitLedNrList(DeviceIDList=[], debug=False):
    global LED_LIST_ALL

    if debug: 
        print("InitLedNrList(): ")
# CReate the list of LedNr's staring from 1 to 96
    for myDevice in DeviceIDList:
        LED_LIST_ALL[myDevice["DeviceUUID"]] = []

        LedNr = 1
        while LedNr <= MAX_LEDS:
            LED_LIST_ALL[myDevice["DeviceUUID"]].append(LedNr)
            LedNr += 1


def Get_DEVICE_LED_LIST_ALL(DeviceUUID):
    return(LED_LIST_ALL[DeviceUUID])


if __name__ == '__main__':
    pass