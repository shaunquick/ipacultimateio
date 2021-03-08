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

# LED_CURRENT_STATES holds the current led number (index valiue), setintensitylevel, fadeintensitylevel and State (On or Off or (setBy)Script) 

LED_CURRENT_STATES = []

def InitLedStatus():
    global LED_CURRENT_STATES

# CReate the list of LedNr's staring from 1 to 96
    LedNr = 1
    while LedNr <= MAX_LEDS:
        LED_CURRENT_STATES.append( {'LedIntensity': 0, 'LedFadeIntensity': 0, 'State' : "On" } )
        LedNr += 1


def Set_LED_CURRENT_STATES_LedIntensity(LedNr,IntensityLevel):

    LED_CURRENT_STATES[LedNr-1]['LedIntensity'] = IntensityLevel

def Set_LED_CURRENT_STATES_LedFadeIntensity(LedNr,IntensityLevel):
    LED_CURRENT_STATES[LedNr-1]['LedFadeIntensity'] = IntensityLevel

def Set_LED_CURRENT_STATES_LedState(LedNr,State):
    LED_CURRENT_STATES[LedNr-1]['State'] = State



def Get_LED_CURRENT_STATES_LedIntensity(LedNr):
    return(LED_CURRENT_STATES[LedNr-1]['LedIntensity'])

def Get_LED_CURRENT_STATES_LedFadeIntensity(LedNr):
    return(LED_CURRENT_STATES[LedNr-1]['LedFadeIntensity'])

def Get_LED_CURRENT_STATES_LedState(LedNr):
    return(LED_CURRENT_STATES[LedNr-1]['State'])


def Get_LED_CURRENT_STATES():
    return(LED_CURRENT_STATES)

def Set_All_LED_CURRENT_STATES_LedState(State):
    for Led in LED_CURRENT_STATES:
        if State: Led['State'] = "On"
        else:  Led['State'] = "Off"


def Set_All_LED_CURRENT_STATES(IntensityLevel,FadeIntensityLevel,State):
    for Led in LED_CURRENT_STATES:
        Led['LedIntensity'] = IntensityLevel
        Led['LedFadeIntensity'] = FadeIntensityLevel
        Led['State'] = State

def Set_Random_LED_CURRENT_STATES():
    for Led in LED_CURRENT_STATES:
        if random.randint(0,1) == 0: 
            Led['LedIntensity'] = 0
            Led['LedFadeIntensity'] = 0
            Led['State'] = "Off"
        else:
            Led['LedIntensity'] = random.randint(0,255)
            Led['LedFadeIntensity'] = Led['LedIntensity']
            Led['State'] = "On"


if __name__ == '__main__':
    pass