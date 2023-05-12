Ultimarc-Ultimate I/O 
======================

Library and command script utility to configure the LEDs on the Ultimarc Ultimate IO Board or multiple Ultimarc Ultimate IO Boards

Introduction
=============
This utility will configure the LEDs on the following Ultimarc boards; IPAC Ultimate. It uses json files to send one or many commands to the board.

This library and command line utility has been tested with only the current IPAC Ultimate board.

This has been written in python.

It has been used successfully with the raspberry pi, with either the Raspberry Pi OS (https://www.raspberrypi.org/software/) or 
Retropie (https://retropie.org.uk/). It may work in other environments but has not been tested.


Multiple Boards have been coded to be supported (but not fully tested) - please refer to the Section Muliboard Setup - any feedback on issues are welcome
It is strongly suggest that you run this utility in single board mode first before looking to configure multiple boards

The library includes all the python source code, but it is intended to be used via the command line as a utility.

Donations 
==========
Donations will be  gratefully received for use of this utility !
Donations are entirely optional 

https://paypal.me/quicksyuk?locale.x=en_GB


Pre-Requisites
===============
Python installed version 3.7.3 (or above)
https://projects.raspberrypi.org/en/projects/generic-python-install-python3

Required Python modules
To use this tool the following python modules need to be installed on your system.
*  pip install pyusb  (https://pyusb.github.io/pyusb/) (https://pypi.org/project/pyusb/)

The following commands may help....
$ sudo apt install python3-pip
$ python3 -m pip install pyusb


Installation
=============

The ultimarc library can be download via git hub with the following command

$ cd ~
$ git clone https://github.com/shaunquick/ipacultimateio.git

-UDEV Rule:
# Once the library has been downloaded the Board needs to allow the python utility to be able to write data out to it. 
An additional permission needs to be granted at root level.
To do this, there is a file called 'ipacultimateio.rules' that can be moved to /etc/udev/rules.d folder

$ sudo mv  ~/ipacultimateio/ipacultimateio.rules /etc/udev/rules.d/

You will need to reboot the raspberry pi for this permission to become active.



Running a Test
===============
Plug in one Ultimarc IO USB board 

Now run a test- 
$ python3 ~/ipacultimateio/set-ultimateio-leds.py

This assumes you installed the libray in the folder ~/ipacultimateio/ - if you installed it elsewhere then change those settings
If there are LED devices connected to your board - some of those will light up. Otherwise you will receive an error message.
If you receive a permission denied, it is likely that the UDEV rule has not been configured (don't forget to re-boot).



How it works
=============
Once you have downloaded the github project, there will be a main python module called

set-ultimateio-leds.py in the main folder

Plug in your Ultimate I/O Board into the Raspberry Pi 4

To see the help page run
$ python3 set-ultimateio-leds.py --help

To run a test script run
$ python3 set-ultimateio-leds.py

To run your own script
$ python3 set-ultimateio-leds.py <scriptname>
where <scriptname> is the name of the json script file that resides in the scripts sub-folder or a fully qualified filename
The script should be placed in the sub-folder scripts (although you can pass in the full path if you do not want to hold your scripts there.


Scripts
========
Scripts are json files that allow you to execute a sequence of different commands to the Board. These will allow you to set the colour of a 
led, flash an led, fade a led etc - each of those commands require a set of paramaters and informaiton to allow them to configure
the Leds.
The normal expectation is that 3 leds (red/green/blue) are attached to a button. The functionality of the commands will assume you have 
configured your Leds in this way, to make understanding how a command will affect your buttons. However you can easily try out the commands 
yourself so you can see how each command will affect how you have configured your buttons to the IO Board.

There are four levels of commands
- All Leds - the command will affect all Leds in the same way
	- All leds can be configured to have the same configuration.
    - the following commands are available
        - SetAllLedIntensities:     Set all LEDs to the specified brightness level;
                                    all buttons will be the same colour
        - SetAllLedRandomStates:    Set all LEDs to be randomly on or off;
                                    all buttons will have a randomised colour
        - SetAllLedFlash:           Set All LEDs to flash x times at the flash interval specified;
                                    all buttons will flash on and off
        - SetAllLedRandomFlash:     Buttons will randomly be turned on and off

        - SetAllLedStates:          Turn All LEDs On or Off - when turning back on, the previous setting will be re-applied;
                                    all buttons will be turned off or on
        - SetAllLedFadeReverb:      Fade down and then back up All LEDs;
                                    all butttons wil fade down to off and then back up to the previously set colour
        - SetAllLedFadeToOff:       Fade down all LEDs;
                                    all buttons will fade down to off
        - SetAllLedFadeToOn:        Fade up all LEDs;
                                    all buttons will fade up to the previously set colour

- A list of Leds
	- you can pass in a list of Led Numbers and configure those together, useful if you don't have many scripts or you know/remember
      which button is configured to which Led Numbers and that you don't change them. Don't forget that the Board Led NR's are in order
	  of RGB for Led numbers up to 48 and then become BGR from 49 onwards - If the colour of a button is red and you expect it to be blue 
      you may have set the wrong Led Number.

    - the following commands are available
        - SetLedNrListToSameIntensityLevel: Set a list of LEDs to the same specified brightness level;
                                            changes the colour of the buttons connected to those Leds
        - SetLedNrListFlash:                Set a list of LEDs to flash x times at the flash interval specified;
                                            changes the colour of the buttons connected to those Leds
        - SetLedNrListFadeReverb:           Fade down and then back up the list of LEDs;
                                            changes the colour of the buttons connected to those Leds
        - SetLedNrListFadeToOff:            Fade down the list of LEDs
                                            changes the colour of the buttons connected to those Leds
        - SetLedNrListFadeToOn:             Fade up the list of LEDs
                                            changes the colour of the buttons connected to those Leds
        - SetLedNrIntensityLevelList:       Set a list of LEDs to an LED specific brightness level
                                            will change the colour of a button
        - SetLedNrStateList:                Set a list specific LEDs On or Off - when turning back on, the previous setting will be re-applied;
                                            will change the colour of a button

- A group of Leds 
	- you can define a GroupName (e.g. "button1") and provide a list of 3 Led Numbers (or in groups of 3) for that (e.g. 16,17,18 for the Red/Green/Blue Led 
          Numbers of that button (or BGR numbers for 49-96 pins)
          A group name would noramlly define a button i.e. the LED Nr's for a particular button, but you can use it to group as many LED's together 
          as you want.
          You can then run a defined set of commands for that groupName (or list of GroupNames) and effectively configure the underlying Led Numbers.
          It provides a layer of encapsulation, meaning that if button1 is not longer configured for led numbers 16,17,19 - you can redefine the Led 
          Numbers you wish to be associated with that name
    - the following commands are available
        - SetLedGroupNameIntensity :        Set all Led's in the group to the same intensity/colour;
                                            changes the colour of a button
        - SetLedGroupNameListIntensities:   Set a list of LedGroupNames to the specific intensity level for that group
        - SetLedGroupNameListFlash:         Set a list of LedGroupNames to flash on and off
        - SetLedGroupNameListFadeReverb:    Set a list of LedGroupNames to fade down and then back up to the previously set colour
        - SetLedGroupNameListFadeToOff:     Set a list of LedGroupNames to fade down to off
        - SetLedGroupNameListFadeToOn:      Set a list of LedGroupNames to fade up to the previously set colour
        - SetLedGroupNameListRainbowCycle:  For the list of LedGroupsNames, produce a rainbow effect in the order
                                            that the LedGroupNames have been entered in the list;
                                            cycles the buttons through colours of the rainbow
        - SetLedGroupNameIntensityList:     Set a list of LED groups to an LED group specific brightness level
                                            will change the colour of a button
        - SetLedGroupNameStateList:         Set a list specific LEDs On or Off - when turning back on, the previous setting will be re-applied;
                                            will turn a list of buttons (LedGroup Names) to either on or off 


- A specific Led
	- you can pass in a specific Led Numbers and configure those together, useful if you don;t have many scripts or you know/remember
      which button is configured to which Led Numbers and that you don't change them. Don't forget that the Board Led NR's are in order
	  of RGB for Led numbers up to 48 and then become BGR from 49 onwards - If the colour of a button is red and you expect it to be blue 
      you may have set the wrong Led Number.

    - the following commands are available
        - SetLedNrToIntensityLevel:        Set a specific LED to the specified brightness level;
                                    This changes the colour of a button



- There are prebuilt scripts that are used for emulation station in retropie - you can of course configure these for your Led setup



Emulationstation
=================
The following resource is useful and will need to be read and understood
https://retropie.org.uk/docs/EmulationStation/#scripting

There will be a folder called ./emulationstation/scripts as part of this utility

The contents of that folder needs to be moved to ~.emulationstation if you wish to configure the Leds when Retropie is installed so that you can have 
different Led settings when you
- Start a Game
- Finish a Game
- Emulationstation goes into screensaver mode
- Emulationstation wakes after screensaver mode

This will create the folder structure expected for some emulation station events to be captured (as above).

Once copied ensure that the script have execute access to ensure emulation station executes them for the events.

You will need to edit the scripts for your chosen configuration


Utility Folder Structure
================
- main folder -
Holds the main python program that you will execute to set the Led colours :- set-ultimateio-leds.py

- scripts folder
An example script (default_script.json) is provided which shows the structure of the file that you will need to adhere to, which includes an example of all 
command that can be used.
You can create your own scripts in this folder, to configure the Board as you want.
It also holds the following scripts 
1buttons.json - to light player1 button 1 only
2buttons.json - to light player1 button 1 only
allbuttons.json - to set all buttons 
attract.json - 
gamesmenu - set Led configuration 

Emulationstation uses the above provided scripts - change the contents to how you want to confgure your Leds. I would strongly recommend to backup  
your scripts (or give them different names) to ensure that if, in the unfortunate event, they are overwritten then you can recover your scripts. 


- data folder -
If you wish to use GroupNames to configure a button, the configuration/definition file is held in this folder and is called 'LedGroupNameDefinitions.json'
the LedNrRGB values will need to be configured for your set-up - additionally the LedGroupName value can also be changed to any name that you want 
to use - remember that in the script you will also need to reference that new name in order to use the configuration in the command.
I would strongly recommend to backup your definitions to ensure that if, in the unfortunate event, they are overwritten then you can recover your 
definitions.
There is a further data file that is used for the emulation station configuration - to set Led's to the prefferred configuration per rom.
this is a list of romnames and the script to execute. Where you want to execute a different script for a particlaur rom, just add the rom in the format
of the examples.

- libs folder -
A set of underlyig python modules - the core subfolder holder all the functions that cab be externally called within other programs (not tested!). 
The sub folders hold additional modules that are needed for this utility.

- docs folder -
The full readme file is here ! Additonal documentation may be provided at a later date.



Multi-Board Setup
=====================

There are many ways in which to control multiple boards. 
If you use the LedGroupName 



In the command script - you can either add the DeviceUUID so that a commend will execute on a specific board or
do not provide the DeviceUUID and it will execute the command on all identified devices.
to obtain a list of devices either run
$ python3 ~/ipacultimateio/set-ultimateio-leds.py -l
or
$ python3 ~/ipacultimateio/set-ultimateio-leds.py -xl
depending on whether you are running any boards with X-Input mode


X-Input - this has been coded but not fully tested - an extra option needs to be added on the command line of -x
e.g.
$ python3 ~/ipacultimateio/set-ultimateio-leds.py -x
will find any devices configured as X-Input  (both Ultimarc devices and generic X-Input devices. 





- scripts folder
For mulitboard configuration an example script is provided which shows the structure of the file that you will need to adhere to, which includes an example of all 
command that can be used.
For this to work in yuor setup you will need to change the values for the Device UUID

- data folder -
For mulitboard configuration an example script
If you wish to use GroupNames to configure a button,
