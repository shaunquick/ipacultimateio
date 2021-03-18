#!/bin/bash
# $1 is the full path of the rom
# $2 is the rom name.

# kill any other current scripts running
pkill -f set-ultimateio-leds.py


case "$2" in
        "romname1")
        echo "running generic romname1 script" >> ~/.emulationstation/scripts/output.log
	python3  ~/ipacultimateio/set-ultimateio-leds.py 1buttons.json >> ~/.emulationstation/scripts/output.log &
        ;;
        "romname2")
        echo "running generic romname2 script" >> ~/.emulationstation/scripts/output.log
	python3  ~/ipacultimateio/set-ultimateio-leds.py 2buttons.json >> ~/.emulationstation/scripts/output.log &
        ;;
        *)
        echo "running generic game-start script" >> ~/.emulationstation/scripts/output.log
        python3  ~/ipacultimateio/set-ultimateio-leds.py allbuttons.json >> ~/.emulationstation/scripts/output.log &
        ;;
esac
