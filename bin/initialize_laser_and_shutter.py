#!/usr/bin/env python

import optparse, time
import cbp.cbp_instrument as CBP
import cbp
import cbp.shutter
import thorlabs

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-w","--wavelength",default=600,type=int)
    parser.add_option("-v","--verbose", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()
start_time = time.time()
laser_interface = cbp.laser.LaserSerialInterface(loop=False)
laser_interface.change_wavelength(opts.wavelength)

#print "closed shutter"
thorlabs.thorlabs.main(val=2)
cbp.shutter.main(runtype="shutter", val=1)

