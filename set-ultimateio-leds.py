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


from lib.core.ipacultimateiocore import InitDeviceList
from lib.utils.commandscript import RunCommandsFromFile
from lib.utils.help import help
from lib.utils.help import listOfDevicesExample




def main ():
    FUNC_NAME="main(): "
    try:
        arg_names = ["help", "debug", "iodev_uuid=", "xinput_flag", "list_devices"]
        opts, args = getopt.getopt(sys.argv[1:], "hdxli:", arg_names)
    except getopt.GetoptError:
        print("Opt error - this should not have happened")
        print(help())
        sys.exit(0)

    DeviceUUID = None
    debug = False
    outputfile=""
    xinput_flag=False
    list_devices=False
    for option, arg in opts:
        if option in ("-h", "--help"):
            print(help())
            sys.exit(0)

        if option in ("-d", "--debug"):
            debug = True
            if debug: print(FUNC_NAME+"Debug Turned On!!")

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
        DeviceIDList = InitDeviceList(DeviceUUID=DeviceUUID, debug=debug, xinput_flag=xinput_flag)
        if len(DeviceIDList) == 0:
            raise Exception("Error: Could not find Ultimarc I/O Board")
        elif list_devices:
            print(listOfDevicesExample(DeviceIDList))
        else:
            RunCommandsFromFile(DeviceIDList, myScript, debug=debug, xinput_flag=xinput_flag)
    except Exception as err:
        print("we got exception")
        print(err)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
# main()
    main()