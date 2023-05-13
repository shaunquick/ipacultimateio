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


from ..common.common_lib import IsDebugOn



def GetHelpTextListOfDevicesExample(DeviceIDList):
    help_text = "Devices found are :- \n"
    for myDevice in DeviceIDList:
        help_text += "DeviceUUID = " + myDevice["DeviceUUID"] +"\n"
        help_text += "Device Manufacturer = " + myDevice["DeviceID"].manufacturer +"\n"
        help_text += "Device Product = " + myDevice["DeviceID"].product +"\n\n"
    help_text += "Use these values in the command files to execute a command against a specific device \n\n"
    help_text += """{ \"Command\" : {  \"comment\": \"Set all LEDs to the same specified brightness level\",
        \"Function\" : \"SetAllLedIntensities\",
        \"DeviceUUID\" : \"""" + myDevice["DeviceUUID"] + """\",
        \"IntensityLevel\": 255 }},
        
 Please Note:  If you have only one device you can ignore the DeviceUUID and the attibute is optional
               If you have multiple devices, all devices will be set based on the commmand unless you specifc the DeviceUUID
        """
    return (help_text)


def GetHelpTextMain():
     
    helptext= """Usage: set-ultimateio-leds.py [OPTION] FILE
This is for use with the ultimarc I/O Board, The FILE will hold the set of
instructions/commands that need to be sent to the board in json format.
This utility supports 
1. Easy use of the capability with a single board
2. controlling two (or more) boards identically (using LedNr or LedGroupName)
3. being able to send commands to one board at a time using LedNr or LedGroupName (you can either re-use the Ledgroup Name or create one per board)
4. Multiple boards performing a rainbow effect across all of the boards (one or many)

This will be a json list in the format example here
please note that the DeviceUUID is only required if you have a multiboard configuration
and you want to control which board the command executes against

There are also examples of a multiboard script in the \scripts folder

There is also an example of a multiboard LedGroupNameDefinitions setup, in the data folder, which you can use to control a set of Led's on a device

[
{ \"Command\" : {   \"comment\": \"Wait for x seconds\",
                    \"Function\" : \"Wait\",
                    \"WaitIntervalTime\": 1 }},
{ \"Command\" : {   \"comment\": \"Set all LEDs to the same specified brightness level\",
                    \"Function\" : \"SetAllLedIntensities\",
                    \"IntensityLevel\": 255,
                    \"DeviceUUID\" : \"53769:1040:1:3\"}},
{ \"Command\" : {   \"comment\": \"Set a specific LED to the specified brightness level\",
                    \"Function\" : \"SetLedNrToIntensityLevel\",
                    \"LedNr\": 3,
                    \"IntensityLevel\": 255,
                    \"DeviceUUID\" : \"53769:1040:1:3\"}},
{ \"Command\" : {   \"comment\": \"Set a list of LEDs to the same specified brightness level\",
                    \"Function\"     : \"SetLedNrListToSameIntensityLevel\",
                    \"LedNrList\": [1,10,11,12, 13,14,15, 88,89,90,96],
                    \"IntensityLevel\": 255,
                    \"DeviceUUID\" : \"53769:1040:1:3\"   }},
{ \"Command\" : {   \"comment\": \"All LEDs wil be set to a random brightness\",
                    \"Function\" : \"SetAllLedRandomStates\",
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Set a list of LEDs to an LED specific brightness level\",
                    \"Function\" : \"SetLedNrAndIntensityLevelList\",
                    \"LedNrIntensityList\": [   {\"LedNr\": 1, \"IntensityLevel\": 255}, 
                    {\"LedNr\": 95, \"IntensityLevel\": 255}],
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Set All LEDs to flash x times at the flash interval specified\",
                    \"Function\" : \"SetAllLedFlash\",
                    \"FlashCount\" : 5,
                    \"FlashIntervalTime\" : 0.25,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Set All LEDs to randomly flash x times at the flash interval specified\",
                    \"Function\" : \"SetAllLedRandomFlash\",
                    \"FlashCount\" : 5,
                    \"FlashIntervalTime\" : 0.25 }},
{ \"Command\" : {   \"comment\": \"Set a list of LEDs to flash x times at the flash interval specified\",
                    \"Function\" : \"SetLedNrListFlash",
                    \"FlashCount\" : 5,
                    \"LedNrList\": [1,10,11,12, 13,14,15, 88,89,90,96],
                    \"FlashIntervalTime\" : 0.25,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Turn  All LEDs On or Off - when turning back on, the previous setting will be re-applied\",
                    \"Function\" : \"SetAllLedStates\",
                    \"State\": true,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Set a list LEDs On or Off - when turning back on, the previous setting will be re-applied\",
                    \"Function\" : \"SetLedNrAndStateList\",
                    \"LedNrStateList\": [   {\"LedNr\": 10, \"State\": true}, 
                    {\"LedNr\": 11, \"State\": false} ],
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Fade down and then back up the list of LEDs \",
                    \"Function\" : \"SetLedNrListFadeReverb\",
                    \"LedNrList": [1,10,11,12, 13,14,15, 88,89,90,96],
                    \"FadeIncrement\": 10, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Fade down and then back up All LEDs \",
                    \"Function\" : \"SetAllLedFadeReverb\",
                    \"FadeIncrement\": 20, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Fade down all LEDs \",
                    \"Function\" : "SetAllLedFadeToOff\",
                    \"FadeIncrement\": 30, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Fade up all LEDs \",
                    \"Function\" : \"SetAllLedFadeToOn\",
                    \"FadeIncrement\": 40, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Fade down the list of LEDs \",
                    \"Function\" : \"SetLedNrListFadeToOff\",
                    \"LedNrList\": [1,3,4,5,6,7,8,9,96],
                    \"FadeIncrement\": 50, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"comment\": \"Fade up the list of LEDs \",
                    \"Function\" : \"SetLedNrListFadeToOn\",
                    \"LedNrList\": [1,10,11,12, 13,14,15, 88,89,90,96],
                    \"FadeIncrement\": 60, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\"  }},



{ \"Command\" : {   \"Function\" : \"SetLedGroupNameIntensity", 
                    \"LedGroupName\" : \"p2b6\", 
                    \"RGBIntensity\" : [100,100,100],
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"Function\" : \"SetLedGroupNameListIntensities", 
                    \"LedGroupNameList\": [ \"p1b1\", \"p1b2\", \"p1b3\", \"p1b4\" ],
                    \"IntensityLevel\": 255,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"Function\" : \"SetLedGroupNameIntensity", 
                    \"LedGroupName\" : \"p1b1\", 
                    \"RGBIntensity\" : [255,11,22],
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},

{ \"Command\" : {   \"Function\" : \"SetLedGroupNameIntensityList\",
                    "LedGroupNameIntensityList": [ {\"LedGroupName\" : \"p1b1\", 
                    \"RGBIntensity\" : [255,11,22] }, 
                    {\"LedGroupName\" : \"p1b2\", \"RGBIntensity\" : [255,11,22] }],
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},

{ \"Command\" : {   \"Function\" : \"SetLedGroupNameListFlash\", 
                    \"FlashCount\" : 5, 
                    \"LedGroupNameList\": [\"p1b1\", \"p1b2\", \"p2b1\", \"p2b2\", \"p2b5\", \"p1b6\" ], 
                    \"FlashIntervalTime\" : 0.25,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},

{ \"Command\" : {   \"Function\" : \"SetLedGroupNameStateList\",
                    \"LedGroupNameStateList\": [ {\"LedGroupName\" : \"p1b1\", \"State\": true }, 
                    {\"LedGroupName\" : \"p1b2\", \"State\": false } ],
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},

{ \"Command\" : {   \"Function\" : \"SetLedGroupNameListFadeReverb",
                    \"LedGroupNameList\": [\"p1b1\", \"p1b2\", \"p2b1\", \"p2b2\", \"p2b5\", \"p1b6\" ],
                    \"FadeIncrement\": 10, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"Function\" : \"SetLedGroupNameListFadeToOff", 
                    \"LedGroupNameList\": [\"p1b1\", \"p1b2\", \"p2b1\", \"p2b2\", \"p2b5\", \"p1b6\" ],
                    \"FadeIncrement\": 50, 
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\" }},
{ \"Command\" : {   \"Function\" : \"SetLedGroupNameListFadeToOn", 
                    \"LedGroupNameList\": [\"p1b1\", \"p1b2\", \"p2b1\", \"p2b2\", \"p2b5\", \"p1b6\" ], 
                    \"FadeIncrement\": 60,  
                    \"FadeIntervalTime\": 0.2,
                    \"DeviceUUID\" : \"53769:1040:1:3\"  }},


{ \"Command\" : {   \"Function\" : \"RepeatLastCommands\", 
                    \"NrPreviousCommandsToRepeat\" : 14, 
                    \"NrOfRepetitions\" :3 }},

{ \"Command\" : {   \"comment\": \"Reset the board (and restart the firmware script \",
                    \"Function\" : \"ResetBoard\",
                    \"DeviceUUID\" : \"53769:1040:1:3\"} }

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




Mandatory arguments to long options are mandatory for short options too.
      -h --help             display this help and exit
      -d --debug            allows debug messages to be shown on stdoutput
      -i --iodev_uuid={ID}  the device ID input will be the only device that will be 
                            have their LED's set
      -x --xinput_flag      will treat Xinput devices as a ipacultimate LED device
      -l --list_devices     will list all identfied devices - please use to identify your DeviceUUIDs - they will be unique to your setup


"""
    return (helptext)



def GetHelpTextRomLeds():

    helptext= """Usage: set-ultimateio-rom-leds.py [OPTION] romname
This is for use with the ultimarc I/O Board. This command will allow
a bespoke Led Script to be executed based on the rom name. The 1st
parameter will be the RomName. This will be used to identify the Led
script that should be executed
The "data" folder holds a json file named RomScriptDefinitions.json.
It is expected that this data file is updated to add the romname
and the script name that will be executed for that romname. The script
name can either be a full filename or a script that can be loaded into
the scripts folder.

Mandatory arguments to long options are mandatory for short options too.
      -h --help     display this help and exit
      -d --debug    allows debug messages to be shown on stdoutput
      -l --list_devices     will list all identfied devices - please use to identify your DeviceUUIDs - they will be unique to your setup

"""
    return (helptext)


