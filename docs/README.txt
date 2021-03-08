Ultimarc-Ultimate I/O 
==============

Library and command script utility

Introduction
=============
This utility will configure the LEDs on the following Ultimarc boards; IPAC Ultimate. It uses json files to sned one or many commands to the board.

This library and command line utility has been tested with only the current IPAC Ultimate board.

This has been written in python

Pre-Requisites
==============

Required Python modules
To use this tool the following python modules need to be installed on your system.
*  pip install pyusb  (https://pyusb.github.io/pyusb/) (https://pypi.org/project/pyusb/)


How it works
=============
Once you have downloaded the github project, there will be a main python module called

set-ultimateio-leds.py

Plug in your Ultimate I/O Board into the Raspberry Pi 4

To see the help page run
$python3 set-ultimateio-leds.py --help

To run a test script run
$python3 set-ultimateio-leds.py

To run your own script
$python3 set-ultimateio-leds.py <scriptname>
where <scriptname> is the name of the json script file
The script should be placed in the sub-folder scripts (although you can pass in the full path if you do not want to hold your scrips there.


Folder Structure
================
main folder -

scripts folder -

libs folder -

docs  folder -

