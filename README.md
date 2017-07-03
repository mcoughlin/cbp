# cbp
Scripts for running the collimated beam projector and analyzing output

Logging + Data taking:
python instimage.py -v -p 1000 -w 550 -c IMAGE0
   p is the number of photons, w is the wavelength, c is a comment

or by ssh:

photons=1000
wavelength=550
comment=MY_COMMENT_HERE
filename=/tmp/test.dat
ssh pi@10.136.250.2 "cd /home/pi/Code/cbp/bin; python instimage.py -v -p $photons -w $wavelength -c $comment -f $filename"
scp pi@10.136.250.2:$filename .

Filter Wheel:
There are 10 slots in the filter wheel, 5 dedicated to masks and 5 dedicated to filters. These can be found in masks.txt and filters.txt respectively.

Examples:

Accelerometer: python runinst.py --doRun -i phidget
   Returns x, y, and z in units of g, altitude angle in degrees 

AltAz: python runinst.py --doRun --doSteps -i altaz -m 1 -n 100
   m = 1, n > 0: Right
   m = 1, n < 0: Left
   m = 2, n > 0: Up
   m = 2, n < 0: Down

Potentiometer: python runinst.py --doRun -i potentiometer
   Alt: Left number, Increasing: Up, Decreasing: Down
   Az: Right number, Increasing: Left, Decreasing: Right

Photodiode: python runinst.py --doRun -i photodiode
   Returns value in units of whatever setting you are on

Birger: python runinst.py --doRun -i birger --doAperture -p 24
        python runinst.py --doRun -i birger --doFocus -f 1024
   Aperture: 0 - 24 (Open-Closed), Focus: 0 - 16383 (4.5-Infinity)

Shutter: python runinst.py --doRun --doShutter -i shutter -s 1000
   Shutter in milliseconds, -1 for open

Filter Wheel: python runinst.py --doRun --doFWPosition -i filter_wheel --mask 0 --filter 0

Lamp: python runinst.py --doRun --doLamp -i lamp -l 255
   Lamp: 0 - 255

Monochrometer:  python runinst.py --doRun --doMonoWavelength -i monochrometer --wavelength 600

Keithley: python runinst.py -i keithley --doKeithley --doRun

Spectrograph: python runinst.py -i spectrograph --doSpectrograph --doRun

Laser: python  runinst.py --doRun --doLaser -i laser --wavelength 521
