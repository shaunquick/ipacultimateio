#!/bin/bash
# $1 is the full path of the rom
# $2 is the rom name.

# kill any other current scripts running
pkill -f set-ultimateio-leds.py

echo "running romname script" >> ~/.emulationstation/scripts/output.log
python3  ~/ipacultimateio/set-ultimateio-rom-leds.py $2 >> ~/.emulationstation/scripts/output.log &
