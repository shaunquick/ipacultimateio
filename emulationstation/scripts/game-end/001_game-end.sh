#!/bin/bash

# kill any other current scripts running
pkill -f set-ultimateio-leds.py

echo "running game-end script" >> ~/.emulationstation/scripts/output.log

python3 ~/ipacultimateio/set-ultimateio-leds.py setallblue.json >> ~/.emulationstation/scripts/output.log &
