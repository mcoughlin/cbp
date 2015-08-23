#!/usr/bin/env python

import serial, sys, time, glob, struct
import optparse
import FLI

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()

    parser.add_option("-p","--position",default=0,type=int)
    parser.add_option("--doHome", action="store_true",default=False)
    parser.add_option("--doPosition", action="store_true",default=False)
    parser.add_option("--doGetPosition", action="store_true",default=False)

    opts, args = parser.parse_args()

    return opts

# Parse command line
opts = parse_commandline()

fws = FLI.focuser.USBFocuser.find_devices()
print fws
fw0 = fws[0]

if opts.doGetPosition:
    pos = fw0.get_stepper_position()
    print "Current Position: %d"%pos

if opts.doHome:
    fw0.home_focuser()
    pos = fw0.get_stepper_position()
    print "New Position: %d"%pos

if opts.doPosition:
    fw0.step_motor(opts.position,blocking=False, force=True)
    pos = fw0.get_stepper_position()
    print "New Position: %d"%pos



