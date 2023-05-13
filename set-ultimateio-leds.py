#!/usr/bin/env python3
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

# This is the main program - you can call it in various forms

# To set the led board with a default script
# python3 set-ultimateio-leds.py
# To set the led board with a script in the script sub-folder
# python3 set-ultimateio-leds.py myscript.json
# To set the led board with a script in the folder of your choice
# python3 set-ultimateio-leds.py ~/myfolder/myscript.json
#
#
# THis has been tested with the 2020 ultimarc io boards - although this
# should work for all ulimateio boards this cannot be gauranteed.


import sys
import getopt

from lib.common.common_lib import SetDebugOn
from lib.common.common_lib import IsDebugOn


from lib.core.ipacultimateiocore import InitialiseDeviceLists
from lib.utils.commandscript import RunCommandsFromFile
from lib.utils.help import GetHelpTextMain
from lib.utils.help import GetHelpTextListOfDevicesExample



def main ():

# there are a number of Options that can be passed in
# With the Exception of the debug the follwoing flags are checked
# iodev_UUID = you can pass in one device UUID and this program will only ever execute commands against it, no matter
# how many devices are attached to the computer and will disregard other data in the config files.
# xinput_dev - if you have configured the the ultimarc io noards from Keyboard mode to XInput mode, you
# have to apss in this flag so that the program will recognise them
# list_devices - where you do have multiple boards - and you want to control them individually
# you will need to obtain the uniwue ideneitfier tha the program recognises the devie as.
# you can then use this value in the configuration files to control that device Led's.
    FUNC_NAME="main(): "

    try:
        arg_names = ["help", "debug", "iodev_uuid=", "xinput_flag", "list_devices"]
        opts, args = getopt.getopt(sys.argv[1:], "hdxli:", arg_names)
    except getopt.GetoptError:
        print("Opt error - this should not have happened")
        print(GetHelpTextMain())
        sys.exit(0)

    DeviceUUID = None

    outputfile=""
    xinput_flag=False
    list_devices=False
    for option, arg in opts:
        if option in ("-h", "--help"):
            print(GetHelpTextMain())
            sys.exit(0)

        if option in ("-d", "--debug"):
            SetDebugOn()
            if IsDebugOn(): print(FUNC_NAME+"Debug Turned On!!")
        if option in ("-i", "--iodev_uuid"):
            DeviceUUID = arg[1:]
 
        if option in ("-x", "--xinput_flag"):
            xinput_flag=True

        if option in ("-l", "--list_devices"):
            list_devices=True



    if not args:
        myScript = "default_script.json"
    else:
        myScript = args[0]


    try:
# Initialise the board and run the script privided or run the default script
        DeviceIDList = InitialiseDeviceLists(DeviceUUID=DeviceUUID, xinput_flag=xinput_flag)
        if len(DeviceIDList) == 0:
            raise Exception("Error: Could not find Ultimarc I/O Board")
        elif list_devices:
            print(GetHelpTextListOfDevicesExample(DeviceIDList))
            if IsDebugOn():
                print(FUNC_NAME+"Device List is :-")
                for DeviceID in DeviceIDList:
                   print(DeviceID["DeviceID"])
        else:
            RunCommandsFromFile(myScript)
    except Exception as err:
        print("Exception found:  {0}".format(err))
        sys.exit(2)
    else:
        if IsDebugOn(): print(FUNC_NAME+ "Finished Successfully")


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
# main()
    main()