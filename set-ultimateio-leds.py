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

# THis is the main program - you can call it in various forms

# To run the board with a default script
# python3 set-ultimateio-leds.py



import sys

# Load all the functions as their names - to be used across the utility

from lib.core.ipacultimateiocore import InitDevice
from lib.utils.commandscript import RunCommandsFromFile
#from lib.utils.commandscript import GetLedCommandsFromFile
#from lib.utils.commandfile import RunLedCommands

def main ():
    try: arg1 = sys.argv[1]
    except IndexError:
        arg1 = ""

    if (arg1.upper() == "--HELP" or arg1.upper() == "-h"):
        print("""Usage: {0} FILE
This is for use with the ultimarc I/O Board, The FILE will hold the set of
instructions/commands that need to be sent to the board in json format.
This will be a json list in the format example here

[
{ \"Command\" : { \"comment\": \"Wait for x seconds\",
        \"Function\" : \"Wait\",
        \"WaitIntervalTime\": 1 }},
{ \"Command\" : {  \"comment\": \"Set all LEDs to the same specified brightness level\",
        \"Function\" : \"SetAllLedIntensities\",
        \"IntensityLevel\": 255 }},
{ \"Command\" : {\"comment\": \"Set a specific LED to the specified brightness level\",
        \"Function\" : \"SetLedIntensity\",
        \"LedNr\": 3,
        \"IntensityLevel\": 255 }},
{ \"Command\" : {\"comment\": \"Set a list of LEDs to the same specified brightness level\",
        \"Function\" : \"SetLedListIntensities\",
        \"LedNrList\": [0,10,11,12, 13,14,15, 88,89,90,95],
        \"IntensityLevel\": 255   }},
{ \"Command\" : { \"comment\": \"All LEDs wil be set to a random brightness\",
        \"Function\" : \"SetAllLedRandomStates\" }},
{ \"Command\" : {\"comment\": \"Set a list of LEDs to an LED specific brightness level\",
        \"Function\" : \"SetLedIntensityList\",
        \"LedIntensityList\": [   {\"LedNr\": 0, \"IntensityLevel\": 255}, 
                    {\"LedNr\": 95, \"IntensityLevel\": 255}] }},
{ \"Command\" : {\"comment\": \"Set All LEDs to flash x times at the flash interval specified\",
        \"Function" : \"SetAllLedFlash\",
        \"FlashCount\" : 5,
        \"FlashIntervalTime\" : 0.25 }},
{ \"Command\" : {\"comment\": \"Set All LEDs to randomly flash x times at the flash interval specified\",
        \"Function\" : \"SetAllLedRandomFlash\",
        \"FlashCount\" : 5,
        \"FlashIntervalTime\" : 0.25 }},
{ \"Command\" : {\"comment\": \"Set a list of LEDs to flash x times at the flash interval specified\",
       \"Function\" : \"SetLedListFlash",
       \"FlashCount\" : 5,
       \"LedNrList\": [0,10,11,12, 13,14,15, 88,89,90,95],
       \"FlashIntervalTime\" : 0.25 }},
{ \"Command\" : { \"comment\": \"Turn  All LEDs On or Off - when turning back on, the previous setting will be re-applied\",
        \"Function\" : \"SetAllLedStates\",
        \"State\": true }},
{ \"Command\" : {\"comment\": \"Set a list LEDs On or Off - when turning back on, the previous setting will be re-applied\",
        \"Function\" : \"SetLedStateList\",
        \"LedStateList\": [   {\"LedNr\": 10, \"State\": true}, 
                    {\"LedNr\": 11, \"State\": false} ] }},
{ \"Command\" : { \"comment\": \"Fade down and then back up the list of LEDs \",
        \"Function\" : \"SetLedListFadeReverb\",
        \"LedNrList": [0,10,11,12, 13,14,15, 88,89,90,95],
        \"FadeIncrement\": 10, 
        \"FadeIntervalTime\": 0.2 }},
{ \"Command\" : {\"comment\": \"Fade down and then back up All LEDs \",
        \"Function" : \"SetAllLedFadeReverb\",
        \"FadeIncrement\": 20, 
        \"FadeIntervalTime\": 0.2 }},
{ \"Command\" : {\"comment\": \"Fade down all LEDs \",
        \"Function\" : "SetAllLedFadeToOff\",
        \"FadeIncrement\": 30, 
        \"FadeIntervalTime\": 0.2 }},
{ \"Command\" : {\"comment\": \"Fade up all LEDs \",
        \"Function\" : \"SetAllLedFadeToOn\",
        \"FadeIncrement\": 40, 
        \"FadeIntervalTime\": 0.2 }},
{ \"Command\" : {\"comment\": \"Fade down the list of LEDs \",
        \"Function\" : \"SetLedListFadeToOff\",
        \"LedNrList\": [0,3,4,5,6,7,8,9,95],
        \"FadeIncrement\": 50, 
        \"FadeIntervalTime\": 0.2 }},
{ \"Command\" : {\"comment\": \"Fade up the list of LEDs \",
        \"Function\" : \"SetLedListFadeToOn\",
        \"LedNrList\": [0,10,11,12, 13,14,15, 88,89,90,95],
        \"FadeIncrement\": 60, 
        \"FadeIntervalTime\": 0.2  }},
{ \"Command\" : {\"comment\": \"Reset the board (and restart the firmware script \",
                 \"Function\" : \"ResetBoard\"} }
]

All functions available are documented above
Any additonal name/value pair withint the command will be ignored.
This is helpful if you wish to provide comments on particlaur commands
e.g.
...
{ \"Command\" : {\"comment\" : \"ask the script to wait this number of seconds between commands to the board\",
               \"Function\" : \"Wait\",
               \"WaitIntervalTime\": 1 }},
...

""")
    

    try:
        DeviceID = InitDevice()
        RunCommandsFromFile(DeviceID, arg1)
    except Exception as err:
        print(err)






# If we're running in stand alone mode, run the application
if __name__ == '__main__':
# main()
    main()