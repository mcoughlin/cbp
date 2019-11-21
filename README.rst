===
CBP
===

Scripts for running the collimated beam projector and analyzing output

Logging + Data taking:
----------------------

.. code:: bash

    python instimage.py -v -p 1000 -w 550 -c IMAGE0


-p    p is the number of photons
-w    w is the wavelength
-c    c is a comment

or by ssh:
----------

.. code:: bash

    photons=1000
    wavelength=550
    comment=MY_COMMENT_HERE
    filename=/tmp/test.dat
    ssh pi@10.136.250.2 "cd /home/pi/Code/cbp/bin; python instimage.py -v -p $photons -w $wavelength -c $comment -f $filename"
    scp pi@10.136.250.2:$filename .

Filter Wheel
    There are 10 slots in the filter wheel, 5 dedicated to masks and 5 dedicated to filters. These can be found in masks.txt and filters.txt respectively.

Examples:
---------

Accelerometer:
    Returns x, y, and z in units of g, altitude angle in degrees

.. code:: bash

    python runinst.py phidget

AltAz:
    m = 1, n > 0: Right
    m = 1, n < 0: Left
    m = 2, n > 0: Up
    m = 2, n < 0: Down

.. code:: bash

    python runinst.py altaz 1  100


Potentiometer:
    Alt: Left number, Increasing: Up, Decreasing: Down
    Az: Right number, Increasing: Left, Decreasing: Right

.. code:: bash

    python runinst.py potentiometer


Photodiode:
    Returns value in units of whatever setting you are on

.. code:: bash

    python runinst.py photodiode


Birger:
    Aperture: 0 - 24 (Open-Closed), Focus: 0 - 16383 (4.5-Infinity)

.. code::  bash

    python runinst.py birger aperture 24
    python runinst.py birger focus 1024

Shutter:
   Shutter in milliseconds, -1 for open

.. code:: bash

    python runinst.py shutter 1000

Uniblitz Shutter:
   Uniblitz Shutter, 1 for open, 2 for close

.. code:: bash

    python runinst.py uniblitz 1

Polarizer:
.. code:: bash

    python runinst.py polarizer home 
    python runinst.py polarizer getposition
    python runinst.py polarizer 0

Filter Wheel:

.. code:: bash

    python runinst.py 'filter wheel' position 0 0
    python runinst.py 'filter wheel' 'get position'

Lamp:
    Lamp: 0 - 255

.. code:: bash

    python runinst.py lamp 255

Monochrometer:

.. code:: bash

    python runinst.py monochrometer wavelength 600

Keithley:

.. code:: bash

    python runinst.py keithley

Spectrograph:

.. code:: bash

    python runinst.py spectrograph

Laser:

.. code:: bash

    python  runinst.py laser change_wavelength 521
