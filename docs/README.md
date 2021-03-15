Ultimarc-Ultimate I/O 
==============

Library and command script utility

Introduction
=============
This utility will configure the LEDs on the following Ultimarc boards; IPAC Ultimate. It uses json files to send one or many commands to the board.

This library and command line utility has been tested with only the current IPAC Ultimate board.

This has been written in python.

It has been used successfully with the raspberry pi. It may be work in other environments but has not been tested.

The library has all the python source, but it is intended to be used via the command line as a complete utility.

Pre-Requisites
==============
Python installed version 3.7.3 (or above)
https://projects.raspberrypi.org/en/projects/generic-python-install-python3

Required Python modules
To use this tool the following python modules need to be installed on your system.
*  pip install pyusb  (https://pyusb.github.io/pyusb/) (https://pypi.org/project/pyusb/)

The following commands may help....
$ sudo apt install python3-pip
$ python3 -m pip install pyusb



Installation
============

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
Now run a test- 
$ python3 ~/ipacultimateio/set-ultimateio-leds.py
If there are LED devices connected to your board - some of those will light up.



How it works
=============
Once you have downloaded the github project, there will be a main python module called

set-ultimateio-leds.py in the main folder

Plug in your Ultimate I/O Board into the Raspberry Pi 4

To see the help page run
$python3 set-ultimateio-leds.py --help

To run a test script run
$python3 set-ultimateio-leds.py

To run your own script
$python3 set-ultimateio-leds.py <scriptname>
where <scriptname> is the name of the json script file that resides in the scripts sub-folder or a fully qualified filename
The script should be placed in the sub-folder scripts (although you can pass in the full path if you do not want to hold your scripts there.


Scripts
========
Scripts are json files that allow you to execute a sequence of different commands to the Board. These will allow you to set the colour of a 
led, flash an led, fade a led etc - each of those commands require a set of paramaters and informaiton to allow them to configure
the Leds.

There are three levels of commands
- All Leds
	- All leds can be configured to have the same configuration.
- A list of Led's
	- you can pass in a list of Led Numbers and configure those together, useful if you don;t have many scripts or you know/remember
          which button is configured to which Led Numbers and that you don't change them.
- A group of Leds 
	- you can define a GroupName (e.g. "button1") and provide a list of Led Numbers for that (e.g. 16,17,18 for the Red/Green/Blue Led NUmbers of that 
          button.
          You can then run a defined set of commands for that groupName (or list of GroupNames) and effectively configure the underlying Led Numbers.
          It provides a layer of encapsulation, meaning that if button1 is not longer configured for led numbers 16,17,19 - you can redefine the Led 
          Numbers you wish to be associated with that name



Emulationstation
=================
The following resource is useful
https://retropie.org.uk/docs/EmulationStation/#scripting

There will be a folder called ./emulationstation/scripts

The contents of that folder needs to be moved to ~.emulationstation

This will create the folder structure exp[ected for some emulation station events to be captured.
You will need to edit the scripts to your chosen configuration



Folder Structure
================
- main folder -
Holds the main python program that you will execute :- set-ultimateio-leds.py

- scripts folder
An example script (default_script.json) is provided which shows the structure of the file that you will need to adhere to, which includes an example of all 
command that can be used.
You can create your own scripts in this folder, to configure the Board as you want.

- data folder -
If you wish to use GroupNames to configure a button, the configuration/definition file is held in this folder and is called 'LedGroupNameDefinitions.json'
the LedNrRGB values will need to be configured for your set-up - additionally the LedGroupName value can also be changed to any name that you want 
to use - remember that in the script you will also need to reference that new name in order to use the configuration in the command.

- libs folder -
A set of underlyig python modules - the core subfolder holder all the functions that cab be externally called within other programs (not tested!)
Othe sub folders hold additional modules that are needed for this utility

- docs folder -
The full readme file is here ! Additonal documentation may be provided at a later date.


