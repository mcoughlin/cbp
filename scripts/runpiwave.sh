
wavelength=$1

ssh pi@139.229.12.11 "cd /home/pi/Code/cbp/bin; python runinst.py --doRun --doMonoWavelength -i monochrometer --wavelength $wavelength"

