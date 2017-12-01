#!/usr/bin/env python

import optparse, time
import numpy as np

import cbp.cbp_instrument as CBP
import cbp
import cbp.shutter
import thorlabs

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-d","--duration",default=1,type=int)
    parser.add_option("-w","--wavelength",default=600,type=int)
    parser.add_option("-f","--filename",default="/tmp/test.xml")
    parser.add_option("-s","--shutter",default=1,type=int)

    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()
laser_interface = cbp.laser.LaserSerialInterface(loop=False)
cbp_inst = CBP.CBP(phidget=False,birger=False,potentiometer=False,laser=False,filter_wheel=False,keithley=True,spectrograph=True,flipper=True)
cbp_inst.flipper.run_flipper(1)

wavelengths = np.arange(400,1001,1)
filename = '/tmp/test.xml'
duration = 1
doShutter = True

outfile = 'duration_test3.dat'
fid = open(outfile,'w')
for wavelength in wavelengths:
    laser_interface.change_wavelength(wavelength)     

    cbp_inst.keithley.do_reset(mode="char",nplc=1)
    currents = []
    for ii in xrange(10):
        current = cbp_inst.keithley.getread()[0]
        currents.append(current)

    print wavelength,np.max(currents)
    fid.write('%.0f %.5e\n'%(wavelength,np.max(currents)))
fid.close()

