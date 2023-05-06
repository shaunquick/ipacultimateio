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


# This module keeps a track of the Leds intensity level and state -
# This is used by many of the higher level functions where the current
# state of the LEDs need to be shared across modules
# The data held in this list is used to set the leds intensity on
# the ultimarc baod

import random

from ..common.globalvar import MAX_LEDS

from ..common.validations import _IsValidIntensityLevel
from ..common.validations import _IsValidState

from ..common.validations import _IsValidLedNr



# LED_CURRENT_STATES holds, for each device, the current led number (index valiue), setintensitylevel, fadeintensitylevel and State (On or Off or (setBy)Script) 

LED_CURRENT_STATES = {}

def Initialise_DeviceListLEDCurrentStates(DeviceIDList=[], debug=False):
# Create the list of LedNr's staring from 1 to 96
    global LED_CURRENT_STATES

    if debug: print("InitLedStatus(): ")

    LED_CURRENT_STATES={}

    for aDevice in DeviceIDList:
        LED_CURRENT_STATES[aDevice["DeviceUUID"]] = []
        
        LedNr = 1
        while LedNr <= MAX_LEDS:
            LED_CURRENT_STATES[aDevice["DeviceUUID"]].append( {'LedIntensity': 0, 'LedFadeIntensity': 0, 'State' : True } )
            LedNr += 1


def Set_DeviceLEDCurrentStates_LedIntensity(DeviceUUID,LedNr,IntensityLevel):
# Set the intensity level in the list to the value passed in
    global LED_CURRENT_STATES

    if _IsValidIntensityLevel(IntensityLevel):
        if _IsValidLedNr(LedNr):
            LED_CURRENT_STATES[DeviceUUID][LedNr-1]['LedIntensity'] = IntensityLevel
        else:
            raise Exception("Set_DeviceLEDCurrentStates_LedIntensity(): LedNr valid")
    else:
        raise Exception("Set_DeviceLEDCurrentStates_LedIntensity(): State not valid")

def Set_DeviceLEDCurrentStates_LedFadeIntensity(DeviceUUID,LedNr,IntensityLevel):
    global LED_CURRENT_STATES

    # Set the fade intensity level in the list to the value passed in
    if _IsValidIntensityLevel(IntensityLevel):
        if _IsValidLedNr(LedNr):
            LED_CURRENT_STATES[DeviceUUID][LedNr-1]['LedFadeIntensity'] = IntensityLevel
        else:
            raise Exception("Set_DeviceLEDCurrentStates_LedFadeIntensity(): LedNr valid")
    else:
        raise Exception("Set_DeviceLEDCurrentStates_LedFadeIntensity(): State not valid")

def Set_DeviceLEDCurrentStates_LedState(DeviceUUID,LedNr,State):
    global LED_CURRENT_STATES
    
    # Set the state in the list to the value passed in
    if _IsValidState(State):
        if _IsValidLedNr(LedNr):
            LED_CURRENT_STATES[DeviceUUID][LedNr-1]['State'] = State
        else:
            raise Exception("Set_DeviceLEDCurrentStates_LedState(): LedNr valid")
    else:
        raise Exception("Set_DeviceLEDCurrentStates_LedState(): State not valid")

def Set_All_DeviceLEDCurrentStates_LedState(DeviceUUID,State):
    global LED_CURRENT_STATES
    # Set all the LED's in the list to be True(On) or False(Off)
    if  _IsValidState(State):
        for Led in LED_CURRENT_STATES[DeviceUUID]:
            if State  : Led['State'] = True
            else:  Led['State'] = False
    else:
        raise Exception("Set_All_DeviceLEDCurrentStates_LedState(): State not valid")


def Set_All_DeviceLEDCurrentStates(DeviceUUID,IntensityLevel,FadeIntensityLevel,State):
    global LED_CURRENT_STATES
    
    # Set all the LED's in the list with the same intesnity level, fade itensity level and state
    if  _IsValidState(State):
        for Led in LED_CURRENT_STATES[DeviceUUID]:
            Led['LedIntensity'] = IntensityLevel
            Led['LedFadeIntensity'] = FadeIntensityLevel
            Led['State'] = State
    else:
        raise Exception("Set_All_DeviceLEDCurrentStates(): State not valid")

def Set_Random_DeviceLEDCurrentStates(DeviceUUID):
    global LED_CURRENT_STATES
    
    # Set the led states to be random - this is used when
    for Led in LED_CURRENT_STATES[DeviceUUID]:
        if random.randint(0,1) == 0: 
            Led['LedIntensity'] = 0
            Led['LedFadeIntensity'] = 0
            Led['State'] = False
        else:
            Led['LedIntensity'] = random.randint(0,255)
            Led['LedFadeIntensity'] = Led['LedIntensity']
            Led['State'] = True


def Get_DeviceLEDCurrentStates_LedIntensity(DeviceUUID,LedNr):
# return the current value of the led nr intensity 
    if _IsValidLedNr(LedNr):
        return(LED_CURRENT_STATES[DeviceUUID][LedNr-1]['LedIntensity'])
    else:
        raise Exception("Get_DeviceLEDCurrentStates_LedIntensity(): LedNr valid")

def Get_DeviceLEDCurrentStates_LedFadeIntensity(DeviceUUID,LedNr):
# return the current value of the led nr fade intensity 
    if _IsValidLedNr(LedNr):
        return(LED_CURRENT_STATES[DeviceUUID][LedNr-1]['LedFadeIntensity'])
    else:
        raise Exception("Get_DeviceLEDCurrentStates_LedFadeIntensity(): LedNr valid")

def Get_DeviceLEDCurrentStates_LedState(DeviceUUID,LedNr):
# return the current value of the led nr state 
    if _IsValidLedNr(LedNr):
        return(LED_CURRENT_STATES[DeviceUUID][LedNr-1]['State'])
    else:
        raise Exception("Get_DeviceLEDCurrentStates_LedState(): LedNr valid")

def Get_DeviceLEDCurrentStates(DeviceUUID):
# retrn the full list of leds and their current seetings
    return(LED_CURRENT_STATES[DeviceUUID])

if __name__ == '__main__':
    pass