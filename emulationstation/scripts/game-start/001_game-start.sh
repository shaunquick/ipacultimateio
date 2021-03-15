#!/bin/bash
# $1 is the full path of the rom
# $2 is the rom name.

# kill any other current scripts running
pkill -f set-ultimateio-leds.py


case "$2" in
        "romname1") python3 -m
	python3 -m  ~/ipacultimateio/set-ultimateio-leds.py 1buttons.json
        ;;
        "romname2") python3 -m
	python3 -m  ~/ipacultimateio/set-ultimateio-leds.py 2buttons.json
        ;;
        *)
        echo "running generic button script" >> ~/.emulationstation/scripts/game-start/output.log
        python3 -m  ~/ipacultimateio/set-ultimateio-leds.py allbuttons.json
        ;;
esac
